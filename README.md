# Aplicación Web Interactiva para el Análisis de Mortalidad en Colombia (2019)

# Integrantes
John Alexander Ocoro Lerma

# Enlace de la aplicación web en la nube (PaaS - Render):

https://mortalidad-colombia-2019.onrender.com (Nota: Al estar alojada en el plan gratuito de Render, si el servidor se encuentra inactivo, la primera carga puede tomar unos segundos en despertar).

# Enlace al repositorio del proyecto en GitHub:

https://github.com/AlexanderOcoro/mortalidad_colombia_2019

## Introducción del Proyecto
Esta aplicación web dinámica desarrollada en Python utiliza (Dash) y (Plotly) para procesar, analizar y visualizar microdatos de mortalidad en Colombia correspondientes al año 2019, publicados por el DANE (Estadísticas Vitales - EEVV).

## Objetivo
Facilitar la exploración visual intuitiva de patrones demográficos, causas de defunción, distribución regional y disparidades por género y ciclo de vida en la población colombiana durante 2019.

## Gráficos

# 1. Distribución Total de Muertes por Departamento (2019)
![app mortalidad](img/1app_mortalidad.png)

Gráfico de barras interactivo con gradiente de color que muestra el volumen acumulado de defunciones por departamento, permitiendo identificar rápidamente las regiones con mayor densidad poblacional y concentración de registros.

# 2. Tendencia de Mortalidad por Mes en Colombia
![app mortalidad](img/2Tendencia_Mortalidad.png)

Gráfico de líneas con marcadores que detalla la evolución mensual de las defunciones durante el año 2019, evidenciando los meses con mayores picos y descensos a nivel nacional.

# 3. Top 5 Ciudades con Mayor Incidencia de Violencia / Homicidios
![app mortalidad](img/3Ciudades_MayorMortalidad.png)

Gráfico de barras que resalta los municipios con mayores registros de muertes asociadas a hechos violentos u homicidios en el país.

# 4. Las 10 Ciudades con Menor Índice de Mortalidad
![app mortalidad](img/4Ciudad_MenorIndiceMortalidad.png)

Gráfico circular tipo dona que ilustra la distribución porcentual de los diez municipios con menor cantidad de defunciones reportadas.

# 5. Listado de las 10 Principales Causas de Muerte en Colombia
![app mortalidad](img/5Causas_Muerte_Colombia.png)

Tabla estructurada que detalla los códigos de las diez causas de defunción más frecuentes en el país junto con el número total de casos asociados a cada una.

# 6. Comparación de Mortalidad por Sexo y Departamento
![app mortalidad](img/6Comparacion_Mortalidad_Sexo.png)

Gráfico de barras apiladas que contrasta y analiza la proporción de defunciones desglosada por sexo en los diferentes departamentos.

# 7. Distribución de Mortalidad por Ciclo de Vida (Grupo de Edad DANE)
![app mortalidad](img/7Distribucion_Mortalidad.png)

Histograma que representa la frecuencia de los fallecimientos agrupados según los rangos de edad y etapas del ciclo vital definidos por el DANE.

## Estructura del Proyecto
```text
mortalidad_colombia_2019/
│
├── data/                    # Archivos Excel fuente (DANE)
│   ├── NoFetal2019.xlsx
│   ├── CodigosDeMuerte.xlsx
│   └── Divipola.xlsx
│
├── app.py                   # Script principal de la aplicación Dash
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto

