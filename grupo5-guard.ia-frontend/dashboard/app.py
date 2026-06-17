import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do backend para manter consistência
# Ajuste o caminho se necessário dependendo de onde o streamlit é executado
load_dotenv("../../grupo5-guard.ia-backend/.env")

# 1. Configurações da Página
st.set_page_config(
    page_title="Guard.IA - Monitoramento",
    page_icon="🛡️",
    layout="wide"
)

# Funções de Banco de Dados
@st.cache_data(ttl=600)  # Cache por 10 minutos
def get_stats():
    """Busca estatísticas gerais do banco de dados."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "monitoramento_legislativo"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        with conn.cursor() as cur:
            # Total de proposições
            cur.execute("SELECT COUNT(*) FROM proposicoes;")
            total = cur.fetchone()[0]
            
            # Categorias
            cur.execute("SELECT categoria, COUNT(*) FROM proposicoes GROUP BY categoria;")
            categorias = cur.fetchall()
            
            # Última coleta
            cur.execute("SELECT MAX(coletado_em) FROM proposicoes;")
            ultima_coleta = cur.fetchone()[0]
            
        conn.close()
        return {
            "total": total,
            "categorias": {cat if cat else "Não classificado": count for cat, count in categorias},
            "ultima_coleta": ultima_coleta
        }
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return {
            "total": 0,
            "categorias": {},
            "ultima_coleta": "N/A"
        }

# 2. CSS Customizado
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho Principal
st.markdown('<p class="main-title">🛡️ Guard.IA</p>', unsafe_allow_html=True)
st.subheader("Inteligência de Dados na Proteção da Infância e Adolescência")

st.divider()

# Busca dados reais
stats = get_stats()

# 4. Painel de Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Projetos Coletados", value=stats["total"])
with col2:
    # Exemplo: Cyberbullying
    cb_count = stats["categorias"].get("cyberbullying", 0)
    st.metric(label="Cyberbullying", value=cb_count)
with col3:
    # Exemplo: Privacidade
    priv_count = stats["categorias"].get("privacidade_dados", 0)
    st.metric(label="Privacidade de Dados", value=priv_count)
with col4:
    st.metric(label="Última Coleta", value=str(stats["ultima_coleta"]).split('.')[0] if stats["ultima_coleta"] else "N/A")

st.divider()

# 5. Visualização Adicional (Gráfico de Categorias)
if stats["categorias"]:
    st.markdown("### 📊 Distribuição por Temas")
    df_cat = pd.DataFrame(list(stats["categorias"].items()), columns=["Categoria", "Quantidade"])
    st.bar_chart(df_cat.set_index("Categoria"))

st.divider()

# 6. Seção de Boas-vindas e Instruções
st.markdown("### 🚀 Próximos Passos para o Desenvolvimento")
st.write("""
Este dashboard agora está **conectado ao PostgreSQL** em tempo real!
- **Dados Reais:** As métricas acima refletem o que está na tabela `proposicoes`.
- **Navegação:** Utilize a barra lateral para acessar outras páginas (quando criadas em `/pages`).
- **Segurança:** Lembre-se que o acesso completo exige login (Release 1 em integração).
""")

st.info("Utilize a barra lateral à esquerda para navegar entre os módulos do sistema.")