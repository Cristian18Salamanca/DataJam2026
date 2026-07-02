Predicción de Morbilidad en Servicios de Urgencias de la Subred Sur de Bogotá 
utilizando Analítica Predictiva y Variables Climáticas (2022–2026)

Descripción del proyecto

Este proyecto tiene como objetivo desarrollar un modelo de analítica predictiva para estimar el comportamiento de la morbilidad en los servicios de urgencias de la Subred Integrada de Servicios de Salud Sur de Bogotá, utilizando información histórica entre los años 2022 y 2025 y validando las predicciones con los datos reales del primer semestre de 2026.

La metodología integra variables epidemiológicas, temporales y climáticas, permitiendo identificar patrones, tendencias y comportamientos asociados a la demanda hospitalaria.

La información utilizada en este proyecto fue obtenida inicialmente desde bases de datos institucionales almacenadas en SQL Server. Posteriormente, los resultados fueron exportados a archivos Excel para realizar los procesos de extracción, transformación, integración, modelado predictivo y visualización.

Origen de datos

SQL Server
        ↓
Consulta SQL
        ↓
Exportación Excel
        ↓
Python ETL

Información climática

Se utilizó la API gratuita:

Open-Meteo API
https://open-meteo.com

La API permitió obtener variables climáticas históricas para las localidades de Bogotá asociadas a cada fecha de consulta.

Metodología

La metodología utilizada se basó en el enfoque CRISP-DM.

FASE 1 — Consolidación y ETL

Objetivo:

Unificar los archivos históricos de morbilidad.
Estandarizar variables.
Corregir inconsistencias.

Archivos procesados:

Morbilidad_Urgencias_22.xlsx
Morbilidad_Urgencias_23.xlsx
Morbilidad_Urgencias_24.xlsx
Morbilidad_Urgencias_25.xlsx
Morbilidad_Urgencias_26.xlsx

Actividades:

Unión de archivos.
Conversión de formatos.
Normalización de columnas.
Limpieza de registros.

Resultado:

01_dataset_maestro.xlsx
FASE 2 — Ingeniería geográfica y clima

Objetivo:

Extraer información territorial y climática.

Actividades:

Extracción territorial

A partir de la variable:

LOCALIDAD - BARRIO - SECTOR

se generaron:

new_localidad
new_barrio
Variables climáticas

Mediante Open-Meteo API se obtuvieron:

Temperatura promedio.
Temperatura máxima.
Temperatura mínima.
Precipitación.
Lluvia.
Velocidad del viento.

Resultado:

02_clima_localidades.csv
FASE 3 — Construcción de tabla agregada

Objetivo:

Construir el dataset analítico.

Granularidad:

Fecha
Localidad
Grandes grupos
Enfermedades comunes
Subgrupos

Variables generadas:

Año.
Mes.
Semana.
Día.
Nombre del día.
Nombre del mes.
Fin de semana.

Resultado:

03_tabla_agregada.xlsx
FASE 4 — Construcción del dataset de modelado

Objetivo:

Crear los datasets de entrenamiento y validación evitando fuga de información.

División temporal:

Entrenamiento
2022
2023
2024
2025
Validación
Primer semestre 2026

Variables creadas:

Temporales
Mes.
Día.
Semana.
Trimestre.
Semestre.
Bimestre.
Semana epidemiológica.
Estacionales
Temporada de lluvias.
Temporada seca.
Temporada respiratoria.
Climáticas
Temperatura media.
Temperatura máxima.
Temperatura mínima.
Precipitación.
Viento.
Rango térmico.

Resultados:

04_train.xlsx
04_test.xlsx
FASE 5 — Modelo predictivo

Modelo utilizado:

XGBoost Regressor

Objetivo:

Predecir el comportamiento de la morbilidad del primer semestre de 2026.

Resultados del modelo:

Métrica	Resultado
MAE	1.09
RMSE	2.01
MAPE	39.7%
R²	0.6557

Estos resultados indican que el modelo logró explicar aproximadamente el 66% de la variabilidad observada en la demanda hospitalaria.

Resultados:

05_predicciones_2026.xlsx
05_importancia_variables.xlsx
modelo_xgboost.pkl
FASE 6 — Evaluación

Se evaluó el modelo mediante:

Error absoluto medio.
Error cuadrático medio.
Error porcentual.
Coeficiente de determinación.

Archivos generados:

06_evaluacion_general.xlsx
06_evaluacion_localidad.xlsx
06_evaluacion_grupos.xlsx
06_evaluacion_enfermedad.xlsx
06_dashboard_powerbi.xlsx
FASE 7 — Visualización y análisis

Se generaron automáticamente las gráficas para el análisis estadístico.

Interpretación de las gráficas
1. Real vs Predicho

Archivo:

02_real_vs_predicho.png
Interpretación

La gráfica evidencia que el modelo logra capturar adecuadamente la tendencia general de la morbilidad durante el primer semestre de 2026.

Se observa:

Un comportamiento cíclico semanal.
Incrementos y disminuciones consistentes.
Una adecuada aproximación entre la serie observada y la serie estimada.

Esto indica que el modelo posee capacidad para identificar patrones temporales relevantes.

2. Error promedio mensual

Archivo:

03_error_mensual.png
Interpretación

El error promedio mensual se mantuvo relativamente estable durante el periodo analizado.

Hallazgos:

Junio presentó el menor error.
Julio y agosto presentaron errores ligeramente superiores.
No se observaron desviaciones críticas.

Esto demuestra estabilidad predictiva.

3. Error por localidad

Archivo:

04_error_localidad.png
Interpretación

El error no fue homogéneo entre localidades.

Hallazgos:

Algunas localidades presentaron errores inferiores a 0.25 atenciones.
Otras localidades alcanzaron errores cercanos a 2 atenciones.

Esto evidencia diferencias territoriales en la capacidad predictiva.

4. Error por grandes grupos

Archivo:

05_error_grupo.png
Interpretación

El comportamiento predictivo varió según la clasificación epidemiológica.

Hallazgos:

Las enfermedades no transmisibles presentaron menor error.
Los eventos asociados a causas externas presentaron mayor variabilidad.
5. Top enfermedades con mayor error

Archivo:

06_error_enfermedad.png
Interpretación

Las enfermedades con mayor variabilidad asistencial presentaron mayores errores de predicción.

Esto es esperable debido a:

Estacionalidad.
Eventos externos.
Variabilidad clínica.
6. Importancia de variables

Archivo:

07_importancia_variables.png
Interpretación

Las variables con mayor aporte predictivo fueron:

Grandes grupos epidemiológicos.
Semestre.
Localidad.
Subgrupos.
Enfermedades comunes.
Semana epidemiológica.

Las variables climáticas mostraron una contribución moderada.

7. Temperatura vs Morbilidad

Archivo:

08_temperatura_vs_morbilidad.png
Interpretación

Se observó una relación no lineal entre la temperatura y la morbilidad.

Hallazgos:

Temperaturas medias entre 11°C y 13°C presentaron mayores niveles de atención.
Temperaturas superiores mostraron una disminución relativa.
8. Lluvia vs Morbilidad

Archivo:

09_lluvia_vs_morbilidad.png
Interpretación

La precipitación mostró una asociación moderada con la demanda de urgencias.

Se evidenció:

Mayor dispersión durante periodos lluviosos.
Incrementos en determinados grupos de enfermedades.
9. Distribución de errores

Archivo:

10_residuales.png
Interpretación

La distribución de los errores presenta una forma aproximadamente normal y centrada en cero.

Esto indica:

Ausencia de sesgos importantes.
Buen ajuste global.
Errores aleatorios y controlados.
10. Correlación climática

Archivo:

11_correlacion_clima.png
Interpretación

La matriz de correlación mostró:

Correlaciones bajas entre clima y morbilidad.
Asociación moderada entre temperatura y demanda.
Influencia limitada del viento.

Esto sugiere que las variables climáticas actúan como factores complementarios y no como determinantes únicos.