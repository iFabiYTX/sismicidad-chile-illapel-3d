import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Configuración de página
st.set_page_config(
    page_title="Sismicidad en Chile - Illapel 2015",
    page_icon="🌋",
    layout="wide"
)

# Constantes de consulta USGS
USGS_API_URL = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    "&starttime=2015-09-15"
    "&endtime=2015-10-15"
    "&minmagnitude=3.0"
    "&minlatitude=-35.0"
    "&maxlatitude=-28.0"
    "&minlongitude=-74.0"
    "&maxlongitude=-69.0"
)
CSV_FILENAME = "illapel_2015_usgs.csv"

@st.cache_data
def cargar_y_procesar_datos():
    if not os.path.exists(CSV_FILENAME):
        df_raw = pd.read_csv(USGS_API_URL)
        df_raw.to_csv(CSV_FILENAME, index=False)
    else:
        df_raw = pd.read_csv(CSV_FILENAME)
        
    df = df_raw.copy()
    df['datetime'] = pd.to_datetime(df['time'])
    cols = ['datetime', 'latitude', 'longitude', 'depth', 'mag', 'place']
    df = df[cols].dropna().drop_duplicates().sort_values('datetime').reset_index(drop=True)
    
    # DBSCAN espacial 3D
    X_coords = df[['latitude', 'longitude', 'depth']].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_coords)
    
    db = DBSCAN(eps=0.45, min_samples=8)
    df['cluster'] = db.fit_predict(X_scaled)
    df['categoria'] = df['cluster'].apply(
        lambda c: 'Sismicidad de fondo / Ruido' if c == -1 else f'Secuencia de réplicas (Cluster {c})'
    )
    return df

df = cargar_y_procesar_datos()

# Encabezado principal
st.title("🌋 Visualización Espaciotemporal de Sismicidad en Chile")
st.markdown(
    "**Asignatura:** EIN092B Visualización de Datos — **Caso de Estudio:** Terremoto de Illapel 2015 ($M_w\\ 8.3$)  \n"
    "*Plataforma interactiva para el análisis 3D de hipocentros y segmentación de réplicas con DBSCAN.*"
)

# Barra lateral con controles
st.sidebar.header("🎛️ Filtros Interactivos")

min_mag, max_mag = st.sidebar.slider(
    "Rango de Magnitud ($M_w$)",
    min_value=float(df['mag'].min()),
    max_value=float(df['mag'].max()),
    value=(3.0, float(df['mag'].max())),
    step=0.1
)

min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()
rango_fechas = st.sidebar.date_input(
    "Ventana temporal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categorias_disp = df['categoria'].unique().tolist()
cat_seleccionadas = st.sidebar.multiselect(
    "Filtrar por grupo sismológico",
    options=categorias_disp,
    default=categorias_disp
)

# Aplicar filtros
if len(rango_fechas) == 2:
    f_inicio, f_fin = rango_fechas
    mask_fecha = (df['datetime'].dt.date >= f_inicio) & (df['datetime'].dt.date <= f_fin)
else:
    mask_fecha = True

mask_mag = (df['mag'] >= min_mag) & (df['mag'] <= max_mag)
mask_cat = df['categoria'].isin(cat_seleccionadas)

df_filtrado = df[mask_fecha & mask_mag & mask_cat].copy()

# Métricas resumen (KPIs)
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Eventos Mostrados", f"{len(df_filtrado)} de {len(df)}")
if len(df_filtrado) > 0:
    c2.metric("Magnitud Máxima", f"Mw {df_filtrado['mag'].max():.1f}")
    c3.metric("Profundidad Media", f"{df_filtrado['depth'].mean():.1f} km")
    sismos_falla = len(df_filtrado[df_filtrado['cluster'] != -1])
    pct_falla = (sismos_falla / len(df_filtrado)) * 100
    c4.metric("% en Falla Activa", f"{pct_falla:.1f} %")
else:
    c2.metric("Magnitud Máxima", "N/A")
    c3.metric("Profundidad Media", "N/A")
    c4.metric("% en Falla Activa", "N/A")

st.markdown("---")

if len(df_filtrado) == 0:
    st.warning("No hay eventos que coincidan con los filtros seleccionados.")
else:
    # Pestañas de visualización
    tab1, tab2, tab3 = st.tabs([
        "🗺️ Mapa Geoespacial 2D", 
        "🌐 Perfil 3D de Subducción", 
        "📈 Evolución Temporal de Réplicas"
    ])
    
    with tab1:
        st.subheader("Distribución Epicentral sobre Mapa Satelital / OpenStreetMap")
        st.caption("Responde a la sugerencia del docente de incorporar mapas dinámicos interactivos.")
        
        fig_map = px.scatter_map(
            df_filtrado,
            lat="latitude",
            lon="longitude",
            color="depth",
            size="mag",
            size_max=16,
            color_continuous_scale="Viridis_r",
            hover_name="place",
            hover_data={"latitude": ":.2f", "longitude": ":.2f", "depth": ":.1f km", "mag": True, "categoria": True},
            zoom=5.5,
            center={"lat": -31.57, "lon": -71.65},
            map_style="open-street-map"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550)
        st.plotly_chart(fig_map, width="stretch")
        
    with tab2:
        st.subheader("Perfil Hipocentral 3D: Subducción de la Placa de Nazca")
        st.caption("Permite rotar 360° con el mouse para visualizar la profundización de los sismos hacia el Este.")
        
        fig_3d = px.scatter_3d(
            df_filtrado,
            x="longitude",
            y="latitude",
            z=-df_filtrado['depth'],
            color="depth",
            size="mag",
            size_max=12,
            color_continuous_scale="Inferno",
            hover_name="place",
            hover_data={"depth": ":.1f km", "mag": True, "categoria": True},
            labels={"z": "Cota (km)", "longitude": "Longitud (°O)", "latitude": "Latitud (°S)"}
        )
        fig_3d.update_layout(height=600, scene=dict(
            xaxis_title="Longitud (°O)",
            yaxis_title="Latitud (°S)",
            zaxis_title="Profundidad (-km)"
        ))
        st.plotly_chart(fig_3d, width="stretch")
        
    with tab3:
        st.subheader("Secuencia Temporal y Decaimiento de Réplicas (Ley de Omori)")
        st.caption("Visualización de la energía liberada a lo largo del mes posterior al sismo principal.")
        
        fig_time = px.scatter(
            df_filtrado,
            x="datetime",
            y="mag",
            color="depth",
            size="mag",
            color_continuous_scale="Viridis_r",
            hover_name="place",
            labels={"datetime": "Fecha y Hora (UTC)", "mag": "Magnitud (Mw)", "depth": "Profundidad (km)"}
        )
        fig_time.update_layout(height=450)
        st.plotly_chart(fig_time, width="stretch")
