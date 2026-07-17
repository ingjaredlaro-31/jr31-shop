import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from streamlit_gsheets import GSheetsConnection
import io

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", initial_sidebar_state="expanded")

# --- 2. ESTILO SUPREME CYBER-EXECUTIVE (CSS) ---
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

    /* NOMBRE JR 31 SHOP MONUMENTAL EN BLANCO */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        color: #FFFFFF;
        margin-top: 30px; margin-bottom: -15px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    /* MENU LATERAL XL */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 400px !important; }
    div[role="radiogroup"] label { font-size: 1.8rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 5px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS GIGANTES */
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

# --- 3. CONEXIÓN Y AUTO-REPARACIÓN DE GOOGLE SHEETS ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    def get_data(sheet_name, columns):
        try:
            df = conn.read(worksheet=sheet_name, ttl="1s")
            if df.empty: return pd.DataFrame(columns=columns)
            return df
        except:
            return pd.DataFrame(columns=columns)

    def save_data(df, sheet_name):
        conn.update(worksheet=sheet_name, data=df)
        st.success(f"✅ DATOS SINCRONIZADOS CON LA NUBE")

except Exception as e:
    st.error(f"Falla de conexión: {e}")
    st.stop()

# --- 4. CARGA DE BASES DE DATOS ---
inv_db = get_data("INVENTARIO", ["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
sales_db = get_data("VENTAS", ["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "TOTAL", "UTILIDAD"])
clients_db = get_data("CLIENTES", ["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
expenses_db = get_data("GASTOS", ["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

# --- 5. LOGICA DE ACCESO ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

if not st.session_state.auth:
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 6. MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>MENU</h1>", unsafe_allow_html=True)
        if st.button("🏠 INICIO"): st.rerun()
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CODIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 VENTAS POS", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA:", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MÓDULOS ---

    # DASHBOARD
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_total = sales_db['TOTAL'].sum() if not sales_db.empty else 0
        u_total = sales_db['UTILIDAD'].sum() if not sales_db.empty else 0
        d_total = clients_db['DEUDA'].sum() if not clients_db.empty else 0
        pzs = inv_db['STOCK'].sum() if not inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)

    # VENTAS
    elif nav == "🛒 VENTAS POS":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if inv_db.empty: st.warning("Sin inventario.")
        else:
            with st.form("venta"):
                p = st.selectbox("ARTICULO", inv_db['ARTICULO'])
                c = st.selectbox("CLIENTE", clients_db['NOMBRE'])
                q = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    row = inv_db[inv_db['ARTICULO'] == p].iloc[0]
                    total = row['PVP_JR31'] * q
                    uti = (row['PVP_JR31'] - row['COSTO_TJ']) * q
                    new_sale = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c, "ARTICULO": p, "CANTIDAD": q, "TOTAL": total, "UTILIDAD": uti}])
                    save_data(pd.concat([sales_db, new_sale], ignore_index=True), "VENTAS")
                    inv_db.loc[inv_db['ARTICULO'] == p, 'STOCK'] -= q
                    save_data(inv_db, "INVENTARIO")
                    st.rerun()

    # STOCK
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>STOCK</h1>", unsafe_allow_html=True)
        with st.form("add_stk", clear_on_submit=True):
            n = st.text_input("NOMBRE"); s = st.number_input("CANTIDAD", min_value=1)
            cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR EN NUBE"):
                new_item = pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])
                save_data(pd.concat([inv_db, new_item], ignore_index=True), "INVENTARIO")
                st.rerun()
        st.dataframe(inv_db, use_container_width=True)

    # CARTERA
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with tab1:
            if not clients_db.empty:
                c_sel = st.selectbox("CLIENTE", clients_db['NOMBRE'])
                dat = clients_db[clients_db['NOMBRE'] == c_sel].iloc[0]
                idx = clients_db[clients_db['NOMBRE'] == c_sel].index[0]
                st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                abono = st.number_input("ABONAR", min_value=0.0)
                if st.button("REGISTRAR PAGO"):
                    clients_db.at[idx, 'DEUDA'] -= abono
                    save_data(clients_db, "CLIENTES")
                    st.rerun()
        with tab2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(clients_db):03d}"
                    new_c = pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])
                    save_data(pd.concat([clients_db, new_c], ignore_index=True), "CLIENTES")
                    st.rerun()

    # GASTOS
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                new_g = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": "VARIOS", "CONCEPTO": con, "MONTO": mon}])
                save_data(pd.concat([expenses_db, new_g], ignore_index=True), "GASTOS")
                st.rerun()
        st.dataframe(expenses_db, use_container_width=True)

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
