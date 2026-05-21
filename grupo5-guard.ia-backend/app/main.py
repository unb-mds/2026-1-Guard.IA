import sys
from pathlib import Path

# Adiciona o diretório 'app' ao sys.path para permitir imports relativos/absolutos
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from coleta.coletor_camara import coletar as coletar_camara
from coleta.coletor_senado import coletar as coletar_senado
from filtro.filtragem import iniciar_filtragem
from armazenamento.armazenamento import iniciar_armazenamento

def main():
    print("="*60)
    print("🛡️  GUARD.IA - PIPELINE DE MONITORAMENTO LEGISLATIVO")
    print("="*60)

    # 1. ETAPA DE COLETA
    print("\n[1/3] Iniciando Etapa de Coleta...")
    try:
        coletar_camara()
        coletar_senado()
    except Exception as e:
        print(f"❌ Erro na Coleta: {e}")
        # Decidimos continuar para o filtro caso existam dados brutos anteriores
    
    # 2. ETAPA DE FILTRO
    print("\n[2/3] Iniciando Etapa de Filtro...")
    try:
        iniciar_filtragem()
    except Exception as e:
        print(f"❌ Erro no Filtro: {e}")
        return

    # 3. ETAPA DE ARMAZENAMENTO
    print("\n[3/3] Iniciando Etapa de Armazenamento...")
    try:
        iniciar_armazenamento()
    except Exception as e:
        print(f"❌ Erro no Armazenamento: {e}")
        return

    print("\n" + "="*60)
    print("✨ PIPELINE EXECUTADO COM SUCESSO!")
    print("="*60)

if __name__ == "__main__":
    main()
