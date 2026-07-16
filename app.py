import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | SUPREME ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DISEÑO SUPREME EXECUTIVE (CSS) ---
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

    /* MENÚ LATERAL XL */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    div[role="radiogroup"] label {
        font-size: 1.7rem !important; /* ICONOS GIGANTES */
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin-bottom: 25px !important;
    }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border-top: 4px solid #FF8C00;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS Y BOTONES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
        font-size: 1.8rem !important; text-transform: uppercase;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS (SUPER BLINDADA) ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "TOTAL", "UTILIDAD"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA", "LIMITE"])
    default_c = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0, "LIMITE": 0.0}])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'cart' not in st.session_state: st.session_state.cart = []
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA DE ADMINISTRACIÓN Y VENTA</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("USUARIO ADMIN")
        u_pw = st.text_input("CONTRASEÑA", type="password")
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
        if st.button("CERRAR SESIÓN"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULOS ---

    # --- DASHBOARD PANORÁMICO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>ESTADO DEL NEGOCIO</h1>", unsafe_allow_html=True)
        v_total = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_total = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_total = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0
        pzs_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS ACUMULADAS</p><p class="metric-value">${v_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">GANANCIA REAL</p><p class="metric-value" style="color:#2E8B57;">${u_total:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">EN CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_total:,.0f}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs_stock:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">INVERSIÓN REAL (TJ)</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">COSTO USA (USD)</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL VENTA (CON CARRITO) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE COBRO</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en Gestión Stock.")
        else:
            col_l, col_r = st.columns([1, 1.2])
            with col_l:
                search = st.text_input("🔍 BUSCAR ARTÍCULO")
                filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
                with st.form("add_cart", clear_on_submit=True):
                    it = st.selectbox("PRODUCTO", filt['ARTICULO'])
                    qt = st.number_input("CANTIDAD", min_value=1)
                    if st.form_submit_button("➕ AÑADIR"):
                        data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                        if qt > data['STOCK']: st.error("Stock insuficiente")
                        else:
                            st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
                            st.success("Añadido")
            with col_r:
                if st.session_state.cart:
                    df_c = pd.DataFrame(st.session_state.cart)
                    st.table(df_c[["ART", "QTY", "SUB"]])
                    t_ticket = df_c['SUB'].sum()
                    st.markdown(f"## TOTAL: ${t_ticket:,.2f}")
                    if st.button("🗑️ VACIAR TICKET"): st.session_state.cart = []; st.rerun()
                    
                    cli_v = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                    modo_v = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                    if st.button("✅ FINALIZAR VENTA"):
                        uti_v = sum([(i['PVP'] - i['COSTO']) * i['QTY'] for i in st.session_state.cart])
                        for i in st.session_state.cart:
                            st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli_v, "ARTICULO": i['ART'], "CANTIDAD": i['QTY'], "TOTAL": i['SUB'], "UTILIDAD": (i['PVP']-i['COSTO'])*i['QTY']}])], ignore_index=True)
                            st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                        if modo_v == "CRÉDITO":
                            idx_c = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cli_v].index[0]
                            st.session_state.clients_db.at[idx_c, 'DEUDA'] += t_ticket
                        st.session_state.cart = []; st.balloons(); st.rerun()

    # --- CARTERA (RESTAURADA) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES Y PAGOS", "➕ NUEVO CLIENTE"])
        with t1:
            cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                st.markdown(f"""<div style='border:1px solid #FF8C00; padding:20px; border-radius:10px;'>
                <p><b>ID:</b> {dat['ID']}</p><p><b>DIR:</b> {dat['DIRECCION']}</p><p><b>TEL:</b> {dat['TELEFONO']}</p></div>""", unsafe_allow_html=True)
            with col_ex2:
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                ab = st.number_input("ABONAR", min_value=0.0)
                if st.button("PAGAR"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                    st.rerun()
        with t2:
            with st.form("n_c"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0, "LIMITE": 0.0}])], ignore_index=True)
                    st.success("Guardado"); st.rerun()

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with tab_a:
            with st.form("stk"):
                col1, col2 = st.columns(2)
                art_n = col1.text_input("ARTICULO")
                art_q = col2.number_input("CANTIDAD", min_value=1)
                art_u = col1.number_input("COSTO USA")
                art_t = col2.number_input("COSTO TJ")
                art_p = col1.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": art_n, "STOCK": art_q, "COSTO_USA": art_u, "COSTO_TJ": art_t, "PVP_JR31": art_p, "VENDIDOS": 0}])], ignore_index=True)
        with tab_b:
            if not st.session_state.inv_db.empty:
                ed = st.selectbox("MODIFICAR:", st.session_state.inv_db['ARTICULO'])
                idx_e = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx_e, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx_e, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx_e, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx_e, 'PVP_JR31'] = new_p
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
