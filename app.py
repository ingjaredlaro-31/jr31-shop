import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JR31 SHOP | SUPREME SYSTEM", layout="wide", page_icon="⚡")

# --- SUPREME LUXURY STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Background Elite Black */
    .stApp { 
        background: #000000;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER */
    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px; z-index: 1000; line-height: 1.5; font-weight: 700;
        letter-spacing: 1px;
    }

    /* MONUMENTAL STORE NAME */
    .shop-name-colossal {
        font-family: 'Orbitron', sans-serif;
        font-size: 15vw; /* MONUMENTAL SIZE */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -20px;
        margin-bottom: -30px;
        filter: drop-shadow(0 0 35px rgba(255,69,0,0.6));
        line-height: 0.8;
        letter-spacing: -12px;
        text-transform: uppercase;
    }

    .sub-elegant {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Montserrat', sans-serif; 
        letter-spacing: 20px; 
        font-weight: 100;
        font-size: 1.8rem;
        margin-bottom: 50px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* INPUT FIELDS STYLE */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border-bottom: 2px solid #333 !important;
        border-radius: 0px !important;
    }
    
    input {
        color: #FF8C00 !important;
        font-size: 1.6rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    /* ACCESS BUTTON STYLE */
    .stButton>button {
        background: transparent !important;
        color: #FFFFFF !important; 
        font-family: 'Orbitron' !important;
        font-weight: 100 !important; 
        border-radius: 0px !important; 
        border: 1px solid #FF8C00 !important;
        height: 3.5em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 1.8rem !important;
        letter-spacing: 12px;
        margin-top: 40px;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background: #FF8C00 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        box-shadow: 0 0 50px rgba(255, 140, 0, 0.7) !important;
    }

    /* DASHBOARD CARDS */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 20px; padding: 40px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu, footer, header { visibility: hidden; }
    
    label { 
        color: rgba(255,255,255,0.4) !important; 
        font-family: 'Montserrat' !important; 
        font-size: 0.8rem !important;
        text-transform: uppercase;
    }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION (LOGIC IN ENGLISH) ---
def initialize_database():
    if 'inventory' not in st.session_state: 
        st.session_state.inventory = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PRECIO"])
    if 'sales' not in st.session_state: 
        st.session_state.sales = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "GANANCIA", "METODO"])
    if 'clients' not in st.session_state: 
        st.session_state.clients = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'payments' not in st.session_state:
        st.session_state.payments = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False

initialize_database()

# --- PDF GENERATION LOGIC ---
def generate_master_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE EJECUTIVO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Generado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    
    total_sales = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, f"TOTAL VENTAS: ${total_sales:,.2f} MXN", ln=True)
    return pdf.output()

# --- AUTHENTICATION SCREEN ---
if not st.session_state.authenticated:
    st.markdown('<p class="shop-name-colossal">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-elegant">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        user_id = st.text_input("USUARIO ADM")
        user_key = st.text_input("CONTRASEÑA", type="password")
        if st.button("ACCEDER"):
            if user_id == "admin_jr31" and user_key == "JR31_2024_Chiapas":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- INTERNAL NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.5rem; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Admin Lock System
        if not st.session_state.is_admin:
            admin_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if admin_code == "291329":
                    st.session_state.is_admin = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.is_admin = False
                st.rerun()

        st.markdown("---")
        # Spanish Menu for Users
        modules = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin:
            modules += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav_selection = st.sidebar.radio("SISTEMA", modules)
        
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.authenticated = False
            st.session_state.is_admin = False
            st.rerun()

    # --- MODULE 1: DASHBOARD ---
    if nav_selection == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        total_v = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        total_d = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-card"><p style="color:#FF8C00; font-family:Orbitron;">VENTAS TOTALES</p><p style="font-size:6rem; font-weight:900;">${total_v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><p style="color:#2E8B57; font-family:Orbitron;">PENDIENTE COBRO</p><p style="font-size:6rem; font-weight:900;">${total_d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- MODULE 2: POS ---
    elif nav_selection == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty:
            st.info("Sin inventario. Ingrese productos en Gestión Stock.")
        else:
            with st.form("pos_sale"):
                item_sel = st.selectbox("ARTÍCULO", st.session_state.inventory['ARTICULO'])
                client_sel = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                qty = st.number_input("CANTIDAD", min_value=1)
                method = st.selectbox("PAGO", ["CONTADO/EFECTIVO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR TRANSACCIÓN"):
                    data = st.session_state.inventory[st.session_state.inventory['ARTICULO'] == item_sel].iloc[0]
                    total_amount = data['PRECIO'] * qty
                    profit = (data['PRECIO'] - data['COSTO']) * qty
                    
                    # Update Sales
                    new_sale = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": client_sel, "ARTICULO": item_sel, "TOTAL": total_amount, "GANANCIA": profit, "METODO": method}])
                    st.session_state.sales = pd.concat([st.session_state.sales, new_sale], ignore_index=True)
                    # Update Stock
                    st.session_state.inventory.loc[st.session_state.inventory['ARTICULO'] == item_sel, 'STOCK'] -= qty
                    # Update Debt
                    if method == "CRÉDITO":
                        st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == client_sel, 'DEUDA'] += total_amount
                    st.success("Venta Procesada")

    # --- MODULE 3: CLIENTS ---
    elif nav_selection == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        tab_h, tab_n = st.tabs(["📋 EXPEDIENTES", "➕ ALTA CLIENTE"])
        with tab_h:
            cl_name = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients['NOMBRE'])
            cl_data = st.session_state.clients[st.session_state.clients['NOMBRE'] == cl_name].iloc[0]
            st.metric("DEUDA ACTUAL", f"${cl_data['DEUDA']:,.2f}")
            payment_val = st.number_input("REGISTRAR ABONO", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl_name, 'DEUDA'] -= payment_val
                new_pay = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl_name, "MONTO": payment_val}])
                st.session_state.payments = pd.concat([st.session_state.payments, new_pay], ignore_index=True)
                st.rerun()
            if not st.session_state.sales.empty:
                st.subheader("Historial de Compras")
                st.dataframe(st.session_state.sales[st.session_state.sales['CLIENTE'] == cl_name], use_container_width=True)

        with tab_n:
            new_cl = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR CLIENTE"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": new_cl, "DEUDA": 0.0}])], ignore_index=True)
                st.success("Registrado")

    # --- MODULE 4: STOCK (ADMIN ONLY) ---
    elif nav_selection == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("inventory_form", clear_on_submit=True):
            name_in = st.text_input("NOMBRE DEL PRODUCTO")
            stock_in = st.number_input("STOCK", min_value=1)
            cost_in = st.number_input("COSTO ADQUISICIÓN")
            price_in = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR INVENTARIO"):
                new_item = pd.DataFrame([{"ARTICULO": name_in, "STOCK": stock_in, "COSTO": cost_in, "PRECIO": price_in}])
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_item], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    # --- MODULE 5: EXPENSES (ADMIN ONLY) ---
    elif nav_selection == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("expense_form"):
            concept = st.text_input("CONCEPTO")
            amount = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                new_exp = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": concept, "MONTO": amount}])
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_exp], ignore_index=True)
        st.table(st.session_state.expenses)

    # --- MODULE 6: REPORTS (ADMIN ONLY) ---
    elif nav_selection == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF MAESTRO"):
            pdf_bytes = generate_master_pdf()
            st.download_button("📥 DESCARGAR REPORTE", pdf_bytes, "JR31_Reporte.pdf")
