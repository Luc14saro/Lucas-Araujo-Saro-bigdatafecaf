"""Dashboard Streamlit que consome as views SQL do PostgreSQL.

Executar:  streamlit run src/dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from db import get_engine

st.set_page_config(page_title="Dashboard de Temperaturas IoT", layout="wide")
engine = get_engine()


@st.cache_data(ttl=60)
def load_data(view_name: str) -> pd.DataFrame:
    """Carrega todos os registros de uma view."""
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


st.title("Dashboard de Temperaturas IoT")
st.caption("Pipeline: CSV (Kaggle) → Python/SQLAlchemy → PostgreSQL (Docker) → Streamlit")

try:
    df_avg_temp = load_data("avg_temp_por_dispositivo")
    df_leituras_hora = load_data("leituras_por_hora")
    df_temp_max_min = load_data("temp_max_min_por_dia")
except Exception as erro:  # banco fora do ar ou views ainda não criadas
    st.error(
        "Não foi possível ler as views. Suba o container (docker compose up -d) "
        f"e rode src/ingest.py antes.\n\nDetalhe: {erro}"
    )
    st.stop()

# Indicadores gerais
c1, c2, c3 = st.columns(3)
c1.metric("Total de leituras", f"{int(df_avg_temp['total_leituras'].sum()):,}".replace(",", "."))
c2.metric("Temperatura máxima", f"{df_temp_max_min['temp_max'].max():.0f} °C")
c3.metric("Temperatura mínima", f"{df_temp_max_min['temp_min'].min():.0f} °C")

# Gráfico 1: média de temperatura por dispositivo
st.header("Média de Temperatura por Dispositivo")
fig1 = px.bar(
    df_avg_temp,
    x="device_id",
    y="avg_temp",
    color="location",
    barmode="group",
    labels={"device_id": "Dispositivo", "avg_temp": "Temperatura média (°C)", "location": "Local"},
)
st.plotly_chart(fig1, width="stretch")

# Gráfico 2: contagem de leituras por hora
st.header("Leituras por Hora do Dia")
fig2 = px.line(
    df_leituras_hora,
    x="hora",
    y="contagem",
    markers=True,
    labels={"hora": "Hora do dia", "contagem": "Nº de leituras"},
)
st.plotly_chart(fig2, width="stretch")

# Gráfico 3: temperaturas máximas e mínimas por dia
st.header("Temperaturas Máximas e Mínimas por Dia")
fig3 = px.line(
    df_temp_max_min,
    x="data",
    y=["temp_max", "temp_min"],
    labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Medida"},
)
st.plotly_chart(fig3, width="stretch")
