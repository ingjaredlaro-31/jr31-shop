import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. PAGE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE INTERFACE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Background: Infinite Deep Green & Black */
    .stApp { 
        background: radial-gradient(circle at center, #0f2b1d 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER: THE ENGINEER */
    .header-jared {
        position: absolute; top: 20px; right: 50px;
        color: #FF8C00; font-family: 'Orbitron', sans-serif;
        font-size: 32px; font-weight: 900; 
        text-shadow: 0 0 20px rgba(255, 140, 0, 0.7); z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER: OFFICIAL SIGNATURE */
    .footer-signature {
        position: fixed; bottom: 20px; left: 30px;
        color: #2E8B57; font-family: 'Montserrat', sans-serif;
        font-size: 14px; z-index: 1000; line-height: 1.6; font-weight: 900;
        text-shadow: 1px 1px 5px black;
    }

    /* --- THE COLOSSAL JR 31 SHOP LOGO --- */
    .monumental-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 14vw; /* MASIVO */
        font-weight: 900;
        text-align: center;
        color: #FFFFFF; /* PURE WHITE */
        margin-top: 50px;
        margin-bottom: -20px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,1));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
        animation: glow 3s infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 20px #FF8C00; }
        to { text-shadow: 0 0 50px #2E8B57; }
    }

    .monumental-sub {
        text-align: center; color: #FF8C00; font-family: 'Montserrat', sans-serif; 
        letter-spacing: 20px; font-weight: 100; font-size: 2rem;
        margin-bottom: 60px; text-transform: uppercase; opacity: 0.9;
    }

    /* --- XL INPUTS & BUTTONS --- */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 80px !important; /* XL SIZE */
        margin-bottom: 15px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 2rem !important; /* TEXTO GRANDE */
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-align: center !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important; border: none !important;
        height: 4em !important; width: 100%; transition: 0.4s;
        font-size: 2.2rem !important; /* BOTÓN MONUMENTAL */
        letter-spacing: 10px; margin-top: 20px;
        text-transform: uppercase;
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.4) !important;
    }
    .stButton>button:hover { 
        transform: scale(1.02);
        box-shadow: 0 0 60px #2E8B57 !important;
        background: #2E8B57 !important;
    }

    /* CLEANUP: NO OVERFLOW, NO TRASH */
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #2E8B57 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    </style>
    
    <div class="header-jared">ING. JARED LARO</div>
    <div class="footer-signature">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION (ENGLISH LOGIC) ---
def init_core_database():
    if 'inventory_db' not in st.session_state:
        st.session_state.inventory_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
    if 'sales_history' not in st.session_state:
        st.session_state.sales_history = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "GANANCIA", "MODO"])
    if 'client_base' not in st.session_state:
        st.session_state.client_base = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'expense_tracker' not in st.session_state:
        st.session_state.expense_tracker = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if 'admin_privileges' not in st.session_state: st.session_state.admin_privileges = False

init_core_database()

# --- 4. ACCESS CONTROL SCREEN ---
if not st.session_state.authenticated:
    # TITULO MONUMENTAL (COMO LOGO)
    st.markdown('<p class="monumental-logo">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="monumental-sub">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([0.8, 1.4, 0.8])
    with col_form:
        user_id = st.text_input("ADMIN ID")
        user_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if user_id == "admin_jr31" and user_pw == "JR31_2024_Chiapas":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("DATOS INVÁLIDOS")
else:
    # --- 5. MAIN SYSTEM NAVEGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.admin_privileges:
            admin_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if admin_code == "291329":
                    st.session_state.admin_privileges = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO ACTIVO")
            if st.button("BLOQUEAR ADMIN"):
                st.session_state.admin_privileges = False
                st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.admin_privileges:
            menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"):
            st.session_state.authenticated = False
            st.rerun()

    # --- MODULES LOGIC ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_history['TOTAL'].sum() if not st.session_state.sales_history.empty else 0
        d = st.session_state.client_base['DEUDA'].sum() if not st.session_state.client_base.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div style="border-top:5px solid #FF8C00; background:rgba(255,255,255,0.05); padding:40px; border-radius:15px; text-align:center;"><p style="font-family:Orbitron; color:#FF8C00;">VENTAS TOTALES</p><p style="font-size:6rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="border-top:5px solid #2E8B57; background:rgba(255,255,255,0.05); padding:40px; border-radius:15px; text-align:center;"><p style="font-family:Orbitron; color:#2E8B57;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${d:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory_db.empty: st.info("Registre productos en GESTIÓN STOCK primero.")
        else:
            with st.form("pos_form"):
                it = st.selectbox("PRODUCTO", st.session_state.inventory_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR VENTA"):
                    data = st.session_state.inventory_db[st.session_state.inventory_db['ARTICULO'] == it].iloc[0]
                    total = data['PVP'] * qt
                    profit = (data['PVP'] - data['COSTO']) * qt
                    st.session_state.sales_history = pd.concat([st.session_state.sales_history, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total, "GANANCIA": profit, "MODO": md}])], ignore_index=True)
                    st.session_state.inventory_db.loc[st.session_state.inventory_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl, 'DEUDA'] += total
                    st.success("Operación Exitosa")

    elif nav == "📦 GESTIÓN STOCK" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            n = st.text_input("ARTÍCULO")
            s = st.number_input("CANTIDAD", min_value=1)
            c = st.number_input("COSTO ADQ")
            p = st.number_input("PVP VENTA")
            if st.form_submit_button("AÑADIR A INVENTARIO"):
                st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory_db, use_container_width=True)

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
            dc = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == cl].iloc[0]
            st.metric("DEUDA ACTUAL", f"${dc['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR ABONO"):
                st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl, 'DEUDA'] -= ab
                st.rerun()
            st.dataframe(st.session_state.sales_history[st.session_state.sales_history['CLIENT'] == cl], use_container_width=True)
        with t2:
            nn = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"NOMBRE": nn, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()
