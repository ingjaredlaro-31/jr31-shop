import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. SET ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="JR31 SHOP | SUPREME SYSTEM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Background: Deep Executive Emerald & Black */
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT: OWNER NAME */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 30px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* BOTTOM LEFT: OFFICIAL SIGNATURE */
    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: #FF8C00; font-family: 'Montserrat', sans-serif;
        font-size: 13px; z-index: 1000; line-height: 1.6; font-weight: 900;
    }

    /* THE MONUMENTAL LOGO JR 31 SHOP */
    .shop-logo-colossal {
        font-family: 'Orbitron', sans-serif;
        font-size: 14vw; /* SIZE FOR MAXIMUM IMPACT */
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: -30px;
        filter: drop-shadow(0 15px 40px rgba(0,0,0,0.9));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; 
        font-weight: 400;
        font-size: 2vw;
        margin-bottom: 50px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(46, 139, 87, 0.5);
    }

    /* MASSIVE INPUTS FOR LOGIN */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 5px !important;
        height: 75px !important;
        margin-bottom: 10px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    /* ACCEDER BUTTON - SLIM & ELEGANT */
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
        letter-spacing: 15px;
        margin-top: 40px;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        background: #FF8C00 !important;
        color: #000000 !important;
        box-shadow: 0 0 50px rgba(255, 140, 0, 0.7) !important;
        transform: scale(1.02);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF4500;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 15px; padding: 40px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #2E8B57 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    
    <div class="header-jared">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC & DATABASE ---
def init_app_data():
    # Inventory Table
    if 'inventory_db' not in st.session_state:
        st.session_state.inventory_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PRECIO"])
    # Sales Table
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    # Clients Table
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    # Abonos History
    if 'payments_db' not in st.session_state:
        st.session_state.payments_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    # Expenses Table
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if 'admin_unlocked' not in st.session_state: st.session_state.admin_unlocked = False

init_app_data()

# --- 4. PDF GENERATOR FUNCTION ---
def generate_pdf_master():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE GERENCIAL", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Financial Stats
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "BALANCE GENERAL:", ln=True)
    pdf.set_font("Arial", "", 12)
    v_total = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    u_total = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
    pdf.cell(0, 10, f"- Ventas Totales: ${v_total:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Utilidades: ${u_total:,.2f} MXN", ln=True)
    pdf.ln(10)
    
    # Stock List
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "INVENTARIO DISPONIBLE:", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, row in st.session_state.inventory_db.iterrows():
        pdf.cell(0, 8, f"{row['ARTICULO']}: {row['STOCK']} unidades | PVP: ${row['PRECIO']}", ln=True)
    
    return pdf.output()

# --- 5. AUTHENTICATION / LANDING SCREEN ---
if not st.session_state.authenticated:
    # EL LOGO MONUMENTAL
    st.markdown('<p class="shop-logo-colossal">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        user_input = st.text_input("USUARIO ADMIN")
        pass_input = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if user_input == "admin_jr31" and pass_input == "JR31_2024_Chiapas":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Acceso Inválido. Intente de nuevo.")
else:
    # --- 6. INTERNAL MANAGEMENT SYSTEM ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # ADMIN LOCK (CODE 291329)
        if not st.session_state.admin_unlocked:
            master_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if master_code == "291329":
                    st.session_state.admin_unlocked = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.admin_unlocked = False
                st.rerun()

        st.markdown("---")
        # Navigation
        modules = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.admin_unlocked:
            modules += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.radio("NAVEGACIÓN SISTEMA", modules)
        
        st.markdown("---")
        if st.button("SALIR DE LA APP"):
            st.session_state.authenticated = False
            st.session_state.admin_unlocked = False
            st.rerun()

    # --- 7. MODULES CODE ---

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_val = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_val = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:2rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${v_val:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:2rem;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${d_val:,.0f}</p></div>', unsafe_allow_html=True)

    # --- POS TERMINAL ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory_db.empty:
            st.info("Registre stock en el módulo de GESTIÓN STOCK.")
        else:
            with st.form("pos_form"):
                p_item = st.selectbox("ARTÍCULO", st.session_state.inventory_db['ARTICULO'])
                p_client = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                p_qty = st.number_input("CANTIDAD", min_value=1)
                p_mode = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR TRANSACCIÓN"):
                    data = st.session_state.inventory_db[st.session_state.inventory_db['ARTICULO'] == p_item].iloc[0]
                    total_sale = data['PRECIO'] * p_qty
                    utilidad = (data['PRECIO'] - data['COSTO']) * p_qty
                    
                    # Update History
                    new_sale = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": p_client, "ARTICULO": p_item, "TOTAL": total_sale, "UTILIDAD": utilidad, "MODO": p_mode}])
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, new_sale], ignore_index=True)
                    # Update Stock
                    st.session_state.inventory_db.loc[st.session_state.inventory_db['ARTICULO'] == p_item, 'STOCK'] -= p_qty
                    # Update Debt
                    if p_mode == "CRÉDITO":
                        st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == p_client, 'DEUDA'] += total_sale
                    st.success(f"Venta Exitosa: ${total_sale}")

    # --- CLIENTS & HISTORY ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_hist, t_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_hist:
            c_sel = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            c_data = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == c_sel].iloc[0]
            st.metric("DEUDA ACTUAL", f"${c_data['DEUDA']:,.2f}")
            c_pay = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == c_sel, 'DEUDA'] -= c_pay
                new_payment = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "MONTO": c_pay}])
                st.session_state.payments_db = pd.concat([st.session_state.payments_db, new_payment], ignore_index=True)
                st.rerun()
            
            st.markdown("---")
            st.subheader("Historial de Compras")
            if not st.session_state.sales_db.empty:
                st.dataframe(st.session_state.sales_db[st.session_state.sales_db['CLIENTE'] == c_sel], use_container_width=True)
        with t_new:
            n_name = st.text_input("NOMBRE DEL CLIENTE")
            if st.button("GUARDAR"):
                st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"NOMBRE": n_name, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.admin_unlocked:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a_n = st.text_input("ARTICULO")
            a_s = st.number_input("CANTIDAD", min_value=1)
            a_c = st.number_input("COSTO ADQUISICIÓN")
            a_p = st.number_input("PVP VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                new_item = pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO": a_c, "PRECIO": a_p}])
                st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, new_item], ignore_index=True)
        st.dataframe(st.session_state.inventory_db, use_container_width=True)

    # --- GASTOS (ADMIN) ---
    elif nav == "💸 GASTOS" and st.session_state.admin_unlocked:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("gst"):
            g_c = st.text_input("CONCEPTO")
            g_m = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR GASTO"):
                new_exp = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": g_c, "MONTO": g_m}])
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, new_exp], ignore_index=True)
        st.table(st.session_state.expenses_db)

    # --- REPORTS (ADMIN) ---
    elif nav == "📝 REPORTES" and st.session_state.admin_unlocked:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inventory_db.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), f"JR31_MASTER_REPORT.xlsx")
        with c_r2:
            if st.button("📄 GENERAR PDF GERENCIAL"):
                pdf_bytes = generate_pdf_master()
                st.download_button("📥 DESCARGAR PDF", pdf_bytes, f"Reporte_JR31.pdf", mime="application/pdf")
