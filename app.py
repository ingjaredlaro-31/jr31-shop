import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER: THE ENGINEER */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
        line-height: 1.6; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.1rem; }

    /* LOGO JR 31 SHOP MONUMENTAL */
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .subtitle-executive {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* SIDEBAR EMOJIS GIGANTES */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    /* Estilo para que las opciones del radio button del menú sean más grandes */
    div[data-testid="stSidebarNav"] li, div[role="radiogroup"] label {
        font-size: 1.5rem !important; /* EMOJIS Y TEXTO MÁS GRANDE */
        font-weight: 700 !important;
        margin-bottom: 10px;
    }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; 
        color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; 
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 2rem !important;
        border-radius: 8px !important; border: none !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px;
        border-top: 6px solid #FF8C00; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .metric-val { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; text-transform: uppercase; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION (ANTI-ERROR) ---
def init_all_data():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_REAL", "ORIGINAL_USD", "PVP_JR31", "VENDIDOS"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "GANANCIA_NETA", "TOTAL"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
    if 'abonos_db' not in st.session_state:
        st.session_state.abonos_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_all_data()

# --- 4. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-executive">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
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
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.auth = False
            st.rerun()

    # --- 6. MODULES LOGIC ---

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_total = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_total = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        piezas_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="executive-card"><p class="metric-title">VENTAS</p><p class="metric-val">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p class="metric-title">CARTERA</p><p class="metric-val" style="color:#FF4500;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="executive-card"><p class="metric-title">STOCK</p><p class="metric-val">{piezas_stock:,.0f}</p></div>', unsafe_allow_html=True)

    # --- CARTERA CLIENTES (RESTAURADO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        tab_exp, tab_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        
        with tab_exp:
            search_cl = st.selectbox("BUSCAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == search_cl].iloc[0]
            
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #FF8C00;">
                    <p style="color:#FF8C00; font-family:Orbitron;">FICHA TÉCNICA:</p>
                    <p><b>ID:</b> {dat['ID']}</p>
                    <p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p>
                    <p><b>TELÉFONO:</b> {dat['TELEFONO']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c_col2:
                st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
                abono = st.number_input("REGISTRAR PAGO ($)", min_value=0.0)
                if st.button("APLICAR ABONO"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == search_cl, 'DEUDA'] -= abono
                    new_pay = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": search_cl, "MONTO": abono}])
                    st.session_state.abonos_db = pd.concat([st.session_state.abonos_db, new_pay], ignore_index=True)
                    st.rerun()

        with tab_new:
            with st.form("alta_cl", clear_on_submit=True):
                n = st.text_input("NOMBRE COMPLETO")
                d = st.text_input("DIRECCIÓN")
                t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR EN SISTEMA"):
                    new_id = f"JR31-{len(st.session_state.clients_db):03d}"
                    nuevo = pd.DataFrame([{"ID": new_id, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, nuevo], ignore_index=True)
                    st.success(f"Registrado con ID: {new_id}")

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with tab_a:
            with st.form("stk", clear_on_submit=True):
                a_n = st.text_input("ARTICULO")
                a_s = st.number_input("CANTIDAD", min_value=1)
                a_c = st.number_input("COSTO REAL")
                a_u = st.number_input("PRECIO USA (USD)")
                a_p = st.number_input("PVP JR31")
                if st.form_submit_button("ACTUALIZAR STOCK"):
                    new_item = pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO_REAL": a_c, "ORIGINAL_USD": a_u, "PVP_JR31": a_p, "VENDIDOS": 0}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos primero.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qty = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p_sel].iloc[0]
                    total = data['PVP_JR31'] * qty
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "TOTAL": total}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p_sel, 'STOCK'] -= qty
                    st.success(f"Venta Exitosa por ${total}")

# --- FOOTER CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
