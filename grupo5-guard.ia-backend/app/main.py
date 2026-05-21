import sys
import time
from pathlib import Path

# Adiciona o diretório 'app' ao sys.path para permitir imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from coleta.coletor_camara import coletar as coletar_camara
    from coleta.coletor_senado import coletar as coletar_senado
    from filtro.filtragem import iniciar_filtragem
    from armazenamento.armazenamento import iniciar_armazenamento
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de que está rodando o script a partir da raiz do backend.")
    sys.exit(1)

def run_stage(name, func):
    print(f"\n{'='*10} 🚀 ESTÁGIO: {name} {'='*10}")
    start_time = time.time()
    try:
        result = func()
        duration = round(time.time() - start_time, 2)
        print(f"✅ {name} finalizado em {duration}s")
        return result
    except Exception as e:
        print(f"❌ Falha crítica no estágio {name}: {e}")
        return False

def main():
    print("="*60)
    print("🛡️  GUARD.IA - ORQUESTRADOR DO PIPELINE (RELEASE 1)")
    print("="*60)
    
    start_total = time.time()

    # 1. COLETA
    print("\n[1/3] Iniciando Coleta de Dados Brutos...")
    # Coletamos ambos; falha em um não necessariamente impede o outro
    run_stage("Coleta Câmara", coletar_camara)
    run_stage("Coleta Senado", coletar_senado)
    
    # 2. FILTRO
    # O Filtro depende de existir o arquivo dados_brutos.json
    success_filtro = run_stage("Filtragem de Relevância", iniciar_filtragem)
    if not success_filtro:
        print("🛑 Pipeline interrompido: Falha na filtragem.")
        return

    # 3. ARMAZENAMENTO
    # O Armazenamento depende de existir o arquivo dados_filtrados.json
    success_db = run_stage("Carga no PostgreSQL", iniciar_armazenamento)
    if not success_db:
        print("🛑 Pipeline interrompido: Falha no armazenamento.")
        return

    duration_total = round(time.time() - start_total, 2)
    print("\n" + "="*60)
    print(f"✨ PIPELINE EXECUTADO COM SUCESSO EM {duration_total}s!")
    print("="*60)

if __name__ == "__main__":
    main()
