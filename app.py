import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | SUPREME ERP", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V12.0 (EL MÁS IMPACTANTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Montserrat:wght@300;900&display=swap');
    
    /* Fondo General con Efecto de Malla Tecnológica */
    .stApp { 
        background: radial-gradient(circle at center, #1b263b 0%, #000000 100%);
        background-image: 
            linear-gradient(rgba(46, 139, 87, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(46, 139, 87, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        color: #e0e1dd !important; 
    }
    
    /* FIRMA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed; bottom: 15px; left: 20px;
        color: #2E8B57; font-family: 'Montserrat', sans-serif;
        font-size: 13px; z-index: 1000; line-height: 1.5; font-weight: 900;
        text-shadow: 0 0 5px rgba(46, 139, 87, 0.5);
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 32px; font-weight: 900; 
        text-shadow: 0 0 20px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP - TAMAÑO MONUMENTAL Y BRILLANTE */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif; 
        font-size: 13rem; /* TAMAÑO EXTREMO */
        font-weight: 900;
        background: linear-gradient(to bottom, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-top: 50px;
        margin-bottom: -20px;
        filter: drop-shadow(0 0 40px rgba(255,69,0,0.7));
        line-height: 0.8;
        letter-spacing: -8px;
        animation: pulse 3s infinite;
    }

    @keyframes pulse {
        0% { filter: drop-shadow(0 0 40px rgba(255,69,0,0.5)); }
        50% { filter: drop-shadow(0 0 60px rgba(46, 139, 87, 0.8)); }
        100% { filter: drop-shadow(0 0 40px rgba(255,69,0,0.5)); }
    }

    /* SUBTÍTULO SISTEMA */
    .subtitle-grande {
        text-align: center; 
        color: #FFFFFF; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 12px; 
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 50px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
    }

    /* Caja de Login Estilizada */
    .login-container {
        background: rgba(13, 27, 42, 0.8);
        padding: 50px;
        border-radius: 40px;
        border: 2px solid #FF4500;
        box-shadow: 0 0 50px rgba(0,0,0,0.9), inset 0 0 20px rgba(255,69,0,0.2);
        backdrop-filter: blur(15px);
    }

    /* Inputs que brillan */
    input {
        background-color: #0b0d17 !important;
        color: #FFFFFF !important;
        border: 2px solid #415a77 !important;
        font-size: 1.4rem !important;
        border-radius: 15px !important;
        height: 65px !important;
        transition: 0.3s !important;
    }
    input:focus {
        border: 2px solid #2E8B57 !important;
        box-shadow: 0 0 20px rgba(46, 139, 87, 0.6) !important;
    }

    /* Botón ACCEDER Imponente */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 20px !important; border: none !important;
        height: 4.5em !important; width: 100%; transition: 0.5s;
        font-size: 2.2rem !important;
        margin-top: 40px;
        box-shadow: 0 10px 40px rgba(255, 69, 0, 0.4) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 70px #2E8B57 !important; 
        transform: scale(1.03) translateY(-5px); 
    }

    /* Sidebar y Dashboard */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF4500; }
    .dash-card {
        background: rgba(27, 38, 59, 0.9);
        border-radius: 30px; padding: 40px;
        border-bottom: 8px solid #2E8B57;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: center;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 4.5rem; font-weight: 900; color: #FFFFFF; }
    
    header, footer, #MainMenu { visibility: hidden; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
def check_db():
    if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
    if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
    if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'es_admin' not in st.session_state: st.session_state.es_admin = False
    if 'log' not in st.session_state: st.session_state.log = False

check_db()

# --- FUNCIÓN PDF ---
def exportar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.ln(10)
    v = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, f"TOTAL VENTAS: ${v:,.2f} MXN", ln=True)
    return pdf.output()

# --- INTERFAZ DE ACCESO ---
if not st.session_state.log:
    # LOGO GIGANTE
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-grande">SISTEMA DE ADMINISTRACIÓN Y VENTA JR31</p>', unsafe_allow_html=True)
    
    col_l, col_f, col_r = st.columns([0.7, 1, 0.7])
    with col_f:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        u = st.text_input("ADMIN ID")
        p = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if u == "admin_jr31" and p == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DATOS INVÁLIDOS")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ PRINCIPAL ---
    with st.sidebar:
        st.markdown("<h1 style='color: #FF4500; font-family: Orbitron; text-align: center; font-size: 1.5rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("---")
        if not st.session_state.es_admin:
            cod = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if cod == "291329": st.session_state.es_admin = True; st.rerun()
        else:
            st.success("🔒 ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.es_admin = False; st.rerun()
        
        mod = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin: mod += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.radio("MENÚ", mod)
        if st.button("SALIR DE LA APP"): st.session_state.log = False; st.rerun()

    # --- CONTENIDO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center; font-size: 4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="dash-card"><p class="metric-title">VENTAS TOTALES</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="dash-card"><p class="metric-title" style="color:#FF4500;">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Inventario vacío.")
        else:
            with st.form("v"):
                ps = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                cs = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cv = st.number_input("CANTIDAD", min_value=1)
                mo = st.selectbox("MODO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    dt = st.session_state.inv[st.session_state.inv['ARTICULO'] == ps].iloc[0]
                    tv = dt['PVP'] * cv
                    ut = (dt['PVP'] - dt['COSTO_ADQ']) * cv
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cs, "ARTICULO": ps, "TOTAL": tv, "UTILIDAD": ut, "MODO": mo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == ps, 'CANTIDAD'] -= cv
                    if mo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cs, 'SALDO_DEUDOR'] += tv
                    st.success("Venta Exitosa")

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["HISTORIAL", "NUEVO CLIENTE"])
        with t1:
            cl = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            dc = st.session_state.cli[st.session_state.cli['NOMBRE'] == cl].iloc[0]
            st.metric("DEUDA", f"${dc['SALDO_DEUDOR']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR ABONO"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cl, 'SALDO_DEUDOR'] -= ab
                st.rerun()
        with t2:
            n = st.text_input("NOMBRE")
            if st.button("GUARDAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()

    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("s"):
            ap = st.text_input("ARTÍCULO")
            cp = st.number_input("CANTIDAD", min_value=1)
            ca = st.number_input("COSTO ADQ")
            pv = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": ap, "CANTIDAD": cp, "COSTO_ADQ": ca, "PVP": pv}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF"):
            data = exportar_pdf()
            st.download_button("📥 DESCARGAR", data, "JR31_Reporte.pdf")
