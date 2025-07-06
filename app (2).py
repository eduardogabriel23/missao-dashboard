from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# Usa fonte que entende acento e português
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)

pdf.cell(0, 10, 'Relatório de Vendas por Filial', ln=True)

for filial, valor in resumo.items():
    pdf.cell(0, 10, f'{filial}: R$ {valor:,.2f}', ln=True)

pdf.output("relatorio_vendas.pdf")
