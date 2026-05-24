# Autenticação

## Visão Geral

O sistema implementa autenticação com níveis de acesso:

| Tipo de usuário | O que pode ver |
|---|---|
| Não cadastrado | Preview da página inicial (um gráfico ou trecho do mapa) |
| Cadastrado e logado | Dashboard completo, tabelas, filtros e todas as páginas |

---

## Segurança de Senhas

Senhas nunca são armazenadas em texto puro. O sistema usa **bcrypt** para gerar hashes saltados:

```python
import bcrypt

# Criar hash ao cadastrar
senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

# Verificar ao fazer login
bcrypt.checkpw(senha_digitada.encode(), senha_hash_do_banco)
```

!!! danger "Regra obrigatória"
    Jamais armazenar senha em texto puro. Jamais retornar `senha_hash` em consultas de listagem.

---

## CRUD de Usuários

Localização: `grupo5-guard.ia-backend/app/armazenamento/usuarios.py`

Funções implementadas:

| Função | Descrição |
|---|---|
| `criar_usuario(nome, email, senha)` | Cadastra novo usuário com hash de senha |
| `buscar_por_email(email)` | Retorna usuário pelo e-mail (sem `senha_hash`) |
| `verificar_senha(senha, hash)` | Valida credenciais no login |
| `deletar_usuario(email)` | Remove usuário do banco |
