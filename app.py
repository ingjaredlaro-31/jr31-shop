import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO SUPREME LUXURY PLATINUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Fondo Obsidian & Emerald */
    .stApp { 
        background: radial-gradient(circle at center, #0d1a14 0%, #050505 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* NOMBRE DEL INGENIERO ARRIBA DERECHA */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* TITULO MONUMENTAL JR 31 SHOP */
    .shop-logo-main {
        font-family: 'Orbitron', sans-serif;
        font-size: 14vw;
        font-weight: 900;
        text-align: center;
        color: #FFFFFF; /* BLANCO PURO */
        text-shadow: 0 10px 30px rgba(255, 140, 0, 0.5);
        margin-top: 50px;
        margin-bottom: -20px;
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; color: #FF8C00; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; font-weight: 900; font-size: 2.2rem;
        margin-bottom: 60px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO PROFESIONAL */
    .footer-professional {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 120px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.3); padding-top: 30px;
    }
    .footer-professional b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    /* MENU LATERAL XL */
    [data-testid="stSidebar"] { 
        background-color: #0b0d17 !important; 
        border-right: 5px solid #FF8C00; 
        min-width: 400px !important; 
    }
    div[role="radiogroup"] label { 
        font-size: 1.8rem !important; 
        font-weight: 900; 
        color: #FFFFFF !important; 
        margin-bottom: 25px !important;
        padding: 10px;
        border-radius: 10px;
    }
    div[role="radiogroup"] label:hover { background: rgba(255, 140, 0, 0.1); }

    /* DASHBOARD CARDS */
    .metric-box {
        background: rgba(255, 255, 255, 0.04); border-radius: 20px; padding: 35px;
        text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); border-top: 5px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 12px !important; height: 80px !important; }
    input { color: #FFFFFF !important; font-size: 2rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 8px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS ---
def init_all():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_all()

# --- 4. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-main">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">BUSINESS INTELLIGENCE SYSTEM</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- 5. MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 DASHBOARD / INICIO"): st.rerun()
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CLAVE MAESTRA", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 PANORAMA", "🛒 VENTAS POS", "👤 CARTERA"]
        # Respaldo solo visible para Admin
        if st.session_state.is_admin: 
            menu += ["📦 STOCK", "💸 GASTOS", "💾 RESPALDO MASTER", "📝 REPORTES"]
        
        nav = st.sidebar.radio("NAVEGACIÓN:", menu)
        if st.button("🚪 SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULO: RESPALDO MAESTRO (SOLO ADMIN) ---
    if nav == "💾 RESPALDO MASTER" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CENTRO DE SEGURIDAD DE DATOS</h1>", unsafe_allow_html=True)
        
        col_down, col_up = st.columns(2)
        
        with col_down:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.subheader("📥 Exportar Datos")
            st.write("Descargue un archivo Excel con toda su información actual.")
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
                st.session_state.clients_db.to_excel(w, index=False, sheet_name='CARTERA')
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.download_button("DESCARGAR MI INVENTARIO", buf.getvalue(), f"Respaldo_JR31_{datetime.now().strftime('%d%m%y')}.xlsx")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_up:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.subheader("📤 Cargar / Actualizar")
            st.write("Suba un archivo Excel de respaldo para restaurar o actualizar el sistema.")
            up_file = st.file_uploader("Seleccione archivo .xlsx", type="xlsx")
            if up_file:
                try:
                    new_data = pd.read_excel(up_file, sheet_name=None)
                    if 'STOCK' in new_data: st.session_state.inv_db = new_data['STOCK']
                    if 'CARTERA' in new_data: st.session_state.clients_db = new_data['CARTERA']
                    if 'VENTAS' in new_data: st.session_state.sales_db = new_data['VENTAS']
                    st.success("✅ SISTEMA ACTUALIZADO EXITOSAMENTE.")
                except:
                    st.error("Error al leer el archivo.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 7. DASHBOARD ---
    elif nav == "📊 PANORAMA":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        p = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:5px solid #2E8B57;"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#2E8B57;">${d:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">STOCK</p><p class="metric-value">{p:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 8. STOCK (ADMIN) ---
    elif nav == "📦 STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE STOCK</h1>", unsafe_allow_html=True)
        t_a, t_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with t_a:
            with st.form("add"):
                n = st.text_input("ARTÍCULO"); s = st.number_input("CANTIDAD", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with t_b:
            if not st.session_state.inv_db.empty:
                ed = st.selectbox("EDITAR:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 9. TERMINAL VENTAS ---
    elif nav == "🛒 VENTAS POS":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL</h1>", unsafe_allow_html=True)
        bus = st.text_input("🔍 BUSCAR ARTÍCULO")
        filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(bus, case=False)]
        with st.form("v"):
            p = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
            cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            qt = st.number_input("CANTIDAD", min_value=1)
            if st.form_submit_button("VENDER"):
                row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p].iloc[0]
                total = row['PVP_JR31'] * qt
                st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": total, "UTILIDAD": (row['PVP_JR31']-row['COSTO_TJ'])*qt}])], ignore_index=True)
                st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                st.success(f"Venta de ${total} registrada.")

    # --- 10. CARTERA ---
    elif nav == "👤 CARTERA":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_exp, t_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_exp:
            cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.rerun()
        with t_new:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

# --- 11. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-professional">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
