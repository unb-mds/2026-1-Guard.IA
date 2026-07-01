# Infraestrutura como Código — Docker e Ambiente

## O Problema do "Na Minha Máquina Funciona"

Um dos maiores desafios em projetos de software desenvolvidos em equipe é a inconsistência de ambientes. Com 6 desenvolvedores no Guard.IA usando sistemas operacionais diferentes (macOS, Windows, Linux), versões diferentes do Python e configurações distintas de banco de dados, o cenário clássico se repetia:

```
Desenvolvedor A: "Funcionou aqui."
Desenvolvedor B: "Na minha máquina dá erro de conexão."
Desenvolvedor C: "Qual versão do PostgreSQL você instalou?"
Desenvolvedor D: "Que porta está usando?"
```

A solução adotada foi **Docker** — uma plataforma de containerização que empacota o software e todas as suas dependências em unidades isoladas e reproduzíveis chamadas **containers**.

!!! info "O que é um container?"
    Um container é um ambiente de execução isolado que contém tudo que uma aplicação precisa para rodar: sistema de arquivos, bibliotecas, variáveis de ambiente e configurações. É mais leve que uma máquina virtual e garante comportamento idêntico em qualquer host.

---

## Docker no Guard.IA

### O que foi containerizado

Na Release 1, o Docker é utilizado exclusivamente para o **banco de dados PostgreSQL**. Isso resolve o problema mais crítico de ambiente: garantir que todos os membros da equipe usem a mesma versão, configuração e porta do banco.

### O arquivo docker-compose.yml

O `docker-compose.yml` define o ambiente de forma declarativa:

```yaml
services:
  db:
    image: postgres:15
    container_name: monitoramento_legislativo_db
    environment:
      POSTGRES_DB: guardia
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./app/armazenamento/schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  postgres_data:
```

Cada campo tem uma função específica:

| Campo | Função |
|---|---|
| `image: postgres:15` | Define a versão exata do PostgreSQL — todos usam a mesma |
| `container_name` | Nome fixo para o container, facilitando comandos de manutenção |
| `environment` | Variáveis de configuração — lidas do arquivo `.env` |
| `ports` | Mapeia a porta 5432 do container para a máquina local |
| `volumes` | Persiste os dados mesmo após reiniciar o container |
| `docker-entrypoint-initdb.d` | Executa o `schema.sql` automaticamente na primeira inicialização |

!!! success "Inicialização automática do schema"
    O mapeamento do `schema.sql` para `docker-entrypoint-initdb.d/` é um recurso nativo do PostgreSQL no Docker. Na primeira vez que o container é iniciado, ele executa automaticamente todos os arquivos `.sql` da pasta — criando as tabelas `proposicoes` e `usuarios` sem nenhum comando manual.

---

## Variáveis de Ambiente e Segurança

### Por que não colocar credenciais no código?

Hardcodar credenciais de banco diretamente no código é uma prática insegura que:

- Expõe senhas no histórico do Git
- Impede o uso de credenciais diferentes em produção e desenvolvimento
- Dificulta a rotação de senhas em caso de comprometimento

```python
# ❌ NUNCA fazer isso
conn = psycopg2.connect(
    host="localhost",
    password="minha_senha_secreta"  # exposta no Git
)
```

### O arquivo .env

O Guard.IA usa variáveis de ambiente carregadas de um arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=guardia
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

O arquivo `.env` **nunca é versionado** — está no `.gitignore`. O repositório contém apenas o `.env.example` com os campos necessários mas sem valores reais:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=guardia
DB_USER=postgres
DB_PASSWORD=
```

!!! warning "Regra obrigatória do projeto"
    O arquivo `.env` nunca deve ser commitado. Credenciais expostas no Git são uma vulnerabilidade de segurança grave — mesmo em repositórios privados. O GEMINI.md registra essa regra formalmente: *"Nunca versionar `.env`"*.

### Como o Python lê as variáveis

```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", 5432),
    "dbname":   os.getenv("DB_NAME", "guardia"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}
```

---

## Como Subir o Ambiente

Com Docker instalado, qualquer membro da equipe consegue ter o banco rodando com dois comandos:

```bash
# 1. Copiar o arquivo de ambiente
cp .env.example .env
# (editar .env com a senha desejada)

# 2. Subir o container do banco
docker compose up -d
```

O banco estará disponível em `localhost:5432` em segundos, com as tabelas já criadas e pronto para receber dados do pipeline.

Para verificar se está saudável:

```bash
docker ps
# CONTAINER ID   IMAGE         STATUS
# abc123         postgres:15   Up 2 minutes (healthy)
```

Para encerrar:

```bash
docker compose down
```

!!! info "Persistência dos dados"
    O volume `postgres_data` garante que os dados inseridos no banco sobrevivem ao `docker compose down`. Para apagar tudo e começar do zero: `docker compose down -v`.

---

## Isolamento do Pipeline de Dados

O Docker garante que o banco está sempre em um estado conhecido antes do pipeline executar. O `main.py` pode assumir que:

1. O banco está disponível em `localhost:5432`
2. As tabelas `proposicoes` e `usuarios` existem
3. As constraints (`UNIQUE`, `NOT NULL`) estão ativas

Isso elimina uma classe de erros do tipo `relation "proposicoes" does not exist` que ocorre quando o banco não foi inicializado corretamente.

```
docker compose up -d        # banco sobe com schema aplicado
        ↓
python -m app.main          # pipeline executa com banco garantido
        ↓
655 proposições inseridas   # resultado previsível e reproduzível
```

---

## Release 2 — Docker Compose Completo

Na Release 1, apenas o banco é containerizado. Para a Release 2, o plano é expandir o `docker-compose.yml` para incluir todos os serviços:

```yaml
services:
  db:        # PostgreSQL
  api:       # FastAPI
  frontend:  # React (build estático)
  dashboard: # Streamlit
```

Com isso, o comando `docker compose up` sobe o sistema inteiro — banco, API, frontend e dashboard — sem nenhuma instalação manual além do próprio Docker.

!!! tip "Objetivo da Release 2"
    Um único `docker compose up` para subir o Guard.IA completo. Zero configuração manual. Ambiente 100% reproduzível em qualquer máquina.

---

## Referências

- Docker Documentation. *Docker Compose*. Disponível em: https://docs.docker.com/compose/
- Docker Documentation. *Use environment variables*. Disponível em: https://docs.docker.com/compose/environment-variables/
- PostgreSQL Docker Hub. *Official Image Documentation*. Disponível em: https://hub.docker.com/_/postgres
