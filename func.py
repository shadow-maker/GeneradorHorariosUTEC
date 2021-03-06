# Copyright 2021
#
# github.com/shadow-maker

from itertools import product

# Calcula la menor y mayor hora de inicio de clases de un horario
def getLimHoras(horario):
	minList = []
	maxList = []
	for dia in horario:
		for i in range(len(dia)):
			if dia[i]:
				minList.append(i)
				break

		for i in range(len(dia), 0, -1):
			if dia[i - 1]:
				maxList.append(i - 1)
				break

	return min(minList), max(maxList)

# Calcula la menor y mayor hora de inicio de clases de varios horario
def getLimHorasHorarios(horarios):
	minList = []
	maxList = []

	for horario in horarios:
		min, max = getLimHoras(horario)
		minList.append(int(min))
		maxList.append(int(max))

	return minList, maxList

# Formatear horario a una tabla de listas para almacenarse en CSV
def formatHorario(horario, minH, maxH):
	formatted = []

	def prof(dia, hora):
		prof = dia[hora]["docente"].split(", ")[1] + " " + dia[hora]["docente"].split(", ")[0] if dia[hora]["docente"].count(", ") == 1 else dia[hora]["docente"]
		return prof

	for hora in range(minH, maxH + 1):
		formatted.append([str(hora) + ":00 - " + str(hora + 1) + ":00"])
		formatted[-1] += [(
			dia[hora]["codigo"] + " \n" + dia[hora]["nombre"] + "\n(sec" + dia[hora]["seccion"] + "), " + dia[hora]["nomSesion"] + ",\n" + prof(dia, hora)
		) if len(dia[hora]) > 0 else "" for dia in horario]

	return formatted

# Formatear el horario de una seccion de un curso como una lista de listas de diccionarios que represente el horario en una semana
def genSemana(seccion, sec, cod, nombre):
	semana = [[{} for j in range(24)] for i in range(7)]
	for ses in seccion["sesiones"]:
		for i in range(ses["duracion"]):
			semana[ses["dia"]][ses["hora"]+ i] = {
				"codigo": cod,
				"nombre": nombre,
				"seccion": sec,
				"nomSesion": ses["sesion"],
				"vacantes": seccion["vacantes"],
				"matriculados": seccion["matriculados"],
				"docente": ses["docente"],
				"correoDoc": ses["correoDoc"]
			}
	return semana

# Formatear los horarios de todas las secciones de un curso como una lista de listas de diccionarios que represente el horario en una semana
def genSecCurso(curso, cod):
	# Solo genera horario si hay vacantes disponibles
	return [genSemana(sec[1], sec[0], cod, curso["nombre"]) for sec in curso["secciones"].items() if sec[1]["matriculados"] < sec[1]["vacantes"]]

# Combinar los horarios de las secciones de distintos cursos en un solo horario, si no existen conflictos
def combHorario(horarios, filtHoraMin, filtHoraMax):
	horario = [[{} for j in range(24)] for i in range(7)]

	for dia in range(len(horario)):
		horariosDia = [i[dia] for i in horarios]
		for hora in range(len(horario[dia])):
			horariosHora = [i[hora] for i in horariosDia]
			# ??Cumple filtros?
			if (hora < filtHoraMin or hora > filtHoraMax) and len([1 for i in horariosHora if i]) > 0:
				return []
			# ??Existe conflicto?
			if len([1 for i in horariosHora if i]) > 1:
				return []
			for i in horariosHora:
				if i:
					horario[dia][hora] = i
					break
	return horario

# Comparar los horarios de todas las secciones de todos los cursos seleccionados
def compCursos(cursos, filtHoraMin, filtHoraMax):
	posHorarios = []
	for comb in product(*cursos):
		horario = combHorario(list(comb), filtHoraMin, filtHoraMax)
		if len(horario) != 0:
			posHorarios.append(horario)
	return posHorarios
