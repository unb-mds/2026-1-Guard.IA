# Release Notes

## Release 1 — 2026/1

**Data:** Maio de 2026  
**Versão:** 1.0.0  
**Branch:** `release-1-integration`

---

### Resumo

Primeira entrega do Guard.IA: pipeline de monitoramento legislativo completo, do consumo das APIs públicas até a visualização em dashboard e portal web com autenticação de usuários.

---

### Funcionalidades Entregues

#### Pipeline de Dados

- **Coleta (Câmara)** — consumo paginado da API da Câmara dos Deputados com checkpoint por página, evitando reprocessamento em execuções subsequentes.
- **Coleta (Senado)** — consumo da API do Senado Federal com cursor por data e checkpoint incremental.
- **Filtro por palavras-chave** — filtragem automática das proposições coletadas com normalização de texto (remoção de acentos, caixa baixa), reduzindo ruído antes do armazenamento.
- **Armazenamento no PostgreSQL** — carga das proposições filtradas com deduplicação em lote via `id_externo`. Schema com tabelas `proposicoes` e `usuarios`.
- **Pipeline orquestrado** — `main.py` executa as 3 etapas em sequência com logs de progresso e tratamento de falhas por estágio.

#### API e Autenticação

- **API FastAPI** — rotas de registro, login e listagem de proposições (`/registrar`, `/login`, `/proposicoes`).
- **CRUD de usuários** — criação, leitura, atualização e exclusão, com senhas armazenadas via hash `bcrypt`.
- **CORS configurado** — integração habilitada com o frontend React (porta 5173).

#### Frontend React

- **Página de Login** — formulário com validação de campos e integração com a API.
- **Página de Cadastro** — fluxo completo de criação de conta integrado à API.
- **Home Page** — apresentação do produto e da equipe com identidade visual consolidada.

#### Dashboard Analítico

- **Dashboard Streamlit** — visualização das proposições armazenadas no PostgreSQL com gráficos e tabelas filtráveis, conectado diretamente ao banco.

#### Documentação

- **MkDocs publicado** — documentação técnica do projeto disponível via GitHub Pages, cobrindo arquitetura, pipeline, tecnologias, atas de sprint e equipe.

---

### Arquitetura

O sistema segue o padrão **Pipes and Filters**:

```
Coleta → dados_brutos.json → Filtro → dados_filtrados.json → Armazenamento → PostgreSQL → API / Dashboard
```

Cada etapa é independente e se comunica apenas via contrato de dados JSON fixo.

---

### Limitações Conhecidas

- Classificação por IA/NLP não entregue nesta release — planejada para a Release 2.
- Coleta incremental automática via GitHub Actions não configurada — execução manual via `python -m app.main`.
- Enriquecimento de dados (autor, partido, estado) retorna `"A pesquisar"` para a maioria dos registros.
- Acesso completo ao dashboard exige login — preview limitado para usuários não autenticados ainda não implementado.

---

### Equipe

| Membro | Área |
|---|---|
| Lucas | Arquitetura, CRUD, GitHub Actions |
| Gabriella | Frontend (Home, Dashboard) |
| Clara | Frontend (Login, User Flow) |
| Otávio | Backend (Filtro, API) |
| Edvaldo | Dados, DevOps, Redesign |
| João | Dados (Coleta, LLM) |

---

### Próxima Release

- Classificação temática por NLP (modelo BERT em português)
- Dashboard completo com gráficos avançados e mapas
- Coleta incremental diária via GitHub Actions
- Docker Compose unificando todos os serviços
