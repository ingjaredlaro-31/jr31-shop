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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Background: Deep Executive Emerald & Black */
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER: THE ENGINEER */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* BOTTOM LEFT FOOTER: OFFICIAL SIGNATURE */
    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px; z-index: 1000; line-height: 1.6; font-weight: 900;
    }

    /* MONUMENTAL STORE NAME (LOGO) */
    .monumental-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 15vw;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: -15px;
        filter: drop-shadow(0 15px 35px rgba(0,0,0,1));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 900;
        font-size: 2.5rem;
        margin-top: 10px;
        margin-bottom: 60px;
        text-transform: uppercase;
    }

    /* INPUT FIELDS GIGANTIC */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 80px !important;
        margin-bottom: 15px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    /* ACCESS BUTTON */
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

    /* EXECUTIVE CARDS FOR DASHBOARD */
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 30px;
        border-left: 10px solid #FF8C00;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        text-align: center;
    }

    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        color: #FFFFFF;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF4500;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.1rem !important; text-transform: uppercase;}
    </style>
    
    <div class="header-jared">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        SISTEMA DE ADMINISTRACIÓN JR 31 SHOP - EXCLUSIVE LICENSE
    </div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE LOGIC (ENGLISH BACKEND) ---
def start_app_database():
    if 'inventory' not in st.session_state:
        st.session_state.inventory = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
    if 'sales' not in st.session_state:
        st.session_state.sales = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "GANANCIA", "MODO"])
    if 'clients' not in st.session_state:
        st.session_state.clients = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DEUDA": 0.0}])
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

start_app_database()

# --- 4. EXPORT ENGINE (PDF) ---
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "JR 31 SHOP - BUSINESS INTELLIGENCE", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    v_total = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"ESTADO DE RESULTADOS:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"- Ventas Totales: ${v_total:,.2f}", ln=True)
    pdf.cell(0, 8, f"- Capital en Cartera: ${st.session_state.clients['DEUDA'].sum():,.2f}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "DETALLE DE INVENTARIO:", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, r in st.session_state.inventory.iterrows():
        pdf.cell(0, 7, f"- {r['ARTICULO']}: {r['STOCK']} pzs", ln=True)
    
    return pdf.output()

# --- 5. INTERFACE LOGIC ---

# LOGIN SCREEN
if not st.session_state.auth:
    # EL NOMBRE NO SE VE PEQUEÑO NUNCA MÁS
    st.markdown('<p class="monumental-logo">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_center, col_r = st.columns([1, 1.2, 1])
    with col_center:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # MAIN SYSTEM
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin:
            menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        choice = st.radio("SELECCIONE MÓDULO", menu)
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.auth = False
            st.rerun()

    # MODULE 1: DASHBOARD
    if choice == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>PANEL DE CONTROL</h1>", unsafe_allow_html=True)
        v = st.session_state.sales['TOTAL'].sum() if not st.session_state.sales.empty else 0
        d = st.session_state.clients['DEUDA'].sum() if not st.session_state.clients.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-container"><p style="color:#FF8C00; font-family:Orbitron; font-size:1.5rem;">VENTAS ACUMULADAS</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-container" style="border-left: 10px solid #2E8B57;"><p style="color:#2E8B57; font-family:Orbitron; font-size:1.5rem;">SALDO EN CARTERA</p><p class="metric-value" style="color:#2E8B57;">${d:,.0f}</p></div>', unsafe_allow_html=True)
        
        # ALERTAS DE STOCK
        if st.session_state.is_admin:
            st.markdown("### 🚨 ALERTAS DE SUMINISTRO (STOCK BAJO)")
            low_stock = st.session_state.inventory[st.session_state.inventory['STOCK'] <= 5]
            if not low_stock.empty:
                st.warning(f"Tienes {len(low_stock)} productos por agotarse.")
                st.dataframe(low_stock, use_container_width=True)

    # MODULE 2: POS
    elif choice == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>NUEVA VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory.empty: st.info("Registre mercancía en GESTIÓN STOCK primero.")
        else:
            with st.form("pos_form"):
                it = st.selectbox("ARTÍCULO", st.session_state.inventory['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("MODO PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR VENTA"):
                    row = st.session_state.inventory[st.session_state.inventory['ARTICULO'] == it].iloc[0]
                    total = row['PVP'] * qt
                    uti = (row['PVP'] - row['COSTO']) * qt
                    # UPDATE DATA
                    st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total, "GANANCIA": uti, "MODO": md}])], ignore_index=True)
                    st.session_state.inventory.loc[st.session_state.inventory['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == cl, 'DEUDA'] += total
                    st.success("Venta Exitosa")

    # MODULE 3: CLIENTS
    elif choice == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            search_cl = st.text_input("🔍 BUSCAR POR NOMBRE")
            filtered_clients = st.session_state.clients[st.session_state.clients['NOMBRE'].str.contains(search_cl, case=False)]
            sel_c = st.selectbox("RESULTADO", filtered_clients['NOMBRE'])
            c_data = st.session_state.clients[st.session_state.clients['NOMBRE'] == sel_c].iloc[0]
            
            c_ab1, c_ab2 = st.columns(2)
            c_ab1.metric("DEUDA", f"${c_data['DEUDA']:,.2f}")
            with c_ab2:
                abono = st.number_input("REGISTRAR ABONO", min_value=0.0)
                if st.button("PAGAR"):
                    st.session_state.clients.loc[st.session_state.clients['NOMBRE'] == sel_c, 'DEUDA'] -= abono
                    st.rerun()
            
            st.markdown("---")
            st.subheader("Historial de Compras")
            if not st.session_state.sales.empty:
                st.dataframe(st.session_state.sales[st.session_state.sales['CLIENTE'] == sel_c], use_container_width=True)

        with t2:
            new_n = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.clients = pd.concat([st.session_state.clients, pd.DataFrame([{"NOMBRE": new_n, "DEUDA": 0.0}])], ignore_index=True)
                st.rerun()

    # MODULE 4: STOCK (ADMIN)
    elif choice == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a_n = st.text_input("PRODUCTO")
            a_s = st.number_input("CANTIDAD", min_value=1)
            a_c = st.number_input("COSTO ADQ")
            a_p = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO": a_c, "PVP": a_p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory, use_container_width=True)

    # MODULE 6: REPORTS
    elif choice == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inventory.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 EXCEL COMPLETO", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%d%m%y')}.xlsx")
        with col_r2:
            if st.button("📄 GENERAR PDF"):
                p_bytes = generate_pdf_report()
                st.download_button("📥 DESCARGAR PDF", p_bytes, "Reporte_Gerencial.pdf")
