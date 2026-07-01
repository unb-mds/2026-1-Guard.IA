import sys
import time

try:
    from app.armazenamento.database import execute_query
    from app.coleta.coletor_senado import buscar_autoria_senado
except ImportError as e:
    print(f" Erro de importacao: {e}")
    print("Certifique-se de que está rodando com: py -m app.backfill_autoria_senado")
    sys.exit(1)

RATE_LIMIT_DELAY = 0.5

def backfill():
    rows = execute_query(
        "SELECT id_externo FROM proposicoes WHERE casa = 'Senado' AND autor = 'A pesquisar'",
        fetch=True
    )
    if not rows:
        print("Nenhum registro do Senado para corrigir.")
        return

    print(f"Encontrados {len(rows)} registros para reprocessar.")

    atualizados = 0
    for (id_externo,) in rows:
        codigo = id_externo.replace("SENADO-", "")
        detalhes = buscar_autoria_senado(codigo)

        if detalhes["autor"] == "A pesquisar":
            print(f"⏭️  {id_externo} sem autoria disponível na API.")
            time.sleep(RATE_LIMIT_DELAY)
            continue

        execute_query(
            """
            UPDATE proposicoes
            SET autor = %s, partido = %s, estado = %s
            WHERE id_externo = %s
            """,
            (detalhes["autor"], detalhes["partido"], detalhes["estado"], id_externo)
        )
        atualizados += 1
        print(f"✅ {id_externo} -> {detalhes['autor']} ({detalhes['partido']}/{detalhes['estado']})")
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\nConcluído: {atualizados}/{len(rows)} registros atualizados.")

if __name__ == "__main__":
    backfill()