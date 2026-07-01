1. Descrição:

- Implementação do CRUD completo de usuários para o sistema Guard.IA, permitindo que pessoas se cadastrem e façam login para acessar as informações sobre projetos de lei.

O que foi feito:

- Criada a API REST com FastAPI em grupo5-guard.ia-backend/app/usuario/ com os seguintes arquivos:

models.py — define a tabela de usuários no banco de dados
schemas.py — validação de entrada e saída dos dados
database.py — conexão com o banco de dados via SQLite (desenvolvimento) e PostgreSQL (produção)
usuarios.py — rotas da API

2. Endpoints disponíveis:

POST /usuarios — cadastrar usuário
GET /usuarios — listar todos os usuários
GET /usuarios/{id} — buscar usuário por ID
PATCH /usuarios/{id} — atualizar usuário
DELETE /usuarios/{id} — deletar usuário
POST /login — verificar credenciais

3. Como testar:
bashcd grupo5-guard.ia-backend/app/usuario
pip install -r requirements.txt
uvicorn usuarios:app --reload
Acessa http://127.0.0.1:8000/docs para ver e testar todos os endpoints.