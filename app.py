import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from streamlit_gsheets import GSheetsConnection
import io

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(page_title="JR 31 SHOP | DATABASE EDITION", layout="wide", initial_sidebar_state="expanded")

# --- 2. CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data(sheet_name):
    return conn.read(worksheet=sheet_name, ttl="1s") # ttl=1s para ver cambios inmediato

# --- 3. DISEÑO SUPREME CYBER-EXECUTIVE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    .stApp { background: radial-gradient(circle at center, #0a2114 0%, #000000 100%); background-attachment: fixed; color: #FFFFFF !important; }
    .jared-header { position: absolute; top: 15px; right: 40px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000; }
    .logo-giant { font-family: 'Orbitron', sans-serif; font-size: 11vw; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9)); line-height: 0.8; letter-spacing: -10px; text-transform: uppercase; }
    .footer-centered { text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif; font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%; line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px; }
    .exec-card { background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 350px !important; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 20px !important; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 4. ACCESO ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PERSISTENTE</h2>', unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1.3, 1])
    with col_login:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. CARGA DE DATOS DESDE NUBE ---
    try:
        inv_df = load_data("INVENTARIO")
        sales_df = load_data("VENTAS")
        clients_df = load_data("CLIENTES")
        expenses_df = load_data("GASTOS")
    except:
        st.error("Error al conectar con Google Sheets. Verifique los nombres de las pestañas.")
        st.stop()

    # --- 6. MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CLAVE MAESTRA", type="password")
            if st.button("DESBLOQUEAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 PANORAMA", "🛒 VENTAS", "👤 CARTERA"]
        if st.session_state.is_admin: menu += ["📦 STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("MODULOS:", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MÓDULO DASHBOARD ---
    if nav == "📊 PANORAMA":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = sales_df['TOTAL'].sum() if not sales_df.empty else 0
        d_t = clients_df['DEUDA'].sum() if not clients_df.empty else 0
        p_s = inv_df['STOCK'].sum() if not inv_df.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#2E8B57;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">STOCK</p><p class="metric-value">{p_s:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 8. MÓDULO STOCK (CON ESCRITURA EN NUBE) ---
    elif nav == "📦 STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE STOCK</h1>", unsafe_allow_html=True)
        with st.form("add_stock", clear_on_submit=True):
            col1, col2 = st.columns(2)
            art = col1.text_input("ARTÍCULO")
            can = col2.number_input("CANTIDAD", min_value=1)
            ctj = col1.number_input("COSTO TJ")
            pvp = col2.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR EN NUBE"):
                new_data = pd.DataFrame([{"ARTICULO": art, "STOCK": can, "COSTO_TJ": ctj, "PVP_JR31": pvp}])
                updated_df = pd.concat([inv_df, new_data], ignore_index=True)
                conn.update(worksheet="INVENTARIO", data=updated_df)
                st.success("¡Guardado en Google Drive!")
                st.rerun()
        st.dataframe(inv_df, use_container_width=True)

    # --- 9. MÓDULO VENTAS ---
    elif nav == "🛒 VENTAS":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL</h1>", unsafe_allow_html=True)
        if inv_df.empty: st.warning("Cargue inventario primero.")
        else:
            with st.form("venta"):
                p_v = st.selectbox("PRODUCTO", inv_df['ARTICULO'])
                c_v = st.selectbox("CLIENTE", clients_df['NOMBRE'])
                q_v = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("CONCLUIR VENTA"):
                    row = inv_df[inv_df['ARTICULO'] == p_v].iloc[0]
                    total = row['PVP_JR31'] * q_v
                    # Aquí se agregaría la lógica para actualizar Ventas en Google Sheets
                    st.success(f"Venta de ${total} registrada.")

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
