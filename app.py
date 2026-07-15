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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
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

    /* LOGO JR 31 SHOP MONUMENTAL (WHITE & BOLD) */
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 15vw; /* MONUMENTAL */
        font-weight: 900;
        text-align: center;
        color: #FFFFFF; /* PURE WHITE */
        margin-top: 30px;
        margin-bottom: -15px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .subtitle-executive {
        text-align: center; color: #FF8C00; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    div[role="radiogroup"] label {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 15px;
    }

    /* XL INPUTS & BUTTONS */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 75px !important;
    }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
        font-size: 2rem !important; text-transform: uppercase;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* PIE DE PÁGINA CENTRADO SOLICITADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION ---
def start_db():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USD", "COSTO_REAL_MXN", "PVP"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

start_db()

# --- 4. ACCESS SCREEN ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-executive">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ID ADMIN")
        u_pw = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("ERROR")
else:
    # --- 5. NAVEGACIÓN ---
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

    # --- 6. MÓDULO: GESTIÓN STOCK (CON TRIPLE PRECIO) ---
    if nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE INVENTARIO Y PRECIOS</h1>", unsafe_allow_html=True)
        t_add, t_edit = st.tabs(["📥 ALTA DE PRODUCTO", "✏️ EDITAR COSTOS Y STOCK"])
        
        with t_add:
            with st.form("add_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                n = col1.text_input("NOMBRE DEL ARTÍCULO")
                s = col2.number_input("STOCK DISPONIBLE", min_value=1)
                cu = col1.number_input("COSTO ORIGINAL (USD)")
                cr = col2.number_input("COSTO REAL (MXN)")
                pvp = col1.number_input("PVP (VENTA FINAL MXN)")
                if st.form_submit_button("GUARDAR ARTÍCULO"):
                    new_item = pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USD": cu, "COSTO_REAL_MXN": cr, "PVP": pvp}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
                    st.success("Guardado en sistema.")
                    st.rerun()

        with t_edit:
            if not st.session_state.inv_db.empty:
                item_sel = st.selectbox("PRODUCTO A MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item_sel].index[0]
                
                with st.form("edit_form"):
                    st.subheader(f"Editando valores de: {item_sel}")
                    col_e1, col_e2 = st.columns(2)
                    upd_s = col_e1.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    upd_cu = col_e2.number_input("COSTO USD", value=float(st.session_state.inv_db.at[idx, 'COSTO_USD']))
                    upd_cr = col_e1.number_input("COSTO REAL MXN", value=float(st.session_state.inv_db.at[idx, 'COSTO_REAL_MXN']))
                    upd_p = col_e2.number_input("PVP FINAL", value=float(st.session_state.inv_db.at[idx, 'PVP']))
                    
                    btn_up, btn_del = st.columns(2)
                    if btn_up.form_submit_button("💾 ACTUALIZAR PRECIOS"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = upd_s
                        st.session_state.inv_db.at[idx, 'COSTO_USD'] = upd_cu
                        st.session_state.inv_db.at[idx, 'COSTO_REAL_MXN'] = upd_cr
                        st.session_state.inv_db.at[idx, 'PVP'] = upd_p
                        st.success("Precios actualizados."); st.rerun()
                    if btn_del.form_submit_button("🗑️ ELIMINAR ARTÍCULO"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.warning("Eliminado."); st.rerun()

        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 7. MÓDULO: TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en Gestión Stock.")
        else:
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total = row['PVP'] * qt
                    uti = (row['PVP'] - row['COSTO_REAL_MXN']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total, "UTILIDAD": uti}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl, 'DEUDA'] += total
                    st.success("Venta Exitosa")

    # --- 8. MÓDULO: CARTERA CLIENTES ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            cf = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
            dat = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == cf].iloc[0]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR31-{len(st.session_state.client_base):03d}"
                    st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- 9. DASHBOARD ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        inv = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_REAL_MXN']).sum() if not st.session_state.inv_db.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.metric("VENTAS", f"${v:,.2f}")
        with c2: st.metric("CAPITAL INVERTIDO (STOCK)", f"${inv:,.2f}")

# --- PIE DE PÁGINA CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
