import pandas as pd
import streamlit as st

# Carrega os dados da planilha
df = pd.read_excel("vendas_realistas.xlsx")

# Título do dashboard
st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Filtro por filial
filial = st.selectbox("Filtrar por filial:", df["filial"].unique())
df_filtro = df[df["filial"] == filial]

# Métricas principais
st.metric("Total Vendido", f'R$ {df_filtro["preço"].sum():,.2f}')
st.metric("Itens Vendidos", df_filtro.shape[0])

# Gráfico de linha com soma de vendas por data
df_filtro["data"] = pd.to_datetime(df_filtro["data"])
st.line_chart(df_filtro.groupby("data")["preço"].sum())

# Tabela detalhada
st.dataframe(df_filtro)