
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Vendas - Missão Anti-Planilha™", layout="wide")

st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Carregar os dados
df = pd.read_excel("vendas_realistas.xlsx")

# Filtro por cidade
cidade = st.selectbox("Filtrar por cidade:", df["cidade"].unique())
df_filtro = df[df["cidade"] == cidade]

# Métricas
st.metric("Total Vendido", f'R$ {df_filtro["valor"].sum():,.2f}')
st.metric("Itens Vendidos", df_filtro.shape[0])

# Gráfico de linha
st.line_chart(df_filtro.groupby("data")["valor"].sum())

# Tabela de dados
st.dataframe(df_filtro)
