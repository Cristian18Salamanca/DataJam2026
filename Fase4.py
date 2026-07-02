# ==================================================
# FASE 4
# DATASET MODELADO SIN LEAKAGE
# ==================================================

import pandas as pd
import numpy as np

# ==================================================
# CARGAR
# ==================================================

tabla = pd.read_excel(
    "03_tabla_agregada.xlsx"
)

clima = pd.read_csv(
    "02_clima_localidades.csv"
)

tabla['fecha'] = pd.to_datetime(
    tabla['fecha']
)

clima['fecha'] = pd.to_datetime(
    clima['fecha']
)

tabla['new_localidad'] = (
    tabla['new_localidad']
    .str.upper()
    .str.strip()
)

clima['new_localidad'] = (
    clima['new_localidad']
    .str.upper()
    .str.strip()
)

# ==================================================
# MERGE
# ==================================================

df = tabla.merge(

    clima,

    on=[
        'fecha',
        'new_localidad'
    ],

    how='left'

)

# ==================================================
# VARIABLES TEMPORALES
# ==================================================

df['trimestre'] = (
    df['fecha']
    .dt.quarter
)

df['semestre'] = np.where(
    df['mes']<=6,
    1,
    2
)

df['bimestre'] = np.ceil(
    df['mes']/2
)

df['semana_epidemiologica'] = (
    df['semana']
)

df['temporada_lluvias'] = (
    df['mes']
    .isin([3,4,5,10,11])
).astype(int)

df['temporada_seca'] = (
    df['mes']
    .isin([1,2,6,7,8,12])
).astype(int)

df['temporada_respiratoria'] = (
    df['mes']
    .isin([3,4,5,9,10,11])
).astype(int)

# ==================================================
# VARIABLES CLIMA
# ==================================================

df['rango_termico'] = (
    df['temp_max']
    -
    df['temp_min']
)

df['lluvia_fuerte'] = (
    df['precipitacion']>10
).astype(int)

df['temperatura_alta'] = (
    df['temp_max']>22
).astype(int)

df['temperatura_baja'] = (
    df['temp_min']<7
).astype(int)

df['viento_fuerte'] = (
    df['viento']>20
).astype(int)

# ==================================================
# INDICE SATURACION
# ==================================================

p75 = (

    df[
        df['anio']<=2025
    ]

    .groupby(
        [
            'new_localidad',
            'GRANDES_GRUPOS'
        ]
    )

    ['atenciones']

    .quantile(.75)

)

p75 = p75.reset_index()

p75.columns = [
    'new_localidad',
    'GRANDES_GRUPOS',
    'p75'
]

df = df.merge(
    p75,
    on=[
        'new_localidad',
        'GRANDES_GRUPOS'
    ]
)

df['indice_saturacion'] = (
    df['atenciones']
    /
    df['p75']
)

# ==================================================
# TRAIN TEST
# ==================================================

train = df[
    df['anio']<=2025
]

test = df[
    df['anio']==2026
]

train.to_excel(
    '04_train.xlsx',
    index=False
)

test.to_excel(
    '04_test.xlsx',
    index=False
)

print(train.shape)
print(test.shape)