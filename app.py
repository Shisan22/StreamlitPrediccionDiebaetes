# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import pickle
import time

# 1. Configuración de la página (layout ancho para el mostrador)
st.set_page_config(page_title="Pastelería Predictiva 🧁", page_icon="🍬", layout="centered")

# 2. Magia CSS para transformar Streamlit en una Pastelería
st.markdown("""
<style>
    /* Fondo general de la tienda: Rosa pastel con textura */
    .stApp {
        background-color: #FFF0F5;
        background-image: radial-gradient(#FFC0CB 15%, transparent 16%), radial-gradient(#FFC0CB 15%, transparent 16%);
        background-size: 40px 40px;
        background-position: 0 0, 20px 20px;
    }
    
    /* Tipografía amigable */
    h1, h2, h3, p, label {
        color: #5C3A21 !important; 
        font-family: 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif;
        font-weight: bold;
    }

    /* Contenedor principal (El cristal del mostrador) */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        border: 8px solid #FFB6C1;
        padding: 2rem;
        box-shadow: 0 20px 30px rgba(0,0,0,0.15);
        margin-top: 1rem;
    }

    /* Cobertura de los cupcakes (Emojis gigantes flotantes) */
    .cupcake-top {
        font-size: 65px;
        text-align: center;
        margin-bottom: -35px;
        z-index: 10;
        position: relative;
        text-shadow: 2px 5px 5px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .cupcake-top:hover {
        transform: scale(1.2) rotate(5deg);
    }

    /* Pirotines (Bases de los cupcakes) aplicados a los inputs nativos */
    div[data-baseweb="input"] > div, div.stSlider > div > div {
        border-radius: 5px 5px 30px 30px !important; 
        border: 3px solid #8B4513 !important;
        box-shadow: inset 0 -5px 10px rgba(0,0,0,0.1);
        padding-top: 10px;
    }

    /* Fondo blanco dentro del campo numérico para que el usuario vea qué escribe */
    input {
        background-color: rgba(255,255,255,0.9) !important;
        border-radius: 10px !important;
        text-align: center;
    }

    /* COLORES DE LOS CUPCAKES (Patrones de rayas para los pirotines) */
    /* Columna 1: Pirotín Rosa Fresa */
    div[data-testid="column"]:nth-of-type(1) div[data-baseweb="input"] > div {
        background: repeating-linear-gradient(to right, #FFB6C1, #FFB6C1 10px, #FF69B4 10px, #FF69B4 20px) !important;
    }
    /* Columna 2: Pirotín Celeste Chicle */
    div[data-testid="column"]:nth-of-type(2) div[data-baseweb="input"] > div {
        background: repeating-linear-gradient(to right, #E0FFFF, #E0FFFF 10px, #87CEFA 10px, #87CEFA 20px) !important;
    }
    /* Columna 3: Pirotín Verde Menta */
    div[data-testid="column"]:nth-of-type(3) div[data-baseweb="input"] > div,
    div[data-testid="column"]:nth-of-type(3) div.stSlider > div > div {
        background: repeating-linear-gradient(to right, #98FB98, #98FB98 10px, #3CB371 10px, #3CB371 20px) !important;
    }

    /* Estantes de madera del mostrador */
    .shelf {
        height: 20px;
        background: linear-gradient(to bottom, #DEB887, #8B4513);
        border-radius: 10px;
        box-shadow: 0 8px 10px rgba(0,0,0,0.3);
        margin-top: 15px;
        margin-bottom: 30px;
        position: relative;
        z-index: 5;
    }

    /* Botón mágico de desenvolver */
    div.stButton > button:first-child {
        background: linear-gradient(to right, #FF69B4, #FFA07A);
        color: white !important;
        font-size: 26px;
        border-radius: 50px;
        border: 4px dashed white;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
        height: 60px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-5px);
        background: linear-gradient(to right, #FFA07A, #FF69B4);
        box-shadow: 0 15px 20px rgba(0,0,0,0.4);
    }

    /* Cajas de Resultados */
    .alerta {
        background-color: #FFF0F5; border: 5px solid #FF4500; padding: 25px; border-radius: 20px; text-align: center;
        animation: pop-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }
    .favorable {
        background-color: #F0FFFF; border: 5px solid #00CED1; padding: 25px; border-radius: 20px; text-align: center;
        animation: pop-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    }
    @keyframes pop-in {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# 3. Cargar Recursos
@st.cache_resource
def cargar_recursos():
    with open('modelo_diabetes_optimizado.pkl', 'rb') as file:
        modelo, variables, scaler = pickle.load(file)
    return modelo, variables, scaler

modelo, variables, scaler = cargar_recursos()

# 4. Título
st.markdown("<h1 style='text-align: center; font-size: 45px;'>🏪 El Mostrador de la Salud 🧁</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>Escoge los ingredientes clínicos de los estantes y descubre tu resultado.</p>", unsafe_allow_html=True)

# ---- FILA 1 DEL MOSTRADOR ----
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="cupcake-top">🍓</div>', unsafe_allow_html=True)
    pregnancies = st.number_input('Embarazos', min_value=0, max_value=20, value=0, step=1)
with col2:
    st.markdown('<div class="cupcake-top">🫐</div>', unsafe_allow_html=True)
    glucose = st.number_input('Glucosa', min_value=0.0, max_value=300.0, value=110.0, step=1.0)
with col3:
    st.markdown('<div class="cupcake-top">🍏</div>', unsafe_allow_html=True)
    blood_pressure = st.number_input('Presión Arterial', min_value=0.0, max_value=150.0, value=70.0, step=1.0)

# Estante de madera 1
st.markdown('<div class="shelf"></div>', unsafe_allow_html=True)

# ---- FILA 2 DEL MOSTRADOR ----
col4, col5, col6 = st.columns(3)
with col4:
    # Este hereda el color Rosa de la columna 1
    st.markdown('<div class="cupcake-top">🍋</div>', unsafe_allow_html=True)
    bmi = st.number_input('IMC (BMI)', min_value=0.0, max_value=80.0, value=25.0, step=0.1)
with col5:
    # Este hereda el color Celeste de la columna 2
    st.markdown('<div class="cupcake-top">🍇</div>', unsafe_allow_html=True)
    dpf = st.number_input('Pedigrí', min_value=0.0, max_value=3.0, value=0.5, step=0.01)
with col6:
    # Este hereda el color Menta de la columna 3
    st.markdown('<div class="cupcake-top">🍒</div>', unsafe_allow_html=True)
    age = st.slider('Edad', min_value=1, max_value=120, value=30, step=1)

# Estante de madera 2
st.markdown('<div class="shelf"></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 5. Botón y Predicción
if st.button('🍬 Desenvolver el Resultado 🍬', use_container_width=True):
    
    # Animación de desenvolver el caramelo
    espacio = st.empty()
    espacio.markdown("<h2 style='text-align: center;'>Desenvolviendo el papel... 📜</h2>", unsafe_allow_html=True)
    time.sleep(0.8)
    espacio.markdown("<h2 style='text-align: center;'>Analizando la receta... 🥣</h2>", unsafe_allow_html=True)
    time.sleep(0.8)
    espacio.empty() 

    # Predicción
    datos_crudos = [[pregnancies, glucose, blood_pressure, bmi, dpf, age]]
    df_crudo = pd.DataFrame(datos_crudos, columns=variables)
    df_normalizado = pd.DataFrame(scaler.transform(df_crudo), columns=variables)
    prediccion = modelo.predict(df_normalizado)[0]
    
    # Lógica corregida
    if prediccion == 1:
        st.markdown("""
        <div class='alerta'>
            <h2 style='color:#B22222 !important;'>⚠️ ¡Es momento de cuidarse! 🩺</h2>
            <p style='font-size:18px;'>El modelo indica riesgo de Diabetes. <b>¡Hoy nada de dulces para ti!</b> Te recomendamos mejorar tu alimentación, hacer ejercicio y visitar a tu médico pronto.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown("""
        <div class='favorable'>
            <h2 style='color:#008B8B !important;'>✅ ¡Todo excelente! 🍬🍭🧁</h2>
            <p style='font-size:18px;'>¡Felicidades! Tus indicadores son muy buenos y no se detecta riesgo. <b>¡Te mereces disfrutar de un delicioso postre hoy!</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("🔍 Ver los ingredientes técnicos"):
        st.write("Datos ingresados a la batidora (normalizados):")
        st.dataframe(df_normalizado)
        st.info(f"Chef algorítmico en uso: {type(modelo).__name__}")