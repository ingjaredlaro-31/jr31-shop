import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO SUPREME CYBER-LUXURY (CSS) ---
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
        font-family: 'Orbitron', sans-serif;
        font-size: 12vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; 
        color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; 
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.6rem !important; font-weight: 700 !important; margin-bottom: 15px; }

    .executive-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px;
        border-top: 6px solid #FF8C00; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .metric-val { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; text-transform: uppercase; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS REFORZADA ---
def core_maintenance():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

core_maintenance()

# --- 4. LOGIN ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- 5. MENÚ ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:1.5rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULO GASTOS (CORREGIDO Y ACTIVO) ---
    if nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CONTROL DE EGRESOS</h1>", unsafe_allow_html=True)
        
        # Resumen de Gastos
        total_g = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        st.markdown(f'<div class="executive-card"><p class="metric-title">TOTAL GASTADO</p><p class="metric-val" style="color:#FF4500;">${total_g:,.2f}</p></div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1, 1.5])
        with col_g1:
            st.markdown("### 📝 Registrar Gasto")
            with st.form("form_g", clear_on_submit=True):
                cat = st.selectbox("CATEGORÍA", ["PALLETS", "OFICINA", "LOGISTICA", "SUMINISTROS", "VARIOS"])
                con = st.text_input("CONCEPTO (Ej. Compra de tarimas)")
                mon = st.number_input("MONTO ($)", min_value=0.1)
                if st.form_submit_button("GUARDAR GASTO"):
                    nuevo_g = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon}])
                    st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, nuevo_g], ignore_index=True)
                    st.success("Gasto registrado."); st.rerun()

        with col_g2:
            st.markdown("### 📋 Historial")
            st.dataframe(st.session_state.expenses_db, use_container_width=True)

    # --- DASHBOARD ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.markdown(f'<div class="executive-card"><p class="metric-title">VENTAS TOTALES</p><p class="metric-val">${v:,.0f}</p></div>', unsafe_allow_html=True)

    # --- STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a = st.text_input("ARTICULO")
            s = st.number_input("STOCK", min_value=1)
            c = st.number_input("COSTO TJ")
            p = st.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR"):
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_TJ": c, "PVP_JR31": p}])], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Sin inventario.")
        else:
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total = row['PVP_JR31'] * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": total}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    st.success(f"Venta registrada: ${total}")

    # --- CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        cl_f = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
        dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cl_f].iloc[0]
        st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
