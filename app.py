# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="App Diabetes", layout="centered")

@st.cache_resource
def cargar_recursos():
    with open('modelo_diabetes_optimizado.pkl', 'rb') as file:
        modelo, variables, scaler = pickle.load(file)
    return modelo, variables, scaler

modelo, variables, scaler = cargar_recursos()

st.title('🩺 Diagnóstico Preventivo de Diabetes')
st.markdown("Por favor, ingrese los valores clínicos del paciente para predecir el riesgo.")

st.header("Datos del Paciente")
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input('Número de Embarazos', min_value=0, max_value=20, value=0, step=1)
    glucose = st.number_input('Nivel de Glucosa', min_value=0.0, max_value=300.0, value=110.0, step=1.0)
    blood_pressure = st.number_input('Presión Arterial Diastólica', min_value=0.0, max_value=150.0, value=70.0, step=1.0)

with col2:
    bmi = st.number_input('Índice de Masa Corporal (BMI)', min_value=0.0, max_value=80.0, value=25.0, step=0.1)
    dpf = st.number_input('Función del Pedigrí', min_value=0.0, max_value=3.0, value=0.5, step=0.01)
    age = st.slider('Edad (años)', min_value=1, max_value=120, value=30, step=1)

st.markdown("---")

if st.button('Generar Predicción', use_container_width=True):
    with st.spinner("Procesando datos..."):
        datos_crudos = [[pregnancies, glucose, blood_pressure, bmi, dpf, age]]
        df_crudo = pd.DataFrame(datos_crudos, columns=variables)
        df_normalizado = pd.DataFrame(scaler.transform(df_crudo), columns=variables)
        
        prediccion = modelo.predict(df_normalizado)[0]
        
        st.header("Resultado:")
        if prediccion == 1:
            st.error("⚠️ ALTO RIESGO: El paciente presenta indicadores de Diabetes.")
        else:
            st.success("✅ RIESGO BAJO: No se detectan indicadores clínicos de Diabetes.")
            
        with st.expander("Ver validación de datos internos"):
            st.write("Datos procesados:")
            st.dataframe(df_normalizado)
            st.info(f"Modelo en uso: {type(modelo).__name__}")