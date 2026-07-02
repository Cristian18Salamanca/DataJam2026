# ==================================================
# DATAJAM 2026
# FASE 6
# VALIDACION
# ==================================================

import pandas as pd

# ==================================================
# CARGAR
# ==================================================

df = pd.read_excel(
    "05_predicciones_2026.xlsx"
)

# ==================================================
# GENERAL
# ==================================================

general = pd.DataFrame({

    'REAL':[

        df['real'].sum()

    ],

    'PREDICHO':[

        df['predicho'].sum()

    ],

    'ERROR_ABS':[

        df['error_abs'].mean()

    ],

    'ERROR_PCT':[

        df['error_pct'].mean()

    ]

})

# ==================================================
# LOCALIDAD
# ==================================================

localidad = (

    df

    .groupby(
        'new_localidad'
    )

    .agg(

        real=('real','sum'),

        predicho=('predicho','sum'),

        error=('error_abs','mean'),

        error_pct=('error_pct','mean')

    )

    .reset_index()

)

# ==================================================
# GRANDES GRUPOS
# ==================================================

grupos = (

    df

    .groupby(
        'GRANDES_GRUPOS'
    )

    .agg(

        real=('real','sum'),

        predicho=('predicho','sum'),

        error=('error_abs','mean'),

        error_pct=('error_pct','mean')

    )

    .reset_index()

)

# ==================================================
# ENFERMEDADES
# ==================================================

enfermedades = (

    df

    .groupby(
        'ENFERMEDADES_COMUNES'
    )

    .agg(

        real=('real','sum'),

        predicho=('predicho','sum'),

        error=('error_abs','mean'),

        error_pct=('error_pct','mean')

    )

    .reset_index()

)

# ==================================================
# SUBGRUPOS
# ==================================================

subgrupos = (

    df

    .groupby(
        'SUBGRUPOS'
    )

    .agg(

        real=('real','sum'),

        predicho=('predicho','sum'),

        error=('error_abs','mean'),

        error_pct=('error_pct','mean')

    )

    .reset_index()

)

# ==================================================
# REAL VS PREDICHO
# ==================================================

real_pred = (

    df

    .groupby(
        'fecha'
    )

    .agg(

        real=('real','sum'),

        predicho=('predicho','sum')

    )

    .reset_index()

)

real_pred['error'] = (

    real_pred['predicho']
    -
    real_pred['real']

)

# ==================================================
# DASHBOARD
# ==================================================

dashboard = df.copy()

# ==================================================
# GUARDAR
# ==================================================

general.to_excel(

    '06_evaluacion_general.xlsx',

    index=False

)

localidad.to_excel(

    '06_evaluacion_localidad.xlsx',

    index=False

)

grupos.to_excel(

    '06_evaluacion_grupos.xlsx',

    index=False

)

enfermedades.to_excel(

    '06_evaluacion_enfermedad.xlsx',

    index=False

)

subgrupos.to_excel(

    '06_evaluacion_subgrupos.xlsx',

    index=False

)

real_pred.to_excel(

    '06_real_vs_predicho.xlsx',

    index=False

)

dashboard.to_excel(

    '06_dashboard_powerbi.xlsx',

    index=False

)

print("\n======================")
print("FASE 6 FINALIZADA")
print("======================")

print(
    "06_evaluacion_general.xlsx"
)

print(
    "06_evaluacion_localidad.xlsx"
)

print(
    "06_evaluacion_grupos.xlsx"
)

print(
    "06_evaluacion_enfermedad.xlsx"
)

print(
    "06_evaluacion_subgrupos.xlsx"
)

print(
    "06_real_vs_predicho.xlsx"
)

print(
    "06_dashboard_powerbi.xlsx"
)