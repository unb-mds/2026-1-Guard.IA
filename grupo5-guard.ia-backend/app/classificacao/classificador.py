try:
    from sentence_transformers import SentenceTransformer, util
    HAS_TRANSFORMERS = True
except Exception as e:
    print(f"⚠️ AVISO: sentence_transformers indisponível, usando fallback de palavras-chave: {e}")
    HAS_TRANSFORMERS = False

try:
    from app.armazenamento.database import get_connection, release_connection
except ImportError:
    from ..armazenamento.database import get_connection, release_connection

# GEMINI.md Regra 19: classificações são estimativas, nunca fatos absolutos.
# GEMINI.md Regra 20: confianca deve sempre acompanhar categoria na visualização.

MODELO_ID = "paraphrase-multilingual-MiniLM-L12-v2"
LIMIAR_INCERTEZA = 0.7  # abaixo desse valor a classificação é sinalizada como incerta

# Categorias definidas em docs/estudos/requisitos_e_ia.md
# Cada descrição é convertida em embedding para comparação semântica com as ementas.
CATEGORIAS = {
    "cyberbullying": (
        "assédio, bullying, violência psicológica online, "
        "perseguição virtual, ameaça por mensagem"
    ),
    "privacidade_dados": (
        "coleta de dados pessoais, LGPD, proteção de informações "
        "de menores, consentimento digital, vazamento de dados"
    ),
    "tempo_de_tela": (
        "uso excessivo de dispositivos, dependência digital, "
        "limite de acesso, restrição de horário para menores"
    ),
    "conteudo_inapropriado": (
        "pornografia infantil, violência, conteúdo adulto, "
        "plataformas de streaming, moderação de conteúdo"
    ),
    "educacao_digital": (
        "letramento digital, ensino de tecnologia, "
        "alfabetização midiática, segurança online nas escolas"
    ),
}


def _buscar_sem_categoria() -> list[tuple]:
    """Retorna (id, ementa) das proposições ainda sem categoria no banco."""
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, ementa FROM proposicoes "
                "WHERE categoria IS NULL AND ementa IS NOT NULL "
                "ORDER BY id"
            )
            return cur.fetchall()
    except Exception as e:
        print(f"  ERRO ao buscar proposições sem categoria: {e}")
        return []
    finally:
        release_connection(conn)


def _salvar_resultados(resultados: list[tuple]) -> None:
    """Batch UPDATE: persiste (categoria, confianca) para cada proposição."""
    if not resultados:
        return
    conn = get_connection()
    if not conn:
        return
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "UPDATE proposicoes SET categoria = %s, confianca = %s WHERE id = %s",
                [(categoria, confianca, id_prop) for id_prop, categoria, confianca in resultados],
            )
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"  ERRO ao salvar classificações (rollback executado): {e}")
        raise
    finally:
        release_connection(conn)


def iniciar_classificacao() -> bool:
    """
    Etapa 4 do pipeline: classifica proposições sem categoria.

    Fluxo:
      PostgreSQL (categoria IS NULL) → embeddings → similaridade cosseno → UPDATE

    Retorna True em caso de sucesso (mesmo que não haja proposições pendentes).
    """
    print("  Iniciando etapa de Classificação por IA...")
    print(f"  Modelo: {MODELO_ID}")

    proposicoes = _buscar_sem_categoria()
    if not proposicoes:
        print("  Nenhuma proposição pendente de classificação.")
        return True

    total = len(proposicoes)
    print(f"  {total} proposições para classificar...")

    nomes_categorias = list(CATEGORIAS.keys())
    descricoes_categorias = list(CATEGORIAS.values())
    resultados = []
    incertas = 0

    if HAS_TRANSFORMERS:
        modelo = SentenceTransformer(MODELO_ID)

        # Embeddings fixos das 5 categorias (operação única, independente do volume)
        emb_categorias = modelo.encode(
            descricoes_categorias,
            convert_to_tensor=True,
            show_progress_bar=False,
        )

        # Batch encode de todas as ementas de uma só vez
        ementas = [row[1] for row in proposicoes]
        emb_ementas = modelo.encode(
            ementas,
            convert_to_tensor=True,
            show_progress_bar=True,
            batch_size=64,
        )

        # Matriz de similaridade cosseno: shape (N_proposicoes, N_categorias)
        similaridades = util.cos_sim(emb_ementas, emb_categorias)

        for i, (id_prop, _) in enumerate(proposicoes):
            sims = similaridades[i]
            idx_melhor = int(sims.argmax())
            # Clamp [0, 1] para satisfazer CHECK do schema.sql
            confianca = round(max(0.0, min(1.0, float(sims[idx_melhor]))), 4)
            categoria = nomes_categorias[idx_melhor]

            if confianca < LIMIAR_INCERTEZA:
                incertas += 1

            resultados.append((id_prop, categoria, confianca))
    else:
        # Fallback simples baseado em presença de palavras-chave nas ementas.
        print('⚠️ Executando classificação fallback sem embeddings.')
        for id_prop, ementa in proposicoes:
            ementa_norm = ementa.lower() if ementa else ''
            melhor_categoria = 'educacao_digital'
            melhor_score = 0.0

            for idx, descricao in enumerate(descricoes_categorias):
                score = sum(1 for termo in descricao.split() if termo in ementa_norm)
                if score > melhor_score:
                    melhor_score = score
                    melhor_categoria = nomes_categorias[idx]

            confianca = round(min(1.0, 0.4 + 0.1 * melhor_score), 4)
            if confianca < LIMIAR_INCERTEZA:
                incertas += 1
            resultados.append((id_prop, melhor_categoria, confianca))

    _salvar_resultados(resultados)

    print(f"  Classificação concluída: {total} proposições processadas.")
    print(f"  Estimativas incertas (confianca < {LIMIAR_INCERTEZA}): {incertas} ({round(incertas/total*100, 1)}%)")
    print("  [Regra 19/20] Sempre exibir confianca junto à categoria — são estimativas, não fatos.")
    return True
