import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="GamerVault Analytics", layout="wide", page_icon="📊")

st.title("📊 GamerVault: Dashboard de Análisis Visual")
st.markdown("---")

# URL del servicio dentro de la red de Docker (usa el nombre del servicio del backend)
API_URL = "http://api-juegos:8080/api/games"

try:
    # Consumo de la API REST
    response = requests.get(API_URL, timeout=5)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        if not df.empty:
            # Métricas Principales
            m1, m2, m3 = st.columns(3)
            m1.metric("Juegos Registrados", len(df))
            m2.metric("Rating Promedio", f"{df['rating'].mean():.1f} ⭐")
            m3.metric("Plataforma Principal", df['platform'].value_counts().idxmax())

            st.markdown("### Visualización de Datos")
            col_a, col_b = st.columns(2)

            with col_a:
                st.write("**Distribución por Plataforma**")
                fig_pie = px.pie(df, names='platform', hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_b:
                st.write("**Calificación por Género**")
                fig_bar = px.bar(df, x='genre', y='rating', color='platform', barmode='group')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Tabla de datos crudos para auditoría
            with st.expander("Ver tabla completa de datos"):
                st.dataframe(df[['id', 'title', 'platform', 'genre', 'rating']])
        else:
            st.info("Aún no hay juegos registrados en la base de datos.")
    else:
        st.error(f"Error al conectar con la API (Código: {response.status_code})")

except Exception as e:
  st.error("Esperando conexión con el Backend... Asegúrate de que el servicio 'api-juegos' esté arriba.")