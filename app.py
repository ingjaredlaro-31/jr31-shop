import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DISEÑO CYBER-EXECUTIVE (VERDE PROFUNDO Y NARANJA NEÓN) ---
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
    .logo-colosal {
        font-family: 'Orbitron', sans-serif;
        font-size: 12vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px; margin-bottom: -15px;
        filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -8px; text-transform: uppercase;
    }

    .sub-elegante {
        text-align: center; color: #2E8B57; font-family: 'Montserrat', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem;
        margin-bottom: 50px; text-transform: uppercase;
    }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    
    .stButton>button { 
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; 
        color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; 
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 2rem !important;
        border-radius: 8px !important; border: none !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px;
        border-top: 6px solid #FF8C00; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .metric-val { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; text-transform: uppercase; }

    /* FOOTER CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.6; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.1rem; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important;}
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS REFORZADA (ANTI-ERROR) ---
def repair_and_init_db():
    # Estructura del Inventario
    inv_cols = ["ARTICULO", "STOCK", "COSTO_REAL", "ORIGINAL_USD", "PVP_JR31", "VENDIDOS"]
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=inv_cols)
    else:
        # Si la tabla existe pero le faltan columnas nuevas, las añadimos
        for col in inv_cols:
            if col not in st.session_state.inv_db.columns:
                st.session_state.inv_db[col] = 0 if col in ["STOCK", "VENDIDOS"] else 0.0

    # Estructura de Ventas
    sales_cols = ["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "GANANCIA_NETA", "TOTAL"]
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=sales_cols)
    
    # Estructura de Clientes
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)

    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

repair_and_init_db()

# --- 4. PANTALLA DE ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-colosal">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-elegante">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
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
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULOS ---

    # --- DASHBOARD (SOLUCIÓN AL ERROR KEYERROR) ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        
        # Cálculos Seguros
        piezas_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        piezas_vta = st.session_state.inv_db['VENDIDOS'].sum() if not st.session_state.inv_db.empty else 0
        total_inv = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_REAL']).sum() if not st.session_state.inv_db.empty else 0
        total_ganancia = st.session_state.sales_db['GANANCIA_NETA'].sum() if not st.session_state.sales_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">GANANCIA REAL</p><p class="metric-val" style="color:#2E8B57;">${total_ganancia:,.2f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card"><p class="metric-title">PIEZAS VENDIDAS</p><p class="metric-val">{piezas_vta:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">PIEZAS EN STOCK</p><p class="metric-val">{piezas_stock:,.0f}</p></div>', unsafe_allow_html=True)

        if st.session_state.is_admin:
            st.markdown("---")
            st.markdown(f'<div class="exec-card" style="border-top:6px solid #FFFFFF;"><p class="metric-title">CAPITAL TOTAL EN BODEGA</p><p class="metric-val">${total_inv:,.2f}</p></div>', unsafe_allow_html=True)

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 AÑADIR PRODUCTO", "✏️ EDITAR PRECIOS"])
        
        with tab_a:
            with st.form("stk", clear_on_submit=True):
                col1, col2 = st.columns(2)
                a = col1.text_input("NOMBRE DEL PRODUCTO")
                s = col2.number_input("STOCK INICIAL", min_value=1)
                c = col1.number_input("MI COSTO REAL (MXN)")
                u = col2.number_input("PRECIO USA (USD)")
                p = col1.number_input("PRECIO JR31 SHOP (MXN)")
                if st.form_submit_button("GUARDAR EN BODEGA"):
                    new_item = pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_REAL": c, "ORIGINAL_USD": u, "PVP_JR31": p, "VENDIDOS": 0}])
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, new_item], ignore_index=True)
                    st.success("Guardado.")

        st.subheader("Inventario Actual")
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- VENTAS (VENDEDORA) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en STOCK.")
        else:
            search = st.text_input("🔍 BUSCAR ARTÍCULO")
            filtered = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
            
            with st.form("pos"):
                p_sel = st.selectbox("PRODUCTO", filtered['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                can_v = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("AÑADIR AL TICKET"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == p_sel].iloc[0]
                    if can_v > data['STOCK']: st.error("No hay stock suficiente.")
                    else:
                        utilidad = (data['PVP_JR31'] - data['COSTO_REAL']) * can_v
                        st.session_state.cart.append({"ART": p_sel, "QTY": can_v, "PVP": data['PVP_JR31'], "UTI": utilidad, "TOTAL": data['PVP_JR31']*can_v})
            
            if st.session_state.cart:
                st.table(pd.DataFrame(st.session_state.cart))
                if st.button("✅ FINALIZAR VENTA"):
                    for item in st.session_state.cart:
                        # Venta
                        nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": item['ART'], "CANTIDAD": item['QTY'], "GANANCIA_NETA": item['UTI'], "TOTAL": item['TOTAL']}])
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, nv], ignore_index=True)
                        # Inventario
                        idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item['ART']].index[0]
                        st.session_state.inv_db.at[idx, 'STOCK'] -= item['QTY']
                        st.session_state.inv_db.at[idx, 'VENDIDOS'] += item['QTY']
                    st.session_state.cart = []; st.success("Venta completada."); st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
