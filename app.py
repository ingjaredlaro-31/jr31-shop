import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", initial_sidebar_state="expanded")

# --- 2. SUPREME LUXURY STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    .shop-logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 13vw; font-weight: 900; text-align: center;
        color: #FFFFFF; margin-top: 30px; margin-bottom: -15px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 400px !important; }
    div[role="radiogroup"] label { font-size: 1.8rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATA INITIALIZATION (LOCAL BRAIN) ---
def start_app():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

start_app()

# --- 4. ACCESS SCREEN ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    
    # MALETÍN DE RECUPERACIÓN (SI SE BORRÓ TODO)
    with st.expander("💾 RECOBRAR MI INFORMACIÓN (SUBIR RESPALDO)"):
        uploaded_file = st.file_uploader("Suba su último Excel guardado", type="xlsx")
        if uploaded_file:
            try:
                all_data = pd.read_excel(uploaded_file, sheet_name=None)
                st.session_state.inv_db = all_data.get('STOCK', st.session_state.inv_db)
                st.session_state.clients_db = all_data.get('CARTERA', st.session_state.clients_db)
                st.session_state.sales_db = all_data.get('VENTAS', st.session_state.sales_db)
                st.success("✅ ¡INFORMACIÓN RECUPERADA EXITOSAMENTE!")
            except:
                st.error("Archivo no compatible.")

    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:2rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 INICIO / DASHBOARD"): st.session_state.page = "📊 DASHBOARD"
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "💾 RESPALDOS"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULOS ---

    # RESPALDOS (EL MÁS IMPORTANTE PARA USTED)
    if nav == "💾 RESPALDOS":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CENTRO DE SEGURIDAD DE DATOS</h1>", unsafe_allow_html=True)
        st.info("Descargue su respaldo al final del día. Si la app se borra, súbalo aquí mismo para recuperar todo.")
        
        # DESCARGAR
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.clients_db.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR MI MALETÍN JR31 (EXCEL)", buf.getvalue(), f"Respaldo_JR31_{datetime.now().strftime('%d%m%y')}.xlsx")
        
        # SUBIR
        st.markdown("---")
        st.subheader("Subir archivo para restaurar")
        up = st.file_uploader("Cargar respaldo", type="xlsx", key="restore")
        if up:
            all_d = pd.read_excel(up, sheet_name=None)
            st.session_state.inv_db = all_d.get('STOCK', st.session_state.inv_db)
            st.session_state.clients_db = all_d.get('CARTERA', st.session_state.clients_db)
            st.session_state.sales_db = all_d.get('VENTAS', st.session_state.sales_db)
            st.success("DATOS RESTAURADOS.")

    # DASHBOARD
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">DEUDA CARTERA</p><p class="metric-value" style="color:#2E8B57;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)

    # STOCK (AÑADIR Y EDITAR)
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📥 ALTA", "✏️ EDITAR/BORRAR"])
        with t1:
            with st.form("stk"):
                a = st.text_input("ARTICULO"); s = st.number_input("STOCK", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with t2:
            if not st.session_state.inv_db.empty:
                ed_it = st.selectbox("PRODUCTO:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed_it].index[0]
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

    # TERMINAL VENTA
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL</h1>", unsafe_allow_html=True)
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
                st.success(f"Venta de ${t} realizada.")

# --- 7. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
