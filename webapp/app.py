from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image  # Para el logo

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Alquileres - Granada",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar recursos (modelo y columnas)
@st.cache_resource
def load_resources():
    # Cargar modelo Ridge
    with open('.\\resources\modelo_ridge.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Cargar columnas esperadas por el modelo
    encoded_columns = np.load('.\\resources\encoded_columns.npy', allow_pickle=True)
    
    return model, encoded_columns


model, encoded_columns = load_resources()

# Después de cargar el modelo en tu app.py
# Después de cargar el modelo y encoded_columns
st.sidebar.header("Debug Info")
st.sidebar.write("Número de coeficientes:", len(model.coef_))
st.sidebar.write("Número de columnas esperadas:", len(encoded_columns))
st.sidebar.write("Primeras 5 columnas:", encoded_columns[:20])

# Logo y cabecera
col1, col2 = st.columns([1, 4])
with col1:
    st.image(Image.open('.\modelo_predictivo_alquiler\logo.png') if Path('.\modelo_predictivo_alquiler\logo.png').exists() else Image.new('RGB', (100, 100), color='grey'), width=100)
with col2:
    st.title("📊 Predictor de Precios de Alquiler")
    st.caption("Predice el valor de alquiler en Granada basado en las características de la propiedad")

# Sidebar con información
with st.sidebar:
    st.header("⚙️ Configuración")
    st.markdown("""
    **Variables consideradas:**
    - Características principales (metros, habitaciones...)
    - Servicios (ascensor, garaje...)
    - Ubicación y planta
    """)
    
    st.divider()
    st.markdown("**Tipo de modelo:** Ridge Regression")
    st.markdown(f"**Número de características:** {len(encoded_columns)}")
    
    if st.checkbox("Mostrar columnas esperadas"):
        st.write(encoded_columns)

# Formulario principal
with st.form("prediction_form"):
    st.subheader("📝 Datos de la Propiedad")
    
    # Organización en columnas
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 1. Información básica
        metros_reales = st.slider("Metros cuadrados", 20, 200, 65, 5)
        habitaciones = st.selectbox("Habitaciones", [1, 2, 3, 4, 5])
        banos = st.selectbox("Baños", [1, 2, 3])
        
        # 2. Localización
        localizacion = st.selectbox(
            "Zona de Granada",
            ["Recogidas", "Centro", "Zaidín", "Albaicín", "Chana", "Otro"]
        )
        
    with col_right:
        # 3. Características de la propiedad
        piso = st.radio(
            "Planta",
            ["Bajo", "Primeros_pisos", "Intermedios", "Áticos"],
            horizontal=True
        )
        
        # 4. Servicios (organizados en dos columnas)
        st.markdown("**Servicios incluidos:**")
        serv_col1, serv_col2 = st.columns(2)
        
        with serv_col1:
            ascensor = st.checkbox("Ascensor", value=True)
            garaje = st.checkbox("Garaje")
            calefaccion = st.checkbox("Calefacción")
            
        with serv_col2:
            aire_acondicionado = st.checkbox("Aire acondicionado")
            terraza = st.checkbox("Terraza")
            armarios_empotrados = st.checkbox("Armarios empotrados")
        
        # 5. Otros servicios
        trastero = st.checkbox("Trastero incluido")
        piscina = st.checkbox("Piscina comunitaria")
        zonas_verdes = st.checkbox("Zonas verdes")
    
    # Botón de submit
    submitted = st.form_submit_button("Calcular Precio de Alquiler")

# Procesamiento después del submit
if submitted:
    try:
        # 1. Crear DataFrame con los datos del formulario
        input_data = {
            'metros_reales': metros_reales,
            'habitaciones': habitaciones,
            'baños': banos,
            'ascensor': int(ascensor),
            'garaje': int(garaje),
            'calefaccion': int(calefaccion),
            'aire_acondicionado': int(aire_acondicionado),
            'terraza': int(terraza),
            'armarios_empotrados': int(armarios_empotrados),
            'trastero': int(trastero),
            'piscina': int(piscina),
            'zonas_verdes': int(zonas_verdes),
            'localizacion': localizacion,
            'piso': piso
        }
        
        input_df = pd.DataFrame([input_data])
        
        # 2. Aplicar one-hot encoding como en el entrenamiento
        input_encoded = pd.get_dummies(input_df, dtype='int', columns=["localizacion", "piso"])
        
        # 3. Asegurar que tenemos todas las columnas esperadas
        missing_cols = [col for col in encoded_columns if col not in input_encoded.columns and col != 'titulo' and col != 'precio']
        for col in missing_cols:
            if col != 'precio':  # Excluir la variable objetivo si está en las columnas
                input_encoded[col] = 0
        
        # 4. Ordenar columnas como el modelo espera
        input_encoded = input_encoded.reindex(columns=[col for col in encoded_columns if col != 'titulo' and col != 'precio'], fill_value=0)
        
        # 5. Realizar predicción
        prediction = model.predict(input_encoded)
        
        # 6. Mostrar resultados
        st.success("### Resultado de la Predicción")
        
        # Mostrar el precio estimado con estilo
        st.metric(
            label="**Precio estimado de alquiler mensual**",
            value=f"{prediction[0]:.2f} €",
            delta="Competitivo" if prediction[0] < 600 else "Alto para el mercado"
        )
        
        # Sección de análisis expandible
        with st.expander("🔍 Detalles técnicos de la predicción"):
            st.write("**Características utilizadas:**")
            st.dataframe(input_encoded.T.rename(columns={0: 'Valor'}))
            
            if hasattr(model, 'coef_'):
                st.write("**Coeficientes más relevantes:**")
                coef_df = pd.DataFrame({
                    'Variable': input_encoded.columns,
                    'Coeficiente': model.coef_
                }).sort_values('Coeficiente', key=abs, ascending=False).head(20)
                
                st.bar_chart(coef_df.set_index('Variable'))
                
                st.write("""
                **Interpretación:**
                - Coeficientes positivos aumentan el precio estimado
                - Coeficientes negativos disminuyen el precio estimado
                """)
    
    except Exception as e:
        st.error(f"❌ Error al realizar la predicción: {str(e)}")
        st.error("Por favor verifica que todos los datos estén correctamente ingresados")

# Pie de página
st.divider()
st.markdown("""
**Instrucciones:**
1. Completa todos los campos del formulario
2. Haz clic en 'Calcular Precio de Alquiler'
3. Revisa el resultado y los detalles técnicos
""")
st.caption("© 2023 Predictor de Alquileres - Modelo Ridge Regression")