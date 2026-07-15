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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    .shop-logo-colossal {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: -20px;
        filter: drop-shadow(0 15px 40px rgba(0,0,0,0.9));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2rem;
        margin-bottom: 50px; text-transform: uppercase; text-shadow: 0 0 10px rgba(46, 139, 87, 0.5);
    }

    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 75px !important;
    }
    
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron', sans-serif !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
        font-size: 2rem !important; text-transform: uppercase;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; line-height: 1.6; width: 100%;
        border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.1rem; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF4500; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. AUTHENTICATION ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-colossal">JR 31 SHOP</p>', unsafe_allow_html=True)
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
        if st.button("SALIR DE LA APP"): st.session_state.auth = False; st.rerun()

    # --- MODULE: GESTIÓN STOCK (CON EDITOR PROFESIONAL) ---
    if nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL MAESTRO DE INVENTARIO</h1>", unsafe_allow_html=True)
        
        tab_new, tab_edit = st.tabs(["📥 AÑADIR NUEVO", "✏️ EDITAR / CORREGIR"])
        
        with tab_new:
            with st.form("stock_add", clear_on_submit=True):
                a_n = st.text_input("NOMBRE DEL PRODUCTO")
                a_s = st.number_input("CANTIDAD INICIAL", min_value=0)
                a_c = st.number_input("COSTO DE ADQUISICIÓN")
                a_p = st.number_input("PVP (PRECIO DE VENTA)")
                if st.form_submit_button("GUARDAR EN STOCK"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a_n, "STOCK": a_s, "COSTO": a_c, "PVP": a_p}])], ignore_index=True)
                    st.success("Registrado.")

        with tab_edit:
            if st.session_state.inv_db.empty:
                st.info("No hay productos para editar.")
            else:
                edit_item = st.selectbox("SELECCIONAR PRODUCTO PARA MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == edit_item].index[0]
                
                with st.form("stock_edit"):
                    col1, col2 = st.columns(2)
                    new_name = col1.text_input("CORREGIR NOMBRE", value=st.session_state.inv_db.at[idx, 'ARTICULO'])
                    new_stock = col2.number_input("CORREGIR STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_cost = col1.number_input("CORREGIR COSTO", value=float(st.session_state.inv_db.at[idx, 'COSTO']))
                    new_pvp = col2.number_input("CORREGIR PVP", value=float(st.session_state.inv_db.at[idx, 'PVP']))
                    
                    c_edit, c_del = st.columns(2)
                    if c_edit.form_submit_button("ACTUALIZAR CAMBIOS"):
                        st.session_state.inv_db.at[idx, 'ARTICULO'] = new_name
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_stock
                        st.session_state.inv_db.at[idx, 'COSTO'] = new_cost
                        st.session_state.inv_db.at[idx, 'PVP'] = new_pvp
                        st.success("Información actualizada.")
                        st.rerun()
                    
                    if c_del.form_submit_button("🗑️ ELIMINAR PRODUCTO"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.warning("Producto eliminado.")
                        st.rerun()

        st.markdown("---")
        st.subheader("VISTA PREVIA DEL INVENTARIO")
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- MODULO: TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en STOCK.")
        else:
            with st.form("pos"):
                it = st.selectbox("ARTÍCULO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    t = row['PVP'] * qt
                    u = (row['PVP'] - row['COSTO']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": t, "UTILIDAD": u}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO": st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl, 'DEUDA'] += t
                    st.success(f"Venta registrada: ${t}")

    # --- OTROS MÓDULOS (VERSION COMPLETA) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_exp, t_new = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_exp:
            cl_f = st.selectbox("BUSCAR", st.session_state.client_base['NOMBRE'])
            dat = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == cl_f].iloc[0]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl_f, 'DEUDA'] -= ab
                st.rerun()
        with t_new:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELEFONO")
                if st.form_submit_button("GUARDAR"):
                    new_id = f"JR31-{len(st.session_state.client_base):03d}"
                    st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"ID": new_id, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.metric("VENTAS TOTALES", f"${v:,.2f}")

# --- PIE DE PÁGINA CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
