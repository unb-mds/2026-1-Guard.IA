import streamlit as st
import pandas as pd

# 1. Configurações da Página (Isso aparece na aba do navegador)
st.set_page_config(
    page_title="Guard.IA - Monitoramento",
    page_icon="🛡️",
    layout="wide"
)

# 2. CSS Customizado (Para a Gabi começar a brincar com o visual do Figma)
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

# 4. Painel de Métricas (Dashboard inicial)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Projetos Coletados", value="1.240", delta="12 hoje")
with col2:
    st.metric(label="Aguardando Filtro", value="85", delta="-5", delta_color="normal")
with col3:
    st.metric(label="Classificados pela IA", value="1.155")
with col4:
    st.metric(label="Alertas Críticos", value="42", delta="2 novos", delta_color="inverse")

st.divider()

# 5. Seção de Boas-vindas e Instruções
st.markdown("### 🚀 Próximos Passos para o Desenvolvimento")
st.write("""
Este é o esqueleto inicial do nosso portal. A estrutura de **Pipes and Filters** já está integrada!
- **Desenvolvedor(a) Front-end:** Você pode editar este arquivo para mudar o visual ou adicionar novos elementos.
- **Novas Páginas:** Basta criar um arquivo `.py` dentro da pasta `/pages` e ele aparecerá no menu ao lado automaticamente.
- **Dados:** O backend salvará os arquivos processados na pasta `/data`, e o Streamlit fará a leitura em tempo real.
""")

st.info("Utilize a barra lateral à esquerda para navegar entre os módulos do sistema.")