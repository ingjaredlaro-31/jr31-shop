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

    /* LOGO JR 31 SHOP MONUMENTAL */
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .subtitle-executive {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* SIDEBAR EMOJIS GIGANTES */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    div[role="radiogroup"] label {
        font-size: 1.6rem !important; /* ICONOS GIGANTES */
        font-weight: 700 !important;
        margin-bottom: 15px;
    }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; 
        color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; 
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important;
        border-radius: 8px !important;
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
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION (LOGIC IN ENGLISH) ---
def start_database():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_REAL", "ORIGINAL_USD", "PVP_JR31", "VENDIDOS"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "GANANCIA_NETA", "TOTAL"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

start_database()

# --- 4. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-executive">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
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
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.auth = False
            st.rerun()

    # --- 6. MÓDULO: GESTIÓN STOCK (EDITOR CORREGIDO) ---
    if nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL MAESTRO DE INVENTARIO</h1>", unsafe_allow_html=True)
        tab_add, tab_edit = st.tabs(["📥 AÑADIR NUEVO PRODUCTO", "✏️ EDITAR / CORREGIR STOCK"])
        
        with tab_add:
            with st.form("add_product", clear_on_submit=True):
                col1, col2 = st.columns(2)
                name = col1.text_input("NOMBRE DEL ARTÍCULO")
                stock = col2.number_input("CANTIDAD INICIAL", min_value=1)
                cost = col1.number_input("COSTO REAL (MXN)")
                usd = col2.number_input("PRECIO ORIGINAL (USD)")
                pvp = col1.number_input("PRECIO JR31 (MXN)")
                if st.form_submit_button("GUARDAR EN BODEGA"):
                    new_item = pd.DataFrame([{"ARTICULO": name, "STOCK": stock, "COSTO_REAL": cost, "ORIGINAL_USD": usd, "PVP_JR31": pvp, "VENDIDOS": 0}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
                    st.success("Registrado correctamente.")
                    st.rerun()

        with tab_edit:
            if st.session_state.inv_db.empty:
                st.info("No hay productos registrados para editar.")
            else:
                edit_item = st.selectbox("SELECCIONAR PRODUCTO PARA MODIFICAR", st.session_state.inv_db['ARTICULO'])
                # Obtener el índice del producto seleccionado
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == edit_item].index[0]
                
                with st.form("edit_product"):
                    st.subheader(f"Editando: {edit_item}")
                    col_e1, col_e2 = st.columns(2)
                    upd_name = col_e1.text_input("NOMBRE", value=st.session_state.inv_db.at[idx, 'ARTICULO'])
                    upd_stock = col_e2.number_input("CANTIDAD EN STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    upd_cost = col_e1.number_input("COSTO REAL (MXN)", value=float(st.session_state.inv_db.at[idx, 'COSTO_REAL']))
                    upd_pvp = col_e2.number_input("PRECIO VENTA (MXN)", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    
                    btn_upd, btn_del = st.columns(2)
                    if btn_upd.form_submit_button("💾 ACTUALIZAR DATOS"):
                        st.session_state.inv_db.at[idx, 'ARTICULO'] = upd_name
                        st.session_state.inv_db.at[idx, 'STOCK'] = upd_stock
                        st.session_state.inv_db.at[idx, 'COSTO_REAL'] = upd_cost
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = upd_pvp
                        st.success("Cambios guardados con éxito.")
                        st.rerun()
                    
                    if btn_del.form_submit_button("🗑️ ELIMINAR ARTÍCULO"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.warning("Producto eliminado del sistema.")
                        st.rerun()

        st.markdown("---")
        st.subheader("VISTA PREVIA DEL INVENTARIO")
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 7. MÓDULO: CARTERA CLIENTES (REFORZADO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        
        with t1:
            if st.session_state.client_base.empty:
                st.info("Sin clientes registrados.")
            else:
                c_sel = st.selectbox("BUSCAR CLIENTE", st.session_state.client_base['NOMBRE'])
                dat = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == c_sel].iloc[0]
                
                c_c1, c_c2 = st.columns(2)
                with c_c1:
                    st.markdown(f"""<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #FF8C00;'>
                    <p style='color:#FF8C00; font-family:Orbitron;'>FICHA TÉCNICA:</p>
                    <p><b>ID:</b> {dat['ID']}</p><p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p><p><b>TEL:</b> {dat['TELEFONO']}</p></div>""", unsafe_allow_html=True)
                with c_c2:
                    st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
                    abono = st.number_input("REGISTRAR PAGO ($)", min_value=0.0)
                    if st.button("PAGAR"):
                        st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == c_sel, 'DEUDA'] -= abono
                        st.success("Abono aplicado."); st.rerun()

        with t2:
            with st.form("new_cl"):
                n = st.text_input("NOMBRE COMPLETO"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    new_id = f"JR31-{len(st.session_state.client_base):03d}"
                    st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"ID": new_id, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.success(f"ID Asignado: {new_id}"); st.rerun()

    # --- OTROS MÓDULOS (VENTA Y DASHBOARD) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos primero.")
        else:
            with st.form("v"):
                p = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p].iloc[0]
                    total = row['PVP_JR31'] * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": total}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                    st.success("Venta realizada.")

    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.markdown(f'<div class="executive-card"><p style="color:#FF8C00; font-family:Orbitron; font-size:2rem;">VENTAS</p><p style="font-size:6rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)

# --- 8. PIE DE PÁGINA CENTRADO SOLICITADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
