import tkinter as tk
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# Mensajes de Inicio
print("INICIO")
print("Preparando Datasets")

# Ruta Relativa
ruta = os.path.abspath(os.path.dirname(__file__))
# Lectura del DataFrame Base
df = pd.read_csv(ruta+"/BaseFiltrada.csv", encoding="utf8", parse_dates=True)

# OBTENER FECHAS COMO LISTA
fechas = list(df["fecha_referencia_tipo_caso"].unique())
fechas.sort()
# PREDEFINIR LISTA DE CANTIDADES DE GRUPOS DE EDAD A DIFERENCIAR
cantidadGruposEdad = [1, 2, 3, 4, 5]

#input("Presione ENTER para iniciar el Asistente\n")

# CREAR VENTANA DE TKINTER
miVentana = tk.Tk()
miVentana.title("HERRAMIENTA CONSULTAS COVID-19 CABA")
miVentana.geometry("450x550")

#Variable Tkinter

fechaDesde = tk.StringVar(miVentana)
fechaDesde.set(fechas[0])

fechaHasta = tk.StringVar(miVentana)
fechaHasta.set(fechas[-1])

edades = tk.StringVar(miVentana)
edades.set(cantidadGruposEdad[0])

version = tk.StringVar(miVentana)


# CREAR FUNCIONES PARA EL COMMAND DE CADA BOTÓN y FUNCIONES ACCESORIAS
def actualizarReportes():
    # Al ejecutarse esta función, se obtienen las fechas seleccionadas por el usuario,
    # y se crea un DF filtrado llamado "dfFiltroFecha"
    # Además se obtiene la fecha actual, para el número de versión y los nombres de los archivos
    # Por último, se llama a dos funciones secundarias pasándole como parámetro los datos obtenidos/filtrados

    fechaInicio = fechaDesde.get()  # Reemplace por código correspondiente
    fechaFin = fechaHasta.get()  # Reemplace por código correspondiente
    dfFiltroFecha = df[(df["fecha_referencia_tipo_caso"] >= fechaInicio) & (df["fecha_referencia_tipo_caso"] <= fechaFin)]
    fechaHora = datetime.datetime.now()
    

    # Actualice el label "Versión: " con la fecha correspondiente

    actualizarVisorVentana(dfFiltroFecha, fechaHora)
    crearPivotsCsv(dfFiltroFecha, fechaHora)


def actualizarVisorVentana(dfFiltrado, fechaHora):
    dfFemenino = dfFiltrado[(dfFiltrado["sexo"] == "F")] 
    dfMasculino = dfFiltrado[(dfFiltrado["sexo"] == "M")]
    dfConfirmados = dfFiltrado[(dfFiltrado["clasificacion_resumen"] == "Confirmado")]
    dfConfirmadosFemenino = dfConfirmados[(dfConfirmados["sexo"] == "F")]
    dfConfirmadosMasculino = dfConfirmados[(dfConfirmados["sexo"] == "M")]

    version.set(f"Versión: {fechaHora}\n" + 
    f"TOTAL CASOS ANALIZADOS: {len(dfFiltrado)}\n"
    f"Subtotal Femenino: {len(dfFemenino)}\n"
    f"Subtotal Masculino: {len(dfMasculino)}\n"
    f"TOTAL CASOS CONFIRMADOS: {len(dfConfirmados)}\n"
    f"Subtotal Femenino: {len(dfConfirmadosFemenino)}\n"
    f"Subtotal Masculino: {len(dfConfirmadosMasculino)}\n")


def crearPivotsCsv(dfFiltrado, feHo):
    # Convierta la fecha recibida a texto
    fechaTexto = feHo.strftime("%Y_%m_%d__%H-%M-%S")

    # Averigüe la cantidad de grupos de edad deseados para el análisis
    qIngresada = 1  # Reemplace valor "1" falso con el código correspondiente

    dfFiltrado["grupo_edad"] = None  # Utilice la funcion pd.cut()

    # Pivotee por fecha y genere output como csv

    # Pivotee por Comuna y genere output como csv


def crearGraficoTemporal():
    plt.close('all')
    frecuencias = df[["fecha_referencia_tipo_caso","clasificacion_resumen"]]
    print(frecuencias)
    frecuencias.plot.line(x="fecha_referencia_tipo_caso", y="clasificacion_resumen")
    plt.show()


def crearGraficoTortaEdades():
    plt.close('all')
    frecuencias = df["edad"].value_counts()
    print(frecuencias)
    frecuencias.plot.pie(autopct='%.2f')
    plt.show()



# CREE UN DICCIONARIO CON TODOS LOS ELEMENTOS (ORDENADOS)
elementos = {
    "label1_Titulo": tk.Label(miVentana, text="Bienvenido/a a la Herramienta de Consultas COVID-19 CABA"),
    "label2A_FechaDesde": tk.Label(miVentana, text="Fecha Desde:"),
    "label2B_FechaDesde" : tk.OptionMenu(miVentana, fechaDesde, *fechas),
    "label3A_FecheHasta": tk.Label(miVentana, text="Fecha Hasta:"),
    "label3B_FechaHasta" : tk.OptionMenu(miVentana, fechaHasta, *fechas),

    #Grupos Edades
    "label1A_GruposEdades": tk.Label(miVentana, text="Cantidad Grupos Edades:"),
    "label1B_GruposEdades": tk.OptionMenu(miVentana, edades, *cantidadGruposEdad),

    #Actualizacion Reportes
    "label1A_Reportes": tk.Button(miVentana, text="Actualizar Reportes por Comuna y Fecha", command=actualizarReportes),
    "label2_Reportes": tk.Label(miVentana, textvariable=version),

    #Graficos
    "label_graficos": tk.Label(miVentana, text="GRÁFICOS"),
    "labelA_temporal": tk.Button(miVentana, text="Generar Gráfico Temporal Total", command=crearGraficoTemporal),
    "labelB_edades": tk.Button(miVentana, text="Generar Gráfico Distribución Grupos Edades", command=crearGraficoTortaEdades),
}




# REALICE EL "PACK" DE TODOS LOS ELEMENTOS DEL DICCIONARIO
for e in elementos.values():
    e.pack()

actualizarReportes()

# EJECUTE (correr) MAINLOOP DE LA VENTANA
miVentana.mainloop()
