from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .armazenamento.usuarios import criar_usuario, buscar_por_email, verificar_senha, listar_usuarios
from .armazenamento.database import execute_query

app = FastAPI(title="Guard.IA API", version="1.0.0")

# Configuração de CORS para permitir acesso do React (Vite usa porta 5173 por padrão)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as URLs permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validação de dados
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

class ProposicaoResponse(BaseModel):
    id: int
    id_externo: str
    ementa: Optional[str]
    autor: Optional[str]
    partido: Optional[str]
    estado: Optional[str]
    casa: Optional[str]
    data_apresentacao: Optional[str]
    categoria: Optional[str]
    confianca: Optional[float]

# --- ROTAS DE AUTENTICAÇÃO ---

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate):
    existing_user = buscar_por_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    user_id = criar_usuario(user.nome, user.email, user.senha)
    if not user_id:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")
    
    return {"id": user_id, "nome": user.nome, "email": user.email}

@app.post("/auth/login")
def login(user: UserLogin):
    db_user = buscar_por_email(user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    if not verificar_senha(user.senha, db_user["senha_hash"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Aqui poderíamos retornar um token JWT, mas para a Release 1 retornaremos os dados básicos
    return {
        "id": db_user["id"],
        "nome": db_user["nome"],
        "email": db_user["email"],
        "message": "Login realizado com sucesso"
    }

# --- ROTAS DE DADOS ---

@app.get("/proposicoes", response_model=List[ProposicaoResponse])
def get_proposicoes(limit: int = 100, offset: int = 0):
    query = """
        SELECT id, id_externo, ementa, autor, partido, estado, 
               casa, data_apresentacao, categoria, confianca
        FROM proposicoes
        ORDER BY data_apresentacao DESC
        LIMIT %s OFFSET %s;
    """
    try:
        results = execute_query(query, (limit, offset), fetch=True)
        proposicoes = []
        if results:
            for row in results:
                proposicoes.append({
                    "id": row[0],
                    "id_externo": row[1],
                    "ementa": row[2],
                    "autor": row[3],
                    "partido": row[4],
                    "estado": row[5],
                    "casa": row[6],
                    "data_apresentacao": str(row[7]) if row[7] else None,
                    "categoria": row[8],
                    "confianca": row[9]
                })
        return proposicoes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar proposições: {e}")

@app.get("/stats")
def get_stats():
    """Retorna estatísticas para o dashboard."""
    query_total = "SELECT COUNT(*) FROM proposicoes;"
    query_categorias = "SELECT categoria, COUNT(*) FROM proposicoes GROUP BY categoria;"
    
    try:
        total = execute_query(query_total, fetch=True)[0][0]
        categorias = execute_query(query_categorias, fetch=True)
        
        return {
            "total_proposicoes": total,
            "por_categoria": {cat: count for cat, count in categorias if cat}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Guard.IA API is running"}
