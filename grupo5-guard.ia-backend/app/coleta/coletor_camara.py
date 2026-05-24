import requests
import json
import time
from pathlib import Path

# Configurações e Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "dados_brutos.json"
CHECKPOINT_FILE = DATA_DIR / "checkpoint_camara.json"

API_URL = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
START_DATE = "2023-01-01"
HEADERS = {"Accept": "application/json"}
RATE_LIMIT_DELAY = 0.5

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar checkpoint: {e}")
    return {"last_date": START_DATE, "last_page": 1}

def save_checkpoint(date, page):
    checkpoint = {"last_date": date, "last_page": page}
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=4)
    except Exception as e:
        print(f"❌ Erro ao salvar checkpoint: {e}")

def load_existing_ids():
    """Carrega apenas os IDs existentes para economizar memória."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return set()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return {p["id_externo"] for p in dados}
    except Exception as e:
        print(f"❌ Erro ao carregar IDs existentes: {e}")
    return set()

def save_data(novas_proposicoes):
    """Lê o arquivo, adiciona os novos dados e salva tudo (Merge)."""
    dados_completos = []
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                dados_completos = json.load(f)
        except Exception:
            dados_completos = []
    
    dados_completos.extend(novas_proposicoes)
    
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dados_completos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Erro ao salvar dados brutos: {e}")

def format_proposicao(prop, detalhes):
    return {
        "id_externo": f"CAMARA-{prop.get('id')}",
        "ementa": (prop.get("ementa") or "").strip(),
        "autor": detalhes.get("autor", "A pesquisar"),
        "partido": detalhes.get("partido", "A pesquisar"),
        "estado": detalhes.get("estado", "A pesquisar"),
        "casa": "Câmara",
        "data_apresentacao": prop.get("dataApresentacao", "")
    }

def coletar():
    checkpoint = load_checkpoint()
    data_inicio = checkpoint["last_date"]
    if data_inicio and "T" in data_inicio:
        data_inicio = data_inicio.split("T")[0]

    pagina_atual = checkpoint["last_page"]
    
    # Sênior: Carregamos apenas os IDs para o set de deduplicação (economiza RAM)
    ids_existentes = load_existing_ids()
    
    print(f"🚀 Iniciando coleta Câmara a partir de {data_inicio}, página {pagina_atual}...")
    print(f"📊 Registros já conhecidos: {len(ids_existentes)}")

    try:
        while True:
            params = {
                "dataInicio": data_inicio,
                "ordem": "ASC",
                "ordenarPor": "id",
                "pagina": pagina_atual,
                "itens": 100
            }

            response = requests.get(API_URL, headers=HEADERS, params=params, timeout=30)
            response.raise_for_status()
            dados = response.json().get("dados", [])

            if not dados:
                print("🏁 Fim da coleta. Nenhum dado novo encontrado.")
                break

            proposicoes_do_lote = []
            ultima_data_processada = data_inicio

            for prop in dados:
                id_prop = prop.get("id")
                if not id_prop:
                    continue
                    
                id_ext = f"CAMARA-{id_prop}"
                if id_ext in ids_existentes:
                    continue

                detalhes_placeholder = {
                    "autor": "A pesquisar",
                    "partido": "A pesquisar",
                    "estado": "A pesquisar"
                }

                proposicao_formatada = format_proposicao(prop, detalhes_placeholder)
                proposicoes_do_lote.append(proposicao_formatada)
                ids_existentes.add(id_ext)

                data_prop = prop.get("dataApresentacao", ultima_data_processada)
                if data_prop and "T" in data_prop:
                    data_prop = data_prop.split("T")[0]
                ultima_data_processada = data_prop

            # Batch Saving: Salvamos apenas os novos registros da página
            if proposicoes_do_lote:
                save_data(proposicoes_do_lote)
                print(f"✅ Página {pagina_atual} finalizada: {len(proposicoes_do_lote)} novos registros.")
            else:
                print(f"ℹ️ Página {pagina_atual} processada: nenhum registro novo.")

            save_checkpoint(ultima_data_processada, pagina_atual)
            pagina_atual += 1
            time.sleep(RATE_LIMIT_DELAY)

    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário. Checkpoint salvo.")
    except Exception as e:
        print(f"\n❌ Erro crítico durante a coleta: {e}")
    finally:
        print(f"✨ Coleta encerrada.")
    
    return True

if __name__ == "__main__":
    coletar()
