import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | Premium POS", layout="wide", page_icon="🍊")

# --- DISEÑO CORREGIDO Y VISIBLE ---
st.markdown("""
    <style>
    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #CFD8DC 0%, #ECEFF1 100%);
    }

    /* Cuadros de contenido (Glassmorphism corregido) */
    .main-container {
        background-color: rgba(255, 255, 255, 0.95); /* Casi blanco sólido para ver bien */
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #FF4500;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: #1B5E20;
    }

    /* FUERZA EL COLOR DE LAS LETRAS PARA QUE SE VEAN */
    label, p, span, h1, h2, h3, .stMarkdown {
        color: #1B5E20 !important; /* Verde oscuro para todo el texto */
        font-weight: 700 !important;
    }

    /* Ajuste para los campos de entrada (Inputs) */
    input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #FF4500 !important;
    }

    /* BOTONES JR 31 */
    .stButton>button {
        background: linear-gradient(135deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        height: 3.5em !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 69, 0, 0.3) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #1B5E20 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN LOGO ---
def cargar_logo():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=250)
    else:
        st.markdown("<h1 style='text-align: center; color: #FF4500;'>🍊 JR 31 SHOP</h1>", unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "USD_Unit", "MXN_Total", "Precio_Vta"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Monto", "Metodo"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"Nombre": "Venta de Mostrador", "Deuda": 0.0}])

# --- SISTEMA DE LOGIN ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        cargar_logo()
        st.markdown("<h3 style='text-align: center;'>TERMINAL PRIVADA</h3>", unsafe_allow_html=True)
        
        user_input = st.text_input("ID de Administrador")
        pass_input = st.text_input("Clave de Acceso", type="password")
        
        if st.button("ACCEDER AL SISTEMA"):
            if user_input == "admin_jr31" and pass_input == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MENÚ PRINCIPAL ---
    with st.sidebar:
        cargar_logo()
        st.markdown("---")
        nav = st.radio("MÓDULOS", ["📊 Dashboard", "📦 Logística Importación", "💸 Terminal Ventas", "👥 Cartera Clientes", "📂 Reportes"])
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- SECCIONES ---
    if nav == "📊 Dashboard":
        st.markdown("<h1>📊 Resumen de Operaciones</h1>", unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("VENTAS", f"${st.session_state.ven['Monto'].sum():,.2f}")
        c2.metric("STOCK (USD)", f"${st.session_state.inv['USD_Unit'].sum():,.2f}")
        c3.metric("DEUDA CLIENTES", f"${st.session_state.cli['Deuda'].sum():,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "📦 Logística Importación":
        st.markdown("<h1>📦 Gestión de Importación</h1>", unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        with st.form("inv"):
            p = st.text_input("Producto")
            q = st.number_input("Cantidad", min_value=1)
            u = st.number_input("Costo Unitario USD")
            t = st.number_input("Tasa Cambio", value=18.5)
            v = st.number_input("Precio Venta MXN")
            if st.form_submit_button("REGISTRAR ENTRADA"):
                nueva = pd.DataFrame([{"Producto": p, "Stock": q, "USD_Unit": u, "MXN_Total": q*u*t, "Precio_Vta": v}])
                st.session_state.inv = pd.concat([st.session_state.inv, nueva], ignore_index=True)
                st.success("Guardado")
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.inv)

    elif nav == "💸 Terminal Ventas":
        st.markdown("<h1>💸 Nueva Venta</h1>", unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        cli = st.selectbox("Cliente", st.session_state.cli['Nombre'])
        monto = st.number_input("Monto MXN")
        metodo = st.selectbox("Método", ["Contado", "Crédito"])
        if st.button("FINALIZAR VENTA"):
            nv = pd.DataFrame([{"Fecha": datetime.now(), "Cliente": cli, "Monto": monto, "Metodo": metodo}])
            st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
            if metodo == "Crédito":
                st.session_state.cli.loc[st.session_state.cli['Nombre'] == cli, 'Deuda'] += monto
            st.success("Venta Exitosa")
        st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "👥 Cartera Clientes":
        st.markdown("<h1>👥 Cartera de Clientes</h1>", unsafe_allow_html=True)
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        nc = st.text_input("Nombre de Cliente")
        if st.button("Añadir Cliente"):
            st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"Nombre": nc, "Deuda": 0.0}])], ignore_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.cli)

    elif nav == "📂 Reportes":
        st.markdown("<h1>📂 Centro de Reportes</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='Ventas')
        st.download_button("📥 DESCARGAR EXCEL DE VENTAS", buf.getvalue(), "JR31_Reporte.xlsx")
