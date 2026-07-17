import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os
# Librería para que la App lo recuerde
import extra_streamlit_components as stx 

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | SUPREME PERSISTENCE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTIÓN DE "RECUÉRDAME" (COOKIES) ---
def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

# --- 3. ESTILO SUPREME EXECUTIVE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    .logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 4. INICIALIZACIÓN DE DATOS ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])], ignore_index=True)
if 'cart' not in st.session_state: st.session_state.cart = []
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 5. LÓGICA DE PERSISTENCIA (COOKIES) ---
# Intentamos recuperar la sesión guardada
saved_auth = cookie_manager.get(cookie="jr31_session")
if saved_auth == "active":
    st.session_state.auth = True

# --- 6. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; color:#2E8B57;">SISTEMA DE ADMINISTRACIÓN Y VENTA</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                # Guardamos la cookie por 30 días
                cookie_manager.set("jr31_session", "active", expires_at=datetime.now().replace(year=datetime.now().year + 1))
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- INTERFAZ DEL SISTEMA (MENÚ) ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 INICIO / DASHBOARD"): 
            st.session_state.page = "📊 DASHBOARD"
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CLAVE MAESTRA", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        
        if st.button("🚪 CERRAR SESIÓN"):
            st.session_state.auth = False
            st.session_state.is_admin = False
            cookie_manager.delete("jr31_session") # Borramos la llave
            st.rerun()

    # --- 7. MÓDULO DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#2E8B57;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 8. MÓDULO TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        bus = st.text_input("🔍 BUSCAR ARTÍCULO")
        filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(bus, case=False)]
        with st.form("v"):
            p = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
            cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            qt = st.number_input("CANTIDAD", min_value=1)
            if st.form_submit_button("VENDER"):
                row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p].iloc[0]
                t = row['PVP_JR31'] * qt
                st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": t, "UTILIDAD": (row['PVP_JR31']-row['COSTO_TJ'])*qt}])], ignore_index=True)
                st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                st.success("Operación Exitosa")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
