import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JR31 SHOP | ELITE ERP", layout="wide", page_icon="⚡")

# --- ULTRA LUXURY BLACK & GOLD STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@100;400;700;900&family=Orbitron:wght@400;900&display=swap');
    
    /* Background: Black & Gold Gradient */
    .stApp { 
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 40%, #43302b 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER */
    .jared-header {
        position: absolute; top: 20px; right: 50px;
        color: #d4af37; font-family: 'Orbitron', sans-serif;
        font-size: 24px; font-weight: 900; 
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5); z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER SIGNATURE */
    .footer-signature {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.3);
        font-family: 'Montserrat', sans-serif;
        font-size: 11px; z-index: 1000; line-height: 1.6; font-weight: 700;
    }

    /* MONUMENTAL WHITE SHOP NAME (LOGO STYLE) */
    .shop-logo-text {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16vw; /* COLOSSAL SIZE */
        font-weight: 900;
        text-align: center;
        color: #FFFFFF; /* PURE WHITE */
        margin-top: 40px;
        margin-bottom: -40px;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.9));
        line-height: 0.9;
        letter-spacing: 5px;
        text-transform: uppercase;
    }

    .sub-tagline {
        text-align: center; 
        color: #d4af37; /* GOLD */
        font-family: 'Montserrat', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 100;
        font-size: 1.4rem;
        margin-bottom: 60px;
        text-transform: uppercase;
    }

    /* SOPHISTICATED INPUT FIELDS */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid #d4af37 !important; /* GOLD BORDER */
        border-radius: 5px !important;
        height: 60px !important;
        margin-bottom: 10px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 1.3rem !important;
        font-family: 'Montserrat', sans-serif !important;
        text-align: center !important;
    }

    /* ELEGANT SLIM ACCESS BUTTON */
    .stButton>button {
        background: transparent !important;
        color: #d4af37 !important; 
        font-family: 'Montserrat' !important;
        font-weight: 700 !important; 
        border: 2px solid #d4af37 !important;
        border-radius: 0px !important; 
        height: 3em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 1.4rem !important; /* BALANCED SIZE */
        letter-spacing: 8px;
        margin-top: 30px;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background: #d4af37 !important;
        color: #000000 !important;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.5) !important;
    }

    /* INTERNAL ELEMENTS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .dash-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #d4af37;
        border-radius: 10px; padding: 30px;
        text-align: center;
    }

    /* CLEANUP */
    #MainMenu, footer, header { visibility: hidden; }
    label { 
        color: #d4af37 !important; 
        font-family: 'Montserrat' !important; 
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-signature">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC (ENGLISH) ---
def init_db():
    if 'inventory' not in st.session_state: 
        st.session_state.inventory = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PRECIO"])
    if 'sales' not in st.session_state: 
        st.session_state.sales = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "GANANCIA", "METODO"])
    if 'clients' not in st.session_state: 
        st.session_state.clients = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_db()

# --- LOGIN SCREEN ---
if not st.session_state.auth:
    # MONUMENTAL STORE NAME AS LOGO
    st.markdown('<p class="shop-logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-tagline">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_center, col_r = st.columns([1, 1, 1])
    with col_center:
        user_in = st.text_input("USUARIO ADM")
        pass_in = st.text_input("CONTRASEÑA", type="password")
        if st.button("ACCEDER"):
            if user_in == "admin_jr31" and pass_in == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acceso denegado")
else:
    # --- INTERNAL NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#d4af37; font-family:Bebas Neue; font-size:2.5rem; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.is_admin:
            code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if code == "291329": 
                    st.session_state.is_admin = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR PRIVILEGIOS"): 
                st.session_state.is_admin = False
                st.rerun()
        
        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "📝 REPORTES"]
        
        choice = st.sidebar.radio("SISTEMA", menu)
        if st.button("LOGOUT"):
            st.session_state.auth = False
            st.rerun()

    # --- DASHBOARD ---
    if choice == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Bebas Neue; text-align:center; font-size:4rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        total_s = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        total_d = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="dash-card"><p style="color:#d4af37; font-family:Montserrat;">VENTAS TOTALES</p><p style="font-size:5rem; font-weight:900;">${total_s:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="dash-card"><p style="color:#FFFFFF; font-family:Montserrat;">POR COBRAR</p><p style="font-size:5rem; font-weight:900;">${total_d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL ---
    elif choice == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Bebas Neue;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty:
            st.info("Registre productos en el área de Stock.")
        else:
            with st.form("venta_pos"):
                art = st.selectbox("ARTÍCULO", st.session_state.inventory['ARTICULO'])
                cli = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                can = st.number_input("CANTIDAD", min_value=1)
                met = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR VENTA"):
                    row = st.session_state.inventory[st.session_state.inventory['ARTICULO'] == art].iloc[0]
                    t = row['PRECIO'] * can
                    g = (row['PRECIO'] - row['COSTO']) * can
                    st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli, "ARTICULO": art, "TOTAL": t, "GANANCIA": g, "METODO": met}])], ignore_index=True)
                    st.session_state.inventory.loc[st.session_state.inventory['ARTICULO'] == art, 'STOCK'] -= can
                    if met == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cli, 'DEUDA'] += t
                    st.success("Venta Exitosa")

    # --- STOCK (ADMIN) ---
    elif choice == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Bebas Neue;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stock_form", clear_on_submit=True):
            n = st.text_input("PRODUCTO")
            s = st.number_input("CANTIDAD", min_value=1)
            c = st.number_input("COSTO")
            p = st.number_input("PRECIO VENTA")
            if st.form_submit_button("AÑADIR ARTÍCULO"):
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PRECIO": p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    # --- CLIENTS ---
    elif choice == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Bebas Neue;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 HISTORIAL", "➕ NUEVO CLIENTE"])
        with t1:
            sel = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
            dat = st.session_state.clients[st.session_state.clients['NOMBRE'] == sel].iloc[0]
            st.metric("SALDO PENDIENTE", f"${dat['DEUDA']:,.2f}")
            abo = st.number_input("ABONAR", min_value=0.0)
            if st.button("APLICAR PAGO"):
                st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == sel, 'DEUDA'] -= abo
                st.rerun()
        with t2:
            nc = st.text_input("NOMBRE")
            if st.button("GUARDAR"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": nc, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()
