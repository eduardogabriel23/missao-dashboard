import pandas as pd
import streamlit as st

# Título da aplicação
st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Carregando a planilha
df = pd.read_excel("vendas_realistas.xlsx")

# Filtro por filial (ajustado)
filial = st.selectbox("Filtrar por filial:", df["filial"].unique())
df_filtro = df[df["filial"] == filial]

# Exibição de métricas com o nome correto da coluna
st.metric("Total Vendido", f'R$ {df_filtro["preco"].sum():,.2f}')
st.metric("Itens Vendidos", df_filtro.shape[0])

# Gráfico de linha por data
st.line_chart(df_filtro.groupby("data")["preco"].sum())

# Exibição da tabela filtrada
st.dataframe(df_filtro)
