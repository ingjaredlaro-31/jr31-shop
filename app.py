import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | BUSINESS INTELLIGENCE",
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

    /* NOMBRE DEL INGENIERO ARRIBA DERECHA */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
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

    /* MENÚ LATERAL XL */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    div[role="radiogroup"] label {
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin-bottom: 20px !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* DASHBOARD CARDS PROFESIONALES */
    .exec-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border-top: 4px solid #FF8C00;
        transition: 0.3s;
    }
    .exec-card:hover { transform: translateY(-5px); border-top: 4px solid #2E8B57; }
    
    .metric-title { font-family: 'Orbitron'; font-size: 0.85rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
    .metric-value { font-family: 'Montserrat'; font-size: 2.5rem; font-weight: 900; color: #FFFFFF; }

    /* FOOTER CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INITIALIZATION ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "CANTIDAD", "TOTAL", "UTILIDAD"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA", "LIMITE"])
    default_c = pd.DataFrame([{"ID": "JR-001", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0, "LIMITE": 0.0}])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. ACCESO ---
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
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. DASHBOARD (RESUMEN TOTAL PANORÁMICO) ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA GENERAL DEL NEGOCIO</h1>", unsafe_allow_html=True)
        
        # CALCULOS
        total_ventas = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        total_ganancia = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        total_piezas_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        total_piezas_vta = st.session_state.sales_db['CANTIDAD'].sum() if not st.session_state.sales_db.empty else 0
        total_inversion = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        total_usa_costs = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0
        total_cartera = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0

        # FILA 1
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="exec-card"><p class="metric-title">🛒 VENTAS ACUMULADAS</p><p class="metric-value">${total_ventas:,.2f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">💰 GANANCIA REAL (UTILIDAD)</p><p class="metric-value" style="color:#2E8B57;">${total_ganancia:,.2f}</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="exec-card"><p class="metric-title">👥 CARTERA POR COBRAR</p><p class="metric-value" style="color:#FF4500;">${total_cartera:,.2f}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # FILA 2
        c4, c5, c6 = st.columns(3)
        with c4:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📦 PIEZAS EN STOCK</p><p class="metric-value">{total_piezas_stock:,.0f}</p></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📉 INVERSIÓN TOTAL (COSTO TJ)</p><p class="metric-value">${total_inversion:,.2f}</p></div>', unsafe_allow_html=True)
        with c6:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">🇺🇸 VALOR TIENDA (COSTO USA)</p><p class="metric-value">${total_usa_costs:,.2f}</p></div>', unsafe_allow_html=True)

    # --- 7. TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre productos en Gestión Stock.")
        else:
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                tipo = st.selectbox("MODO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total = row['PVP_JR31'] * qt
                    uti = (row['PVP_JR31'] - row['COSTO_TJ']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": it, "CANTIDAD": qt, "TOTAL": total, "UTILIDAD": uti}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if tipo == "CRÉDITO":
                        idx_c = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cl].index[0]
                        st.session_state.clients_db.at[idx_c, 'DEUDA'] += total
                    st.success(f"Venta registrada: ${total}"); st.rerun()

    # --- 8. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
        dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
        st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
        abono = st.number_input("REGISTRAR PAGO", min_value=0.0)
        if st.button("PAGAR"):
            st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= abono
            st.rerun()

    # --- 9. GESTIÓN STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk"):
            n = st.text_input("ARTICULO"); s = st.number_input("CANTIDAD", min_value=1)
            cu = st.number_input("COSTO USA (USD)"); ct = st.number_input("COSTO TJ (MXN)"); p = st.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR"):
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p}])], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

# --- FOOTER CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
