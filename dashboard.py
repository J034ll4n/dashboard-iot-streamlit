import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- Configurações da Página ---
st.set_page_config(
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Tema e Estilo Personalizado ---
st.markdown(
    """
    <style>
        :root {
            --primary-color: #00FFFF;
            --background-color: #1E1E24;
            --secondary-background-color: #2B2B36;
            --text-color: #F8F8F2;
            --font-family: sans-serif;
        }
        body {
            color: var(--text-color);
            background-color: var(--background-color);
            font-family: var(--font-family);
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary-color);
        }
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .stMetric, .stAlert, .stCard {
            background-color: var(--secondary-background-color);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stMetric > div > div > div > div {
            color: var(--primary-color);
        }
        .heat-index-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .heat-index-table th, .heat-index-table td {
            border: 1px solid #444;
            padding: 8px;
            text-align: left;
        }
        .heat-index-table th {
            background-color: var(--primary-color);
            color: #1E1E24;
        }
        .bg-green { background-color: #228B22; }
        .bg-yellow { background-color: #CCCC00; }
        .bg-orange { background-color: #FF8C00; }
        .bg-red { background-color: #B22222; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Conexão com o Banco de Dados ---
db_string = "postgresql://postgres:Joe102030!@localhost:5432/postgres"
engine = create_engine(db_string)

# --- Função para Carregar Dados ---
@st.cache_data(ttl=60)
def load_data(view_name):
    try:
        df = pd.read_sql_query(f"SELECT * FROM \"{view_name}\"", engine)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados da view '{view_name}': {e}")
        return pd.DataFrame()

# --- Título Principal ---
st.markdown(
    """
    <h1 style="color:white; text-align:center;">Dashboard <span style="color:#00FFFF;">Temperature  IoT Devices</span></h1>
    """,
    unsafe_allow_html=True
)
st.subheader('Leituras de sensores de temperatura instalados em um "quarto de administração", com medições tanto do ambiente interno (in) quanto externo (out).')

# --- Sessão de Métricas Globais ---
st.markdown("---")
st.subheader("Métricas Globais")

col1, col2, col3, col4 = st.columns(4)

df_min_max_global = load_data('temp_max_min_por_dia')
if not df_min_max_global.empty:
    max_temp_geral = df_min_max_global['temp_max'].max()
    min_temp_geral = df_min_max_global['temp_min'].min()
    col1.metric("Temperatura Máxima Geral", f"{max_temp_geral:.1f} °C")
    col2.metric("Temperatura Mínima Geral", f"{min_temp_geral:.1f} °C")

df_avg_local = load_data('avg_temp_por_local')
if not df_avg_local.empty:
    avg_temp_in = df_avg_local[df_avg_local['location'] == 'In']['avg_temp_geral'].iloc[0]
    avg_temp_out = df_avg_local[df_avg_local['location'] == 'Out']['avg_temp_geral'].iloc[0]
    col3.metric("Média Geral (Interno)", f"{avg_temp_in:.1f} °C")
    col4.metric("Média Geral (Externo)", f"{avg_temp_out:.1f} °C")

st.markdown("---")

# --- Gráficos Comparativos In-Out ---
st.subheader("Análise Comparativa (Interno vs. Externo)")

df_temp_por_local_dia = load_data('temp_por_local_dia')
if not df_temp_por_local_dia.empty:
    fig4 = px.line(
        df_temp_por_local_dia,
        x='data',
        y='avg_temp_diaria',
        color='location',
        title='Tendência da Temperatura Diária (Interno vs. Externo)',
        color_discrete_sequence=['#A020F0', '#00FFFF'],
        labels={'avg_temp_diaria': 'Temperatura Média (°C)', 'data': 'Data', 'location': 'Ambiente'}
    )
    fig4.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#F8F8F2'
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- Gráfico de Variação de Temperatura (Box Plot) ---
st.subheader("Variação da Temperatura por Ambiente")

df_temperatures = pd.read_sql_query(
    "SELECT temperature, location FROM temperature_readings", engine
)
if not df_temperatures.empty:
    fig5 = px.box(
        df_temperatures,
        x='location',
        y='temperature',
        color='location',
        title='Distribuição da Temperatura por Ambiente',
        color_discrete_sequence=['#A020F0', '#00FFFF']
    )
    fig5.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#F8F8F2'
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")


# --- Análise de Mês Mais Quente/Frio ---
st.markdown("---")
st.subheader("Análise Mensal: Mês Mais Quente e Mais Frio")

df_avg_temp_por_mes = load_data('avg_temp_por_mes')
if not df_avg_temp_por_mes.empty:
    # Mapear números do mês para nomes para melhor visualização
    meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                   7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    df_avg_temp_por_mes['mes'] = df_avg_temp_por_mes['mes'].astype(int).map(meses_nomes)

    # Encontrar o mês mais quente e o mais frio
    mes_mais_quente = df_avg_temp_por_mes.loc[df_avg_temp_por_mes['avg_temp'].idxmax()]
    mes_mais_frio = df_avg_temp_por_mes.loc[df_avg_temp_por_mes['avg_temp'].idxmin()]

    # Exibir métricas
    col1, col2 = st.columns(2)
    col1.metric(
        label="Mês Mais Quente",
        value=f"{mes_mais_quente['mes']} ({mes_mais_quente['avg_temp']:.1f} °C)"
    )
    col2.metric(
        label="Mês Mais Frio",
        value=f"{mes_mais_frio['mes']} ({mes_mais_frio['avg_temp']:.1f} °C)"
    )

    # Criar o gráfico de barras
    fig_mes = px.bar(
        df_avg_temp_por_mes,
        x='mes',
        y='avg_temp',
        title='Temperatura Média por Mês',
        labels={'mes': 'Mês', 'avg_temp': 'Temperatura Média (°C)'},
        color_discrete_sequence=['#00FFFF']
    )
    fig_mes.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#F8F8F2'
    )
    st.plotly_chart(fig_mes, use_container_width=True)

# --- Informações Adicionais ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Projeto Pipeline de Dados com IoT e Docker</p>", unsafe_allow_html=True)