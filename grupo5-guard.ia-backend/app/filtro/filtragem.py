import json
import re
import unicodedata
import time
from pathlib import Path

# Configuração de caminhos dinâmicos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DADOS_BRUTOS_FILE = DATA_DIR / "dados_brutos.json"
DADOS_FILTRADOS_FILE = DATA_DIR / "dados_filtrados.json"

# Lista de palavras-chave centralizada (Conforme GEMINI.md)
PALAVRAS_CHAVE = [
    "crianca", "adolescente", "menor", "internet", "digital",
    "online", "cyberbullying", "redes sociais", "lgpd",
    "marco civil", "privacidade", "aplicativo", "eca",
    "conteudo inapropriado", "tempo de tela"
]

def normalizar(texto: str) -> str:
    """
    Normalização padrão Guard.IA: minúsculas + remoção de acentos.
    """
    if not texto or not isinstance(texto, str):
        return ""
    # 1. Minúsculas e Decomposição NFD
    texto = unicodedata.normalize("NFD", texto.lower())
    # 2. Filtrar apenas caracteres que não sejam marcas de acentuação
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

# Pré-processamento Sênior das Palavras-Chave
PALAVRAS_CHAVE_NORM = sorted([normalizar(p) for p in PALAVRAS_CHAVE], key=len, reverse=True)
# Regex com bordas de palavra para evitar casamentos parciais (ex: "menor" vs "pormenorizado")
REGEX_FILTRO = re.compile(r"\b(" + "|".join(re.escape(p) for p in PALAVRAS_CHAVE_NORM) + r")\b")

def analisar_relevancia(ementa: str):
    """
    Analisa a ementa e retorna (bool: relevante, list: termos_encontrados).
    """
    if not ementa:
        return False, []
    
    ementa_norm = normalizar(ementa)
    matches = REGEX_FILTRO.findall(ementa_norm)
    
    return len(matches) > 0, list(set(matches))

def filtrar_proposicoes(proposicoes: list[dict]) -> list[dict]:
    """
    Filtra a lista de dicionários e enriquece com metadados de filtragem.
    """
    filtrados = []
    for p in proposicoes:
        ementa = p.get("ementa", "")
        relevante, termos = analisar_relevancia(ementa)
        
        if relevante:
            # Mantemos a imutabilidade do dado original, mas adicionamos metadados de auditoria
            p_filtrada = p.copy()
            p_filtrada["termos_chave"] = termos
            filtrados.append(p_filtrada)
            
    return filtrados

def iniciar_filtragem():
    """
    Orquestra a etapa de Filtro seguindo a arquitetura Pipes and Filters.
    """
    start_time = time.time()
    print(f"--- 🔍 Módulo de Filtro: Iniciando Processamento ---")
    
    if not DADOS_BRUTOS_FILE.exists():
        print(f"⚠️ Erro: Fonte de dados brutos não encontrada: {DADOS_BRUTOS_FILE}")
        return False

    try:
        with open(DADOS_BRUTOS_FILE, "r", encoding="utf-8") as f:
            proposicoes = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Erro: Arquivo {DADOS_BRUTOS_FILE} corrompido.")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao carregar dados: {e}")
        return False

    total_brutos = len(proposicoes)
    print(f"📊 Processando {total_brutos} registros...")

    # Aplicação do Filtro
    dados_filtrados = filtrar_proposicoes(proposicoes)
    total_filtrados = len(dados_filtrados)

    # Persistência
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DADOS_FILTRADOS_FILE, "w", encoding="utf-8") as f:
            json.dump(dados_filtrados, f, ensure_ascii=False, indent=4)
        
        duration = round(time.time() - start_time, 2)
        print(f"✅ Filtro Finalizado em {duration}s")
        print(f"🎯 Relevantes: {total_filtrados} | Descartados: {total_brutos - total_filtrados}")
        print(f"💾 Resultado em: {DADOS_FILTRADOS_FILE}")
        return True
    except Exception as e:
        print(f"❌ Erro ao persistir dados filtrados: {e}")
        return False

if __name__ == "__main__":
    iniciar_filtragem()
