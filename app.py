import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR31 SHOP | FINANCIAL MASTER",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DISEÑO SUPREMO (VERDE, NARANJA Y BLANCO) ---
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

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
        line-height: 1.6; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }

    /* NOMBRE JR 31 SHOP MONUMENTAL */
    .nombre-tienda-gigante {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .subtitle-elegant {
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* INPUTS Y BOTONES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    .stButton>button { background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 2rem !important; }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* DASHBOARD CARDS */
    .executive-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid #333;
        border-radius: 20px; padding: 30px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        border-top: 5px solid #FF8C00;
    }
    .metric-val { font-family: 'Montserrat'; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS (ESTRUCTURA SOLICITADA) ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_REAL", "ORIGINAL_USD", "PVP_JR31", "VENDIDOS"])

if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "GANANCIA_NETA", "TOTAL"])

if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)

if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'cart' not in st.session_state: st.session_state.cart = []
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. PANTALLA DE ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="nombre-tienda-gigante">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-elegant">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
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
    # --- 5. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
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

    # --- DASHBOARD (ANALÍTICA SOLICITADA) ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        
        # CÁLCULOS FINANCIEROS
        total_inv = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_REAL']).sum() if not st.session_state.inv_db.empty else 0
        ganancia_real = st.session_state.sales_db['GANANCIA_NETA'].sum() if not st.session_state.sales_db.empty else 0
        piezas_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        piezas_vendidas = st.session_state.inv_db['VENDIDOS'].sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="executive-card"><p class="metric-title">GANANCIA REAL ACUMULADA</p><p class="metric-val" style="color:#2E8B57;">${ganancia_real:,.2f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p class="metric-title">PIEZAS VENDIDAS</p><p class="metric-val">{piezas_vendidas:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="executive-card"><p class="metric-title">PIEZAS EN STOCK</p><p class="metric-val">{piezas_stock:,.0f}</p></div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.session_state.is_admin:
            st.markdown(f'<div class="executive-card" style="border-top:5px solid #FFFFFF;"><p class="metric-title">CAPITAL INVERTIDO EN BODEGA</p><p class="metric-val">${total_inv:,.2f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL VENTA (ACTUALIZA VENDIDOS) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en STOCK primero.")
        else:
            search = st.text_input("🔍 BUSCAR ARTÍCULO")
            filtered = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
            
            with st.form("v_form", clear_on_submit=True):
                prod = st.selectbox("PRODUCTO", filtered['ARTICULO'])
                cli = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                can = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("AÑADIR AL TICKET"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == prod].iloc[0]
                    if can > data['STOCK']: st.error("Stock insuficiente.")
                    else:
                        # Cálculo de Ganancia por esta venta específica
                        utilidad_u = data['PVP_JR31'] - data['COSTO_REAL']
                        st.session_state.cart.append({"ART": prod, "QTY": can, "JR31": data['PVP_JR31'], "UTI": utilidad_u * can, "SUB": data['PVP_JR31']*can})
            
            if st.session_state.cart:
                st.table(pd.DataFrame(st.session_state.cart))
                if st.button("✅ FINALIZAR Y ACTUALIZAR STOCK"):
                    for item in st.session_state.cart:
                        # Registrar en Ventas
                        nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli, "ARTICULO": item['ART'], "CANTIDAD": item['QTY'], "GANANCIA_NETA": item['UTI'], "TOTAL": item['SUB']}])
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, nv], ignore_index=True)
                        # Actualizar Inventario (Bajar Stock, Subir Vendidos)
                        idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item['ART']].index[0]
                        st.session_state.inv_db.at[idx, 'STOCK'] -= item['QTY']
                        st.session_state.inv_db.at[idx, 'VENDIDOS'] += item['QTY']
                    st.session_state.cart = []; st.rerun()

    # --- GESTIÓN STOCK (TRIPLE PRECIO) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            col1, col2 = st.columns(2)
            a = col1.text_input("NOMBRE PRODUCTO")
            s = col2.number_input("CANTIDAD INICIAL", min_value=1)
            c = col1.number_input("MI COSTO REAL (MXN)")
            u = col2.number_input("PRECIO ETIQUETA USA (USD)")
            p = col1.number_input("PRECIO JR31 SHOP (MXN)")
            if st.form_submit_button("GUARDAR ARTÍCULO"):
                new_item = pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_REAL": c, "ORIGINAL_USD": u, "PVP_JR31": p, "VENDIDOS": 0}])
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

# --- FOOTER CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
