import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. INITIALIZE ALL SESSION STATES (PREVENT ERRORS) ---
# Esto debe ir al principio para que los selectbox no fallen
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])

if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])

if 'client_base' not in st.session_state:
    # Creamos la base de clientes con los campos solicitados
    st.session_state.client_base = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    # Agregar cliente por defecto para ventas rápidas
    default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    st.session_state.client_base = pd.concat([st.session_state.client_base, default_c], ignore_index=True)

if 'abonos_db' not in st.session_state:
    st.session_state.abonos_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])

if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(page_title="SISTEMA JR31 | BY ING. JARED LARO", layout="wide")

# --- 3. SUPREME LUXURY STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    .shop-logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* INPUTS GIGANTES */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important; border-radius: 10px !important;
        height: 75px !important; margin-bottom: 10px !important;
    }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important; border: none !important;
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 2rem !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid #333;
        border-radius: 20px; padding: 40px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; line-height: 1.6; width: 100%;
        border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; }
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 4. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
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
    # --- 5. INTERNAL NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MODULES ---

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d = st.session_state.client_base['DEUDA'].sum() if not st.session_state.client_base.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:2rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p style="color:#2E8B57; font-family:Orbitron; font-size:2rem;">CARTERA</p><p style="font-size:6rem; font-weight:900;">${d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- POS (TERMINAL VENTA) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en GESTIÓN STOCK primero.")
        else:
            with st.form("pos_form"):
                it = st.selectbox("ARTÍCULO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("MODO PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR TRANSACCIÓN"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total_v = row['PVP'] * qt
                    uti = (row['PVP'] - row['COSTO']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total_v, "UTILIDAD": uti, "MODO": md}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl, 'DEUDA'] += total_v
                    st.success(f"Venta registrada por ${total_v}")

    # --- CLIENTS (CARTERA) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            cl_f = st.selectbox("BUSCAR CLIENTE", st.session_state.client_base['NOMBRE'])
            dat = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == cl_f].iloc[0]
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""<div style='border:1px solid #FF8C00; padding:20px; border-radius:10px;'>
                <p><b>ID:</b> {dat['ID']}</p><p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p><p><b>TEL:</b> {dat['TELEFONO']}</p>
                </div>""", unsafe_allow_html=True)
            with col_b:
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                ab = st.number_input("ABONAR", min_value=0.0)
                if st.button("REGISTRAR PAGO"):
                    st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl_f, 'DEUDA'] -= ab
                    st.success("Abono aplicado."); st.rerun()
            if not st.session_state.sales_db.empty:
                st.subheader("Historial de Compras")
                st.dataframe(st.session_state.sales_db[st.session_state.sales_db['CLIENTE'] == cl_f], use_container_width=True)

        with t2:
            with st.form("new_client"):
                n = st.text_input("NOMBRE COMPLETO"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    new_id = f"JR31-{len(st.session_state.client_base):03d}"
                    st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"ID": new_id, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.success(f"Registrado ID: {new_id}"); st.rerun()

    # --- STOCK (GESTIÓN STOCK CON EDITOR) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["AÑADIR", "EDITAR/CORREGIR"])
        with tab_a:
            with st.form("add"):
                n = st.text_input("PRODUCTO"); s = st.number_input("STOCK", min_value=1); c = st.number_input("COSTO"); p = st.number_input("PVP")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
                    st.rerun()
        with tab_b:
            if not st.session_state.inv_db.empty:
                edit_item = st.selectbox("PRODUCTO A MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == edit_item].index[0]
                with st.form("edit"):
                    new_n = st.text_input("NOMBRE", value=st.session_state.inv_db.at[idx, 'ARTICULO'])
                    new_s = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_c = st.number_input("COSTO", value=float(st.session_state.inv_db.at[idx, 'COSTO']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'ARTICULO'] = new_n
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_s
                        st.session_state.inv_db.at[idx, 'COSTO'] = new_c
                        st.session_state.inv_db.at[idx, 'PVP'] = new_p
                        st.success("Cambiado."); st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            cat = st.selectbox("CAT", ["PALLETS", "OFICINA", "LOGISTICA", "VARIOS"])
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

# --- PIE DE PÁGINA CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
