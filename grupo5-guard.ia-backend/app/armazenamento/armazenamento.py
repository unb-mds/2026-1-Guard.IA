import json
from pathlib import Path
from .database import execute_batch

# Configuração de caminhos dinâmicos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DADOS_FILTRADOS_FILE = DATA_DIR / "dados_filtrados.json"

def carregar_dados_filtrados():
    """Lê o arquivo JSON de dados filtrados."""
    if not DADOS_FILTRADOS_FILE.exists():
        print(f"❌ Erro: Arquivo {DADOS_FILTRADOS_FILE} não encontrado.")
        return []
    
    try:
        with open(DADOS_FILTRADOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return []

def salvar_proposicoes(proposicoes: list):
    """
    Salva uma lista de proposições no banco de dados em lote.
    Utiliza ON CONFLICT DO NOTHING para deduplicação no lado do banco.
    """
    if not proposicoes:
        print("ℹ️ Nenhuma proposição para salvar.")
        return 0

    query = """
        INSERT INTO proposicoes (
            id_externo, ementa, autor, partido, estado, 
            casa, data_apresentacao, categoria, confianca
        ) VALUES %s
        ON CONFLICT (id_externo) DO NOTHING;
    """
    
    # Prepara os parâmetros para o execute_values
    params_list = [
        (
            p.get('id_externo'),
            p.get('ementa'),
            p.get('autor', 'A pesquisar'),
            p.get('partido', 'A pesquisar'),
            p.get('estado', 'A pesquisar'),
            p.get('casa'),
            p.get('data_apresentacao'),
            p.get('categoria'),
            p.get('confianca')
        )
        for p in proposicoes
    ]
    
    try:
        execute_batch(query, params_list)
        print(f"✅ Armazenamento concluído: {len(proposicoes)} registros processados via batch insert.")
        return len(proposicoes)
    except Exception as e:
        print(f"❌ Erro crítico no armazenamento em lote: {e}")
        return 0

def iniciar_armazenamento():
    """Função principal para rodar a etapa de armazenamento."""
    print(f"📥 Iniciando etapa de Armazenamento...")
    print(f"📂 Lendo dados filtrados de: {DADOS_FILTRADOS_FILE}")
    
    dados = carregar_dados_filtrados()
    
    if dados:
        salvar_proposicoes(dados)
    else:
        print("ℹ️ Nenhum dado para processar.")

if __name__ == "__main__":
    iniciar_armazenamento()
