# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import pickle
import time

# Configuración de la página
st.set_page_config(page_title="La Pastelería de Datos 🧁", page_icon="🍭", layout="centered")

# Inyección de CSS para transformar la app en una pastelería
st.markdown("""
<style>
    /* Fondo principal: Rosa pastel con un patrón sutil de puntos */
    .stApp {
        background-color: #FFE4E1; 
        background-image: radial-gradient(#FFB6C1 10%, transparent 11%), radial-gradient(#FFB6C1 10%, transparent 11%);
        background-size: 30px 30px;
        background-position: 0 0, 15px 15px;
    }
    
    /* Tipografía y colores de los textos (Marrón chocolate para contraste) */
    h1, h2, h3, p, label {
        color: #8B4513 !important; 
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif;
    }
    
    /* Estilizar el contenedor principal para que parezca una tarjeta de receta */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 3rem;
        border-radius: 25px;
        border: 4px dashed #FF69B4; /* Borde rosa fuerte */
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* Cajas de input numérico y slider (Celeste pastel) */
    div[data-baseweb="input"] > div, div.stSlider > div > div {
        background-color: #E0FFFF !important; 
        border: 2px solid #87CEFA !important; 
        border-radius: 15px;
    }

    /* Botón mágico para desenvolver el caramelo */
    div.stButton > button:first-child {
        background-color: #FFD700; /* Amarillo pastel / Dorado */
        color: #D2691E !important;
        font-size: 22px;
        font-weight: bold;
        border: 3px dashed #FF8C00;
        border-radius: 20px;
        padding: 10px 20px;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div.stButton > button:first-child:hover {
        background-color: #98FB98; /* Verde pastel al pasar el cursor */
        border: 3px dashed #2E8B57;
        transform: scale(1.08) rotate(-2deg);
    }

    /* Animación de los resultados */
    .resultado-favorable {
        padding: 25px; background-color: #E0FFFF; border: 4px solid #87CEFA;
        border-radius: 20px; text-align: center; font-size: 22px; color: #4682B4;
        animation: pop-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }
    
    .resultado-alerta {
        padding: 25px; background-color: #FFFACD; border: 4px solid #FF6347;
        border-radius: 20px; text-align: center; font-size: 22px; color: #B22222;
        animation: pop-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }

    @keyframes pop-in {
        0% { transform: scale(0.1) rotate(10deg); opacity: 0; }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def cargar_recursos():
    with open('modelo_diabetes_optimizado.pkl', 'rb') as file:
        modelo, variables, scaler = pickle.load(file)
    return modelo, variables, scaler

modelo, variables, scaler = cargar_recursos()

st.markdown("<h1 style='text-align: center;'>🧁 La Pastelería Predictiva 🍬</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>¡Bienvenido a nuestra dulce cocina de datos! Ingresa tus ingredientes clínicos para ver qué sorpresa te depara el futuro.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input('🍰 Número de Embarazos', min_value=0, max_value=20, value=0, step=1)
    glucose = st.number_input('🍭 Nivel de Glucosa', min_value=0.0, max_value=300.0, value=110.0, step=1.0)
    blood_pressure = st.number_input('🍓 Presión Arterial Diastólica', min_value=0.0, max_value=150.0, value=70.0, step=1.0)

with col2:
    bmi = st.number_input('🍩 Índice de Masa Corporal (BMI)', min_value=0.0, max_value=80.0, value=25.0, step=0.1)
    dpf = st.number_input('🍫 Función del Pedigrí', min_value=0.0, max_value=3.0, value=0.5, step=0.01)
    age = st.slider('🎂 Edad del catador (años)', min_value=1, max_value=120, value=30, step=1)

st.markdown("<br>", unsafe_allow_html=True)

if st.button('¡Abrir el envoltorio sorpresa! 🍬', use_container_width=True):
    
    espacio_animacion = st.empty()
    
    # Animación de desenvolver
    espacio_animacion.markdown("<h2 style='text-align: center;'>Desenvolviendo... 🍬</h2>", unsafe_allow_html=True)
    time.sleep(0.7)
    espacio_animacion.markdown("<h2 style='text-align: center;'>Quitando el papel... 📜</h2>", unsafe_allow_html=True)
    time.sleep(0.7)
    espacio_animacion.markdown("<h2 style='text-align: center;'>¡Casi listo! ✨</h2>", unsafe_allow_html=True)
    time.sleep(0.7)
    espacio_animacion.empty() 

    # Predicción
    datos_crudos = [[pregnancies, glucose, blood_pressure, bmi, dpf, age]]
    df_crudo = pd.DataFrame(datos_crudos, columns=variables)
    df_normalizado = pd.DataFrame(scaler.transform(df_crudo), columns=variables)
    prediccion = modelo.predict(df_normalizado)[0]
    
    if prediccion == 1:
        st.markdown("""
        <div class='resultado-alerta'>
            <h3>¡Muchos dulces para ti hoy! 🍭⚠️</h3>
            <p>El modelo indica un riesgo alto. Deberías regular un poco tu consumo de dulces para cuidar esa salud y visitar a tu médico para un chequeo de rutina.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown("""
        <div class='resultado-favorable'>
            <h3>¡Felicidades! 🎉🧁</h3>
            <p>Tu salud está excelente y no se detectan riesgos. ¡Aquí tienes tu cupcake virtual de premio por cuidarte tan bien!</p>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("🔍 Ver la receta técnica interna"):
        st.write("Datos ingresados a la batidora (normalizados):")
        st.dataframe(df_normalizado)
        st.info(f"Chef algorítmico: {type(modelo).__name__}")