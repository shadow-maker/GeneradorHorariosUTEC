# Copyright 2021
#
# github.com/shadow-maker

from pathlib import Path
import os
import sys
import json
import csv
import func

print()
print("-" * 30)
print("\nGENERADOR DE HORARIOS UTEC\n")
print("-" * 30)
print()

print("Este programa utiliza el documento de horarios (carga habil) proporcionado por la UTEC para generar todos los posibles horarios con los cursos deseados")
print("IMPORTANTE: Por el momento este programa solo soporta cursos que siguen la 'semana general'")

print()
print("El directorio de este programa contiene el archivo Excel de los horarios del ciclo 2021-1, si este no es el ciclo actual o el documento ha sido actualizado ingrese [Y] a continuacion, si no, enter")

if input(">").lower() == "y":
	import genJSON

if not Path("horarios.json").is_file():
	sys.exit("\n  ERROR: El archivo 'horarios.json' no se encuentra en el directorio\n")

horarios = json.load(open("horarios.json", "r"))

print("\nSe encontraron " + str(len(horarios)) + " cursos en el archivo de horarios")

print("¿Desea mostrar los cursos disponibles? [Y = Si]:")

if input(">").lower() == "y":
	j = 0
	for i in horarios.items():
		nom = i[0] + "-" + i[1]["nombre"]
		endC = " " * (60 - len(nom)) if j % 2 == 0 else "\n"
		print(nom, end=endC)
		j += 1

#
#
#	Pedir al usuario que ingrese cursos
#
#

cursosSel = []

print("\nIngrese (uno por uno) los codigos de los cursos que desea llevar, ingrese enter para terminar")

sel = " "

while sel != "":
	sel = input(">").upper()
	if sel.count("-") > 0 and all([i in list(horarios.keys()) for i in sel.split("-")]):
		cursosSel = sel.split("-")
		break
	elif sel in cursosSel:
		print("Ese curso ya fue seleccionado!")
	elif sel in list(horarios.keys()):
		cursosSel.append(sel)
		print("SELECCIONADO: " + horarios[sel]["nombre"])
	elif sel != "":
		print("Ese curso no existe!")

if len(cursosSel) == 0:
	sys.exit("El programa ha terminado porque no seleccionó ningun curso")

cursosSel.sort()

print("Cursos seleccionados:", end=" ")
print(cursosSel)

#
#
#	Pedir al usuario que ingrese filtros de horas
#
#

print("\n(FILTRO OPCIONAL) Si desea ingrese la hora mínima de inicio de clases [0-23], si no, enter")

sel = input(">")
filtHoraMin = int(sel) if sel in [str(i) for i in range(24)] else 0

print("\n(FILTRO OPCIONAL) Si desea ingrese la hora máxima de fin de clases [0-23], si no, enter")

sel = input(">")
filtHoraMax = int(sel) if sel in [str(i) for i in range(24)] else 23

#
#
#	Generar posibles horarios sin conflictos
#
#

posHorarios = func.compCursos([func.genSecCurso(horarios[cod], cod) for cod in cursosSel], filtHoraMin, filtHoraMax)

print()
print(str(len(posHorarios)) + " posibles horarios sin conflicto encontrados con clases entre las " + str(filtHoraMin) + ":00 y " + str(filtHoraMax) + ":00")

if len(posHorarios) == 0:
	sys.exit("El programa ha terminado porque han encontrado posibles horarios")

#
#
#	Guardar posibles horarios en un archivo JSON (sin formato)
#
#

json.dump(posHorarios, open("posHorarios.json", "w"), indent=4, ensure_ascii=False)

print("Los posibles horarios fueron guardados en formato JSON en el archivo 'posHorarios.json' en este directorio")

#
#
#	Guardar posibles horarios formateados de manera legible en archivos CSV
#
#

print("¿Desea generar un archivo CSV formateado para cada posible horario? [Y = si]")

if input(">").lower() == "y":
	for horario in range(len(posHorarios)):
		dir = "PosiblesHorarios/(" + str(filtHoraMin) + "-" + str(filtHoraMax) + ")_" + "-".join(cursosSel) + "/"
		if not Path(dir).exists():
			os.makedirs(dir)
		with open(dir + str(horario + 1) + ".csv", "w", encoding="utf-8-sig") as file:
			csvWriter = csv.writer(file)
			csvWriter.writerow(["Hora", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
			for line in func.formatHorario(posHorarios[horario]):
				csvWriter.writerow(line)
	"Los horarios formateados fueron almacenados en la carpeta PosiblesHorarios dentro de este directorio"
