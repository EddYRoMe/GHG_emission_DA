import streamlit as st # Importando librería de streamlit
import pandas as pd
import plotly.express as px
from PIL import Image # Para agregar imágenes
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title='Tablero Interactivo Datos de contaminación Ambiental', page_icon="🌎",layout='wide')
#st.subheader('Análisis de emisiones en el mundo')
st.markdown('<style>div.block-container(padding-top:lrem;)</style>', unsafe_allow_html= True)
image=Image.open('/workspaces/GHG_emission_DA/talento.png')

col1,col2 =st.columns((0.2, 0.7))
with col1:
    st.image(image,width=300)
html_title="""
    <style>
        .title-test{
        font-weight:bold;
        padding:14 px;
        border-radius:6px;
        }
    </style>
    <center><h1 class="title-test"> Análisis de Emisiones de CO2 en el Mundo y su relación con la población y el PBI🌎 </h1></center>"""
with col2:
    st.markdown(html_title,unsafe_allow_html= True)

df_1=pd.read_csv('df_1.csv', sep=',')
df_2=pd.read_csv('df_2.csv', sep=',')
df= pd.read_csv('df.csv', sep=',')
df_estad=pd.read_csv('df_estad.csv', sep=',')
#st.dataframe(df)
df_pca=df.sort_values(by='Country', ascending=True)
df1_reset = df_1.reset_index()
# Se usa melt para que la tabla adquiera el formato largo
df1_long1 = df1_reset.melt(id_vars='index', var_name="País", value_name="Emisiones")
#df1_long1=df1_long1.sort_values(by='País', ascending=False)
#df1_long1
df_3=pd.read_csv('df_3.csv')
df_4=pd.read_csv('df_4.csv')


html_title="""
    <style>
        .title-test{
        font-weight:bold;
        padding:12 px;
        border-radius:6px;
        }
    </style>
    <center><h2 class="title-test"> Evolución anual de emisiones de CO2 en el mundo de 1973 - 2023 </h2></center>"""
st.markdown(html_title,unsafe_allow_html= True)


# Lista de organizaciones a eliminar
organizaciones = ["G8", "G20", "World", "OECD", "OECD Americas", "OECD Asia Oceania",
                  "Middle East", "European Union - 27", "G7", "Americas", "OECD Total", 
                  "Non-OECD Total", "OECD Europe", "Non-OECD Europe and Eurasia", 
                  "Asia (excl. China)", "Non-OECD Americas", "Africa"]

# Filtrar el DataFrame excluyendo organizaciones
df_filtrado = df1_long1[~df1_long1["País"].isin(organizaciones)].copy()

# Convertir "Emisiones" a numérico
df_filtrado["Emisiones"] = pd.to_numeric(df_filtrado["Emisiones"], errors="coerce")

# Graficar TODOS los países sin organizaciones
fig3 = px.line(df_filtrado, x="index", y="Emisiones", color="País",width= 1328, 
              height=720,
              title="Evolución de emisiones de CO₂ por país",
              labels={"Emisiones": " Millones Toneladas de CO₂", "index": "Año"},
              markers=False)
st.plotly_chart(fig3)


fig=px.scatter(df_pca, x='PC1',
               y='PC2', 
               color='Country', 
               hover_data='PC1', 
               text='Country', 
               width= 1328, 
               height=720)
fig.update_traces(textposition="bottom right", marker_line_width=3, marker_size=15)
fig.update_layout(
    title=dict(text='PCA'),
                  yaxis_zeroline=True,
                  xaxis_zeroline=True,
                  xaxis_title= 'Componente 1',
                  yaxis_title= 'Componente 2')
marker=dict(
        line_width=3
)

###### Gráfico de variación de emisiones en el tiempo ##### 
bins = [0, 50, 100, 200, 500, 1000, df1_long1["Emisiones"].max()]
labels = ["0-50", "50-100", "100-200", "200-500", "500-1000", "1000+"]

# Crear una nueva columna con categorías
df1_long1["Emisiones Grupo"] = pd.cut(df1_long1["Emisiones"], bins=bins, labels=labels)

# Asegurar que la columna "index" (Año) es numérica y ordenada
df1_long1["index"] = pd.to_numeric(df1_long1["index"], errors="coerce").astype(int)
df1_long1 = df1_long1.sort_values("index")  # Ordenar por año

# Crear el mapa con slider
fig2 = px.choropleth(df1_long1,
                    locations="País",
                    locationmode="country names",
                    color="Emisiones Grupo",  # Usa la columna categórica
                    title="Evolución de emisiones globales (million tonnes of CO2 eq)",
                    category_orders={"Emisiones Grupo": labels},  # Mantiene el orden
                    color_discrete_sequence=px.colors.qualitative.Set1,  # Paleta de colores
                    projection="natural earth",
                    animation_frame="index",
                    width= 1328, 
                    height=720)  # Agrega el slider

# Ajustar el slider para mejor visualización
fig2.update_layout(
    sliders=[{
        "currentvalue": {"prefix": "Año: "},  # Muestra el año seleccionado
        "pad": {"b": 10}  # Espaciado del slider
    }]
)

html_title="""
    <style>
        .title-test{
        font-weight:bold;
        padding:12 px;
        border-radius:6px;
        }
    </style>
    <center><h2 class="title-test"> Medidas de tendencia Central y dispersión de emisiones CO2 por sector 2022</h2></center>"""
st.markdown(html_title,unsafe_allow_html= True)

st.dataframe(df_estad)

col1, col2 = st.columns((0.5, 0.5))
with col1:
    st.plotly_chart(fig,theme="streamlit")
with col2:
        st.plotly_chart(fig2,theme="streamlit")

image2=Image.open('world.jpeg')
image3=Image.open('colomb.jpeg')
col1, col2= st.columns((0.5, 0.5))

with col1:
    st.image(image2, width=2000)
with col2:
     st.image(image3, width=2000)

# Asegurar que no haya valores nulos en 'Continent'
df_merged_cleaned = df_3[df_3['Continent'].notna()]

# Función para generar una espiral uniforme
def create_spiral(num_points, turns=4):
    theta = np.linspace(0, turns * 2 * np.pi, num_points)
    r = np.linspace(0.5, 3, num_points)  # Ajustar radio para mejor distribución
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

# Número de puntos
total_points = len(df_3)

# Generar coordenadas de la espiral
x_spiral, y_spiral = create_spiral(total_points)

# Agregar las coordenadas al DataFrame
df_3['x_spiral'] = x_spiral
df_3['y_spiral'] = y_spiral

# Crear el gráfico animado en espiral de los continentes
fig3= px.scatter(
    df_3,
    x='x_spiral',
    y='y_spiral',
    animation_frame="Year",
    animation_group="Country",
    size="kgCO2 per USD",
    color="Continent",
    hover_name="Country",
    facet_col="Continent",
    size_max=40,
    title="Evolución de la Intensidad de CO₂ por PIB a lo largo del tiempo (Espiral)",
)
# Personalizar el título de las facetas
fig3.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))

# Renombrar correctamente la columna de China
df_comparacion= df_4[["United States", "China (incl. Hong Kong, China)", "Colombia"]].reset_index()
df_comparacion.rename(columns={"index": "Year", "United States": "USA", "China (incl. Hong Kong, China)": "China","Colombia":"Colombia"}, inplace=True)

# Transformar a formato largo para mejor visualización
df_long2 = df_comparacion.melt(id_vars=["Year"], var_name="Country", value_name="kgCO2 per USD")

# Crear gráfico de líneas entre Colombia, USA y China
fig4= px.line(df_long2, x="Year", y="kgCO2 per USD", color="Country", markers=False,
              title="Comparación de la Intensidad de CO₂ por PIB: China vs. EE.UU. (1971-2022)",
              labels={"Year": "Año", "kgCO2 per USD": "kg CO₂ / USD"},
              line_shape="spline", color_discrete_map={"USA": "blue", "China": "red", "Colombia": "green"})


col1, col2 = st.columns((0.6,0.4))
with col1:
    st.plotly_chart(fig3,theme="streamlit")
with col2:
     st.plotly_chart(fig4,theme="streamlit")