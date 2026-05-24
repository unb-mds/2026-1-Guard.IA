# Stack do Projeto

## Visão Geral

| Parte do Sistema | Tecnologia |
|---|---|
| Coleta, Filtro, Classificação, Armazenamento | Python 3.10+ |
| Banco de dados | PostgreSQL (via Docker) |
| Conector Python → Banco | psycopg2 (SQL puro) |
| Dashboard | Streamlit + Plotly |
| Autenticação | bcrypt |
| Infraestrutura | Docker + Docker Compose + GitHub Actions |
| Gerenciamento de dependências | pip + requirements.txt |

---

## Por que Python?

- Ecossistema completo para dados e IA
- Bibliotecas nativas para consumo de APIs REST
- Compatível com os modelos de NLP utilizados na classificação
- Toda a equipe tinha familiaridade com a linguagem

---

## Por que PostgreSQL?

- Banco relacional robusto e gratuito
- Suporte nativo a `INSERT ... ON CONFLICT DO NOTHING` — fundamental para deduplicação em lote
- Compatível com Docker para ambiente local consistente entre todos os membros

!!! danger "SQLite é proibido"
    O projeto usa exclusivamente PostgreSQL. Código usando SQLite deve ser adaptado.

---

## Por que psycopg2 e não SQLAlchemy?

Decisão arquitetural intencional:

- O pipeline de dados trabalha com SQL direto, sem necessidade de ORM
- `psycopg2` é mais leve e transparente
- `execute_values` do `psycopg2.extras` permite inserção em lote de alta performance

---

## Classificação (Release 2)

| Modelo | Uso |
|---|---|
| `neuralmind/bert-base-portuguese-cased` | Modelo principal — BERT treinado em português |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Modelo alternativo para hardware com menos memória |
