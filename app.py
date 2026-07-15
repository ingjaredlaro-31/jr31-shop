import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN ESTRUCTURAL ---
st.set_page_config(page_title="JR 31 SHOP | ERP SYSTEM", layout="wide", page_icon="💼")

# --- DISEÑO DE VANGUARDIA (CSS DE ALTO NIVEL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;800;900&display=swap');

    /* Fondo con Imagen Profesional de Negocios/USA */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-attachment: fixed;
    }

    /* Tipografía General */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF !important;
    }

    /* Títulos Impactantes */
    h1, h2, .title-font {
        font-family: 'Bebas Neue', cursive !important;
        letter-spacing: 3px;
        color: #FF4500 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }

    /* Tarjetas de Contenido Modernas */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }

    /* Inputs Estilizados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: rgba(255,255,255,0.9) !important;
        color: #1B5E20 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border: 2px solid #FF4500 !important;
    }

    /* BOTONES DE ALTO IMPACTO */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important;
        font-family: 'Bebas Neue' !important;
        font-size: 1.5rem !important;
        letter-spacing: 2px;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 40px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 20px rgba(255, 69, 0, 0.4) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(46, 139, 87, 0.6) !important;
        background: linear-gradient(90deg, #2E8B57, #1B5E20) !important;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #FF8C00 !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
    }

    /* Sidebar Premium */
    [data-testid="stSidebar"] {
        background: rgba(13, 46, 17, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 5px solid #FF4500;
    }
    
    label {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["PRODUCTO", "STOCK", "USD_UNIT", "MXN_TOTAL", "PRECIO_VTA"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO", "METODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "PÚBLICO GENERAL", "DEUDA": 0.0}])

# --- SISTEMA DE ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    col1, col_login, col2 = st.columns([0.5, 1, 0.5])
    with col_login:
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        if os.path.exists("logo.png"):
            st.image("logo.png", width=350)
        else:
            st.markdown("<h1 style='font-size: 4rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: white !important;'>BUSINESS TERMINAL v2.0</h3>", unsafe_allow_html=True)
        
        id_user = st.text_input("ADMIN ID")
        pw_user = st.text_input("ACCESS KEY", type="password")
        
        if st.button("DESBLOQUEAR TERMINAL"):
            if id_user == "admin_jr31" and pw_user == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else:
                st.error("ACCESO DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MENÚ DE NAVEGACIÓN ---
    with st.sidebar:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_column_width=True)
        st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>MASTER MENU</h1>", unsafe_allow_html=True)
        st.markdown("---")
        nav = st.radio("MÓDULOS DE CONTROL", ["📊 DASHBOARD", "📦 LOGÍSTICA USA", "💸 TERMINAL POS", "👥 CARTERA", "📂 REPORTES"])
        st.markdown("---")
        if st.button("LOGOUT"):
            st.session_state.log = False
            st.rerun()

    # --- PANEL DE CONTROL ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-size: 3.5rem;'>INTELIGENCIA DE NEGOCIO</h1>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("FLUJO DE CAJA", f"${st.session_state.ven['MONTO'].sum():,.2f}")
        c2.metric("CAPITAL STOCK", f"${st.session_state.inv['USD_UNIT'].sum():,.2f} USD")
        c3.metric("CUENTAS POR COBRAR", f"${st.session_state.cli['DEUDA'].sum():,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🚨 ALERTAS DE CRÉDITO PENDIENTE")
        st.dataframe(st.session_state.cli[st.session_state.cli['DEUDA'] > 0], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LOGÍSTICA USA ---
    elif nav == "📦 LOGÍSTICA USA":
        st.markdown("<h1 style='font-size: 3.5rem;'>LOGÍSTICA INTERNACIONAL</h1>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("inv"):
            col_a, col_b = st.columns(2)
            p = col_a.text_input("DESCRIPCIÓN DEL ARTÍCULO")
            q = col_b.number_input("CANTIDAD ENTRADA", min_value=1)
            u = col_a.number_input("COSTO ADQUISICIÓN (USD)")
            t = col_b.number_input("TASA DE CAMBIO", value=19.0)
            v = col_a.number_input("PVP OBJETIVO (MXN)")
            if st.form_submit_button("REGISTRAR EN STOCK"):
                nueva = pd.DataFrame([{"PRODUCTO": p, "STOCK": q, "USD_UNIT": u, "MXN_TOTAL": q*u*t, "PRECIO_VTA": v}])
                st.session_state.inv = pd.concat([st.session_state.inv, nueva], ignore_index=True)
                st.success("MERCANCÍA INDEXADA AL SISTEMA")
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- TERMINAL POS ---
    elif nav == "💸 TERMINAL POS":
        st.markdown("<h1 style='font-size: 3.5rem;'>PUNTO DE VENTA DIRECTO</h1>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c_v1, c_v2 = st.columns(2)
        cli_v = c_v1.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
        monto = c_v2.number_input("IMPORTE TOTAL (MXN)")
        meto = c_v1.selectbox("CONDICIÓN", ["CONTADO", "CRÉDITO JR 31"])
        if st.button("FINALIZAR TRANSACCIÓN"):
            nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CLIENTE": cli_v, "MONTO": monto, "METODO": meto}])
            st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
            if "CRÉDITO" in meto:
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cli_v, 'DEUDA'] += monto
            st.success("TICKET GENERADO CON ÉXITO")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CARTERA ---
    elif nav == "👥 CARTERA":
        st.markdown("<h1 style='font-size: 3.5rem;'>GESTIÓN DE CARTERA</h1>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        nc = st.text_input("NOMBRE DEL NUEVO CLIENTE")
        if st.button("ALTA DE CLIENTE"):
            st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nc, "DEUDA": 0.0}])], ignore_index=True)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.cli, use_container_width=True)

    # --- REPORTES ---
    elif nav == "📂 REPORTES":
        st.markdown("<h1 style='font-size: 3.5rem;'>AUDITORÍA Y REPORTES</h1>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='Ventas')
            st.session_state.inv.to_excel(w, index=False, sheet_name='Inventario')
            st.session_state.cli.to_excel(w, index=False, sheet_name='Cartera')
        st.download_button("📥 DESCARGAR MASTER REPORT (EXCEL)", buf.getvalue(), "JR31_MASTER_REPORT.xlsx")
        st.markdown('</div>', unsafe_allow_html=True)
