import sys
import time

try:
    from app.coleta.coletor_camara import coletar as coletar_camara
    from app.coleta.coletor_senado import coletar as coletar_senado
    from app.backfill_autoria_senado import backfill as backfill_autoria_senado
    from app.filtro.filtragem import iniciar_filtragem
    from app.armazenamento.armazenamento import iniciar_armazenamento
    from app.classificacao.classificador import iniciar_classificacao
except ImportError as e:
    print(f" Erro de importacao: {e}")
    print("Certifique-se de que está rodando com: py -m app.main (a partir da raiz do backend)")
    sys.exit(1)

def run_stage(name, func):
    print(f"\n{'='*10} 🚀 ESTÁGIO: {name} {'='*10}")
    start_time = time.time()
    try:
        result = func()
        duration = round(time.time() - start_time, 2)
        print(f" {name} finalizado em {duration}s")
        return result
    except Exception as e:
        print(f" Falha crítica no estagio {name}: {e}")
        return False

def main():
    print("="*60)
    print("  GUARD.IA - ORQUESTRADOR DO PIPELINE (RELEASE 2)")
    print("="*60)

    start_total = time.time()

    # 1. COLETA
    print("\n[1/5] Iniciando Coleta de Dados Brutos...")
    run_stage("Coleta Camara", coletar_camara)
    run_stage("Coleta Senado", coletar_senado)

    # 1.5 BACKFILL AUTOMÁTICO
    # Corrige no banco qualquer proposição do Senado que ficou com "A pesquisar"
    # de execuções anteriores (antes da correção do coletor).
    print("\n[1.5/5] Corrigindo autorias pendentes do Senado...")
    run_stage("Backfill Autoria Senado", backfill_autoria_senado)

    # 2. FILTRO
    success_filtro = run_stage("Filtragem de Relevancia", iniciar_filtragem)
    if not success_filtro:
        print(" Pipeline interrompido: Falha na filtragem.")
        return

    # 3. ARMAZENAMENTO
    success_db = run_stage("Carga no PostgreSQL", iniciar_armazenamento)
    if not success_db:
        print(" Pipeline interrompido: Falha no armazenamento.")
        return

    # 4. CLASSIFICAÇÃO
    success_class = run_stage("Classificacao por IA", iniciar_classificacao)
    if not success_class:
        print(" Pipeline interrompido: Falha na classificação.")
        return

    duration_total = round(time.time() - start_total, 2)
    print("\n" + "="*60)
    print(f" PIPELINE EXECUTADO COM SUCESSO EM {duration_total}s!")
    print("="*60)

if __name__ == "__main__":
    main()