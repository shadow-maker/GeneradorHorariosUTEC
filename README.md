# GeneradorHorariosUTEC
Un script de python que genera todas las posibles combinaciones de horarios sin conflictos con los cursos deseados de la UTEC

**Para usar este programa guardar el proyecto entero (todos los archivos en un directorio) y correr el archivo 'main.py' con Python (probado con Python 3.8.2)**

*IMPORTANTE:*
* Por el momento este programa solo soporta cursos que siguen la 'semana general'
* Este programa fue creado para la matricula del ciclo 2021-1 en la UTEC y contiene el documento (convertio a CSV) de horarios (carga habil) de este ciclo. Si este no es el ciclo actual o el documento ha sido actualizado, deberá guardar el archivo Excel de horarios proporcionado por la UTEC como archivo CSV (eliminar los headers, dejar los titulos de las columnas)
* El programa tiene la funcionalidad generar un archivo PDF con los horarios generados. Para hacer uso de este deberá tener instalado el paquete 'Reportlab' con el comando `pip install reportlab` o visitando [https://www.reportlab.com/dev/install/open_source_installation/](https://www.reportlab.com/dev/install/open_source_installation/)
