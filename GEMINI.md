# GEMINI.md — Guard.IA
> Arquivo de contexto arquitetural. Leia completamente antes de qualquer implementação.

---

## Projeto

**Guard.IA** — plataforma de monitoramento legislativo focada na proteção de crianças e adolescentes na internet. O sistema coleta automaticamente proposições da Câmara dos Deputados e do Senado Federal, filtra as relevantes por palavras-chave, classifica por tema usando IA e exibe os dados em um portal visual acessível.

O sistema é focado em cidadãos, pesquisadores, jornalistas e profissionais interessados em acompanhar a legislação sobre proteção digital de menores.

---

## Constituição

### Confiabilidade e Qualidade

1. O sistema deve continuar funcional mesmo quando as APIs externas da Câmara ou Senado estiverem indisponíveis temporariamente.
2. Toda coleta de dados legislativos deve ser rastreável via checkpoint, registrando falhas, sucessos e progresso.
3. Nenhuma funcionalidade crítica deve depender exclusivamente de dados em tempo real — prefira dados persistidos no banco.
4. O sistema deve tratar dados incompletos sem quebrar o pipeline ou a interface.

### Arquitetura e Engenharia

5. Respeite rigorosamente a arquitetura **Pipes and Filters**: cada etapa do pipeline é independente e se comunica apenas com a etapa seguinte.
6. Nenhuma etapa do pipeline deve conhecer a implementação interna de outra etapa.
7. O contrato de dados entre etapas é fixo - qualquer alteração no schema JSON deve ser comunicada e aprovada por todas as etapas.
8. Prefira componentes reutilizáveis e desacoplados em vez de soluções rápidas e específicas.

### Dados e Pipeline

9. O arquivo `dados_brutos.json` é de responsabilidade exclusiva da etapa de Coleta.
10. O arquivo `dados_filtrados.json` é de responsabilidade exclusiva da etapa de Filtro.
11. O banco de dados PostgreSQL é de responsabilidade exclusiva da etapa de Armazenamento.
12. Nenhuma etapa deve ler ou escrever no arquivo de outra etapa diretamente.
13. **SQLite é proibido no projeto.** O banco oficial é PostgreSQL. Todo código que usar SQLite deve ser adaptado.

### Ética e Transparência

19. Toda classificação gerada pela IA deve deixar explícito que se trata de uma estimativa — nunca apresentar como fato absoluto.
20. O campo `confianca` deve sempre acompanhar o campo `categoria` na visualização.

---

## Stack Tecnológico

| Parte | Tecnologia |
|---|---|
| Pipeline (Coleta, Filtro, etc.) | Python 3.10+ |
| Backend API | FastAPI |
| Banco de dados | PostgreSQL (via Docker) |
| ORM / Conector | psycopg2 (SQL puro — sem ORM) |
| Frontend Principal | React (Vite) + JavaScript + CSS |
| Documentação | MkDocs (Material theme) |
| Infraestrutura | Docker + GitHub Actions + GitHub Pages |

> **Decisão arquitetural:** O projeto usa `psycopg2` com SQL puro, não SQLAlchemy. Isso é compatível com o pipeline de scripts Python e com o `schema.sql` já existente. Não introduzir ORM sem alinhamento explícito.

---

## Pipeline do Sistema

```
grupo5-guard.ia-backend/app/coleta/
  coletor_camara.py  ──┐
                       ├──► data/dados_brutos.json ──► filtro.py ──► data/dados_filtrados.json ──► armazenamento.py ──► PostgreSQL ──► dashboard/API
  coletor_senado.py  ──┘
```

Cada etapa recebe um input, processa e entrega um output. Nunca pula etapas.

---

## Contrato de Dados (Schema JSON)

Este é o schema padrão que todas as etapas devem respeitar. Nunca altere os nomes dos campos sem alinhar com todas as etapas.

```json
{
  "id_externo": "CAMARA-104417",
  "ementa": "Texto da proposição...",
  "autor": "A pesquisar",
  "partido": "A pesquisar",
  "estado": "A pesquisar",
  "casa": "Câmara",
  "data_apresentacao": "2023-01-15",
  "termos_chave": ["internet", "crianca"]
}
```

**Campos Adicionais (Auditoria):**
- `termos_chave`: (Opcional) Lista de termos que causaram a captura no Filtro.

**Prefixos obrigatórios do `id_externo`:**
- Câmara: `CAMARA-{id}`
- Senado: `SENADO-{codigo}`

---

## Estrutura de Pastas

```
2026-1-Guard.IA/
├── .github/workflows/      # Automação e métricas
├── docs/                   # Documentação MkDocs (Markdown)
├── mkdocs.yml              # Configuração da documentação
├── grupo5-guard.ia/        # FRONTEND — React (Vite)
│   ├── src/
│   │   ├── pages/ (Home, VisualizacaoProposicoes)
│   │   └── App.jsx (Roteamento)
└── grupo5-guard.ia-backend/ # BACKEND — pipeline de dados e API
    ├── app/
    │   ├── api.py          # API FastAPI (Entrega de Dados)
    │   ├── armazenamento/
    │   │   └── database.py # Conexão PostgreSQL e inserção
    │   ├── coleta/
    │   ├── filtro/
    │   └── main.py         # Orquestrador do pipeline
    └── docker-compose.yml
```

---

## Convenções Técnicas

### Python
- Versão: 3.10+
- Funções em `snake_case`, Classes em `PascalCase`.
- API: Porta padrão 8000.

### Frontend (React)
- Vite como build tool.
- CSS puro para estilização (conforme design da branch `feat/pag-cadastro`).
- Comunicação com API via `fetch` para `http://localhost:8000`.

### Documentação (MkDocs)
- Branch de deploy: `gh-pages`.
- Todo conteúdo novo deve ser adicionado em `docs/` como `.md`.

### Armazenamento
- Banco: PostgreSQL.
- Docker obrigatório para subir o banco localmente.

---

## Release 1 — Escopo

Funcionalidades obrigatórias para a Release 1:

- [x] Coleta da Câmara e Senado com checkpoint.
- [x] Filtro por palavras-chave com normalização.
- [x] Armazenamento no PostgreSQL com deduplicação.
- [x] CRUD de usuários com hash de senha (bcrypt).
- [x] API FastAPI (Login, Registro, Listagem de Proposições).
- [x] Frontend React (Home, Login, Cadastro) integrado à API.
- [x] Dashboard Streamlit funcional conectado ao banco.
- [x] Documentação MkDocs publicada via GitHub Pages.

---

## Release 2 — Escopo

- [ ] Classificação por IA/NLP.
- [ ] Dashboard completo com gráficos avançados.
- [ ] Coleta incremental diária via GitHub Actions.
- [ ] Docker Compose unificando Frontend, API e Banco.
- [ ] Remoção do CRUD de Usuários e Login: Sendo um projeto estritamente acadêmico, sem fins lucrativos e focado em dados abertos, a remoção do controle de acesso reduz a complexidade desnecessária de segurança (LGPD, hashes e gerenciamento de estado de sessão), eliminando barreiras para usuários finais (jornalistas/pesquisadores).

---

## Regras de Git

- Nunca commitar na `main` diretamente. Use PRs.
- Mensagens: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Deploy de Docs: `mkdocs gh-deploy` (gera branch `gh-pages`).

---

## Memória Evolutiva

Junho de 2026: Decisão de escopo tomada pela equipe de remover o fluxo de autenticação (Login/Cadastro) e o dashboard Streamlit secundário. O projeto passa a ser um portal de acesso público direto construído puramente em React integrado à API FastAPI, simplificando a arquitetura e focando na transparência dos dados.

-Este arquivo deve ser atualizado sempre que uma decisão técnica mudar o rumo do projeto ou uma nova tecnologia for adotada.-
