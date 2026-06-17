# Decisão de Banco de Dados: PostgreSQL

## Contexto

Durante o desenvolvimento do Guard.IA, um membro da equipe iniciou a implementação do módulo de usuários utilizando **SQLite** como banco de dados. A decisão foi revertida e formalizada como regra arquitetural: **SQLite é proibido no projeto**. Este documento registra o raciocínio técnico por trás dessa decisão e justifica a adoção do PostgreSQL com psycopg2.

---

## Limitações do SQLite para o Guard.IA

SQLite é um banco de dados excelente para prototipagem rápida e aplicações de uso pessoal. No entanto, apresenta limitações críticas para um sistema como o Guard.IA.

### Concorrência limitada

SQLite utiliza um modelo de bloqueio de arquivo inteiro (*file-level locking*). Quando uma operação de escrita está em andamento, **nenhuma outra operação** — leitura ou escrita — pode ocorrer simultaneamente.

No Guard.IA, o pipeline de dados pode executar inserções em lote de centenas de proposições enquanto a API FastAPI recebe requisições de leitura. Com SQLite, esse cenário geraria contenção de lock e falhas imprevisíveis.

```
Pipeline inserindo 655 registros
         ↓
     [LOCK no arquivo .db]
         ↓
API tenta ler dados → ❌ Database is locked
```

!!! warning "Problema real identificado"
    Durante os testes iniciais com SQLite, a equipe identificou erros de `database is locked` ao tentar acessar o banco enquanto o pipeline de armazenamento estava em execução. Esse comportamento é incompatível com um sistema que precisa ser consultado em tempo real.

### Tipagem fraca

SQLite utiliza tipagem dinâmica — qualquer valor pode ser inserido em qualquer coluna, independentemente do tipo declarado. Isso significa que um campo `DATE` pode receber uma string `"ontem"` sem erro.

Em um sistema que processa dados de APIs externas com formatos variados (datas no formato `2023-01-15T00:00:00`, `2023-01-15`, `20230115`), a ausência de tipagem forte é uma fonte constante de bugs silenciosos.

### Ausência de recursos avançados

SQLite não suporta nativamente:

- `INSERT ... ON CONFLICT DO NOTHING` — essencial para a deduplicação em lote do Guard.IA
- Connection pooling — necessário para a API FastAPI com múltiplos workers
- Roles e permissões de acesso
- Replicação e backup incremental

---

## Por que PostgreSQL?

### Concorrência real com MVCC

PostgreSQL utiliza **MVCC (Multiversion Concurrency Control)**, que permite leituras e escritas simultâneas sem bloqueio. Cada transação enxerga um snapshot consistente dos dados, sem interferir nas demais.

```
Pipeline inserindo 655 registros  →  ✅ Executa normalmente
API lendo proposições             →  ✅ Executa simultaneamente
Usuário fazendo login             →  ✅ Executa simultaneamente
```

### Tipagem forte e integridade de dados

PostgreSQL impõe os tipos declarados no schema. Um campo `DATE` só aceita datas válidas. Um campo `VARCHAR(50)` não aceita strings maiores. Isso garante que os dados no banco refletem exatamente o que foi projetado no `schema.sql`.

```sql
-- PostgreSQL rejeita inserções inválidas
INSERT INTO proposicoes (data_apresentacao) VALUES ('ontem');
-- ERROR: invalid input syntax for type date: "ontem"
```

### Suporte a INSERT ... ON CONFLICT

A cláusula `ON CONFLICT DO NOTHING` é fundamental para a estratégia de deduplicação do Guard.IA:

```sql
INSERT INTO proposicoes (id_externo, ementa, ...)
VALUES %s
ON CONFLICT (id_externo) DO NOTHING;
```

Isso elimina o problema de performance N+1 — em vez de fazer `SELECT` + `INSERT` para cada registro, enviamos todo o lote em uma única chamada, delegando a deduplicação ao banco.

!!! success "Resultado mensurável"
    Com `ON CONFLICT DO NOTHING` via `execute_values`, o tempo de inserção de 655 registros caiu para **0.03 segundos**. A abordagem anterior com SELECT + INSERT levaria aproximadamente **13 segundos** para o mesmo volume.

### Escalabilidade

PostgreSQL suporta tabelas com bilhões de registros, índices avançados (B-tree, GIN, GiST), particionamento e replicação. Para a Release 2, quando o Guard.IA precisar de buscas por texto completo na ementa das proposições, o PostgreSQL oferece suporte nativo com `tsvector` e `tsquery`.

---

## Por que Docker para o PostgreSQL?

### O problema sem Docker

Sem Docker, cada membro da equipe precisaria instalar o PostgreSQL localmente, configurar usuário, senha, porta e banco manualmente. Com 6 desenvolvedores em sistemas operacionais diferentes (macOS, Windows, Linux), as configurações divergem e surgem erros do tipo:

- "Na minha máquina funciona"
- Versões diferentes do PostgreSQL
- Conflito de portas
- Configurações de autenticação incompatíveis

### A solução com Docker

O `docker-compose.yml` define o ambiente de forma declarativa e reproduzível:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: guardia
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
```

Com um único comando, qualquer membro da equipe sobe um PostgreSQL idêntico ao de produção:

```bash
docker compose up -d
```

!!! info "Ambientes consistentes"
    Docker garante que o banco que roda no MacBook do desenvolvedor é idêntico ao que rodará no servidor de produção. Isso elimina uma classe inteira de bugs relacionados a diferenças de ambiente.

---

## Por que SQL puro com psycopg2 e não SQLAlchemy?

### O que é um ORM?

Um ORM (Object-Relational Mapper) como SQLAlchemy abstrai o SQL, permitindo manipular o banco através de objetos Python. À primeira vista parece mais simples, mas introduz uma camada de complexidade que não se justifica para o Guard.IA.

### Razões para evitar SQLAlchemy no Guard.IA

**1. O pipeline já usa SQL explícito**

O `schema.sql` define as tabelas diretamente em SQL. Usar SQLAlchemy exigiria reescrever essas definições como classes Python, duplicando a fonte de verdade do schema.

**2. `execute_values` não tem equivalente direto em ORM**

A inserção em lote com `psycopg2.extras.execute_values` é a técnica mais eficiente para inserir centenas de registros de uma vez. ORMs geralmente não expõem esse nível de controle sem configuração avançada.

**3. Complexidade desnecessária**

Para um pipeline de dados com operações CRUD simples e bem definidas, a abstração do ORM adiciona camadas de configuração (sessions, engines, declarative base) sem benefício real.

**4. Transparência arquitetural**

Com SQL puro, cada query é visível e auditável. Não há "mágica" por baixo dos panos. Qualquer desenvolvedor consegue ler o código e entender exatamente o que está sendo executado no banco.

```python
# SQL puro — claro, direto, controlável
query = """
    INSERT INTO proposicoes (id_externo, ementa, casa, data_apresentacao)
    VALUES %s
    ON CONFLICT (id_externo) DO NOTHING;
"""
execute_values(cursor, query, params_list)
```

!!! warning "Decisão formal registrada"
    A proibição de SQLAlchemy está documentada no `GEMINI.md` como regra arquitetural permanente. Qualquer introdução de ORM no projeto requer aprovação explícita de toda a equipe.

---

## Resumo das Decisões

| Decisão | Escolha | Motivo principal |
|---|---|---|
| Banco de dados | PostgreSQL | Concorrência, tipagem forte, `ON CONFLICT` |
| SQLite | ❌ Proibido | Lock de arquivo, tipagem fraca, sem `ON CONFLICT` |
| Ambiente | Docker | Consistência entre máquinas da equipe |
| Conector | psycopg2 | SQL puro, `execute_values`, sem abstração desnecessária |
| ORM | ❌ Não utilizado | Complexidade sem benefício para o pipeline |

---

## Referências

- PostgreSQL Documentation. *Concurrency Control*. Disponível em: https://www.postgresql.org/docs/current/mvcc.html
- KLEPPMANN, Martin. *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
- psycopg2 Documentation. *Fast execution helpers*. Disponível em: https://www.psycopg.org/docs/extras.html#fast-exec
