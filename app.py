import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- PROFESSIONAL UI DESIGN (GREEN & ORANGE THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Global Background: Deep Green Gradient */
    .stApp { 
        background: linear-gradient(135deg, #0a1f12 0%, #1b5e20 50%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* WATERMARK BACKGROUND TEXT */
    .stApp::before {
        content: "ING JARED LARO - JR 31 SHOP - EXCLUSIVE SOFTWARE";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 5vw;
        color: rgba(46, 139, 87, 0.05);
        z-index: -1;
        font-family: 'Orbitron', sans-serif;
        white-space: nowrap;
    }

    /* TOP RIGHT HEADER */
    .header-name {
        position: absolute; top: 15px; right: 40px;
        color: #FF8C00; font-family: 'Orbitron', sans-serif;
        font-size: 24px; font-weight: 900; 
        text-shadow: 0 0 10px rgba(255, 140, 0, 0.5); z-index: 1000;
    }

    /* FOOTER SIGNATURE */
    .footer-text {
        position: fixed; bottom: 15px; left: 25px;
        color: #FF8C00; font-family: 'Montserrat', sans-serif;
        font-size: 11px; z-index: 1000; line-height: 1.4; font-weight: 700;
        text-shadow: 1px 1px 2px black;
    }

    /* MONUMENTAL WHITE SHOP NAME */
    .main-logo-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 14vw; /* ENORME */
        font-weight: 900;
        text-align: center;
        color: #FFFFFF; /* PURE WHITE */
        margin-top: 50px;
        margin-bottom: -30px;
        filter: drop-shadow(0 10px 30px rgba(0,0,0,0.8));
        line-height: 0.8;
        letter-spacing: -5px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; 
        color: #FF8C00; /* ORANGE */
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 60px;
        text-transform: uppercase;
    }

    /* INPUT FIELDS - PROFESSIONAL LOOK */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #2E8B57 !important; /* GREEN BORDER */
        border-radius: 5px !important;
        height: 65px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
        font-family: 'Montserrat', sans-serif !important;
        text-align: center !important;
        font-weight: 700 !important;
    }

    /* ORANGE PROFESSIONAL BUTTON */
    .stButton>button {
        background: #FF8C00 !important; /* SOLID ORANGE */
        color: #FFFFFF !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border-radius: 0px !important; 
        border: none !important;
        height: 3.5em !important; 
        width: 100%; 
        transition: 0.3s;
        font-size: 1.5rem !important;
        letter-spacing: 5px;
        margin-top: 20px;
        text-transform: uppercase;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { 
        background: #2E8B57 !important; /* CHANGES TO GREEN ON HOVER */
        transform: scale(1.02);
    }

    /* SIDEBAR GREEN STYLE */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1f12 0%, #1b5e20 100%) !important;
        border-right: 5px solid #FF8C00;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* DASHBOARD CARDS */
    .status-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px; padding: 30px;
        border-top: 5px solid #FF8C00;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }

    /* CLEANUP */
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    
    <div class="header-name">ING. JARED LARO</div>
    <div class="footer-text">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
def init_db():
    if 'inventory' not in st.session_state: st.session_state.inventory = pd.DataFrame(columns=["ITEM", "QTY", "COST", "PRICE"])
    if 'sales' not in st.session_state: st.session_state.sales = pd.DataFrame(columns=["DATE", "CLIENT", "ITEM", "TOTAL", "PROFIT", "METHOD"])
    if 'clients' not in st.session_state: st.session_state.clients = pd.DataFrame([{"NAME": "VENTA MOSTRADOR (EFECTIVO)", "DEBT": 0.0}])
    if 'payments' not in st.session_state: st.session_state.payments = pd.DataFrame(columns=["DATE", "CLIENT", "AMOUNT"])
    if 'expenses' not in st.session_state: st.session_state.expenses = pd.DataFrame(columns=["DATE", "CONCEPT", "AMOUNT"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_db()

# --- PDF GENERATOR ---
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Generado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    total_sales = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"TOTAL DE VENTAS ACUMULADAS: ${total_sales:,.2f} MXN", ln=True)
    return pdf.output()

# --- LOGIN SCREEN ---
if not st.session_state.auth:
    st.markdown('<p class="main-logo-title">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_center, col_r = st.columns([1, 1.2, 1])
    with col_center:
        user_id = st.text_input("USUARIO ADMIN")
        user_pw = st.text_input("CONTRASEÑA", type="password")
        if st.button("ACCEDER"):
            if user_id == "admin_jr31" and user_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- INTERNAL MENU ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.5rem; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        if not st.session_state.is_admin:
            admin_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if admin_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()
        
        mod_list = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: mod_list += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("Navegación Sistema", mod_list)
        if st.button("CERRAR SESIÓN"): st.session_state.auth = False; st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v_total = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        d_total = st.session_state.clients['DEBT'].sum() if not st.session_state.clients.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="status-card"><p style="color:#FF8C00; font-family:Orbitron;">TOTAL VENTAS</p><p style="font-size:5rem; font-weight:900;">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="status-card"><p style="color:#2E8B57; font-family:Orbitron;">CARTERA PENDIENTE</p><p style="font-size:5rem; font-weight:900;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty: st.info("Primero cargue inventario en la sección de Stock.")
        else:
            with st.form("pos_sale"):
                it_sel = st.selectbox("PRODUCTO", st.session_state.inventory['ITEM'])
                cl_sel = st.selectbox("CLIENTE", st.session_state.clients['NAME'])
                qty_v = st.number_input("CANTIDAD", min_value=1)
                method = st.selectbox("MÉTODO DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR OPERACIÓN"):
                    data = st.session_state.inventory[st.session_state.inventory['ITEM'] == it_sel].iloc[0]
                    total_v = data['PRICE'] * qty_v
                    profit_v = (data['PRICE'] - data['COST']) * qty_v
                    st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([{"DATE": datetime.now().strftime("%d/%m/%y"), "CLIENT": cl_sel, "ITEM": it_sel, "TOTAL": total_v, "PROFIT": profit_v, "METHOD": method}])], ignore_index=True)
                    st.session_state.inventory.loc[st.session_state.inventory['ITEM'] == it_sel, 'QTY'] -= qty_v
                    if method == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NAME'] == cl_sel, 'DEBT'] += total_v
                    st.success(f"Venta registrada: ${total_v}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        tab_list, tab_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with tab_list:
            c_target = st.selectbox("SELECCIONE CLIENTE", st.session_state.clients['NAME'])
            c_info = st.session_state.clients[st.session_state.clients['NAME'] == c_target].iloc[0]
            st.metric("SALDO DEUDOR", f"${c_info['DEBT']:,.2f}")
            abono = st.number_input("ABONAR A CUENTA ($)", min_value=0.0)
            if st.button("REGISTRAR ABONO"):
                st.session_state.clients.loc[st.session_state.clients['NAME'] == c_target, 'DEBT'] -= abono
                st.session_state.payments = pd.concat([st.session_state.payments, pd.DataFrame([{"DATE": datetime.now().strftime("%d/%m/%y"), "CLIENT": c_target, "AMOUNT": abono}])], ignore_index=True)
                st.rerun()
            if not st.session_state.sales.empty:
                st.subheader("Compras Realizadas")
                st.dataframe(st.session_state.sales[st.session_state.sales['CLIENT'] == c_target], use_container_width=True)

        with tab_new:
            new_name = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR CLIENTE"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NAME": new_name, "DEBT": 0.0}])], ignore_index=True)
                st.rerun()

    # --- 4. STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("stk_form", clear_on_submit=True):
            n_i = st.text_input("DESCRIPCIÓN DEL ARTÍCULO")
            q_i = st.number_input("STOCK DISPONIBLE", min_value=1)
            c_i = st.number_input("COSTO ADQUISICIÓN")
            p_i = st.number_input("PRECIO DE VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([{"ITEM": n_i, "QTY": q_i, "COST": c_i, "PRICE": p_i}])], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    # --- 5. GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REGISTRO DE GASTOS</h1>", unsafe_allow_html=True)
        with st.form("gas_form"):
            conc = st.text_input("CONCEPTO")
            amm = st.number_input("IMPORTE ($)")
            if st.form_submit_button("REGISTRAR GASTO"):
                st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([{"DATE": datetime.now().strftime("%d/%m/%y"), "CONCEPT": conc, "AMOUNT": amm}])], ignore_index=True)
        st.table(st.session_state.expenses)

    # --- 6. REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF MAESTRO"):
            pdf_bytes = generate_pdf_report()
            st.download_button("📥 DESCARGAR REPORTE PDF", pdf_bytes, f"JR31_LARO_{datetime.now().strftime('%d%m%y')}.pdf")
        
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inventory.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), "JR31_MASTER_DATA.xlsx")
