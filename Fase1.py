# ==========================================================
# DATAJAM 2026
# FASE 1 ETL
# VERSION XLSX
# ==========================================================

import pandas as pd
import numpy as np
import glob
import os

# ==========================================================
# CONFIGURACION
# ==========================================================

RUTA = r"C:\Users\CSALAMANCA\Desktop\Trabajos Subred Sur\DATAJAM - 2026"

# ==========================================================
# BUSCAR ARCHIVOS XLSX
# ==========================================================

archivos = glob.glob(
    os.path.join(
        RUTA,
        "Morbilidad_Urgencias_*.xlsx"
    )
)

print("\n==============================")
print("ARCHIVOS ENCONTRADOS")
print("==============================")

for a in archivos:
    print(os.path.basename(a))

print("\nTOTAL:", len(archivos))

if len(archivos) == 0:
    raise Exception(
        "No se encontraron archivos xlsx"
    )

# ==========================================================
# LEER ARCHIVOS
# ==========================================================

dfs = []

for archivo in archivos:

    nombre = os.path.basename(archivo)

    print("\nLeyendo:", nombre)

    try:

        tmp = pd.read_excel(
            archivo,
            dtype=str,
            engine='openpyxl'
        )

        tmp["archivo_origen"] = nombre

        print(
            "Registros:",
            len(tmp),
            "Columnas:",
            len(tmp.columns)
        )

        dfs.append(tmp)

    except Exception as e:

        print(
            "ERROR:",
            nombre
        )

        print(e)

# ==========================================================
# VALIDAR
# ==========================================================

if len(dfs) == 0:
    raise Exception(
        "No se pudo cargar ningun archivo"
    )

# ==========================================================
# UNIR
# ==========================================================

df = pd.concat(
    dfs,
    ignore_index=True
)

print("\n==============================")
print("UNION")
print("==============================")

print(
    "Registros:",
    len(df)
)

print(
    "Variables:",
    len(df.columns)
)

# ==========================================================
# LIMPIEZA
# ==========================================================

def limpiar(x):

    if pd.isna(x):
        return np.nan

    return (
        str(x)
        .upper()
        .strip()
        .replace('Á','A')
        .replace('É','E')
        .replace('Í','I')
        .replace('Ó','O')
        .replace('Ú','U')
        .replace('Ñ','N')
    )

# ==========================================================
# LIMPIAR VARIABLES TEXTO
# ==========================================================

texto = [

    'ETAREO',
    'SEXO',
    'BARRIO',
    'DIAGNOSTICO',
    'GRANDES_GRUPOS',
    'ENFERMEDADES_COMUNES',
    'SUBGRUPOS'

]

for c in texto:

    if c in df.columns:

        print("Limpiando:", c)

        df[c] = df[c].apply(
            limpiar
        )

# ==========================================================
# LOCALIDAD ID
# ==========================================================

df['localidad_id'] = df['LOCALIDAD']

# ==========================================================
# EXTRAER LOCALIDAD/BARRIO/SECTOR
# ==========================================================

def extraer(texto):

    if pd.isna(texto):

        return pd.Series([
            None,
            None,
            None
        ])

    partes = [
        x.strip()
        for x in str(texto).split('-')
    ]

    localidad = None
    barrio = None
    sector = None

    if len(partes)>=1:
        localidad = partes[0]

    if len(partes)>=2:
        barrio = partes[1]

    if len(partes)>=3:
        sector = ' - '.join(
            partes[2:]
        )

    return pd.Series([
        localidad,
        barrio,
        sector
    ])

df[
    [
        'new_localidad',
        'new_barrio',
        'new_sector'
    ]
] = df['BARRIO'].apply(
    extraer
)

# ==========================================================
# FECHAS
# ==========================================================

df['FECHA_CONSULTA'] = pd.to_datetime(
    df['FECHA_CONSULTA'],
    errors='coerce'
)

df['anio'] = (
    df['FECHA_CONSULTA']
    .dt.year
)

df['mes'] = (
    df['FECHA_CONSULTA']
    .dt.month
)

df['dia'] = (
    df['FECHA_CONSULTA']
    .dt.day
)

df['hora'] = (
    df['FECHA_CONSULTA']
    .dt.hour
)

df['semana'] = (
    df['FECHA_CONSULTA']
    .dt.isocalendar()
    .week
)

df['trimestre'] = (
    df['FECHA_CONSULTA']
    .dt.quarter
)

df['dia_semana'] = (
    df['FECHA_CONSULTA']
    .dt.dayofweek
)

df['fin_semana'] = (
    df['dia_semana']
    .isin([5,6])
    .astype(int)
)

# ==========================================================
# NUMERICAS
# ==========================================================

numericas = [

    'EDAD',
    'PESO',
    'TALLA',
    'CANT_ATENC',
    'ORDEN_ETAREO',
    'LOCALIDAD'

]

for c in numericas:

    if c in df.columns:

        df[c] = (
            df[c]
            .astype(str)
            .str.replace(',','.')
        )

        df[c] = pd.to_numeric(
            df[c],
            errors='coerce'
        )

# ==========================================================
# DUPLICADOS
# ==========================================================

duplicados = (
    df
    .duplicated()
    .sum()
)

print(
    "\nDuplicados:",
    duplicados
)

df = df.drop_duplicates()

# ==========================================================
# CALIDAD
# ==========================================================

print("\n==============================")
print("CALIDAD")
print("==============================")

print(
    "Registros:",
    len(df)
)

print(
    "Localidades:",
    df['new_localidad']
    .nunique()
)

print(
    "Barrios:",
    df['new_barrio']
    .nunique()
)

print(
    "Sectores:",
    df['new_sector']
    .nunique()
)

print(
    "CIE10:",
    df['CIE10']
    .nunique()
)

# ==========================================================
# GUARDAR
# ==========================================================

salida = os.path.join(
    RUTA,
    "01_dataset_maestro.xlsx"
)

df.to_excel(
    salida,
    index=False
)

print("\n==============================")
print("ETL FINALIZADO")
print("==============================")
print("Registros:", len(df))
print("Variables:", len(df.columns))
print("Archivo:", salida)
print("==============================")