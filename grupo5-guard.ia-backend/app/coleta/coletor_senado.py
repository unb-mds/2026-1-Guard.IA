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

def load_existing_ids():
    """Carrega apenas os IDs existentes para economizar memória."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return set()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return {p["id_externo"] for p in dados}
    except Exception as e:
        print(f"Erro ao carregar IDs existentes: {e}")
    return set()

def save_data(novas_proposicoes):
    """Lê o arquivo, adiciona os novos dados e salva tudo."""
    dados_completos = []
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                dados_completos = json.load(f)
        except Exception:
            dados_completos = []
    
    dados_completos.extend(novas_proposicoes)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=4)

def format_materia(materia):
    """Padroniza o objeto da matéria conforme o contrato de dados Guard.IA."""
    return {
        "id_externo": f"SENADO-{materia.get('Codigo')}",
        "ementa": (materia.get("Ementa") or "").strip(),
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
    
    ids_existentes = load_existing_ids()
    
    print(f"Iniciando coleta Senado a partir de {data_cursor}...")
    print(f"Total de registros já conhecidos: {len(ids_existentes)}")
    
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

            proposicoes_do_lote = []
            ultima_data_lote = data_cursor

            for mat in materias:
                id_mat = mat.get("Codigo")
                if not id_mat:
                    continue
                    
                id_ext = f"SENADO-{id_mat}"
                if id_ext in ids_existentes:
                    continue
                
                proposicao_formatada = format_materia(mat)
                proposicoes_do_lote.append(proposicao_formatada)
                ids_existentes.add(id_ext)
                
                # Atualiza a data para o cursor (formato YYYYMMDD)
                data_ap = mat.get("Data", "")
                if data_ap:
                    ultima_data_lote = data_ap.replace("-", "")

            if not proposicoes_do_lote:
                print("Nenhum registro novo neste lote. Verificando avanço de data...")
                # Se não há novos e a data ainda é a mesma do cursor, precisamos avançar
                try:
                    dt = datetime.strptime(data_cursor, "%Y%m%d")
                    from datetime import timedelta
                    data_cursor = (dt + timedelta(days=1)).strftime("%Y%m%d")
                    continue
                except:
                    break

            # Batch Saving: Salva ao final de cada lote processado
            save_data(proposicoes_do_lote)
            save_checkpoint(ultima_data_lote)
            print(f"Lote processado: {len(proposicoes_do_lote)} novas matérias. Próximo cursor: {ultima_data_lote}")
            
            # Prevenção de loop infinito na mesma data
            if ultima_data_lote == data_cursor:
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
        print(f"Coleta Senado encerrada.")

if __name__ == "__main__":
    coletar()
