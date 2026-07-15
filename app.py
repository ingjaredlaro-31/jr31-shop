import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JR31 SHOP | EXECUTIVE ERP", layout="wide", page_icon="⚡")

# --- SUPREME EXECUTIVE DESIGN (BLACK, ORANGE, GREEN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Background: Deep Executive Gradient */
    .stApp { 
        background: radial-gradient(circle at top right, #1b5e20 0%, #0a0a0a 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT: OWNER NAME */
    .owner-header {
        position: absolute; top: 20px; right: 50px;
        color: #FF8C00; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; 
        text-shadow: 0 0 15px rgba(255, 140, 0, 0.6); z-index: 1000;
    }

    /* BOTTOM LEFT: OFFICIAL SIGNATURE */
    .footer-signature {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 13px; z-index: 1000; line-height: 1.5; font-weight: 700;
        text-shadow: 1px 1px 2px black;
    }

    /* THE MONUMENTAL LOGO (JR 31 SHOP) */
    .colossal-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 14vw; /* MASIVE SIZE */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 30%, #FF8C00 70%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -30px;
        margin-bottom: -40px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .executive-subtitle {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Montserrat', sans-serif; 
        letter-spacing: 25px; 
        font-weight: 100;
        font-size: 1.8rem;
        margin-bottom: 60px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* EXECUTIVE LOGIN BOX */
    .login-glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 50px;
        border-radius: 20px;
        border: 1px solid rgba(255, 140, 0, 0.3);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    /* INPUTS STYLE */
    div[data-baseweb="input"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #333 !important;
        border-radius: 5px !important;
        height: 65px !important;
    }
    
    input {
        color: #FF8C00 !important;
        font-size: 1.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        text-align: center !important;
        font-weight: 700 !important;
    }

    /* ACCESS BUTTON (ORANGE SLIM) */
    .stButton>button {
        background: transparent !important;
        color: #FF8C00 !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border: 2px solid #FF8C00 !important;
        border-radius: 0px !important; 
        height: 3.5em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 1.6rem !important;
        letter-spacing: 10px;
        margin-top: 30px;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background: #FF8C00 !important;
        color: #000000 !important;
        box-shadow: 0 0 50px rgba(255, 140, 0, 0.7) !important;
        transform: translateY(-5px);
    }

    /* DATA CARDS INTERNAL */
    .executive-card {
        background: rgba(0,0,0,0.4);
        border-left: 5px solid #2E8B57;
        padding: 30px; border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* CLEANUP */
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #2E8B57 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; letter-spacing: 2px;}
    </style>
    
    <div class="owner-header">ING. JARED LARO</div>
    <div class="footer-signature">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC (BACKEND) ---
def start_system():
    if 'inventory' not in st.session_state: st.session_state.inventory = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PRECIO"])
    if 'sales' not in st.session_state: st.session_state.sales = pd.DataFrame(columns=["DATE", "CLIENT", "ITEM", "TOTAL", "PROFIT", "METHOD"])
    if 'clients' not in st.session_state: st.session_state.clients = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'payments' not in st.session_state: st.session_state.payments = pd.DataFrame(columns=["DATE", "CLIENT", "AMOUNT"])
    if 'expenses' not in st.session_state: st.session_state.expenses = pd.DataFrame(columns=["DATE", "CONCEPT", "AMOUNT"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

start_system()

# --- PDF ENGINE ---
def get_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 15, "JR 31 SHOP - EXECUTIVE SUMMARY", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    total_sales = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"VENTAS TOTALES: ${total_sales:,.2f} MXN", ln=True)
    return pdf.output()

# --- INTERFACE: LOGIN ---
if not st.session_state.auth:
    # EL LOGO MONUMENTAL
    st.markdown('<p class="colossal-logo">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="executive-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_center, col_r = st.columns([1, 1.3, 1])
    with col_center:
        st.markdown('<div class="login-glass-card">', unsafe_allow_html=True)
        user_id = st.text_input("USUARIO ADM")
        user_pk = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if user_id == "admin_jr31" and user_pk == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acceso Inválido")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- INTERFACE: MAIN SYSTEM ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.5rem; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        if not st.session_state.is_admin:
            code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()
        
        mod_list = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: mod_list += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("Navegación", mod_list)
        if st.button("LOGOUT"): st.session_state.auth = False; st.rerun()

    # --- MODULES ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        sales_val = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        debt_val = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:1.5rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${sales_val:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:1.5rem;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${debt_val:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty: st.info("Registre stock primero.")
        else:
            with st.form("pos_sale"):
                it = st.selectbox("PRODUCTO", st.session_state.inventory['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("MODO PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR TRANSACCIÓN"):
                    row = st.session_state.inventory[st.session_state.inventory['ARTICULO'] == it].iloc[0]
                    total = row['PRECIO'] * qt
                    profit = (row['PRECIO'] - row['COSTO']) * qt
                    st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([{"DATE": datetime.now().strftime("%d/%m/%y"), "CLIENT": cl, "ITEM": it, "TOTAL": total, "PROFIT": profit, "METHOD": md}])], ignore_index=True)
                    st.session_state.inventory.loc[st.session_state.inventory['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl, 'DEUDA'] += total
                    st.success("Venta Procesada")

    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("inv_form", clear_on_submit=True):
            n = st.text_input("ARTÍCULO")
            s = st.number_input("CANTIDAD", min_value=1)
            c = st.number_input("COSTO ADQ")
            p = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PRICE": p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["EXPEDIENTES", "ALTA CLIENTE"])
        with t1:
            sel = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
            dat = st.session_state.clients[st.session_state.clients['NOMBRE'] == sel].iloc[0]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            abo = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == sel, 'DEUDA'] -= abo
                st.rerun()
        with t2:
            name = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": name, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()

    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF MAESTRO"):
            data = get_pdf()
            st.download_button("📥 DESCARGAR", data, f"Reporte_JR31_{datetime.now().strftime('%d%m%y')}.pdf")
