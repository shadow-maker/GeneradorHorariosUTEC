# Copyright 2021
#
# github.com/shadow-maker

#
#
#	La finalidad de este programa es parsear el archivo de horarios proporcionado por la UTEC (convertido a CSV) a un archivo JSON que organice las secciones de cada curso en diccionarios de una manera más entendible por el usuario y por el programa principal
#
#

from pathlib import Path
import csv
import json

print("Para empezar deberá guardar el archivo Excel de horarios proporcionado por la UTEC como archivo CSV (eliminar los headers, dejar los titulos de las columnas).")

print("El nombre por defecto de este archivo (en este directorio) es 'data.csv', si el path/nombre es distinto indicarlo a continuacion, si no presionar enter:")

path = ""
while not Path(path).is_file():
	res = input(">").lower()
	path = "data.csv" if res == "" else res

data = list(csv.DictReader(open(path, "r", encoding="utf-8-sig")))

cursos = {}

diasSemana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

for i in data:
	#print(cursos)
	#print()
	# No hay soporte para cursos que no siguen la 'semana general'
	if i["Frecuencia"] == "Semana General":
		newItem = {
			"sesion": i["Sesión Grupo"],
			"dia": diasSemana.index(i["Día"]),
			"hora": int(i["Hora"].split(" ")[0].split(":")[0]),
			"duracion": int(i["Horas Semanales"].split(":")[0]),
			"vacantes": int(i["Vac."]),
			"matriculados": int(i["Alum. Mat."]),
			"docente": i["Docente"],
			"correoDoc": i["Correo"]
		}

		if i["Cod. Curso"] in cursos:
			if i["Sec"] in cursos[i["Cod. Curso"]]["secciones"]:
				cursos[i["Cod. Curso"]]["secciones"][i["Sec"]]["sesiones"].append(newItem)
			else:
				cursos[i["Cod. Curso"]]["secciones"][i["Sec"]] = {
					"vacantes": int(i["Vac."]),
					"matriculados": int(i["Alum. Mat."]),
					"sesiones": [newItem]
				}
		else:
			cursos[i["Cod. Curso"]] = {"nombre": i["Nombre Curso"], "secciones": {i["Sec"]: {
				"vacantes": int(i["Vac."]),
				"matriculados": int(i["Alum. Mat."]),
				"sesiones": [newItem]
			}}}

for curso in cursos.items():
	newSecs = {}
	for sec in curso[1]["secciones"].items(): # Loop secciones en un curso
		if len([i for i in sec[1]["sesiones"] if int(i["sesion"].split(".")[-1]) not in [0, 1]]) > 0:
			secGen = {
				"vacantes": -1,
				"matriculados": -1,
				"sesiones": [i for i in sec[1]["sesiones"] if int(i["sesion"].split(".")[-1]) == 0]
			}

			for i in range(max([int(j["sesion"].split(".")[-1]) for j in sec[1]["sesiones"]])):
				newSecs[sec[0] + "." + str(i + 1).zfill(2)] = secGen.copy()

			for i in [j for j in sec[1]["sesiones"] if int(j["sesion"].split(".")[-1]) != 0]: # Loop sesiones en una seccion
				key = sec[0] + "." + str(i["sesion"].split(".")[-1]).zfill(2)
				newSecs[key]["vacantes"] = i["vacantes"]
				newSecs[key]["matriculados"] = i["matriculados"]
				newSecs[key]["sesiones"].append(i)

		else:
			newSecs[sec[0]] = sec[1]

	# Editar seccion
	if len([int(i["sesion"].split(".")[-1]) for i in sec[1]["sesiones"] if int(i["sesion"].split(".")[-1]) not in [0, 1]]) > 0:
		cursos[curso[0]]["secciones"] = {i[0]: {
			"vacantes": i[1]["vacantes"],
			"matriculados": i[1]["matriculados"],
			"sesiones": [j for j in i[1]["sesiones"] if int(j["sesion"].split(".")[-1]) in [0, int(i[0].split(".")[-1])]]
		} for i in newSecs.items()}


	for sec in curso[1]["secciones"].values():
		for ses in sec["sesiones"]:
			ses.pop("vacantes", None)
			ses.pop("matriculados", None)


json.dump(cursos, open("horarios.json", "w"), indent=4, ensure_ascii=False)
