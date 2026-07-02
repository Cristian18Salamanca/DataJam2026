# ==================================================
# DATAJAM 2026
# FASE 3
# TABLA AGREGADA
# ==================================================

import pandas as pd

# ==================================================
# CARGAR
# ==================================================

df = pd.read_excel(
    "01_dataset_maestro.xlsx"
)

# ==================================================
# FECHA
# ==================================================

df['fecha'] = pd.to_datetime(
    df['FECHA_CONSULTA']
).dt.date

# ==================================================
# AGRUPAR
# ==================================================

tabla = (

    df

    .groupby(

        [

            'fecha',
            'localidad_id',
            'new_localidad',
            'GRANDES_GRUPOS',
            'ENFERMEDADES_COMUNES',
            'SUBGRUPOS'

        ]

    )

    .size()

    .reset_index(
        name='atenciones'
    )

)

# ==================================================
# VARIABLES FECHA
# ==================================================

tabla['fecha'] = pd.to_datetime(
    tabla['fecha']
)

tabla['anio'] = (
    tabla['fecha']
    .dt.year
)

tabla['mes'] = (
    tabla['fecha']
    .dt.month
)

tabla['nombre_mes'] = (
    tabla['fecha']
    .dt.month_name(
        locale='es_ES'
    )
)

tabla['dia'] = (
    tabla['fecha']
    .dt.day
)

tabla['semana'] = (
    tabla['fecha']
    .dt.isocalendar()
    .week
)

tabla['dia_semana'] = (
    tabla['fecha']
    .dt.dayofweek
)

tabla['nombre_dia'] = (
    tabla['fecha']
    .dt.day_name(
        locale='es_ES'
    )
)

tabla['fin_semana'] = (
    tabla['dia_semana']
    .isin([5,6])
    .astype(int)
)

# ==================================================
# GUARDAR
# ==================================================

tabla.to_excel(
    "03_tabla_agregada.xlsx",
    index=False
)

print(tabla.shape)
print(tabla.head())