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
    
    /* Background: Deep Emerald & Black Gradient */
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

    /* THE MONUMENTAL LOGO JR 31 SHOP */
    .shop-logo-colossal {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: -20px;
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
        font-size: 2rem;
        margin-bottom: 50px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(46, 139, 87, 0.5);
    }

    /* MASSIVE INPUTS FOR LOGIN */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 75px !important;
        margin-bottom: 15px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
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

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        margin-top: 100px;
        padding-bottom: 40px;
        line-height: 1.6;
        width: 100%;
        border-top: 1px solid rgba(46, 139, 87, 0.2);
        padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.1rem; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 15px; padding: 40px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF4500;
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION ---
def initialize_system():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_cli = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_cli], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

initialize_system()

# --- 4. PDF ENGINE ---
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE GERENCIAL", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Generado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "ESTADO DE RESULTADOS:", ln=True)
    v_sum = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"- Ventas Totales: ${v_sum:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"- Deuda en Cartera: ${st.session_state.clients_db['DEUDA'].sum():,.2f} MXN", ln=True)
    
    return pdf.output()

# --- 5. AUTHENTICATION ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-colossal">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("USUARIO ADMIN")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 6. INTERNAL INTERFACE ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329":
                    st.session_state.is_admin = True
                    st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.is_admin = False
                st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin:
            menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR DE LA APP"):
            st.session_state.auth = False
            st.session_state.is_admin = False
            st.rerun()

    # --- MODULE: DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_val = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_val = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:2rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${v_val:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:2rem;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${d_val:,.0f}</p></div>', unsafe_allow_html=True)

    # --- MODULE: POS TERMINAL ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty:
            st.info("Debe registrar productos en STOCK primero.")
        else:
            with st.form("pos_form"):
                it = st.selectbox("ARTÍCULO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("CONCLUIR VENTA"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total_s = row['PVP'] * qt
                    util = (row['PVP'] - row['COSTO']) * qt
                    # Registro
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total_s, "UTILIDAD": util}])], ignore_index=True)
                    # Inventario
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    # Deuda
                    if md == "CRÉDITO":
                        st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cl, 'DEUDA'] += total_s
                    st.success(f"Venta Exitosa por ${total_s}")

    # --- MODULE: CLIENTS (V29.0 EXTENDED) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ REGISTRAR CLIENTE"])
        
        with t1:
            c_sel = st.selectbox("BUSCAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            c_data = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == c_sel].iloc[0]
            
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #FF8C00;">
                    <p style="color:#FF8C00; font-family:Orbitron;">DETALLES DEL CLIENTE:</p>
                    <p><b>ID INTERNO:</b> {c_data['ID']}</p>
                    <p><b>DIRECCIÓN:</b> {c_data['DIRECCION']}</p>
                    <p><b>TELÉFONO:</b> {c_data['TELEFONO']}</p>
                </div>
                """, unsafe_allow_html=True)
            with c_col2:
                st.metric("DEUDA VIGENTE", f"${c_data['DEUDA']:,.2f}")
                abono = st.number_input("ABONAR ($)", min_value=0.0)
                if st.button("PAGAR"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == c_sel, 'DEUDA'] -= abono
                    st.success("Abono aplicado.")
                    st.rerun()

        with t2:
            st.markdown("### 📥 NUEVO EXPEDIENTE")
            with st.form("new_client", clear_on_submit=True):
                n_nom = st.text_input("NOMBRE COMPLETO")
                n_dir = st.text_input("DIRECCIÓN")
                n_tel = st.text_input("TELÉFONO / WHATSAPP")
                if st.form_submit_button("CREAR CLIENTE"):
                    new_id = f"JR31-{len(st.session_state.clients_db):03d}"
                    nuevo_c = pd.DataFrame([{"ID": new_id, "NOMBRE": n_nom, "DIRECCION": n_dir, "TELEFONO": n_tel, "DEUDA": 0.0}])
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, nuevo_c], ignore_index=True)
                    st.success(f"Registrado con éxito. ID: {new_id}")

    # --- MODULE: STOCK (ADMIN ONLY) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stock", clear_on_submit=True):
            a_n = st.text_input("PRODUCTO")
            a_s = st.number_input("STOCK", min_value=1)
            a_c = st.number_input("COSTO")
            a_p = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO": a_c, "PVP": a_p}])], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- MODULE: EXPENSES (ADMIN ONLY) ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("expenses"):
            cat = st.selectbox("CATEGORÍA", ["PALLETS", "OFICINA", "LOGISTICA", "VARIOS"])
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR GASTO"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

    # --- MODULE: REPORTS (ADMIN ONLY) ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.clients_db.to_excel(w, index=False, sheet_name='CARTERA')
            st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"JR31_MASTER_REPORT.xlsx")
        with col_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                p_bytes = generate_pdf_report()
                st.download_button("📥 DESCARGAR PDF", p_bytes, "JR31_Resumen.pdf")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
