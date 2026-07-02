# ==================================================
# DATAJAM 2026
# FASE 7
# GRAFICAS FINALES
# ==================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# CREAR CARPETA
# ==================================================

os.makedirs(
    "Graficas",
    exist_ok=True
)

# ==================================================
# CARGAR
# ==================================================

df = pd.read_excel(
    "05_predicciones_2026.xlsx"
)

imp = pd.read_excel(
    "05_importancia_variables.xlsx"
)

# ==================================================
# ERROR
# ==================================================

df['error'] = (
    df['predicho']
    -
    df['real']
)

df['error_abs'] = abs(
    df['error']
)

# ==================================================
# REAL VS PREDICHO
# ==================================================

tmp = (

    df

    .groupby(
        'fecha'
    )

    [['real','predicho']]

    .sum()

)

plt.figure(
    figsize=(16,6)
)

plt.plot(
    tmp.index,
    tmp['real'],
    label='Real'
)

plt.plot(
    tmp.index,
    tmp['predicho'],
    label='Predicho'
)

plt.legend()

plt.title(
    'Real vs Predicho'
)

plt.savefig(
    'Graficas/02_real_vs_predicho.png'
)

plt.close()

# ==================================================
# ERROR MES
# ==================================================

tmp = (

    df

    .groupby(
        'nombre_mes'
    )

    ['error_abs']

    .mean()

)

plt.figure(
    figsize=(12,5)
)

tmp.plot(
    kind='bar'
)

plt.title(
    'Error promedio mensual'
)

plt.savefig(
    'Graficas/03_error_mensual.png'
)

plt.close()

# ==================================================
# LOCALIDADES
# ==================================================

tmp = (

    df

    .groupby(
        'new_localidad'
    )

    ['error_abs']

    .mean()

)

plt.figure(
    figsize=(12,6)
)

tmp.sort_values().plot(
    kind='bar'
)

plt.title(
    'Error por localidad'
)

plt.savefig(
    'Graficas/04_error_localidad.png'
)

plt.close()

# ==================================================
# GRUPOS
# ==================================================

tmp = (

    df

    .groupby(
        'GRANDES_GRUPOS'
    )

    ['error_abs']

    .mean()

)

plt.figure(
    figsize=(8,5)
)

tmp.plot(
    kind='bar'
)

plt.title(
    'Error por grupo'
)

plt.savefig(
    'Graficas/05_error_grupo.png'
)

plt.close()

# ==================================================
# ENFERMEDADES
# ==================================================

tmp = (

    df

    .groupby(
        'ENFERMEDADES_COMUNES'
    )

    ['error_abs']

    .mean()

    .sort_values(
        ascending=False
    )

    .head(10)

)

plt.figure(
    figsize=(12,6)
)

tmp.plot(
    kind='bar'
)

plt.title(
    'Top enfermedades con error'
)

plt.savefig(
    'Graficas/06_error_enfermedad.png'
)

plt.close()

# ==================================================
# IMPORTANCIA
# ==================================================

imp = imp.head(20)

plt.figure(
    figsize=(10,8)
)

plt.barh(
    imp['variable'],
    imp['importancia']
)

plt.title(
    'Importancia variables'
)

plt.savefig(
    'Graficas/07_importancia_variables.png'
)

plt.close()

# ==================================================
# TEMPERATURA
# ==================================================

tmp = (

    df

    .groupby(
        'temp_media'
    )

    ['real']

    .mean()

)

plt.figure(
    figsize=(8,5)
)

plt.scatter(
    tmp.index,
    tmp.values
)

plt.title(
    'Temperatura vs Morbilidad'
)

plt.savefig(
    'Graficas/08_temperatura_vs_morbilidad.png'
)

plt.close()

# ==================================================
# LLUVIA
# ==================================================

tmp = (

    df

    .groupby(
        'precipitacion'
    )

    ['real']

    .mean()

)

plt.figure(
    figsize=(8,5)
)

plt.scatter(
    tmp.index,
    tmp.values
)

plt.title(
    'Lluvia vs Morbilidad'
)

plt.savefig(
    'Graficas/09_lluvia_vs_morbilidad.png'
)

plt.close()

# ==================================================
# RESIDUALES
# ==================================================

plt.figure(
    figsize=(8,5)
)

plt.hist(
    df['error'],
    bins=40
)

plt.title(
    'Distribucion errores'
)

plt.savefig(
    'Graficas/10_residuales.png'
)

plt.close()

# ==================================================
# CORRELACION
# ==================================================

corr = df[[
    'real',
    'temp_media',
    'precipitacion',
    'viento'
]].corr()

plt.figure(
    figsize=(6,5)
)

plt.imshow(
    corr
)

plt.xticks(
    range(4),
    corr.columns,
    rotation=45
)

plt.yticks(
    range(4),
    corr.columns
)

plt.colorbar()

plt.title(
    'Correlacion clima'
)

plt.savefig(
    'Graficas/11_correlacion_clima.png'
)

plt.close()

print(
    "Graficas generadas"
)