import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP - Punto de Venta", layout="wide", page_icon="🍊")

# --- DISEÑO PROFESIONAL (CSS CUSTOM) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f4f7f6;
    }
    
    /* Títulos en Verde */
    h1, h2, h3 {
        color: #1a5e20 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }

    /* Estilo para los labels (etiquetas) que no se veían */
    label {
        color: #333333 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* Botones Naranja */
    .stButton>button {
        background: linear-gradient(135deg, #FF8C00 0%, #e67e00 100%);
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2E8B57 0%, #1a5e20 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Cuadros de métricas */
    [data-testid="stMetricValue"] {
        color: #FF8C00 !important;
    }

    /* Sidebar verde */
    [data-testid="stSidebar"] {
        background-color: #1a5e20;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Tarjetas de login */
    .login-box {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 5px solid #FF8C00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "Costo USD", "Inversión MXN", "Precio Venta"])
if 'ven' not in st.session_state:
    st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Total", "Tipo", "Estatus"])
if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame([{"Nombre": "Público General", "Deuda": 0.0}])

# --- SISTEMA DE ACCESO ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False

if not st.session_state.ingresado:
    empty1, col_login, empty2 = st.columns([1, 2, 1])
    
    with col_login:
        st.markdown('<div cla
