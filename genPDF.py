#
#	pip install reportlab
#
#	https://www.reportlab.com/dev/install/open_source_installation/
#
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

def gen(path, data, cursosSel):

	maxC = max([max([max([len(max(k.split("\n"))) for k in j]) for j in i]) for i in data])

	margin = 20.0
	fontSize = 10

	colWidth = maxC * 6
	rowHeight = 50

	sizeX = (len(data[0][0]) * colWidth) + (margin * 2)
	sizeY = (len(data[0]) * rowHeight) + (margin * 2) + (fontSize * 5)

	canvas = Canvas(path, pagesize=(sizeX, sizeY))

	i = 0
	for horario in data:
		canvas.setFont("Helvetica", fontSize)
		canvas.setFillColor(colors.black)

		canvas.drawString(margin, sizeY - (fontSize * 1) - margin, "Horario generado usando el Generador de Horarios UTEC - github.com/shadow-maker/GeneradorHorariosUTEC")
		canvas.drawString(margin, sizeY - (fontSize * 3) - margin, "Cursos encontrados en este horario: " + ", ".join(cursosSel))

		table = Table(horario, colWidths=colWidth, rowHeights=rowHeight)

		#table.wrap(20, 20)
		table.wrapOn(canvas, 0, 0)

		table.setStyle(TableStyle([
			#("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#4287f5")),
			("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
			("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
			("FONTSIZE", (0, 0), (-1, 0), 18),
			("ALIGN", (0, 0), (-1, 0), "CENTER"),
			("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
			("FONTSIZE", (0, 1), (0, -1), 14),
			("ALIGN", (0, 1), (0, -1), "RIGHT"),
			("RIGHTPADDING", (0, 1), (0, -1), 20),
			("FONTSIZE", (1, 1), (-1, -1), fontSize),
			('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black)
		]))

		table.drawOn(canvas, margin, margin)

		canvas.showPage()
		i += 1

	canvas.save()
