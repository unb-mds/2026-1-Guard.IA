from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional

# Importamos a lógica de armazenamento já existente
try:
    from .armazenamento import usuarios
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent))
    from armazenamento import usuarios

app = FastAPI(title="Guard.IA API", version="1.0.0")

# Configuração de CORS para permitir que o frontend (Vite) acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir para o domínio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic para validação
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str

@app.get("/")
async def root():
    return {"message": "Guard.IA API is running"}

@app.post("/login", response_model=UserResponse)
async def login(request: LoginRequest):
    """
    Endpoint de login que verifica as credenciais no PostgreSQL.
    """
    user = usuarios.buscar_por_email(request.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Verifica a senha usando o hash bcrypt
    if not usuarios.verificar_senha(request.senha, user["senha_hash"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Retorna os dados do usuário (exceto a senha)
    return {
        "id": user["id"],
        "nome": user["nome"],
        "email": user["email"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
