import requests
import json
import os
from pathlib import Path
from datetime import datetime

# Configurações e Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "dados_brutos.json"
CHECKPOINT_FILE = DATA_DIR / "checkpoint_senado.json"

# Endpoint do Senado para pesquisa de matérias
API_URL = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"
START_DATE = "20230101" # Formato YYYYMMDD exigido pela API
HEADERS = {"Accept": "application/json"}
TIMEOUT = 30

def load_checkpoint():
    """Carrega o progresso da última execução."""
    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar checkpoint: {e}")
    return {"last_date": START_DATE}

def save_checkpoint(date):
    """Salva o progresso atual."""
    checkpoint = {"last_date": date}
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, indent=4)

def load_data():
    """Carrega dados existentes para evitar duplicatas."""
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados existentes: {e}")
    return []

def save_data(proposicoes):
    """Salva a lista completa de proposições em formato JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proposicoes, f, ensure_ascii=False, indent=4)

def format_materia(materia):
    """Padroniza o objeto da matéria conforme o contrato de dados Guard.IA."""
    return {
        "id_externo": f"SENADO-{materia.get('Codigo')}",
        "ementa": materia.get("Ementa", "").strip(),
        "autor": "A pesquisar",
        "partido": "A pesquisar",
        "estado": "A pesquisar",
        "casa": "Senado",
        "data_apresentacao": materia.get("Data", "")
    }

def coletar():
    """Executa o pipeline de coleta do Senado com loop de paginação por data."""
    checkpoint = load_checkpoint()
    data_cursor = checkpoint["last_date"]
    
    proposicoes_existentes = load_data()
    ids_existentes = {p["id_externo"] for p in proposicoes_existentes}
    
    print(f"Iniciando coleta Senado a partir de {data_cursor}...")
    
    try:
        while True:
            params = {
                "dataInicioApresentacao": data_cursor
            }
            
            response = requests.get(API_URL, headers=HEADERS, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            pesquisa = data.get("PesquisaBasicaMateria", {})
            materias_wrapper = pesquisa.get("Materias", {})
            
            if not materias_wrapper:
                print("Fim da coleta. Nenhuma matéria nova encontrada no Senado.")
                break

            materias = materias_wrapper.get("Materia", [])
            if isinstance(materias, dict):
                materias = [materias]

            novos_no_lote = 0
            ultima_data_lote = data_cursor

            for mat in materias:
                id_mat = mat.get("Codigo")
                if not id_mat:
                    continue
                    
                id_ext = f"SENADO-{id_mat}"
                if id_ext in ids_existentes:
                    continue
                
                proposicao_formatada = format_materia(mat)
                proposicoes_existentes.append(proposicao_formatada)
                ids_existentes.add(id_ext)
                
                # Atualiza a data para o cursor (formato YYYYMMDD)
                data_ap = mat.get("Data", "")
                if data_ap:
                    ultima_data_lote = data_ap.replace("-", "")
                
                novos_no_lote += 1

            if novos_no_lote == 0:
                print("Nenhum registro novo neste lote. Encerrando loop.")
                break

            # Batch Saving: Salva ao final de cada lote processado
            save_data(proposicoes_existentes)
            save_checkpoint(ultima_data_lote)
            print(f"Lote processado: {novos_no_lote} novas matérias. Próximo cursor: {ultima_data_lote}")
            
            # Se o lote veio completo e não houver mais o que puxar, o próximo loop quebrará no 'novos_no_lote == 0'
            # Mas para evitar loop infinito na mesma data se a API sempre retornar o mesmo lote:
            if ultima_data_lote == data_cursor:
                # Se a data não avançou, tentamos forçar o avanço de um dia para o próximo cursor
                try:
                    dt = datetime.strptime(data_cursor, "%Y%m%d")
                    from datetime import timedelta
                    data_cursor = (dt + timedelta(days=1)).strftime("%Y%m%d")
                except:
                    break
            else:
                data_cursor = ultima_data_lote

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição à API do Senado: {e}")
    except Exception as e:
        print(f"Erro crítico durante a coleta do Senado: {e}")
    finally:
        print(f"Coleta Senado encerrada. Total de registros: {len(proposicoes_existentes)}")

if __name__ == "__main__":
    coletar()
