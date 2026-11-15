import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px

# --- 1. CARGA Y PREPROCESAMIENTO DE LOS DATOS ---
print("Cargando microdatos del DANE...")
df_mortalidad = pd.read_excel('data/NoFetal2019.xlsx')
df_codigos = pd.read_excel('data/CodigosDeMuerte.xlsx')
df_divipola = pd.read_excel('data/Divipola.xlsx')

# Normalizar nombres de columnas a mayúsculas y limpiar espacios
df_mortalidad.columns = [str(col).strip().upper() for col in df_mortalidad.columns]
df_codigos.columns = [str(col).strip().upper() for col in df_codigos.columns]
df_divipola.columns = [str(col).strip().upper() for col in df_divipola.columns]

# --- 2. CONSTRUCCIÓN DE LAS 7 VISUALIZACIONES REQUERIDAS ---

# 1. Mapa / Gráfico de barras: Distribución total de muertes por departamento
muertes_dept = df_mortalidad.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
fig_mapa = px.bar(muertes_dept, x='COD_DEPARTAMENTO', y='TOTAL_MUERTES',
                  title='1. Distribución Total de Muertes por Departamento (2019)',
                  labels={'COD_DEPARTAMENTO': 'Código Departamento', 'TOTAL_MUERTES': 'Número de Defunciones'},
                  color='TOTAL_MUERTES', color_continuous_scale='Reds')

# 2. Gráfico de líneas: Total de muertes por mes
muertes_mes = df_mortalidad.groupby('MES').size().reset_index(name='TOTAL')
fig_lineas = px.line(muertes_mes, x='MES', y='TOTAL',
                     title='2. Tendencia de Mortalidad por Mes en Colombia',
                     labels={'MES': 'Mes del Año', 'TOTAL': 'Total Defunciones'},
                     markers=True)
fig_lineas.update_traces(line_color='#e74c3c', marker_size=8)

# 3. Gráfico de barras: 5 ciudades más violentas / homicidios (usando MANERA_MUERTE o códigos asociados)
homicidios = df_mortalidad[df_mortalidad['MANERA_MUERTE'].astype(str).str.contains('2|3|HOMICIDIO|VIOL', na=False, case=False)]
top_violentas = homicidios.groupby('COD_MUNICIPIO').size().reset_index(name='HOMICIDIOS').nlargest(5, 'HOMICIDIOS')
fig_violentas = px.bar(top_violentas, x='COD_MUNICIPIO', y='HOMICIDIOS',
                       title='3. Top 5 Ciudades con Mayor Incidencia de Violencia / Homicidios',
                       labels={'COD_MUNICIPIO': 'Código Municipio', 'HOMICIDIOS': 'Casos Registrados'},
                       color='HOMICIDIOS', color_continuous_scale='Sunsetdark')

# 4. Gráfico circular (Pie): 10 ciudades con menor índice de mortalidad
menor_mortalidad = df_mortalidad.groupby('COD_MUNICIPIO').size().reset_index(name='TOTAL').nsmallest(10, 'TOTAL')
fig_pie = px.pie(menor_mortalidad, names='COD_MUNICIPIO', values='TOTAL',
                 title='4. Las 10 Ciudades con Menor Índice de Mortalidad',
                 hole=0.4)

# 5. Tabla: 10 principales causas de muerte en Colombia (usando COD_MUERTE)
top_causas = df_mortalidad.groupby('COD_MUERTE').size().reset_index(name='TOTAL_CASOS')
top_causas = top_causas.nlargest(10, 'TOTAL_CASOS')

# 6. Gráfico de barras apiladas: Comparación de muertes por sexo en cada departamento
muertes_sexo = df_mortalidad.groupby(['COD_DEPARTAMENTO', 'SEXO']).size().reset_index(name='TOTAL')
fig_apiladas = px.bar(muertes_sexo, x='COD_DEPARTAMENTO', y='TOTAL', color='SEXO',
                      title='6. Comparación de Mortalidad por Sexo y Departamento',
                      labels={'COD_DEPARTAMENTO': 'Departamento', 'TOTAL': 'Defunciones', 'SEXO': 'Sexo'},
                      barmode='stack')

# 7. Histograma: Distribución de muertes según GRUPO_EDAD1 (Ciclo de vida)
fig_hist = px.histogram(df_mortalidad, x='GRUPO_EDAD1',
                        title='7. Distribución de Mortalidad por Ciclo de Vida (Grupo de Edad DANE)',
                        labels={'GRUPO_EDAD1': 'Grupos de Edad (DANE)'},
                        nbins=25)
fig_hist.update_traces(marker_color='#3498db')


# --- 3. CONFIGURACIÓN DE LA APLICACIÓN WEB EN DASH ---
app = dash.Dash(__name__)
server = app.server  # Necesario para Gunicorn en Render

app.layout = html.Div(style={'backgroundColor': '#f4f6f7', 'padding': '30px', 'fontFamily': 'Arial'}, children=[
    
    html.H1("Análisis Interactivo de Mortalidad en Colombia - 2019", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
    html.P("Plataforma analítica basada en los microdatos oficiales del DANE (Estadísticas Vitales)", 
           style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),
    
    html.Hr(),

    # Fila 1: Mapa y Gráfico de Líneas
    html.Div([
        html.Div([dcc.Graph(figure=fig_mapa)], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([dcc.Graph(figure=fig_lineas)], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '20px'}),

    # Fila 2: Violencia y Gráfico Circular
    html.Div([
        html.Div([dcc.Graph(figure=fig_violentas)], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([dcc.Graph(figure=fig_pie)], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '20px'}),

    # Fila 3: Barras apiladas e Histograma de edades
    html.Div([
        html.Div([dcc.Graph(figure=fig_apiladas)], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([dcc.Graph(figure=fig_hist)], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ], style={'marginBottom': '30px'}),

    # Fila 4: Tabla de principales causas de muerte
    html.Div([
        html.H3("5. Listado de las 10 Principales Causas de Muerte en Colombia", style={'color': '#2c3e50'}),
        dash_table.DataTable(
            data=top_causas.to_dict('records'),
            columns=[{"name": str(i), "id": str(i)} for i in top_causas.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left', 'padding': '12px', 'backgroundColor': 'white'}
        )
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.05)'})
])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)