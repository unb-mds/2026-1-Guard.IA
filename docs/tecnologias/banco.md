# Banco de Dados

## Schema

O arquivo `schema.sql` define as duas tabelas do sistema:

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

## Deduplicação em Lote

A inserção de proposições usa `ON CONFLICT DO NOTHING` — o banco ignora automaticamente registros com `id_externo` duplicado, sem precisar de queries extras:

```sql
INSERT INTO proposicoes (id_externo, ementa, ...)
VALUES %s
ON CONFLICT (id_externo) DO NOTHING;
```

Isso elimina o problema de performance **N+1** — em vez de fazer `SELECT` + `INSERT` para cada registro, enviamos tudo em uma única chamada de rede.

---

## Configuração Local

O banco sobe via Docker. Crie o arquivo `.env` na raiz do backend:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=guardia
DB_USER=postgres
DB_PASSWORD=sua_senha
```

!!! warning "Nunca versionar o .env"
    O arquivo `.env` contém credenciais e nunca deve ser commitado. Use o `.env.example` como referência.

Depois suba o container:

```bash
cd grupo5-guard.ia-backend
docker compose up -d
```
