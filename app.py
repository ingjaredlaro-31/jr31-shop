import streamlit as st
import pandas as pd

# Configuración básica para evitar errores de arranque
st.set_page_config(page_title="JR 31 SHOP", layout="wide")

# Estilo visual
st.markdown("<style>h1{color: #2E8B57;} .stButton>button{background-color: #FF8C00; color:white;}</style>", unsafe_allow_html=True)

# Login simple
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🍊 JR 31 SHOP - ACCESO")
    user = st.text_input("Usuario")
    pas = st.text_input("Contraseña", type="password")
    if st.button("ENTRAR"):
        if user == "admin_jr31" and pas == "JR31_2024_Chiapas":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
else:
    st.title("✅ ¡JR 31 SHOP EN LÍNEA!")
    st.sidebar.success("Bienvenido")
    
    opcion = st.sidebar.radio("Menu", ["Inicio", "Inventario", "Ventas"])
    
    if opcion == "Inicio":
        st.write("Bienvenido Administrador. El sistema está funcionando correctamente.")
        st.metric("Estado del Sistema", "Activo")
    
    if st.sidebar.button("Salir"):
        st.session_state.auth = False
        st.rerun()
