# ==========================================================
# DATAJAM 2026
# FASE 2
# DESCARGA CLIMA OPEN-METEO
# ==========================================================

import pandas as pd
import requests
import time
from tqdm import tqdm

# ==========================================================
# COORDENADAS BOGOTA
# ==========================================================

coords = {

    'USAQUEN': (4.706,-74.031),
    'CHAPINERO': (4.648,-74.062),
    'SANTA FE': (4.608,-74.082),
    'SAN CRISTOBAL': (4.559,-74.084),
    'USME': (4.476,-74.116),
    'TUNJUELITO': (4.576,-74.132),
    'BOSA': (4.617,-74.185),
    'KENNEDY': (4.626,-74.151),
    'FONTIBON': (4.678,-74.141),
    'ENGATIVA': (4.701,-74.113),
    'SUBA': (4.746,-74.085),
    'BARRIOS UNIDOS': (4.666,-74.078),
    'TEUSAQUILLO': (4.639,-74.090),
    'LOS MARTIRES': (4.609,-74.091),
    'ANTONIO NARIÑO': (4.593,-74.101),
    'PUENTE ARANDA': (4.620,-74.115),
    'LA CANDELARIA': (4.598,-74.072),
    'RAFAEL URIBE': (4.565,-74.110),
    'CIUDAD BOLIVAR': (4.507,-74.154),
    'SUMAPAZ': (4.259,-74.181)

}

# ==========================================================
# RANGO FECHAS
# ==========================================================

fecha_inicio = "2022-01-01"
fecha_fin = "2026-06-30"

# ==========================================================
# DESCARGA
# ==========================================================

clima_total = []

for localidad in tqdm(coords.keys()):

    lat, lon = coords[localidad]

    print("\nDescargando:", localidad)

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={fecha_inicio}"
        f"&end_date={fecha_fin}"
        "&daily="
        "temperature_2m_mean,"
        "temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_sum,"
        "rain_sum,"
        "wind_speed_10m_max"
        "&timezone=America/Bogota"
    )

    try:

        r = requests.get(
            url,
            timeout=60
        )

        datos = r.json()

        clima = pd.DataFrame(
            datos['daily']
        )

        clima['new_localidad'] = localidad

        clima_total.append(
            clima
        )

        time.sleep(1)

    except Exception as e:

        print(
            localidad,
            e
        )

# ==========================================================
# UNIR
# ==========================================================

clima = pd.concat(
    clima_total,
    ignore_index=True
)

# ==========================================================
# RENOMBRAR
# ==========================================================

clima.rename(
    columns={

        'time':'fecha',
        'temperature_2m_mean':'temp_media',
        'temperature_2m_max':'temp_max',
        'temperature_2m_min':'temp_min',
        'precipitation_sum':'precipitacion',
        'rain_sum':'lluvia',
        'wind_speed_10m_max':'viento'

    },
    inplace=True
)

# ==========================================================
# VARIABLES CLIMA
# ==========================================================

clima['fecha'] = pd.to_datetime(
    clima['fecha']
)

clima['rango_temp'] = (
    clima['temp_max']
    -
    clima['temp_min']
)

clima['lluvia_intensa'] = (
    clima['precipitacion'] > 10
).astype(int)

clima['temperatura_alta'] = (
    clima['temp_max'] > 22
).astype(int)

clima['temperatura_baja'] = (
    clima['temp_min'] < 7
).astype(int)

# ==========================================================
# GUARDAR
# ==========================================================

clima.to_csv(
    "02_clima_localidades.csv",
    index=False,
    encoding='utf-8-sig'
)

print("\n===================")
print("FINALIZADO")
print("===================")
print(clima.shape)
print(clima.head())