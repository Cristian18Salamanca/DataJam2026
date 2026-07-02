# ==================================================
# DATAJAM 2026
# FASE 5
# ENTRENAMIENTO SIN DATA LEAKAGE
# VERSION FINAL
# ==================================================

import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from xgboost import XGBRegressor

# ==================================================
# CARGAR
# ==================================================

print("Cargando datasets...")

train = pd.read_excel(
    "04_train.xlsx"
)

test_original = pd.read_excel(
    "04_test.xlsx"
)

test = test_original.copy()

print("Train:", train.shape)
print("Test :", test.shape)

# ==================================================
# VARIABLES CATEGORICAS
# ==================================================

categoricas = [

    'new_localidad',
    'GRANDES_GRUPOS',
    'ENFERMEDADES_COMUNES',
    'SUBGRUPOS',

    'nombre_mes',
    'nombre_dia'

]

encoders = {}

# ==================================================
# LABEL ENCODING
# ==================================================

for c in categoricas:

    print("Encoding:", c)

    le = LabelEncoder()

    train[c] = le.fit_transform(
        train[c].astype(str)
    )

    clases = set(
        le.classes_
    )

    test[c] = test[c].astype(str)

    test[c] = test[c].apply(

        lambda x:
        x
        if x in clases
        else le.classes_[0]

    )

    test[c] = le.transform(
        test[c]
    )

    encoders[c] = le

# ==================================================
# FEATURES
# ==================================================

features = [

    'localidad_id',

    'new_localidad',

    'GRANDES_GRUPOS',

    'ENFERMEDADES_COMUNES',

    'SUBGRUPOS',

    'anio',

    'mes',

    'dia',

    'semana',

    'dia_semana',

    'fin_semana',

    'semestre',

    'bimestre',

    'trimestre',

    'semana_epidemiologica',

    'temporada_lluvias',

    'temporada_seca',

    'temporada_respiratoria',

    'temp_media',

    'temp_max',

    'temp_min',

    'precipitacion',

    'lluvia',

    'viento',

    'rango_termico',

    'lluvia_fuerte',

    'temperatura_alta',

    'temperatura_baja',

    'viento_fuerte'

]

# ==================================================
# X Y
# ==================================================

X_train = train[features]

X_test = test[features]

y_train = train['atenciones']

y_test = test['atenciones']

# ==================================================
# MODELO
# ==================================================

modelo = XGBRegressor(

    objective='reg:squarederror',

    n_estimators=500,

    max_depth=8,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    n_jobs=-1

)

print("\nEntrenando modelo...")

modelo.fit(
    X_train,
    y_train
)

# ==================================================
# PREDICCION
# ==================================================

pred = modelo.predict(
    X_test
)

pred = np.round(pred)

pred[pred < 0] = 0

# ==================================================
# METRICAS
# ==================================================

mae = mean_absolute_error(
    y_test,
    pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        pred
    )
)

r2 = r2_score(
    y_test,
    pred
)

mape = (

    np.abs(
        (
            y_test-pred
        )
        /
        np.where(
            y_test==0,
            1,
            y_test
        )
    )

).mean()*100

print("\n=================")
print("RESULTADOS")
print("=================")

print("MAE :", round(mae,2))
print("RMSE:", round(rmse,2))
print("MAPE:", round(mape,2))
print("R2  :", round(r2,4))

# ==================================================
# IMPORTANCIA
# ==================================================

imp = pd.DataFrame({

    'variable': features,

    'importancia':
        modelo.feature_importances_

})

imp = imp.sort_values(
    'importancia',
    ascending=False
)

# ==================================================
# RESULTADO FINAL
# ==================================================

resultado = test_original.copy()

resultado['real'] = y_test.values

resultado['predicho'] = pred

resultado['error'] = (

    resultado['predicho']
    -
    resultado['real']

)

resultado['error_abs'] = np.abs(
    resultado['error']
)

resultado['error_pct'] = (

    resultado['error_abs']

    /

    np.where(
        resultado['real']==0,
        1,
        resultado['real']
    )

)*100

# ==================================================
# GUARDAR
# ==================================================

resultado.to_excel(

    '05_predicciones_2026.xlsx',

    index=False

)

imp.to_excel(

    '05_importancia_variables.xlsx',

    index=False

)

joblib.dump(

    modelo,

    'modelo_xgboost.pkl'

)

print("\n======================")
print("ARCHIVOS GENERADOS")
print("======================")

print(
    "05_predicciones_2026.xlsx"
)

print(
    "05_importancia_variables.xlsx"
)

print(
    "modelo_xgboost.pkl"
)

print("\nTOP VARIABLES")

print(
    imp.head(20)
)