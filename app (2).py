import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# Título da página
st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Carregando os dados
df = pd.read_excel("vendas_realistas.xlsx")

# Filtro por filial
filial = st.selectbox("📍 Filtrar por filial:", df["filial"].unique())
df_filtro = df[df["filial"] == filial]

# Métricas principais
col1, col2 = st.columns(2)
col1.metric("💰 Total Vendido", f'R$ {df_filtro["preco"].sum():,.2f}')
col2.metric("📦 Itens Vendidos", df_filtro.shape[0])

# Gráfico de vendas por data
st.subheader("📈 Evolução das Vendas")
vendas_por_dia = df_filtro.groupby("data")["preco"].sum()
st.line_chart(vendas_por_dia)

# Alerta automático se estiver abaixo da média
media_vendas = df.groupby("filial")["preco"].sum().mean()
vendas_filial = df_filtro["preco"].sum()

if vendas_filial < media_vendas:
    st.error("⚠️ Esta filial vendeu abaixo da média geral.")
else:
    st.success("✅ Esta filial está performando acima da média!")

# Ranking de vendedores
st.subheader("🏆 Ranking de Vendas por Vendedor")
ranking_vendedores = df_filtro.groupby("vendedor")["preco"].sum().sort_values(ascending=False)
st.bar_chart(ranking_vendedores)

# Botão de download do relatório em PDF
st.subheader("📄 Gerar Relatório PDF")

# Geração do PDF
if st.button("📥 Baixar Relatório"):
    pdf = FPDF()
    pdf.add_page()

    # Adiciona fonte com suporte a acento (você precisa subir o arquivo DejaVuSans.ttf no GitHub!)
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)

    pdf.cell(0, 10, f'Relatório de Vendas - Filial {filial}', ln=True)

    for vendedor, valor in ranking_vendedores.items():
        pdf.cell(0, 10, f'{vendedor}: R$ {valor:,.2f}', ln=True)

    # Salva o PDF
    pdf.output("relatorio_vendas.pdf")

    # Exibe link de download
    with open("relatorio_vendas.pdf", "rb") as f:
        st.download_button(
            label="📎 Clique aqui para baixar o PDF",
            data=f,
            file_name="relatorio_vendas.pdf",
            mime="application/pdf"
        )
