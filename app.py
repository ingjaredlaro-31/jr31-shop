import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="SISTEMA ERP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Global Background: Deep Emerald & Black Gradient */
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER: THE ENGINEER */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 30px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER: OFFICIAL SIGNATURE */
    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: #FF8C00; font-family: 'Montserrat', sans-serif;
        font-size: 13px; z-index: 1000; line-height: 1.6; font-weight: 900;
    }

    /* LANDING SUBTITLE */
    .main-subtitle {
        text-align: center; 
        color: #FFFFFF; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 900;
        font-size: 3.5rem;
        margin-top: 100px;
        margin-bottom: 60px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(46, 139, 87, 0.8);
    }

    /* MASSIVE INPUTS FOR LOGIN */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 3px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 85px !important;
        margin-bottom: 15px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 2.2rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    /* ACCESS BUTTON GIGANTIC */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border-radius: 5px !important; 
        border: none !important;
        height: 4em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 2rem !important;
        letter-spacing: 15px;
        margin-top: 40px;
        text-transform: uppercase;
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.4) !important;
    }
    .stButton>button:hover { 
        background: #2E8B57 !important;
        box-shadow: 0 0 60px #2E8B57 !important;
        transform: scale(1.02);
    }

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF4500;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* INTERNAL DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 15px; padding: 40px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.1rem !important; text-transform: uppercase;}
    </style>
    
    <div class="header-jared">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION (ENGLISH LOGIC) ---
def initialize_system():
    if 'inv' not in st.session_state:
        st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
    if 'sales' not in st.session_state:
        st.session_state.sales = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    if 'clients' not in st.session_state:
        st.session_state.clients = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'abonos' not in st.session_state:
        st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

initialize_system()

# --- 4. PDF GENERATOR ---
def create_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE GERENCIAL", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    v_tot = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    u_tot = st.session_state.sales['UTILIDAD'].sum() if not st.session_state.sales.empty else 0
    
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "ESTADO FINANCIERO:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"- Ventas Totales: ${v_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Utilidades Brutas: ${u_tot:,.2f} MXN", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "INVENTARIO ACTUAL:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, r in st.session_state.inv.iterrows():
        pdf.cell(0, 8, f"- {r['ARTICULO']}: {r['STOCK']} pzs | PVP: ${r['PVP']}", ln=True)
    
    return pdf.output()

# --- 5. AUTHENTICATION MODULE ---
if not st.session_state.auth:
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_in = st.text_input("USUARIO ADMIN")
        p_in = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_in == "admin_jr31" and p_in == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acceso Inválido")
else:
    # --- 6. INTERNAL SYSTEM NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Admin Lock (Master Key: 291329)
        if not st.session_state.is_admin:
            m_key = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_key == "291329":
                    st.session_state.is_admin = True
                    st.rerun()
        else:
            st.success("🔒 ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.is_admin = False
                st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin:
            menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.radio("SELECCIONE MÓDULO", menu)
        
        st.markdown("---")
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.auth = False
            st.session_state.is_admin = False
            st.rerun()

    # --- 7. FUNCTIONAL MODULES ---

    # --- MODULE: DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_val = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        d_val = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:2rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${v_val:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:2rem;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${d_val:,.0f}</p></div>', unsafe_allow_html=True)

    # --- MODULE: POS TERMINAL ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty:
            st.info("Registre productos en GESTIÓN STOCK primero.")
        else:
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("CONCLUIR VENTA"):
                    row = st.session_state.inv[st.session_state.inv['ARTICULO'] == it].iloc[0]
                    t_val = row['PVP'] * qt
                    u_val = (row['PVP'] - row['COSTO']) * qt
                    # Update data
                    st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": t_val, "UTILIDAD": u_val, "MODO": md}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl, 'DEUDA'] += t_val
                    st.success("Venta Exitosa")

    # --- MODULE: CLIENT MANAGEMENT ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ ALTA CLIENTE"])
        with t1:
            cl_f = st.selectbox("BUSCAR CLIENTE", st.session_state.clients['NOMBRE'])
            dat_c = st.session_state.clients[st.session_state.clients['NOMBRE'] == cl_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${dat_c['DEUDA']:,.2f}")
            ab = st.number_input("REGISTRAR PAGO ($)", min_value=0.0)
            if st.button("ABONAR"):
                st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl_f, 'DEUDA'] -= ab
                st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl_f, "MONTO": ab}])], ignore_index=True)
                st.rerun()
            if not st.session_state.sales.empty:
                st.subheader("Compras Realizadas")
                st.dataframe(st.session_state.sales[st.session_state.sales['CLIENT'] == cl_f], use_container_width=True)
        with t2:
            n_name = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": n_name, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()

    # --- MODULE: STOCK (ADMIN ONLY) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a = st.text_input("PRODUCTO")
            s = st.number_input("CANTIDAD", min_value=1)
            c = st.number_input("COSTO ADQUISICIÓN")
            p = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- MODULE: EXPENSES (ADMIN ONLY) ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("gst"):
            exp_c = st.text_input("CONCEPTO")
            exp_m = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": exp_c, "MONTO": exp_m}])], ignore_index=True)
        st.table(st.session_state.expenses)

    # --- MODULE: REPORTS (ADMIN ONLY) ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inv.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%d%m%y')}.xlsx")
        with col_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                pdf_bytes = create_pdf_report()
                st.download_button("📥 DESCARGAR PDF", pdf_bytes, "JR31_Reporte.pdf", mime="application/pdf")
