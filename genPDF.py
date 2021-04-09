#
#	pip install reportlab
#
#	https://www.reportlab.com/dev/install/open_source_installation/
#
import random
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

colColumnas = "dcdcdc"
colHoras = "f0f0f0"
colores = ["e4fbff", "a2d5f2", "ffdecf", "ffcb91", "ffee93", "ade498", "ec4646", "ffe3fe", "a4ebf3", "d789d7"]

def gen(path, data, cursosSel):

	random.shuffle(colores)


	if (len(cursosSel) <= len(colores)):
		coloresCursos = {cursosSel[i]:colores[i] for i in range(len(cursosSel))}

	maxC = max([max([max([len(max(k.split("\n"))) for k in j]) for j in i]) for i in data])

	margin = 20.0
	fontSize = 10

	colWidth = maxC * 6
	rowHeight = 50

	sizeX = (len(data[0][0]) * colWidth) + (margin * 2)
	sizeY = (len(data[0]) * rowHeight) + (margin * 2) + (fontSize * 5)

	canvas = Canvas(path, pagesize=(sizeX, sizeY))

	for horario in data:
		colorCeldas = []

		if (len(cursosSel) <= len(colores)):
			for row in range(1, len(horario)):
				for col in range(1, len(horario[row])):
					for cursoCol in coloresCursos.items():
						if horario[row][col].count(cursoCol[0]) > 0:
							colorCeldas.append(("BACKGROUND", (col, row), (col, row), colors.HexColor("#" + cursoCol[1])))
							break

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
			("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#" + colColumnas)),
			("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
			("FONTSIZE", (0, 1), (0, -1), 14),
			("ALIGN", (0, 1), (0, -1), "RIGHT"),
			("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#" + colHoras)),
			("RIGHTPADDING", (0, 1), (0, -1), 20),
			("FONTSIZE", (1, 1), (-1, -1), fontSize),
			("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black)
		] + colorCeldas))

		table.drawOn(canvas, margin, margin)

		canvas.showPage()

	canvas.save()
