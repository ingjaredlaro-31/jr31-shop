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

# --- 2. ESTILO SUPREME CYBER-LUXURY (CSS) ---
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
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .subtitle-exec {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; 
        color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; 
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 2rem !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* SIDEBAR EMOJIS GIGANTES */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.6rem !important; font-weight: 700 !important; margin-bottom: 15px; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px;
        border-top: 6px solid #FF8C00; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .metric-val { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; text-transform: uppercase; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN Y AUTO-REPARACIÓN DE DATOS ---
def maintenance_db():
    # Definimos columnas exactas
    inv_cols = ["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"]
    
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=inv_cols)
    else:
        # Forzar que existan las columnas para evitar el KeyError
        for col in inv_cols:
            if col not in st.session_state.inv_db.columns:
                st.session_state.inv_db[col] = 0.0

    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "MODO"])
    
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA", "LIMITE"])
        default_c = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0, "LIMITE": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)

    if 'abonos_db' not in st.session_state:
        st.session_state.abonos_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])

    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

maintenance_db()

# --- 4. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-exec">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. MENÚ LATERAL ---
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

    # --- 6. MÓDULOS ---

    # --- DASHBOARD (CORREGIDO SIN KEYERROR) ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        
        # Cálculos Blindados
        v_total = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        d_total = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        # Multiplicación segura: Stock * Costo en TJ
        inv_val = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="executive-card"><p class="metric-title">VENTAS TOTALES</p><p class="metric-val">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p class="metric-title">CARTERA PENDIENTE</p><p class="metric-val" style="color:#FF4500;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="executive-card"><p class="metric-title">INVERSIÓN STOCK</p><p class="metric-val" style="color:#2E8B57;">${inv_val:,.0f}</p></div>', unsafe_allow_html=True)

    # --- GESTIÓN STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with tab_a:
            with st.form("stk", clear_on_submit=True):
                col1, col2 = st.columns(2)
                art_n = col1.text_input("NOMBRE DEL ARTICULO")
                art_q = col2.number_input("CANTIDAD", min_value=1)
                art_u = col1.number_input("COSTO ORIGINAL (USA)")
                art_t = col2.number_input("COSTO REAL (TJ)")
                art_p = col1.number_input("PVP JR31 SHOP")
                if st.form_submit_button("GUARDAR"):
                    new_item = pd.DataFrame([{"ARTICULO": art_n, "STOCK": art_q, "COSTO_USA": art_u, "COSTO_TJ": art_t, "PVP_JR31": art_p, "VENDIDOS": 0}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
                    st.rerun()
        with tab_b:
            if not st.session_state.inv_db.empty:
                item_edit = st.selectbox("PRODUCTO A MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item_edit].index[0]
                with st.form("edit_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_tj = st.number_input("COSTO REAL TJ", value=float(st.session_state.inv_db.at[idx, 'COSTO_TJ']))
                    new_p = st.number_input("PVP JR31", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'COSTO_TJ'] = new_tj
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- CARTERA CLIENTES ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with t1:
            cl_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cl_f].iloc[0]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            abono = st.number_input("REGISTRAR PAGO", min_value=0.0)
            if st.button("APLICAR PAGO"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cl_f, 'DEUDA'] -= abono
                st.success("Abono aplicado."); st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos primero.")
        else:
            search_v = st.text_input("🔍 BUSCAR ARTÍCULO")
            filtered = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search_v, case=False)]
            with st.form("venta"):
                p = st.selectbox("PRODUCTO", filtered['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("CONCLUIR VENTA"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p].iloc[0]
                    total = row['PVP_JR31'] * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": total}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == p, 'STOCK'] -= qt
                    st.success(f"Venta registrada por ${total}"); st.rerun()

# --- FOOTER CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
