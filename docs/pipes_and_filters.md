# Pipes and Filters — A Arquitetura do Guard.IA

## O que é o padrão Pipes and Filters?

Pipes and Filters é um padrão arquitetural clássico de Engenharia de Software utilizado para processar fluxos de dados através de uma sequência de etapas independentes. O conceito é simples e poderoso: os dados entram em uma ponta, passam por uma série de transformações e saem processados na outra.

O padrão é composto por dois elementos fundamentais:

- **Filter (Filtro):** componente que recebe dados, executa uma transformação específica e entrega o resultado para o próximo estágio. Cada filtro tem uma responsabilidade única e bem definida.
- **Pipe (Canal):** mecanismo de comunicação que conecta dois filtros consecutivos, transportando os dados de saída de um para a entrada do outro.

```
[Entrada] ──► [Filter A] ──pipe──► [Filter B] ──pipe──► [Filter C] ──► [Saída]
```

!!! info "Origem do padrão"
    Pipes and Filters tem origem nos sistemas Unix, onde comandos são encadeados via `|` (pipe). O princípio é o mesmo: cada programa faz uma coisa bem feita e passa o resultado adiante. Ex: `cat arquivo.txt | grep "palavra" | sort | uniq`

---

## Características Fundamentais

### Independência entre componentes

Cada filtro opera de forma completamente autônoma. Ele não sabe quem veio antes nem quem vem depois — apenas recebe uma entrada, processa e entrega uma saída. Isso garante que uma mudança em um filtro não propaga efeitos colaterais para os demais.

### Contrato de dados fixo

A comunicação entre filtros é feita exclusivamente através de um formato de dados acordado previamente. No Guard.IA, esse contrato é um schema JSON com campos fixos (`id_externo`, `ementa`, `casa`, `data_apresentacao`, etc.). Nenhum filtro pode alterar esse contrato sem aprovação de toda a equipe.

### Processamento em fluxo

Os dados fluem de forma sequencial e linear: cada etapa recebe exatamente o que a anterior produziu. Não há acesso direto entre etapas não adjacentes.

---

## Vantagens para Pipelines de Dados

### Escalabilidade

Como cada filtro é independente, é possível otimizar, substituir ou escalar uma etapa sem impactar as demais. Se a API da Câmara mudar seu formato de resposta, apenas o coletor precisa ser ajustado — o filtro e o banco permanecem intactos.

### Reuso de componentes

Filtros bem definidos podem ser reutilizados em outros contextos. O módulo de normalização de texto do filtro do Guard.IA, por exemplo, pode ser reaproveitado na etapa de classificação sem modificações.

### Isolamento e testabilidade

Cada filtro pode ser testado de forma isolada, com entradas controladas e saídas verificáveis. Isso facilita a identificação de bugs e a validação de comportamentos esperados sem precisar subir o pipeline inteiro.

### Manutenibilidade

A separação clara de responsabilidades torna o código mais fácil de entender, documentar e manter. Um desenvolvedor novo no projeto consegue compreender e modificar uma etapa sem precisar entender o sistema inteiro.

!!! success "Princípio aplicado"
    Pipes and Filters é uma implementação prática do **Single Responsibility Principle (SRP)** — cada componente faz uma coisa e faz bem feito.

---

## Por que escolhemos Pipes and Filters para o Guard.IA?

### O problema que enfrentamos

O Guard.IA precisa processar dados legislativos de duas fontes distintas (Câmara e Senado), aplicar regras de relevância, classificar por tema e armazenar de forma estruturada. São responsabilidades completamente diferentes que, se misturadas, gerariam um sistema frágil e difícil de manter.

### A decisão arquitetural

Na Sprint 01, avaliamos três abordagens:

| Arquitetura | Vantagem | Desvantagem para o Guard.IA |
|---|---|---|
| **Monolítica** | Simples de começar | Acoplamento total — uma mudança quebra tudo |
| **Microsserviços** | Alta escalabilidade | Complexidade excessiva para o escopo acadêmico |
| **Pipes and Filters** | Separação clara, testável, evolutiva | Requer disciplina no contrato de dados |

A escolha por Pipes and Filters foi natural dado o fluxo linear dos dados: coletar → filtrar → armazenar → visualizar.

### Como o padrão se manifestou no código

```
coletor_camara.py  ──┐
                     ├──► dados_brutos.json ──► filtro.py ──► dados_filtrados.json ──► armazenamento.py ──► PostgreSQL
coletor_senado.py  ──┘
```

Cada arquivo Python representa um filtro com responsabilidade única:

- `coletor_camara.py` e `coletor_senado.py` — **Coleta:** acessa APIs externas e normaliza para o contrato
- `filtro.py` — **Filtro:** recebe dados brutos e entrega apenas o que é relevante
- `armazenamento.py` — **Armazenamento:** recebe dados filtrados e persiste no banco

!!! warning "Regra de ouro"
    Nenhum filtro lê ou escreve diretamente no arquivo de responsabilidade de outro filtro. A comunicação é sempre via pipe (arquivo JSON ou banco de dados), nunca por chamada direta entre módulos.

---

## Comparação com MVC

É comum confundir Pipes and Filters com MVC (Model-View-Controller). A diferença fundamental é o foco:

| Aspecto | MVC | Pipes and Filters |
|---|---|---|
| **Foco** | Separação de interface, lógica e dados | Transformação sequencial de dados |
| **Fluxo** | Bidirecional (usuário ↔ sistema) | Unidirecional (entrada → saída) |
| **Uso ideal** | Aplicações web com interface | Pipelines de processamento de dados |
| **Comunicação** | Controller coordena Model e View | Filtros só conhecem entrada e saída |

Para o Guard.IA, que é essencialmente um **sistema de processamento de dados**, Pipes and Filters é mais adequado que MVC.

---

## Referências

- SHAW, Mary; GARLAN, David. *Software Architecture: Perspectives on an Emerging Discipline*. Prentice Hall, 1996.
- BUSCHMANN, Frank et al. *Pattern-Oriented Software Architecture: A System of Patterns*. Wiley, 1996.
- RICHARDS, Mark. *Software Architecture Patterns*. O'Reilly Media, 2015.
