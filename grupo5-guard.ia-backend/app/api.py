from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .armazenamento.database import execute_query

app = FastAPI(title="Guard.IA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mantemos apenas os modelos de dados úteis para as proposições
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

# --- ROTAS DE DADOS (Mantidas) ---

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
        raise HTTPException(status_code=500, detail=f"Erro ao buscar proposicoes: {e}")

@app.get("/stats")
def get_stats():
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