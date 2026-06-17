import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv


# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do banco via variáveis de ambiente
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "monitoramento_legislativo")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

print("HOST:", repr(DB_HOST))
print("PORT:", repr(DB_PORT))
print("NAME:", repr(DB_NAME))
print("USER:", repr(DB_USER))
print("PASSWORD:", repr(DB_PASSWORD))

# Pool de conexões para eficiência
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 10,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    if connection_pool:
        print(" Pool de conexoes PostgreSQL criado com sucesso")
except Exception as e:
    print("ERRO AO CONECTAR:", repr(e))
    connection_pool = None

def get_connection():
    """Retorna uma conexao do pool."""
    if connection_pool:
        return connection_pool.getconn()
    return None

def release_connection(conn):
    """Devolve a conexao para o pool."""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def execute_query(query, params=None, fetch=False):
    """
    Executa uma query SQL de forma segura com suporte a transacoes
    """
    conn = get_connection()
    if not conn:
        return None
    
    # Desativa autocommit para controle manual de transação
    conn.autocommit = False
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = None
            if fetch:
                result = cursor.fetchall()
            conn.commit()
            return result
    except Exception as e:
        conn.rollback()
        print(f" ERRO SQL (Rollback executado): {e}\nQuery: {query}")
        raise e
    finally:
        release_connection(conn)

def execute_batch(query, params_list):
    """
    Executa uma insercao em lote para alta performance.
    """
    conn = get_connection()
    if not conn:
        return
    
    conn.autocommit = False
    try:
        from psycopg2.extras import execute_values
        with conn.cursor() as cursor:
            execute_values(cursor, query, params_list)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" ERRO SQL Batch (Rollback executado): {e}")
        raise e
    finally:
        release_connection(conn)
