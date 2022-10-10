import pandas as pd
import os

print("INICIO")

path = os.path.abspath(os.path.dirname(__file__))

df = pd.read_csv(path+"/BaseFiltrada.csv", encoding="utf8", parse_dates=True)

print("--- COLUMNAS ---")
print(df.columns)
print("--- RECUENTOS ---")
print(df.count())
print("--- UNICOS ---")
print(df.nunique())
print("--- RESUMEN CLASIFICACIÓN")
print(df["clasificacion_resumen"].unique())
print("--- COMUNAS ---")
print(df["residencia_departamento_nombre"].unique())
print("--- EDADES ---")
print("Edad Mínima:", df["edad"].min())
print("Edad Máxima:", df["edad"].max())
print("Edad Promedio:", df["edad"].mean())
print("--- SEXO ---")
print(df["sexo"].unique())
print("--- FECHAS ---")
print("Fecha Mínima", df["fecha_referencia_tipo_caso"].min())
print("Fecha Máxima", df["fecha_referencia_tipo_caso"].max())

# print("FIN")