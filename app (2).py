
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
df = pd.read_excel("vendas_realistas.xlsx")
df["data"] = pd.to_datetime(df["data"])

# Título do dashboard
st.title("📊 Dashboard de Vendas - Missão Anti-Planilha™")

# Filtro por filial
filial = st.selectbox("Filtrar por filial:", df["filial"].unique())
df_filtro = df[df["filial"] == filial]

# Métricas principais
col1, col2 = st.columns(2)
col1.metric("📉 Média Geral", f'R$ {df.groupby("filial")["preco"].sum().mean():,.2f}')
col2.metric("🏪 Total da Filial", f'R$ {df_filtro["preco"].sum():,.2f}')

# Alerta inteligente
media_vendas = df.groupby("filial")["preco"].sum().mean()
vendas_filial = df_filtro["preco"].sum()

if vendas_filial < media_vendas:
    st.error("⚠️ Esta filial vendeu abaixo da média!")
else:
    st.success("✅ Esta filial está performando acima da média!")

# Gráfico de linha - vendas ao longo do tempo
st.subheader("📈 Vendas ao Longo do Tempo")
st.line_chart(df_filtro.groupby("data")["preco"].sum())

# Ranking de vendedores
ranking_vendedores = df_filtro.groupby("vendedor")["preco"].sum().sort_values(ascending=False)
st.subheader("🏆 Ranking de Vendas por Vendedor")
st.bar_chart(ranking_vendedores)

# Gráfico de barras - Vendas por Filial
st.subheader("🏢 Total de Vendas por Filial")
vendas_filial_total = df.groupby("filial")["preco"].sum().sort_values()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=vendas_filial_total.values, y=vendas_filial_total.index, palette="Blues_d", ax=ax)
ax.set_title("Total de Vendas por Filial")
ax.set_xlabel("R$ Vendido")
ax.set_ylabel("Filial")
st.pyplot(fig)

# Gráfico de pizza - Participação de Produtos
st.subheader("🥧 Participação de Vendas por Produto")
vendas_produto = df.groupby("produto")["preco"].sum()
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(vendas_produto, labels=vendas_produto.index, autopct='%1.1f%%', startangle=140)
ax2.set_title("Participação de Vendas por Produto")
st.pyplot(fig2)

from fpdf import FPDF

st.subheader("📥 Gerar Relatório em PDF")

if st.button("📄 Baixar PDF do Relatório"):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "📊 Relatório de Vendas - Missão Anti-Planilha™", ln=True, align="C")
            self.ln(10)

        def chapter_title(self, title):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, title, ln=True)
            self.ln(5)

        def chapter_body(self, text):
            self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, text)
            self.ln()

    pdf = PDF()
    pdf.add_page()
    
    # Dados do relatório
    media = f"R$ {media_vendas:,.2f}"
    total = f"R$ {vendas_filial:,.2f}"
    
    pdf.chapter_title("📌 Resumo da Filial")
    resumo = f"Média Geral: {media}\nTotal da Filial Selecionada: {total}"
    pdf.chapter_body(resumo)

    pdf.chapter_title("🏆 Ranking de Vendas por Vendedor")
    for vendedor, valor in ranking_vendedores.items():
        pdf.chapter_body(f"{vendedor}: R$ {valor:,.2f}")
    
    # Salvar
    pdf.output("relatorio_vendas.pdf")
    with open("relatorio_vendas.pdf", "rb") as f:
        st.download_button("⬇️ Clique aqui para baixar seu relatório PDF", f, file_name="relatorio_vendas.pdf")

