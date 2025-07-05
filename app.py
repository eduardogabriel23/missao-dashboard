
import pandas as pd
import streamlit as st

# Título do App
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Upload da planilha (aluno pode trocar depois)
df = pd.read_excel("vendas_realistas.xlsx")

# Filtro por cidade
cidade = st.selectbox("Selecione a cidade:", sorted(df["cidade"].unique()))
df_filtro = df[df["cidade"] == cidade]

# Métricas principais
col1, col2 = st.columns(2)
col1.metric("Total Vendido", f'R$ {df_filtro["valor"].sum():,.2f}')
col2.metric("Itens Vendidos", df_filtro.shape[0])

# Gráfico de linha de vendas por data
st.subheader("📈 Evolução das Vendas")
df_agrupado = df_filtro.groupby("data")["valor"].sum().reset_index()
st.line_chart(df_agrupado, x="data", y="valor")

# Tabela detalhada
st.subheader("📋 Detalhamento das Vendas")
st.dataframe(df_filtro.reset_index(drop=True))
