import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- SUPREME LUXURY STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Luxury Background Gradient */
    .stApp { 
        background: linear-gradient(135deg, #1c1c1c 0%, #0f2027 50%, #203a43 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER - ING JARED LARO */
    .jared-header {
        position: absolute; top: 20px; right: 50px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 35px; font-weight: 900; 
        text-shadow: 0 0 20px rgba(46, 139, 87, 0.8); z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER - OFFICIAL SIGNATURE */
    .footer-signature {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Montserrat', sans-serif;
        font-size: 14px; z-index: 1000; line-height: 1.6; font-weight: 700;
        text-shadow: 1px 1px 2px black;
    }

    /* MONUMENTAL SHOP NAME - THE STAR OF THE SHOW */
    .main-title-colossal {
        font-family: 'Orbitron', sans-serif;
        font-size: 10rem; /* GIGANTIC */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 10%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: 0px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.8));
        line-height: 0.85;
        letter-spacing: -5px;
    }

    .main-subtitle {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 700;
        font-size: 2rem;
        margin-top: 20px;
        margin-bottom: 60px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(46, 139, 87, 0.5);
    }

    /* LARGE INPUT FIELDS */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        height: 80px !important; /* MUCH LARGER */
        margin-bottom: 20px !important;
        transition: 0.4s;
    }
    div[data-baseweb="input"]:focus-within {
        border: 2px solid #FF8C00 !important;
        box-shadow: 0 0 25px rgba(255, 140, 0, 0.3);
    }
    
    input {
        color: #FF8C00 !important;
        font-size: 2rem !important; /* GIGANTIC TEXT INSIDE */
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
        text-align: center !important;
    }

    /* LARGE ACCESS BUTTON */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border-radius: 20px !important; 
        border: none !important;
        height: 4.5em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 2.2rem !important; /* MASSIVE BUTTON TEXT */
        letter-spacing: 10px;
        margin-top: 20px;
        text-transform: uppercase;
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.4) !important;
    }
    .stButton>button:hover { 
        background: #2E8B57 !important;
        box-shadow: 0 0 60px rgba(46, 139, 87, 0.8) !important;
        transform: scale(1.02) translateY(-5px);
    }

    /* INTERNAL CARDS */
    .data-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #444;
        border-radius: 25px; padding: 40px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* UI CLEANUP */
    #MainMenu, footer, header { visibility: hidden; }
    label { 
        color: #FFFFFF !important; 
        font-family: 'Orbitron' !important; 
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        letter-spacing: 2px;
        margin-bottom: 10px !important;
        display: block;
    }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-signature">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
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
    if 'payments' not in st.session_state:
        st.session_state.payments = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False
    if 'auth' not in st.session_state: st.session_state.auth = False

init_db()

def make_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Generado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    sales_sum = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "RESUMEN EJECUTIVO:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"- Ventas Totales: ${sales_sum:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Deuda en Cartera: ${st.session_state.clients['DEUDA'].sum():,.2f} MXN", ln=True)
    return pdf.output()

# --- LOGIN SCREEN ---
if not st.session_state.auth:
    # EL TITULO MAS GRANDE JAMAS VISTO
    st.markdown('<p class="main-title-colossal">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    # CENTERING LOGIN WITH COLUMNS
    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        login_id = st.text_input("USUARIO ADMINISTRADOR")
        login_key = st.text_input("CONTRASEÑA DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if login_id == "admin_jr31" and login_key == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acceso Denegado. Verifique credenciales.")
else:
    # --- INTERNAL NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.8rem; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.is_admin:
            admin_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if admin_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()
        
        st.markdown("---")
        mod_list = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: mod_list += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.sidebar.radio("SISTEMA DE GESTIÓN", mod_list)
        if st.button("CERRAR SESIÓN"):
            st.session_state.auth = False
            st.session_state.is_admin = False
            st.rerun()

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        total_v = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        total_d = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="data-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:1.5rem;">VENTAS TOTALES</p><p style="font-size:6rem; font-weight:900;">${total_v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="data-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:1.5rem;">EN CARTERA</p><p style="font-size:6rem; font-weight:900;">${total_d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- POS SYSTEM ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty:
            st.info("Registre productos en inventario primero.")
        else:
            with st.form("pos_form"):
                it = st.selectbox("ARTÍCULO", st.session_state.inventory['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR VENTA"):
                    row = st.session_state.inventory[st.session_state.inventory['ARTICULO'] == it].iloc[0]
                    total = row['PRECIO'] * qt
                    profit = (row['PRECIO'] - row['COSTO']) * qt
                    new_s = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total, "GANANCIA": profit, "METODO": md}])
                    st.session_state.sales = pd.concat([st.session_state.sales, new_s], ignore_index=True)
                    st.session_state.inventory.loc[st.session_state.inventory['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl, 'DEUDA'] += total
                    st.success(f"Venta Exitosa por ${total}")

    # --- CLIENTS ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_exp, t_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_exp:
            sel_cl = st.selectbox("BUSCAR", st.session_state.clients['NOMBRE'])
            c_data = st.session_state.clients[st.session_state.clients['NOMBRE'] == sel_cl].iloc[0]
            st.metric("DEUDA ACTUAL", f"${c_data['DEUDA']:,.2f}")
            pay = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == sel_cl, 'DEUDA'] -= pay
                st.session_state.payments = pd.concat([st.session_state.payments, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": sel_cl, "MONTO": pay}])], ignore_index=True)
                st.rerun()
            if not st.session_state.sales.empty:
                st.subheader("Historial de Compras")
                st.dataframe(st.session_state.sales[st.session_state.sales['CLIENTE'] == sel_cl], use_container_width=True)

        with t_new:
            name_n = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": name_n, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a_n = st.text_input("PRODUCTO")
            a_s = st.number_input("CANTIDAD", min_value=1)
            a_c = st.number_input("COSTO")
            a_p = st.number_input("PRECIO")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO": a_c, "PRECIO": a_p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("gst"):
            exp_c = st.text_input("CONCEPTO")
            exp_m = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR GASTO"):
                st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": exp_c, "MONTO": exp_m}])], ignore_index=True)
        st.table(st.session_state.expenses)

    # --- REPORTS ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF MAESTRO"):
            pdf_b = make_pdf()
            st.download_button("📥 DESCARGAR PDF", pdf_b, f"JR31_LARO_{datetime.now().strftime('%d%m%y')}.pdf")
        
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inventory.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), "JR31_MASTER.xlsx")
