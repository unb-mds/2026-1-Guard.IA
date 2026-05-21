import requests
import json
import time
import os
from pathlib import Path
from datetime import datetime

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
            print(f"Erro ao carregar checkpoint: {e}")
    return {"last_date": START_DATE, "last_page": 1}

def save_checkpoint(date, page):
    checkpoint = {"last_date": date, "last_page": page}
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=4)

def load_data():
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados existentes: {e}")
    return []

def save_data(proposicoes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proposicoes, f, ensure_ascii=False, indent=4)

def format_proposicao(prop, detalhes):
    return {
        "id_externo": f"CAMARA-{prop['id']}",
        "ementa": prop.get("ementa", "").strip(),
        "autor": detalhes["autor"],
        "partido": detalhes["partido"],
        "estado": detalhes["estado"],
        "casa": "Câmara",
        "data_apresentacao": prop.get("dataApresentacao", "")
    }

def coletar():
    checkpoint = load_checkpoint()
    data_inicio = checkpoint["last_date"]
    if data_inicio and "T" in data_inicio:
        data_inicio = data_inicio.split("T")[0]

    pagina_atual = checkpoint["last_page"]
    proposicoes_existentes = load_data()
    ids_existentes = {p["id_externo"] for p in proposicoes_existentes}

    print(f"Iniciando coleta a partir de {data_inicio}, página {pagina_atual}...")

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
                print("Fim da coleta. Nenhum dado novo encontrado.")
                break

            ultima_data_processada = data_inicio
            for prop in dados:
                id_ext = f"CAMARA-{prop['id']}"
                if id_ext in ids_existentes:
                    continue

                print(f"Processando: {id_ext}")

                detalhes_placeholder = {
                    "autor": "A pesquisar",
                    "partido": "A pesquisar",
                    "estado": "A pesquisar"
                }

                proposicao_formatada = format_proposicao(prop, detalhes_placeholder)
                proposicoes_existentes.append(proposicao_formatada)
                ids_existentes.add(id_ext)

                data_prop = prop.get("dataApresentacao", ultima_data_processada)
                if data_prop and "T" in data_prop:
                    data_prop = data_prop.split("T")[0]
                ultima_data_processada = data_prop

            save_data(proposicoes_existentes)
            save_checkpoint(ultima_data_processada, pagina_atual)

            print(f"Página {pagina_atual} finalizada e salva.")
            pagina_atual += 1

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Checkpoint salvo.")
    except Exception as e:
        print(f"\nErro crítico durante a coleta: {e}")
    finally:
        save_data(proposicoes_existentes)
        print(f"Coleta encerrada. Total de registros: {len(proposicoes_existentes)}")

if __name__ == "__main__":
    coletar()