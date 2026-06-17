# Engenharia de Requisitos e a Transição para Inteligência Artificial

## Introdução

O Guard.IA nasceu de uma necessidade concreta e urgente: acompanhar, de forma contínua e automática, a produção legislativa brasileira relacionada à proteção de crianças e adolescentes no ambiente digital. O problema parece simples na superfície — "monitore leis sobre o tema" — mas, quando traduzido em requisitos de software, exige decisões profundas sobre **o que construir**, **em que ordem** e **como validar** cada hipótese antes de avançar.

Este documento é um estudo de caso sobre como a Engenharia de Requisitos guiou as escolhas do Guard.IA: da definição do escopo da Release 1 ao desenho da transição para Inteligência Artificial na Release 2. Mais do que descrever o que foi feito, este registro busca explicar **por que cada decisão foi tomada** — e como a arquitetura foi intencionalmente projetada para sustentar essa evolução.

---

## Release 1 — Base Sólida Antes da Inteligência

### O problema traduzido em requisito

O ponto de partida de qualquer projeto de software bem conduzido é a decomposição do problema em requisitos verificáveis. Para o Guard.IA, a pergunta central foi:

> *"Como identificar, dentre dezenas de milhares de proposições legislativas, quais são relevantes para a proteção digital de menores?"*

Essa questão esconde três subproblemas distintos:

1. **Escopo do domínio** — o que define "relevância"? Qual vocabulário, quais temas, quais tipos de proposição?
2. **Escala operacional** — mais de 32.000 proposições coletadas desde 2023. Qualquer solução precisa ser automatizável.
3. **Estratégia de erro** — é preferível capturar proposições desnecessárias (falsos positivos) ou perder proposições relevantes (falsos negativos)?

!!! info "Requisito funcional central da Release 1"
    O sistema deve ser capaz de, dado um conjunto de proposições legislativas brutas, identificar e separar aquelas que tratam de proteção de crianças e adolescentes no ambiente digital, com **recall** suficiente para validar o pipeline de ponta a ponta — mesmo que a precisão ainda não seja ideal.

A palavra-chave aqui é *recall*. Na Release 1, o objetivo não era ter um classificador perfeito. Era ter um classificador **funcional o suficiente** para provar que o pipeline completo — coleta, filtro, armazenamento, API, dashboard — operava de forma integrada e confiável.

### A decisão estratégica: filtro determinístico

Com base na análise de requisitos, a equipe optou por um **filtro determinístico baseado em palavras-chave**. A lógica é direta: se a ementa de uma proposição contém termos semanticamente associados ao domínio, ela é retida como candidata relevante.

```python
# filtro/filtro.py
PALAVRAS_CHAVE = [
    "crianca", "adolescente", "menor", "internet", "digital",
    "online", "cyberbullying", "redes sociais", "lgpd",
    "marco civil", "privacidade", "aplicativo", "eca",
    "conteudo inapropriado", "tempo de tela", "streaming",
    "plataforma digital", "dado pessoal"
]

def normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas antes da comparação."""
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode().lower()

def filtrar(proposicao: dict) -> bool:
    ementa = normalizar(proposicao.get("ementa", ""))
    termos_encontrados = [p for p in PALAVRAS_CHAVE if p in ementa]
    proposicao["termos_chave"] = termos_encontrados
    return len(termos_encontrados) > 0
```

Essa abordagem foi escolhida por razões técnicas e estratégicas deliberadas:

**Velocidade de implementação e validação** — o filtro determinístico permite validar o pipeline completo sem depender de infraestrutura de Machine Learning, que exige dados anotados, treinamento, avaliação e tempo de desenvolvimento significativamente maior.

**Rastreabilidade total** — cada proposição capturada pode ser auditada. O campo `termos_chave` registra exatamente quais palavras ativaram o filtro, tornando qualquer decisão do sistema completamente explicável e inspecionável.

**Baseline mensurável** — os resultados do filtro determinístico funcionam como referência quantitativa para avaliar o ganho real trazido pela IA na Release 2. Sem um baseline, qualquer melhoria seria subjetiva.

!!! success "Resultado da Release 1"
    De **32.499 proposições coletadas** desde 2023 nas APIs da Câmara dos Deputados e do Senado Federal, o filtro por palavras-chave identificou **655 proposições relevantes** — uma taxa de captura de aproximadamente 2%, consistente com o esperado para um domínio temático específico dentro do universo legislativo geral.

### O que a Release 1 valida, de fato

É importante compreender que o filtro determinístico não é o produto final — é o **instrumento de validação do pipeline**. A Release 1 responde às seguintes hipóteses técnicas:

- O pipeline Pipes and Filters funciona de ponta a ponta sem quebras?
- As APIs da Câmara e do Senado são estáveis o suficiente para coleta regular?
- O schema de dados escolhido é adequado para o domínio?
- A infraestrutura Docker + PostgreSQL suporta o volume de dados?
- A API FastAPI consegue servir os dados filtrados ao frontend?

Quando todas essas hipóteses são confirmadas, a equipe tem confiança para investir no componente mais custoso e complexo: a classificação por IA.

---

## As Limitações do Filtro Determinístico

A abordagem por palavras-chave é eficaz para um primeiro corte, mas apresenta limitações estruturais que motivam a evolução para IA. Conhecê-las com precisão é parte do processo de Engenharia de Requisitos.

### Falsos Positivos — o que entra mas não deveria

O filtro captura proposições que contêm as palavras-chave mas que não tratam do tema central. Esses falsos positivos "poluem" o conjunto de dados relevantes:

| Proposição (ementa) | Palavra-chave ativada | Por que é falso positivo |
|---|---|---|
| *"Altera o Código Civil para reduzir a maioridade civil para 16 anos"* | `menor` | Trata de capacidade civil, não de proteção digital |
| *"Disciplina o uso de aplicativo de pagamento de táxi"* | `aplicativo` | Sem relação com crianças ou adolescentes |
| *"Institui a Semana Nacional de Conscientização sobre Privacidade"* | `privacidade` | Direcionado ao público adulto geral |

!!! warning "Impacto dos falsos positivos"
    Falsos positivos não comprometem o recall do sistema (leis relevantes ainda são capturadas), mas comprometem a **precisão**. Em um dashboard, o usuário vê proposições irrelevantes misturadas com as realmente importantes — degradando a experiência e a confiabilidade percebida do sistema.

### Falsos Negativos — o que deveria entrar mas não entra

O filtro perde proposições genuinamente relevantes que não utilizam o vocabulário exato da lista. Esta é a limitação mais crítica do ponto de vista de negócio:

| Proposição (ementa) | Por que é relevante | Por que não foi capturada |
|---|---|---|
| *"Dispõe sobre a responsabilização de plataformas de streaming por conteúdo nocivo"* | Diretamente relacionada à proteção digital de menores | Não contém nenhuma palavra da lista |
| *"Regulamenta jogos eletrônicos voltados ao público infanto-juvenil"* | Trata de conteúdo e tempo de tela | Usa "infanto-juvenil" em vez de "criança" |
| *"Cria o programa de alfabetização midiática nas escolas públicas"* | Educação digital | Nenhuma palavra-chave presente |

### Fragilidade frente à evolução do vocabulário legislativo

O universo legislativo é vivo: surgem neologismos ("deepfake", "grooming online"), termos técnicos de regulação ("interoperabilidade", "moderação de conteúdo") e expressões legais novas a cada legislatura. Uma lista estática de palavras-chave exige manutenção contínua para não envelhecer.

!!! warning "Requisito emergente para a Release 2"
    As limitações acima não representam um defeito de implementação — são características esperadas e aceitas de um sistema baseado em regras. A transição para NLP não **substitui** o filtro existente: ela o **complementa**, adicionando uma camada de classificação semântica capaz de capturar significado, não apenas forma.

---

## Release 2 — A Inteligência Artificial como Evolução Natural

### Da correspondência lexical à compreensão semântica

A Release 2 introduz um novo componente no pipeline: o **Classificador Semântico**. A diferença fundamental em relação ao filtro por palavras-chave está no nível de abstração da operação:

| Abordagem | Opera sobre | Captura |
|---|---|---|
| Filtro por palavras-chave | Tokens presentes no texto | Forma (presença de termos) |
| Classificador por embeddings | Representação vetorial do texto | Significado (semântica do conteúdo) |

A técnica escolhida é a **similaridade semântica por embeddings**, utilizando modelos de linguagem pré-treinados em português. Esses modelos transformam textos em vetores densos de alta dimensionalidade — representações numéricas que capturam relações semânticas entre palavras e conceitos.

### Os modelos candidatos

| Modelo | Tipo | Melhor para |
|---|---|---|
| `neuralmind/bert-base-portuguese-cased` | BERT — corpus brasileiro | Produção, alta acurácia |
| `paraphrase-multilingual-MiniLM-L12-v2` | SBERT — multilíngue compacto | Hardware limitado, inferência rápida |

!!! info "Por que modelos pré-treinados em português?"
    Modelos treinados em corpora em inglês apresentam degradação significativa em textos jurídicos brasileiros, que possuem estrutura sintática, vocabulário técnico e convenções específicas do direito brasileiro. O `BERTimbau` (neuralmind/bert-base-portuguese-cased) foi pré-treinado em 2,68 GB de textos em português, incluindo fontes formais e jornalísticas.

### O fluxo de classificação

```
Texto: "Dispõe sobre responsabilização de plataformas digitais
        por conteúdo nocivo a menores de 18 anos"
         ↓
   [Tokenização + Normalização]
         ↓
   [Modelo BERT — Inferência]
         ↓
Vetor: [0.23, -0.87, 0.45, ..., 0.12]  ← 768 dimensões
         ↓
   [Cálculo de similaridade cosseno com vetores de cada categoria]
         ↓
Resultado: { "categoria": "conteudo_inapropriado", "confianca": 0.91 }
         ↓
   [Atualização no PostgreSQL]
```

### Categorias definidas por Engenharia de Requisitos

As categorias de classificação **não foram definidas arbitrariamente**. Elas emergem da análise do domínio — revisão de literatura legislativa, consulta a especialistas em políticas públicas e análise das proposições capturadas na Release 1:

```python
# classificador/categorias.py
CATEGORIAS = {
    "cyberbullying": (
        "assédio, bullying, violência psicológica online, "
        "perseguição virtual, ameaça por mensagem"
    ),
    "privacidade_dados": (
        "coleta de dados pessoais, LGPD, proteção de informações "
        "de menores, consentimento digital, vazamento de dados"
    ),
    "tempo_de_tela": (
        "uso excessivo de dispositivos, dependência digital, "
        "limite de acesso, restrição de horário para menores"
    ),
    "conteudo_inapropriado": (
        "pornografia infantil, violência, conteúdo adulto, "
        "plataformas de streaming, moderação de conteúdo"
    ),
    "educacao_digital": (
        "letramento digital, ensino de tecnologia, "
        "alfabetização midiática, segurança online nas escolas"
    )
}
```

Cada categoria é representada por um texto descritivo que é convertido em embedding pelo modelo. A classificação de uma proposição é determinada pela categoria cujo vetor possui maior similaridade com o vetor da ementa.

---

## A Arquitetura Pipes and Filters como Facilitadora da Evolução

### O ponto central deste estudo de caso

Este é o aspecto mais importante deste documento: a transição da Release 1 para a Release 2 **não exige reescrever nenhuma linha de código existente**. Essa não é uma coincidência — é o resultado direto de uma decisão arquitetural tomada no início do projeto.

A escolha pelo padrão **Pipes and Filters** foi motivada, entre outros fatores, pela antecipação de que o sistema precisaria evoluir. O filtro de palavras-chave sempre foi concebido como uma etapa substituível, não como uma solução permanente.

### O Princípio Aberto/Fechado na prática

O pipeline do Guard.IA aplica implicitamente o **Princípio Aberto/Fechado** (Open/Closed Principle): cada componente está **fechado para modificação** (sua interface e contrato de dados não mudam) e **aberto para extensão** (novos componentes podem ser inseridos sem alterar os existentes).

```
╔══════════════ RELEASE 1 ══════════════╗
│                                        │
│  [Coleta] → [Filtro] → [Armazenamento] │
│                                        │
╚════════════════════════════════════════╝

╔══════════════════════ RELEASE 2 ══════════════════════╗
│                                                        │
│  [Coleta] → [Filtro] → [Armazenamento] → [Classificador IA] │
│                                                        │
╚════════════════════════════════════════════════════════╝
```

A adição do `Classificador IA` é uma operação de **inserção**, não de **modificação**. Os pipes anteriores continuam inalterados porque:

1. O contrato de dados entre etapas é fixo — cada pipe recebe e entrega o mesmo schema JSON
2. O classificador opera de forma assíncrona sobre dados já persistidos — não interfere no fluxo de coleta
3. O banco de dados já reserva as colunas `categoria` e `confianca` no schema SQL desde a Release 1

```sql
-- schema.sql — definido na Release 1, já preparado para a Release 2
CREATE TABLE IF NOT EXISTS proposicoes (
    id                SERIAL PRIMARY KEY,
    id_externo        VARCHAR(50) UNIQUE NOT NULL,
    ementa            TEXT,
    -- ... campos da Release 1 ...
    categoria         VARCHAR(100),   -- NULL até a Release 2 classificar
    confianca         FLOAT           -- NULL até a Release 2 classificar
);
```

!!! success "Zero retrabalho arquitetural"
    A separação de responsabilidades implementada na Release 1 garante que a adição da IA na Release 2 não exige refatoração do pipeline existente. O único trabalho necessário é implementar o novo pipe `classificador.py` — os demais módulos são intocados.

### A independência entre os pipes como garantia de segurança

Uma das regras mais importantes da arquitetura Pipes and Filters é que **nenhum pipe lê ou escreve diretamente nos arquivos intermediários de outro pipe**. Toda comunicação passa pelo contrato de dados definido.

Isso significa que o Classificador de IA pode ser desenvolvido, testado e implantado **de forma completamente independente** do pipeline existente — sem risco de regressão na coleta ou no armazenamento. A equipe de IA pode trabalhar em paralelo com a equipe de infraestrutura sem conflitos.

---

## Transparência e Ética na Classificação por IA

### Uma exigência de requisito, não uma escolha opcional

A Constituição do Guard.IA (documento `GEMINI.md`) estabelece nas Regras 19 e 20 um princípio ético inegociável: **toda classificação gerada por IA deve ser apresentada como estimativa, nunca como verdade absoluta**.

Isso se traduz em requisitos concretos de implementação:

- O campo `confianca` (0.0 a 1.0) deve ser sempre exibido junto com a `categoria` no dashboard e na API
- Proposições com `confianca < 0.7` devem ser sinalizadas visualmente como "classificação incerta"
- O usuário deve ter a opção de reportar classificações incorretas (mecanismo de feedback ativo)
- Nenhuma proposição deve ser descartada automaticamente com base apenas na classificação da IA

!!! warning "Por que isso é um requisito e não uma boa prática?"
    O sistema é utilizado por cidadãos, jornalistas e pesquisadores para acompanhar legislação de interesse público. Uma classificação incorreta não é apenas um erro técnico — pode significar que um usuário deixa de acompanhar uma lei relevante. A transparência sobre a incerteza do modelo é uma responsabilidade do sistema, não uma funcionalidade opcional.

---

## Visão Estratégica de Evolução

O Guard.IA foi projetado como um sistema evolutivo e incremental. A progressão entre releases segue uma lógica de validação de hipóteses:

```
┌─────────────────────────────────────────────────────────────────┐
│ Release 1: Infraestrutura → Valida o pipeline e os dados        │
│            Pergunta: "O sistema consegue coletar e armazenar?"  │
├─────────────────────────────────────────────────────────────────┤
│ Release 2: Classificação → Valida a utilidade dos dados         │
│            Pergunta: "O sistema consegue extrair insights?"      │
├─────────────────────────────────────────────────────────────────┤
│ Release 3: Predição → Valida o valor preditivo                  │
│            Pergunta: "O sistema consegue antecipar tendências?"  │
└─────────────────────────────────────────────────────────────────┘
```

Cada release constrói sobre os alicerces da anterior. A Engenharia de Requisitos não foi aplicada apenas para definir **o que** construir — foi aplicada para definir **a ordem certa de construção**.

!!! info "Princípio aplicado"
    *"Construa o suficiente para aprender, não o suficiente para impressionar."* A Release 1 não precisa de IA para ser válida — ela precisa provar que o pipeline funciona e que os dados coletados são úteis. A IA é o próximo passo natural de uma evolução planejada, não uma solução prematura para um problema ainda não completamente compreendido.

---

## Referências

- SOMMERVILLE, Ian. *Engenharia de Software*. 10ª ed. Pearson, 2019.
- PRESSMAN, Roger S.; MAXIM, Bruce R. *Engenharia de Software: Uma Abordagem Profissional*. 8ª ed. McGraw-Hill, 2016.
- DEVLIN, Jacob et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv:1810.04805, 2018.
- SOUZA, Fábio et al. *BERTimbau: Pretrained BERT Models for Brazilian Portuguese*. BRACIS, 2020.
- REIMERS, Nils; GUREVYCH, Iryna. *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP, 2019.
- MARTIN, Robert C. *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall, 2017.
- Hugging Face. *neuralmind/bert-base-portuguese-cased*. Disponível em: [https://huggingface.co/neuralmind/bert-base-portuguese-cased](https://huggingface.co/neuralmind/bert-base-portuguese-cased)
