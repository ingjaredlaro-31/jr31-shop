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

# --- 2. ESTILO CYBER-LUXURY (VERDE, NARANJA Y BLANCO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* NOMBRE SUPERIOR DERECHO */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP MONUMENTAL */
    .nombre-tienda-gigante {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO SOLICITADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron', sans-serif !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
        font-size: 2rem !important; text-transform: uppercase;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE BASES DE DATOS (COLUMNAS SOLICITADAS) ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=[
        "ARTICULO", 
        "STOCK", 
        "COSTO_ORIGINAL_TIENDA", 
        "PRECIO_EN_TJ", 
        "PVP_JR31_SHOP"
    ])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "GANANCIA"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR", "DEUDA": 0.0}])
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. PANTALLA DE ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="nombre-tienda-gigante">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:1.5rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("CERRAR SESIÓN"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULO: GESTIÓN STOCK (CORREGIDO) ---
    if nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO Y COSTOS</h1>", unsafe_allow_html=True)
        t_add, t_edit = st.tabs(["📥 ALTA DE PRODUCTO", "✏️ EDITAR COSTOS Y STOCK"])
        
        with t_add:
            with st.form("add_form", clear_on_submit=True):
                n = st.text_input("NOMBRE DEL ARTÍCULO")
                s = st.number_input("STOCK (PIEZAS)", min_value=1)
                co = st.number_input("COSTO ORIGINAL EN TIENDA (USA)")
                ptj = st.number_input("PRECIO EN TJ (COSTO REAL)")
                pvp = st.number_input("PRECIO DE VENTA AL PUBLICO JR31 SHOP")
                if st.form_submit_button("GUARDAR ARTÍCULO"):
                    new_item = pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_ORIGINAL_TIENDA": co, "PRECIO_EN_TJ": ptj, "PVP_JR31_SHOP": pvp}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
                    st.success("Guardado."); st.rerun()

        with t_edit:
            if not st.session_state.inv_db.empty:
                item_sel = st.selectbox("PRODUCTO A MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item_sel].index[0]
                
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    up_s = col1.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    up_co = col2.number_input("COSTO ORIGINAL USA", value=float(st.session_state.inv_db.at[idx, 'COSTO_ORIGINAL_TIENDA']))
                    up_tj = col1.number_input("PRECIO EN TJ", value=float(st.session_state.inv_db.at[idx, 'PRECIO_EN_TJ']))
                    up_pvp = col2.number_input("PVP JR31", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31_SHOP']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = up_s
                        st.session_state.inv_db.at[idx, 'COSTO_ORIGINAL_TIENDA'] = up_co
                        st.session_state.inv_db.at[idx, 'PRECIO_EN_TJ'] = up_tj
                        st.session_state.inv_db.at[idx, 'PVP_JR31_SHOP'] = up_pvp
                        st.success("Actualizado."); st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 7. MÓDULO: TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en Gestión Stock.")
        else:
            with st.form("pos"):
                it = st.selectbox("ARTÍCULO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total = row['PVP_JR31_SHOP'] * qt
                    uti = (row['PVP_JR31_SHOP'] - row['PRECIO_EN_TJ']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "TOTAL": total, "GANANCIA": uti}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    st.success(f"Venta registrada: ${total}")

    # --- 8. DASHBOARD ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        inv = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['PRECIO_EN_TJ']).sum() if not st.session_state.inv_db.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.metric("VENTAS TOTALES", f"${v:,.2f}")
        with c2: st.metric("CAPITAL EN STOCK (PRECIO TJ)", f"${inv:,.2f}")

# --- PIE DE PÁGINA CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
