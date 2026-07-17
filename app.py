import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR DE ALTO NIVEL ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO SUPREME EXECUTIVE V100 (CSS AGRESIVO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Fondo General con Malla de Ingeniería */
    .stApp { 
        background: radial-gradient(circle at center, #0a1f12 0%, #000000 100%);
        background-image: linear-gradient(rgba(46, 139, 87, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(46, 139, 87, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* NOMBRE DEL INGENIERO ARRIBA DERECHA - SIEMPRE VISIBLE */
    .jared-header {
        position: fixed; top: 10px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 9999;
    }

    /* LOGO JR 31 SHOP MONUMENTAL EN LA ENTRADA */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif;
        font-size: 15vw; /* TAMAÑO MASIVO */
        font-weight: 900;
        text-align: center;
        color: #FFFFFF;
        text-shadow: 0 0 30px #FF8C00, 0 0 60px #FF4500;
        margin-top: 50px;
        margin-bottom: -20px;
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; color: #FF8C00; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; font-weight: 900; font-size: 2.5rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* MENÚ LATERAL GIGANTE */
    [data-testid="stSidebar"] { 
        background-color: #0b0d17 !important; 
        border-right: 5px solid #FF8C00;
        min-width: 450px !important;
    }
    /* Estilo de los botones del menú */
    div[role="radiogroup"] label {
        font-size: 2rem !important; /* LETRAS XL */
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin-bottom: 30px !important;
        padding: 15px !important;
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
    }
    div[role="radiogroup"] label:hover { background: #FF8C00 !important; color: black !important; }

    /* DASHBOARD CARDS DE ALTO IMPACTO */
    .exec-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px; padding: 35px;
        text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border-left: 10px solid #FF8C00;
        margin-bottom: 20px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 80px !important; }
    input { color: #FFFFFF !important; font-size: 2rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.3); padding-top: 30px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS (PROTECCIÓN TOTAL) ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'cart' not in st.session_state: st.session_state.cart = []
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. MOTOR PDF ---
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.ln(10)
    v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"TOTAL VENTAS: ${v:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"ING JARED LARO - SISTEMA ERP", ln=True)
    return pdf.output()

# --- 5. ACCESO AL SISTEMA ---
if not st.session_state.auth:
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- 6. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 INICIO / DASHBOARD"): st.session_state.nav = "📊 DASHBOARD"; st.rerun()
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CLAVE MAESTRA", type="password")
            if st.button("ACTIVAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MÓDULOS ---

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_t = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">🛒 VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">💰 GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">👥 CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📦 PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📉 INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">🇺🇸 COSTO USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- STOCK (EDITAR Y ELIMINAR) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📥 ALTA", "✏️ EDITAR/BORRAR"])
        with t1:
            with st.form("add"):
                n = st.text_input("ARTICULO"); s = st.number_input("STOCK", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with t2:
            if not st.session_state.inv_db.empty:
                ed = st.selectbox("PRODUCTO:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("💾 ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
                    if c2.form_submit_button("🗑️ ELIMINAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_v, t_a = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with t_v:
            cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.rerun()
        with t_a:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        bus = st.text_input("🔍 BUSCAR ARTÍCULO")
        filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(bus, case=False)]
        with st.form("v"):
            p = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
            cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            qt = st.number_input("CANTIDAD", min_value=1)
            if st.form_submit_button("VENDER"):
                row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p].iloc[0]
                t = row['PVP_JR31'] * qt
                st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": t, "UTILIDAD": (row['PVP_JR31']-row['COSTO_TJ'])*qt}])], ignore_index=True)
                st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                st.success("Venta realizada.")

    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": "VARIOS", "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

    # --- REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
        st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), "JR31_MASTER.xlsx")

# --- 8. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
