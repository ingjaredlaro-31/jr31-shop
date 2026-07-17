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

# --- 2. ESTILO SUPREME EXECUTIVE (CSS) ---
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

    .logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 11vw; font-weight: 900; text-align: center;
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

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 350px !important; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 2.8rem; font-weight: 900; color: #FFFFFF; }

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

# --- 3. INICIALIZACIÓN DE DATOS (AUTO-REPARABLE) ---
def init_all_data():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_all_data()

# --- 4. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
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
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:1.5rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 DASHBOARD / INICIO"): st.session_state.nav_choice = "📊 DASHBOARD"
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): 
            st.session_state.auth = False
            st.rerun()

    # --- 6. DASHBOARD ---
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

    # --- 7. CARTERA (CON EDICIÓN Y BORRADO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA Y EXPEDIENTES</h1>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE", "✏️ EDITAR/BORRAR"])
        with t1:
            cf = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()
        with t3:
            if st.session_state.is_admin:
                cli_edit = st.selectbox("EDITAR CLIENTE:", st.session_state.clients_db['NOMBRE'])
                idx_c = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cli_edit].index[0]
                with st.form("ed_cli"):
                    en = st.text_input("NOMBRE", value=st.session_state.clients_db.at[idx_c, 'NOMBRE'])
                    ed = st.text_input("DIRECCIÓN", value=st.session_state.clients_db.at[idx_c, 'DIRECCION'])
                    et = st.text_input("TELÉFONO", value=st.session_state.clients_db.at[idx_c, 'TELEFONO'])
                    if st.form_submit_button("ACTUALIZAR DATOS"):
                        st.session_state.clients_db.at[idx_c, 'NOMBRE'] = en
                        st.session_state.clients_db.at[idx_c, 'DIRECCION'] = ed
                        st.session_state.clients_db.at[idx_c, 'TELEFONO'] = et
                        st.rerun()
                    if st.form_submit_button("🗑️ ELIMINAR CLIENTE"):
                        st.session_state.clients_db = st.session_state.clients_db.drop(idx_c).reset_index(drop=True)
                        st.rerun()

    # --- 8. GESTIÓN STOCK (CON EDICIÓN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR / BORRAR"])
        with tab_a:
            with st.form("stk"):
                a = st.text_input("ARTICULO"); s = st.number_input("STOCK", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p}])], ignore_index=True)
                    st.rerun()
        with tab_b:
            if not st.session_state.inv_db.empty:
                ed_it = st.selectbox("PRODUCTO:", st.session_state.inv_db['ARTICULO'])
                idx_e = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed_it].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx_e, 'STOCK']))
                    new_cu = st.number_input("COSTO USA", value=float(st.session_state.inv_db.at[idx_e, 'COSTO_USA']))
                    new_ct = st.number_input("COSTO TJ", value=float(st.session_state.inv_db.at[idx_e, 'COSTO_TJ']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx_e, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx_e, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx_e, 'COSTO_USA'] = new_cu
                        st.session_state.inv_db.at[idx_e, 'COSTO_TJ'] = new_ct
                        st.session_state.inv_db.at[idx_e, 'PVP_JR31'] = new_p
                        st.rerun()
                    if st.form_submit_button("🗑️ ELIMINAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx_e).reset_index(drop=True)
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 9. GASTOS (CON EDICIÓN Y BORRADO) ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        total_g = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        st.markdown(f'<div class="exec-card"><p class="metric-title">TOTAL GASTADO</p><p class="metric-value" style="color:#FF4500;">${total_g:,.2f}</p></div>', unsafe_allow_html=True)

        t_g1, t_g2 = st.tabs(["📥 REGISTRAR", "✏️ MODIFICAR/BORRAR"])
        with t_g1:
            with st.form("g"):
                con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
                    st.rerun()
        with t_g2:
            if not st.session_state.expenses_db.empty:
                idx_g = st.selectbox("SELECCIONAR GASTO:", st.session_state.expenses_db.index, format_func=lambda x: f"{st.session_state.expenses_db.at[x, 'CONCEPTO']} (${st.session_state.expenses_db.at[x, 'MONTO']})")
                with st.form("ed_g"):
                    gc = st.text_input("CONCEPTO", value=st.session_state.expenses_db.at[idx_g, 'CONCEPTO'])
                    gm = st.number_input("MONTO", value=float(st.session_state.expenses_db.at[idx_g, 'MONTO']))
                    if st.form_submit_button("ACTUALIZAR GASTO"):
                        st.session_state.expenses_db.at[idx_g, 'CONCEPTO'] = gc
                        st.session_state.expenses_db.at[idx_g, 'MONTO'] = gm
                        st.rerun()
                    if st.form_submit_button("🗑️ BORRAR GASTO"):
                        st.session_state.expenses_db = st.session_state.expenses_db.drop(idx_g).reset_index(drop=True)
                        st.rerun()
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

    # --- 10. TERMINAL VENTA ---
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
                uti = (row['PVP_JR31'] - row['COSTO_TJ']) * qt
                st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": p, "TOTAL": t, "UTILIDAD": uti}])], ignore_index=True)
                st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                st.success("Venta realizada.")

    # --- 11. REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        
        st.subheader("Historial de Ventas (Auditoría)")
        if not st.session_state.sales_db.empty:
            idx_v = st.selectbox("VER O BORRAR VENTA:", st.session_state.sales_db.index, format_func=lambda x: f"{st.session_state.sales_db.at[x, 'FECHA']} - {st.session_state.sales_db.at[x, 'CLIENTE']} (${st.session_state.sales_db.at[x, 'TOTAL']})")
            if st.button("🗑️ ANULAR VENTA SELECCIONADA"):
                st.session_state.sales_db = st.session_state.sales_db.drop(idx_v).reset_index(drop=True)
                st.rerun()
            st.dataframe(st.session_state.sales_db, use_container_width=True)

        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
            st.session_state.clients_db.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR EXCEL MASTER", buf.getvalue(), "JR31_MASTER.xlsx")

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
