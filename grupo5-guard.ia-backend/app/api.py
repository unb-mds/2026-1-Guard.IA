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

class ClassificacaoRequest(BaseModel):
    texto: str

class ClassificacaoResponse(BaseModel):
    categoria: str
    confianca: float

@app.get("/proposicoes", response_model=List[ProposicaoResponse])
def get_proposicoes(
    limit: int = 20,
    offset: int = 0,
    categoria: Optional[str] = None,
    partido: Optional[str] = None,
    casa: Optional[str] = None
):
    filters = []
    params = []

    if categoria:
        filters.append("categoria = %s")
        params.append(categoria)
    if partido:
        filters.append("partido = %s")
        params.append(partido)
    if casa:
        filters.append("casa = %s")
        params.append(casa)

    where = ("WHERE " + " AND ".join(filters)) if filters else ""

    query = f"""
        SELECT id, id_externo, ementa, autor, partido, estado,
               casa, data_apresentacao, categoria, confianca
        FROM proposicoes
        {where}
        ORDER BY data_apresentacao DESC
        LIMIT %s OFFSET %s;
    """
    params += [limit, offset]

    try:
        results = execute_query(query, tuple(params), fetch=True)
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
   
@app.get("/proposicoes/{id}", response_model=ProposicaoResponse)
def get_proposicao(id: int):
    query = """
        SELECT id, id_externo, ementa, autor, partido, estado,
               casa, data_apresentacao, categoria, confianca
        FROM proposicoes WHERE id = %s;
    """
    result = execute_query(query, (id,), fetch=True)
    if not result:
        raise HTTPException(status_code=404, detail="Proposição não encontrada")
    row = result[0]
    return {"id": row[0], "id_externo": row[1], "ementa": row[2], "autor": row[3],
            "partido": row[4], "estado": row[5], "casa": row[6],
            "data_apresentacao": str(row[7]) if row[7] else None,
            "categoria": row[8], "confianca": row[9]}

@app.post("/classificar", response_model=ClassificacaoResponse)
def classificar(request: ClassificacaoRequest):
    from .classificacao.classificador import classificar_texto
    resultado = classificar_texto(request.texto)
    return {"categoria": resultado["categoria"], "confianca": resultado["confianca"]}

@app.get("/stats")
def get_stats():
    query_total = "SELECT COUNT(*) FROM proposicoes;"
    query_categorias = "SELECT categoria, COUNT(*) FROM proposicoes GROUP BY categoria;"
    query_partidos = "SELECT partido, COUNT(*) FROM proposicoes GROUP BY partido;"
    query_casa = "SELECT casa, COUNT(*) FROM proposicoes GROUP BY casa;"
    query_estados = "SELECT estado, COUNT(*) FROM proposicoes GROUP BY estado;"
    
    try:
        total = execute_query(query_total, fetch=True)[0][0]
        categorias = execute_query(query_categorias, fetch=True)
        partidos = execute_query(query_partidos, fetch=True)
        casa = execute_query(query_casa, fetch=True)
        estados = execute_query(query_estados, fetch=True)
        
        return {
            "total_proposicoes": total,
            "por_categoria": {cat: count for cat, count in categorias if cat},
            "por_partido": {p: count for p, count in partidos if p},
            "por_casa": {c: count for c, count in casa if c},
            "por_estado": {e: count for e, count in estados if e}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Guard.IA API is running"}