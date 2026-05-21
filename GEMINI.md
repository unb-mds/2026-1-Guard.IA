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
7. O contrato de dados entre etapas é fixo — qualquer alteração no schema JSON deve ser comunicada e aprovada por todas as etapas.
8. Prefira componentes reutilizáveis e desacoplados em vez de soluções rápidas e específicas.

### Dados e Pipeline

9. O arquivo `dados_brutos.json` é de responsabilidade exclusiva da etapa de Coleta.
10. O arquivo `dados_filtrados.json` é de responsabilidade exclusiva da etapa de Filtro.
11. O banco de dados PostgreSQL é de responsabilidade exclusiva da etapa de Armazenamento.
12. Nenhuma etapa deve ler ou escrever no arquivo de outra etapa diretamente.
13. **SQLite é proibido no projeto.** O banco oficial é PostgreSQL. Todo código que usar SQLite deve ser adaptado.

### Acesso e Autenticação

14. Usuários não cadastrados podem visualizar apenas um preview da página inicial (um gráfico ou trecho do mapa).
15. Acesso completo ao dashboard, tabelas, filtros e demais páginas exige cadastro e login.
16. Senhas nunca devem ser armazenadas em texto puro — sempre usar hash via `bcrypt`.
17. O CRUD de usuários é responsabilidade exclusiva do módulo `grupo5-guard.ia-backend/app/armazenamento/usuarios.py`.
18. A pasta `app/usuario/` criada na branch `feat/crud-usuario` deve ser migrada para `app/armazenamento/usuarios.py` e adaptada para PostgreSQL.

### Ética e Transparência

19. Toda classificação gerada pela IA deve deixar explícito que se trata de uma estimativa — nunca apresentar como fato absoluto.
20. O campo `confianca` deve sempre acompanhar o campo `categoria` na visualização.

---

## Stack Tecnológico

| Parte | Tecnologia |
|---|---|
| Coleta, Filtro, Classificação, Armazenamento | Python 3.10+ |
| Banco de dados | PostgreSQL (via Docker) |
| ORM / Conector | psycopg2 (SQL puro — sem ORM) |
| Dashboard | Streamlit + Plotly |
| Autenticação | bcrypt (hash de senha) |
| Infraestrutura | Docker + Docker Compose + GitHub Actions |
| Gerenciamento de dependências | pip + requirements.txt |

> **Decisão arquitetural:** O projeto usa `psycopg2` com SQL puro, não SQLAlchemy. Isso é compatível com o pipeline de scripts Python e com o `schema.sql` já existente. Não introduzir ORM sem alinhamento explícito.

---

## Pipeline do Sistema

```
grupo5-guard.ia-backend/app/coleta/
  coletor_camara.py  ──┐
                       ├──► data/dados_brutos.json ──► filtro.py ──► data/dados_filtrados.json ──► armazenamento.py ──► PostgreSQL ──► dashboard
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
  "data_apresentacao": "2023-01-15"
}
```

**Prefixos obrigatórios do `id_externo`:**
- Câmara: `CAMARA-{id}`
- Senado: `SENADO-{codigo}`

---

## Estrutura Real de Pastas

```
2026-1-Guard.IA/
├── .github/workflows/              # Automação e métricas
├── dashboard/                      # Ignorar — versão antiga
├── docs/                           # Documentação das sprints
├── grupo5-guard.ia/                # Frontend estático (Next.js/React)
├── grupo5-guard.ia-backend/        # BACKEND — pipeline de dados
│   ├── app/
│   │   ├── armazenamento/
│   │   │   ├── database.py         # Conexão PostgreSQL via psycopg2
│   │   │   ├── models.py           # Definições de tabelas
│   │   │   ├── schema.sql          # SQL de criação das tabelas
│   │   │   ├── armazenamento.py    # Inserção de proposições
│   │   │   └── usuarios.py         # CRUD de usuários ← destino oficial
│   │   ├── classificacao/
│   │   ├── coleta/
│   │   │   ├── coletor_camara.py
│   │   │   └── coletor_senado.py
│   │   ├── filtro/
│   │   │   └── filtro.py
│   │   └── main.py
│   ├── data/                       # JSONs gerados localmente — nunca versionar
│   │   ├── dados_brutos.json
│   │   ├── dados_filtrados.json
│   │   ├── checkpoint_camara.json
│   │   └── checkpoint_senado.json
│   └── docker-compose.yml
└── grupo5-guard.ia-frontend/       # FRONTEND — Dashboard Release 1
    └── dashboard/
        ├── app.py
        └── pages/
```

---

## Convenções Técnicas

### Python
- Versão: 3.10+
- Funções nomeadas em `snake_case`
- Constantes em `UPPER_SNAKE_CASE`
- Classes em `PascalCase`
- Arquivos em `snake_case`

### Coleta
- Sempre usar `headers = {"Accept": "application/json"}` nas requisições
- Sempre usar `timeout=30` nas requisições
- Sempre implementar checkpoint para retomada em caso de falha
- Batch saving: salvar dados apenas ao final de cada página/lote, nunca por item
- Deduplicação obrigatória por `id_externo` antes de inserir

### Filtro
- Normalização obrigatória antes de comparar: minúsculas + remoção de acentos via `unicodedata`
- Nunca comparar strings sem normalizar
- Lista de palavras-chave centralizada em uma constante no topo do arquivo

### Classificação
- Modelo principal: `neuralmind/bert-base-portuguese-cased`
- Modelo alternativo (hardware fraco): `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Sempre salvar o campo `confianca` junto com `categoria`

### Armazenamento
- Banco: PostgreSQL
- Conector: `psycopg2` — SQL puro, sem ORM
- Configuração de conexão via variáveis de ambiente (`.env`) — nunca hardcoded
- Sempre verificar duplicatas por `id_externo` antes de inserir
- Docker obrigatório para subir o banco localmente via `docker-compose.yml`

### Usuários
- Arquivo responsável: `grupo5-guard.ia-backend/app/armazenamento/usuarios.py`
- Banco: PostgreSQL — nunca SQLite
- Senhas armazenadas com hash via `bcrypt`
- Funções obrigatórias: `criar_usuario`, `buscar_por_email`, `verificar_senha`, `deletar_usuario`
- Nunca retornar `senha_hash` em consultas de listagem

### Dashboard
- Localização: `grupo5-guard.ia-frontend/dashboard/`
- Framework: Streamlit
- Gráficos: Plotly
- Sempre usar `@st.cache_data` em funções que consultam o banco
- Usuário não logado: vê apenas preview da página inicial (um gráfico ou trecho do mapa)
- Usuário logado: acesso completo a todas as páginas e funcionalidades

---

## Palavras-chave do Filtro

```python
PALAVRAS_CHAVE = [
    "crianca", "adolescente", "menor", "internet", "digital",
    "online", "cyberbullying", "redes sociais", "lgpd",
    "marco civil", "privacidade", "aplicativo", "eca",
    "conteudo inapropriado", "tempo de tela"
]
```
> Nota: a lista deve estar normalizada (sem acentos, minúsculas) pois o texto também será normalizado antes da comparação.

---

## Categorias da Classificação

```python
CATEGORIAS = {
    "cyberbullying":        "assédio, bullying, violência psicológica online",
    "privacidade_dados":    "coleta de dados pessoais, LGPD, proteção de informações",
    "tempo_de_tela":        "uso excessivo, dependência digital, limite de uso",
    "conteudo_inapropriado":"pornografia, violência, conteúdo adulto na internet",
    "educacao_digital":     "letramento digital, ensino, alfabetização tecnológica"
}
```

---

## Schema do Banco de Dados (PostgreSQL)

Localização do arquivo: `grupo5-guard.ia-backend/app/armazenamento/schema.sql`

```sql
CREATE TABLE IF NOT EXISTS proposicoes (
    id                SERIAL PRIMARY KEY,
    id_externo        VARCHAR(50) UNIQUE,
    ementa            TEXT,
    autor             VARCHAR(200),
    partido           VARCHAR(20),
    estado            VARCHAR(2),
    casa              VARCHAR(10),
    data_apresentacao DATE,
    categoria         VARCHAR(100),
    confianca         FLOAT,
    coletado_em       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS usuarios (
    id                SERIAL PRIMARY KEY,
    nome              VARCHAR(100) NOT NULL,
    email             VARCHAR(150) UNIQUE NOT NULL,
    senha_hash        VARCHAR(255) NOT NULL,
    criado_em         TIMESTAMP DEFAULT NOW()
);
```

---

## Regras de Git

- Nunca commitar diretamente na `main`.
- Branch de desenvolvimento: `dev-projeto`
- Padrões de branch:
  - `feat/<nome>`
  - `fix/<nome>`
  - `chore/<nome>`
  - `docs/<nome>`
- Mensagens de commit: Conventional Commits — `feat(armazenamento): descrição`, `fix(filtro): descrição`
- Nunca versionar `data/*.json` — arquivos gerados localmente
- Nunca versionar `__pycache__/`
- Nunca versionar `.env`

---

## Release 1 — Escopo

Funcionalidades obrigatórias para a Release 1:

- [x] Coleta da Câmara funcionando com paginação e checkpoint
- [x] Coleta do Senado funcionando com cursor por data e checkpoint
- [ ] Filtro por palavras-chave com normalização de texto
- [ ] `schema.sql` atualizado com tabelas `proposicoes` e `usuarios`
- [ ] Armazenamento no PostgreSQL — inserção de proposições com deduplicação
- [ ] CRUD de usuários em PostgreSQL com hash de senha
- [ ] Páginas de login e cadastro integradas com o banco
- [ ] Página inicial com preview para usuário não logado
- [ ] Dashboard básico com pelo menos 1 visualização para usuário logado

**Fora do escopo da Release 1:**
- Classificação por IA (Release 2)
- Dashboard completo com todos os gráficos (Release 2)
- Coleta incremental automática via GitHub Actions (Release 2)
- Preenchimento de `autor`, `partido` e `estado` (Release 2)

---

## Release 2 — Escopo

- [ ] Classificação por IA/NLP
- [ ] Dashboard completo com todos os gráficos
- [ ] Coleta incremental diária via GitHub Actions
- [ ] Enriquecimento de dados (autor, partido, estado)
- [ ] Docker Compose unificando todos os serviços

---

## Fora de Escopo Permanente

A menos que explicitamente solicitado, **não faça**:

- Usar SQLite em qualquer parte do projeto
- Usar SQLAlchemy ou qualquer ORM — o projeto usa psycopg2 com SQL puro
- Alterar o schema JSON do contrato de dados sem alinhar todas as etapas
- Adicionar dependências externas sem necessidade real
- Criar lógica de negócio no Dashboard (só visualização)
- Acessar o banco diretamente na etapa de Coleta ou Filtro
- Salvar dados por item dentro de loops (sempre batch saving)
- Fazer chamadas extras à API por proposição
- Modificar arquivos de outras etapas sem alinhamento com o responsável
- Armazenar senhas em texto puro
- Retornar `senha_hash` em consultas de listagem de usuários
- Hardcodar credenciais de banco no código — sempre usar `.env`

---

## Memória Evolutiva

Este arquivo deve ser atualizado sempre que:
- Uma etapa do pipeline for concluída
- Uma decisão técnica importante for tomada
- Uma convenção nova for estabelecida
- O schema de dados for alterado
- A estrutura de pastas mudar

Nunca duplicar informações já existentes. Sempre evolução incremental.
