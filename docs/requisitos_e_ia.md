# Engenharia de Requisitos e a Transição para Inteligência Artificial

## Introdução

O Guard.IA nasceu de uma necessidade real: acompanhar automaticamente a produção legislativa brasileira relacionada à proteção de crianças e adolescentes na internet. Essa necessidade, quando traduzida em software, exige decisões cuidadosas sobre o que construir primeiro, como validar as hipóteses e como evoluir o sistema de forma sustentável.

Este documento registra como a Engenharia de Requisitos guiou as decisões da Release 1 e como a arquitetura foi projetada para suportar a transição para Inteligência Artificial na Release 2.

---

## Release 1 — Engenharia de Requisitos Aplicada

### Do problema ao requisito

O ponto de partida foi a definição precisa do problema: *"Como identificar, dentre milhares de proposições legislativas, quais são relevantes para a proteção digital de menores?"*

A resposta a essa pergunta não é trivial. Ela exige:

1. Conhecimento do domínio legislativo (tipos de proposição, estrutura de ementa)
2. Definição de "relevância" (o que caracteriza uma lei sobre proteção digital?)
3. Uma estratégia de captura que minimize falsos negativos (leis relevantes não capturadas)

!!! info "Requisito funcional central da Release 1"
    O sistema deve ser capaz de, dado um conjunto de proposições legislativas brutas, identificar e separar aquelas que tratam de proteção de crianças e adolescentes no ambiente digital, com recall suficiente para validar o pipeline de ponta a ponta.

### A estratégia determinística — Filtro por Palavras-Chave

Para a Release 1, a equipe optou por um filtro determinístico baseado em palavras-chave. A lógica é direta: se a ementa de uma proposição contém termos como `"criança"`, `"adolescente"`, `"internet"` ou `"cyberbullying"`, ela é considerada candidata à relevância.

```python
PALAVRAS_CHAVE = [
    "crianca", "adolescente", "menor", "internet", "digital",
    "online", "cyberbullying", "redes sociais", "lgpd",
    "marco civil", "privacidade", "aplicativo", "eca",
    "conteudo inapropriado", "tempo de tela"
]
```

Essa abordagem foi escolhida deliberadamente por três razões:

**Velocidade de implementação** — permite validar o pipeline completo sem depender de modelos de IA, que exigem treinamento, infraestrutura e tempo de desenvolvimento.

**Rastreabilidade** — cada proposição capturada pode ser auditada: o campo `termos_chave` registra quais palavras ativaram o filtro, tornando a decisão completamente explicável.

**Baseline mensurável** — os resultados do filtro determinístico servem como referência para avaliar a melhoria trazida pela IA na Release 2.

!!! info "Resultado da Release 1"
    De 32.499 proposições coletadas desde 2023, o filtro por palavras-chave identificou **655 proposições relevantes** — uma taxa de captura de aproximadamente 2%, consistente com o esperado para um domínio temático específico.

---

## Limitações do Filtro Determinístico

A abordagem por palavras-chave é eficaz para um primeiro corte, mas apresenta limitações conhecidas que motivam a evolução para IA.

### Falsos Positivos

O filtro captura proposições que contêm as palavras-chave mas não tratam do tema central. Exemplos reais:

- *"Altera o art. 5º do Código Civil para reduzir a **maioridade** civil"* — contém "menor" mas não é sobre proteção digital
- *"Disciplina o uso de **aplicativo** para pagamento de táxi"* — contém "aplicativo" mas não é sobre crianças

### Falsos Negativos

O filtro perde proposições relevantes que não usam as palavras exatas da lista:

- *"Dispõe sobre a responsabilização de plataformas de streaming por conteúdo inadequado"* — relevante, mas não contém nenhuma das palavras-chave
- *"Regulamenta jogos eletrônicos voltados ao público infanto-juvenil"* — relevante, mas usa vocabulário não previsto

### Dependência de vocabulário fixo

O universo legislativo é rico em sinônimos, eufemismos e neologismos. Uma lista estática de palavras-chave precisa de manutenção constante para acompanhar a evolução do vocabulário legislativo.

!!! warning "Implicação para a Release 2"
    As limitações do filtro determinístico não são um defeito de implementação — são uma característica esperada de um sistema baseado em regras. A transição para NLP não substitui o filtro existente: ela o complementa, adicionando uma camada de classificação semântica que opera sobre os candidatos já pré-selecionados.

---

## Release 2 — A Transição para Inteligência Artificial

### Da regra para a semântica

A Release 2 introduz um novo componente no pipeline: o **Classificador de IA**. Diferente do filtro por palavras-chave — que opera sobre a presença ou ausência de termos — o classificador opera sobre o **significado** do texto.

A técnica escolhida é a **similaridade semântica por embeddings**, utilizando modelos de linguagem pré-treinados em português:

| Modelo | Uso | Característica |
|---|---|---|
| `neuralmind/bert-base-portuguese-cased` | Produção | BERT treinado em corpus brasileiro |
| `paraphrase-multilingual-MiniLM-L12-v2` | Hardware limitado | Modelo leve, multilíngue |

### Como funciona a classificação por embeddings

O modelo transforma textos em vetores numéricos (embeddings) que capturam o significado semântico. Textos com significados similares geram vetores próximos no espaço vetorial.

```
Texto: "Dispõe sobre responsabilização de plataformas digitais por conteúdo nocivo a menores"
         ↓
   [Modelo BERT]
         ↓
Vetor: [0.23, -0.87, 0.45, ..., 0.12]  (768 dimensões)
         ↓
Comparação com vetores das categorias
         ↓
Categoria: "conteudo_inapropriado" | Confiança: 0.91
```

### Categorias definidas por Engenharia de Requisitos

As categorias de classificação foram definidas a partir da análise do domínio, não de forma arbitrária:

```python
CATEGORIAS = {
    "cyberbullying":         "assédio, bullying, violência psicológica online",
    "privacidade_dados":     "coleta de dados pessoais, LGPD, proteção de informações",
    "tempo_de_tela":         "uso excessivo, dependência digital, limite de uso",
    "conteudo_inapropriado": "pornografia, violência, conteúdo adulto na internet",
    "educacao_digital":      "letramento digital, ensino, alfabetização tecnológica"
}
```

Cada categoria representa um eixo temático identificado durante o levantamento de requisitos, baseado nas principais áreas de preocupação legislativa sobre proteção digital de menores.

---

## A Arquitetura Já Está Pronta para a IA

### O princípio do Open/Closed aplicado ao pipeline

Um dos benefícios mais importantes da arquitetura Pipes and Filters é sua extensibilidade. O pipeline do Guard.IA segue implicitamente o **Princípio Aberto/Fechado**: está aberto para extensão e fechado para modificação.

Para integrar a IA na Release 2, basta inserir um novo filtro entre o Armazenamento e o Dashboard — sem modificar nenhuma etapa existente:

```
Release 1:
dados_filtrados.json → armazenamento.py → PostgreSQL → dashboard

Release 2:
dados_filtrados.json → armazenamento.py → PostgreSQL → classificador.py → PostgreSQL (atualizado) → dashboard
```

O classificador lê as proposições armazenadas, adiciona os campos `categoria` e `confianca`, e atualiza o banco. As etapas anteriores não são tocadas.

!!! info "Zero retrabalho arquitetural"
    A separação de responsabilidades implementada na Release 1 garante que a adição da IA na Release 2 não exige refatoração do pipeline existente. O contrato de dados já reserva os campos `categoria` e `confianca` no schema SQL, antecipando essa evolução.

### Transparência obrigatória

Por princípio ético registrado na Constituição do Guard.IA (Regras 19 e 20), toda classificação gerada pela IA deve:

- Ser apresentada como **estimativa**, nunca como fato absoluto
- Sempre exibir o campo `confianca` junto com a `categoria`
- Permitir que o usuário questione e reporte classificações incorretas

---

## Visão Estratégica de Evolução

O Guard.IA foi projetado como um sistema evolutivo, não como uma solução definitiva. A progressão natural é:

```
Release 1: Captura → Validação do pipeline → Baseline de dados
Release 2: Classificação → Insights temáticos → Dashboard analítico
Release 3: Predição → Tendências legislativas → Alertas automáticos
```

Cada release valida hipóteses e constrói sobre os alicerces da anterior. A Engenharia de Requisitos não foi aplicada apenas para definir o que construir — foi aplicada para definir **a ordem certa de construção**.

!!! info "Princípio aplicado"
    *"Construa o suficiente para aprender, não o suficiente para impressionar."* A Release 1 não precisa de IA para ser válida — ela precisa provar que o pipeline funciona e que os dados coletados são úteis. A IA é o próximo passo natural, não o primeiro.

---

## Referências

- SOMMERVILLE, Ian. *Engenharia de Software*. 10ª ed. Pearson, 2019.
- DEVLIN, Jacob et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. arXiv, 2018.
- SOUZA, Fábio et al. *BERTimbau: Pretrained BERT Models for Brazilian Portuguese*. BRACIS, 2020.
- Hugging Face. *neuralmind/bert-base-portuguese-cased*. Disponível em: https://huggingface.co/neuralmind/bert-base-portuguese-cased
