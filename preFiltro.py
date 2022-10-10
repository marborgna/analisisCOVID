import pandas as pd
import numpy as np
import datetime
import os

print("INICIO")
path = os.path.abspath(os.path.dirname(__file__))

# tipos_datos = {
#     "sexo": "string",
#     "edad_años_meses": "string",
#     "residencia_pais_nombre": "string",
#     "residencia_provincia_nombre": "string",
#     "residencia_departamento_nombre": "string",
#     "carga_provincia_nombre": "string",
#     "cuidado_intensivo": "string",
#     "fallecido": "string",
#     "asistencia_respiratoria_mecanica": "string",
#     "origen_financiamiento": "string",
#     "clasificacion": "string",
#     "clasificacion_resumen": "string",
# }

columnasDeseadas = ["sexo","edad","edad_años_meses","residencia_provincia_nombre","residencia_departamento_nombre","fecha_inicio_sintomas","fecha_apertura","fecha_internacion","fecha_cui_intensivo","fecha_fallecimiento","clasificacion_resumen","fecha_diagnostico"]

df = pd.read_csv(path+"/Covid19Casos.csv", encoding="utf8", usecols=columnasDeseadas, parse_dates=["fecha_inicio_sintomas","fecha_apertura","fecha_internacion","fecha_cui_intensivo","fecha_fallecimiento", "fecha_diagnostico"])
print("1 - LEIDO")

distritos = ["CABA"]
df2 = df[df["residencia_provincia_nombre"].isin(distritos)]
del df
print("2a - FILTRADO POR DISTRITO")

def detectarFecha(x):
    if not pd.isna(x["fecha_diagnostico"]):
        return x["fecha_diagnostico"]
    elif not pd.isna(x["fecha_inicio_sintomas"]):
        return x["fecha_inicio_sintomas"]
    elif not pd.isna(x["fecha_internacion"]):
        return x["fecha_internacion"]
    elif not pd.isna(x["fecha_fallecimiento"]):
        return x["fecha_fallecimiento"]
    else:
        return x["fecha_apertura"]

# Problema de Múltiples Fechas
df2.loc[:,"fecha_referencia_tipo_caso"] = df2.apply(lambda row: detectarFecha(row), axis=1)
print("2b - FECHA CALCULADA")

# Problema Edad/Años/Meses
df2.loc[:,"edad"] = df2.apply(lambda row: 0 if row["edad_años_meses"]=="Meses" else row["edad"],axis=1)
print("2c - EDAD CORREGIDA")

columnasFinales = ["fecha_referencia_tipo_caso","residencia_provincia_nombre","residencia_departamento_nombre","sexo","edad","clasificacion_resumen"]

df3 = df2[columnasFinales]
del df2
print("3 - COLUMNAS FINALES SELECCIONADAS")

# Filtrar hasta cierta fecha
df4 = df3[df3["fecha_referencia_tipo_caso"] < "2020-12-01"]
del df3
print("4 - FILTRADO POR FECHA MENOR A...")

# Ordenar por fecha
df5 = df4.sort_values(by="fecha_referencia_tipo_caso")
del df4
print("5 - ORDENADO POR FECHA")

# DUMP CSV
df5.to_csv(path+"/BaseFiltrada.csv", index=False)
del df5
print("-- Archivo Generado --")
print("FIN")