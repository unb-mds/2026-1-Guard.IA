import json
import re
import unicodedata
from pathlib import Path

# Configuração de caminhos dinâmicos
# Estamos em grupo5-guard.ia-backend/app/filtro/
# BASE_DIR deve ser grupo5-guard.ia-backend/
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
    if not texto:
        return ""
    # 1. Minúsculas
    texto = texto.lower()
    # 2. Decompor caracteres acentuados (NFD)
    texto = unicodedata.normalize("NFD", texto)
    # 3. Filtrar apenas caracteres que não sejam marcas de acentuação (Mn)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

# Pré-processamento Sênior: 
# 1. Normalizamos as palavras-chave uma única vez no carregamento do módulo.
PALAVRAS_CHAVE_NORM = [normalizar(p) for p in PALAVRAS_CHAVE]

# 2. Criamos um Regex compilado com bordas de palavra (\b) para evitar falsos positivos.
# Ex: "menor" não deve casar com "pormenorizado".
REGEX_FILTRO = re.compile(r"\b(" + "|".join(re.escape(p) for p in PALAVRAS_CHAVE_NORM) + r")\b")

def contem_palavra_chave(ementa: str) -> bool:
    """
    Verifica se a ementa contém alguma palavra-chave usando Regex otimizado.
    """
    if not ementa:
        return False
    ementa_norm = normalizar(ementa)
    return bool(REGEX_FILTRO.search(ementa_norm))

def filtrar_proposicoes(proposicoes: list[dict]) -> list[dict]:
    """
    Filtra a lista de dicionários baseada na ementa.
    """
    if not proposicoes:
        return []
    
    return [p for p in proposicoes if contem_palavra_chave(p.get("ementa", ""))]

def iniciar_filtragem():
    """
    Orquestra a leitura, filtragem e persistência.
    Garante que a etapa de Filtro seja independente (Pipes and Filters).
    """
    print(f"🔍 Iniciando etapa de Filtro...")
    print(f"📂 Lendo dados brutos de: {DADOS_BRUTOS_FILE}")

    if not DADOS_BRUTOS_FILE.exists():
        print(f"❌ Erro: Arquivo de dados brutos não encontrado em {DADOS_BRUTOS_FILE}")
        return

    try:
        with open(DADOS_BRUTOS_FILE, "r", encoding="utf-8") as f:
            proposicoes = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar dados brutos: {e}")
        return

    total_inicial = len(proposicoes)
    print(f"📊 Total de registros para processar: {total_inicial}")

    # Processamento
    filtrados = filtrar_proposicoes(proposicoes)
    total_final = len(filtrados)

    # Persistência
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DADOS_FILTRADOS_FILE, "w", encoding="utf-8") as f:
            json.dump(filtrados, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Filtro concluído com sucesso!")
        print(f"🎯 Relevantes: {total_final} de {total_inicial} ({round(total_final/total_inicial*100, 2)}%)")
        print(f"💾 Salvo em: {DADOS_FILTRADOS_FILE}")
    except Exception as e:
        print(f"❌ Erro ao salvar dados filtrados: {e}")

if __name__ == "__main__":
    iniciar_filtragem()
