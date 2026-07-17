import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from streamlit_gsheets import GSheetsConnection
import io
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | SUPREME SYSTEM", layout="wide", initial_sidebar_state="expanded")

# --- 2. ESTILO SUPREME CYBER-EXECUTIVE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #0a2114 0%, #000000 100%); background-attachment: fixed; color: #FFFFFF !important; }
    
    .jared-header { position: absolute; top: 15px; right: 40px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000; }

    .logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 380px !important; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 20px !important; }

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
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN A GOOGLE SHEETS (PARA QUE NUNCA SE BORRE NADA) ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    def sync_read(sheet):
        df = conn.read(worksheet=sheet, ttl="1s")
        return df.dropna(how="all")

    def sync_write(df, sheet):
        conn.update(worksheet=sheet, data=df)
        st.cache_data.clear()
except Exception as e:
    st.error(f"Error de conexión a la nube: {e}")
    st.stop()

# --- 4. ACCESO ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PERSISTENTE</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. CARGA DE DATOS REALES ---
    inv_db = sync_read("INVENTARIO")
    sales_db = sync_read("VENTAS")
    clients_db = sync_read("CLIENTES")
    expenses_db = sync_read("GASTOS")

    # --- 6. MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CODIGO MAESTRO", type="password")
            if st.button("ACTIVAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO"); 
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 VENTAS POS", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("🚪 SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_total = sales_db['TOTAL'].sum() if not sales_db.empty else 0
        u_total = sales_db['UTILIDAD'].sum() if not sales_db.empty else 0
        d_total = clients_db['DEUDA'].sum() if not clients_db.empty else 0
        pzs = inv_db['STOCK'].sum() if not inv_db.empty else 0
        inv_tj = (inv_db['STOCK'] * inv_db['COSTO_TJ']).sum() if not inv_db.empty else 0
        inv_usa = (inv_db['STOCK'] * inv_db['COSTO_USA']).sum() if not inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)
        
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">INV. TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">VALOR USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 8. CARTERA (REPARADO Y PROFESIONAL) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            if not clients_db.empty:
                cf = st.selectbox("CLIENTE", clients_db['NOMBRE'])
                dat = clients_db[clients_db['NOMBRE'] == cf].iloc[0]
                idx_c = clients_db[clients_db['NOMBRE'] == cf].index[0]
                st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                ab = st.number_input("ABONAR", min_value=0.0)
                if st.button("PAGAR"):
                    clients_db.at[idx_c, 'DEUDA'] -= ab
                    sync_write(clients_db, "CLIENTES")
                    st.success("Pago guardado en la nube."); st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(clients_db):03d}"
                    new_c = pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])
                    sync_write(pd.concat([clients_db, new_c], ignore_index=True), "CLIENTES")
                    st.rerun()

    # --- 9. STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            col1, col2 = st.columns(2)
            art = col1.text_input("ARTÍCULO")
            can = col2.number_input("CANTIDAD", min_value=1)
            ctj = col1.number_input("COSTO TJ")
            cusa = col2.number_input("COSTO USA")
            pvp = col1.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR EN NUBE"):
                new_p = pd.DataFrame([{"ARTICULO": art, "STOCK": can, "COSTO_USA": cusa, "COSTO_TJ": ctj, "PVP_JR31": pvp, "VENDIDOS": 0}])
                sync_write(pd.concat([inv_db, new_p], ignore_index=True), "INVENTARIO")
                st.success("Inventario actualizado."); st.rerun()
        st.dataframe(inv_db, use_container_width=True)

    # --- 10. GASTOS (ADMIN) ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO (PALLETS, LUZ, ETC)"); mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR GASTO"):
                new_g = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": "VARIOS", "CONCEPTO": con, "MONTO": mon}])
                sync_write(pd.concat([expenses_db, new_g], ignore_index=True), "GASTOS")
                st.rerun()
        st.dataframe(expenses_db)

    # --- 11. REPORTES (ADMIN) ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES MASTER</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            inv_db.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), "JR31_MASTER.xlsx")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
