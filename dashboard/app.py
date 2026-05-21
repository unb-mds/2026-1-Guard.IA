import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Guard.IA", layout="wide")

# =============================
# ESTILO VISUAL GUARD.IA
# =============================
st.markdown("""
<style>
    .stApp {
        background-color: #F5F5F5;
    }

    [data-testid="stSidebar"] {
        background-color: #0B6B4D;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .topbar {
        background-color: #006B4F;
        padding: 18px 32px;
        color: white;
        font-weight: 800;
        font-size: 30px;
        letter-spacing: 1px;
        margin-bottom: 45px;
    }

    .nav {
        float: right;
        font-size: 15px;
        font-weight: 600;
        margin-top: 8px;
    }

    .nav span {
        margin-left: 28px;
    }

    .hero {
        padding: 10px 35px 20px 35px;
    }

    .hero-title {
        font-size: 64px;
        font-weight: 900;
        line-height: 1.05;
        color: #000000;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 22px;
        color: #222222;
        max-width: 950px;
        margin-bottom: 35px;
        font-weight: 500;
    }

    .card {
        background-color: white;
        border-radius: 14px;
        padding: 24px;
        border: 1px solid #E0E0E0;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
        text-align: center;
    }

    .card-title {
        font-size: 15px;
        color: #555;
        font-weight: 600;
    }

    .card-value {
        font-size: 34px;
        color: #006B4F;
        font-weight: 900;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #111;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .block {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E6E6E6;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# CARREGAMENTO
# =============================
@st.cache_data
def carregar_dados_csv():
    return pd.read_csv("dashboard/data_fake.csv")


def carregar_dados_banco():
    """
    Função preparada para futura integração com PostgreSQL.
    """
    pass


df = carregar_dados_csv()
df["data_apresentacao"] = pd.to_datetime(df["data_apresentacao"])

# =============================
# TOPO IGUAL AO PROTÓTIPO
# =============================
st.markdown("""
<div class="topbar">
    GUARD.IA
    <div class="nav">
        <span>Sobre o Sistema</span>
        <span>Dashboard</span>
        <span>Proposições</span>
        <span>Ranking</span>
        <span>Mapa</span>
        <span>🔍</span>
        <span>👤</span>
    </div>
</div>

<div class="hero">
    <div class="hero-title">
        MONITORAMENTO<br>
        LEGISLATIVO
    </div>
    <div class="hero-subtitle">
        Acompanhe proposições relacionadas à proteção de crianças e adolescentes no ambiente digital.
    </div>
</div>
""", unsafe_allow_html=True)

# =============================
# FILTROS
# =============================
st.sidebar.title("Filtros")

categorias = st.sidebar.multiselect(
    "Categoria",
    sorted(df["categoria"].unique()),
    default=sorted(df["categoria"].unique())
)

partidos = st.sidebar.multiselect(
    "Partido",
    sorted(df["partido"].unique()),
    default=sorted(df["partido"].unique())
)

estados = st.sidebar.multiselect(
    "Estado",
    sorted(df["estado"].unique()),
    default=sorted(df["estado"].unique())
)

casas = st.sidebar.multiselect(
    "Casa legislativa",
    sorted(df["casa"].unique()),
    default=sorted(df["casa"].unique())
)

df_filtrado = df[
    (df["categoria"].isin(categorias)) &
    (df["partido"].isin(partidos)) &
    (df["estado"].isin(estados)) &
    (df["casa"].isin(casas))
]

# =============================
# CARDS
# =============================
col1, col2, col3, col4 = st.columns(4)

cards = [
    ("Proposições", len(df_filtrado)),
    ("Categorias", df_filtrado["categoria"].nunique()),
    ("Parlamentares", df_filtrado["autor"].nunique()),
    ("Estados", df_filtrado["estado"].nunique()),
]

for col, (titulo, valor) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{titulo}</div>
            <div class="card-value">{valor}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================
# GRÁFICOS
# =============================
st.markdown('<div class="section-title">Análises principais</div>', unsafe_allow_html=True)

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    categoria_count = df_filtrado["categoria"].value_counts().reset_index()
    categoria_count.columns = ["categoria", "quantidade"]

    fig_categoria = px.bar(
        categoria_count,
        x="categoria",
        y="quantidade",
        text="quantidade",
        title="Proposições por categoria"
    )

    fig_categoria.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111"),
        title_font=dict(size=20)
    )

    st.plotly_chart(fig_categoria, use_container_width=True)

with col_graf2:
    evolucao = (
        df_filtrado
        .groupby(df_filtrado["data_apresentacao"].dt.to_period("M"))
        .size()
        .reset_index(name="quantidade")
    )

    evolucao["data_apresentacao"] = evolucao["data_apresentacao"].astype(str)

    fig_evolucao = px.line(
        evolucao,
        x="data_apresentacao",
        y="quantidade",
        markers=True,
        title="Evolução temporal"
    )

    fig_evolucao.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#111"),
        title_font=dict(size=20)
    )

    st.plotly_chart(fig_evolucao, use_container_width=True)

# =============================
# RANKING E PARTIDO
# =============================
col_rank, col_partido = st.columns(2)

with col_rank:
    st.markdown('<div class="section-title">Ranking dos parlamentares</div>', unsafe_allow_html=True)

    ranking = df_filtrado["autor"].value_counts().reset_index()
    ranking.columns = ["Parlamentar", "Quantidade"]

    st.dataframe(ranking, use_container_width=True)

with col_partido:
    st.markdown('<div class="section-title">Distribuição por partido</div>', unsafe_allow_html=True)

    partido_count = df_filtrado["partido"].value_counts().reset_index()
    partido_count.columns = ["partido", "quantidade"]

    fig_partido = px.pie(
        partido_count,
        names="partido",
        values="quantidade",
        title="Proposições por partido"
    )

    st.plotly_chart(fig_partido, use_container_width=True)

# =============================
# ESTADOS
# =============================
st.markdown('<div class="section-title">Mapa / Distribuição por estado</div>', unsafe_allow_html=True)

estado_count = df_filtrado["estado"].value_counts().reset_index()
estado_count.columns = ["estado", "quantidade"]

fig_estado = px.bar(
    estado_count,
    x="estado",
    y="quantidade",
    text="quantidade",
    title="Quantidade de proposições por estado"
)

st.plotly_chart(fig_estado, use_container_width=True)

# =============================
# TABELA
# =============================
st.markdown('<div class="section-title">Proposições parlamentares</div>', unsafe_allow_html=True)

st.dataframe(
    df_filtrado[
        [
            "id_externo",
            "ementa",
            "autor",
            "partido",
            "estado",
            "casa",
            "data_apresentacao",
            "categoria",
            "confianca"
        ]
    ],
    use_container_width=True
)