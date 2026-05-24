import bcrypt
from .database import execute_query

def hash_senha(senha: str) -> str:
    """Gera um hash saltado para a senha."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash."""
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))

def criar_usuario(nome: str, email: str, senha: str):
    """
    Cria um novo usuário no PostgreSQL.
    Retorna o ID do usuário criado ou None se houver erro (ex: email duplicado).
    """
    senha_hash = hash_senha(senha)
    query = """
        INSERT INTO usuarios (nome, email, senha_hash)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    try:
        result = execute_query(query, (nome, email, senha_hash), fetch=True)
        if result:
            return result[0][0]
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
    return None

def buscar_por_email(email: str):
    """
    Busca um usuário pelo email.
    Retorna um dicionário com os dados ou None.
    """
    query = "SELECT id, nome, email, senha_hash, criado_em FROM usuarios WHERE email = %s;"
    try:
        result = execute_query(query, (email,), fetch=True)
        if result:
            row = result[0]
            return {
                "id": row[0],
                "nome": row[1],
                "email": row[2],
                "senha_hash": row[3],
                "criado_em": row[4]
            }
    except Exception as e:
        print(f"Erro ao buscar por email {email}: {e}")
    return None

def deletar_usuario(usuario_id: int) -> bool:
    """Remove um usuário pelo ID."""
    query = "DELETE FROM usuarios WHERE id = %s;"
    try:
        execute_query(query, (usuario_id,))
        return True
    except Exception:
        return False

def listar_usuarios():
    """
    Lista todos os usuários.
    IMPORTANTE: Nunca retorna o campo senha_hash.
    """
    query = "SELECT id, nome, email, criado_em FROM usuarios;"
    results = execute_query(query, fetch=True)
    
    usuarios = []
    if results:
        for row in results:
            usuarios.append({
                "id": row[0],
                "nome": row[1],
                "email": row[2],
                "criado_em": row[3]
            })
    return usuarios
