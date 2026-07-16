import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
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

    /* NOMBRE DEL INGENIERO ARRIBA DERECHA */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP MONUMENTAL */
    .nombre-tienda-gigante {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

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
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF !important; font-family: 'Orbitron'; font-size: 1.2rem; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE BASES DE DATOS ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "GANANCIA"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. ACCESO AL SISTEMA ---
if not st.session_state.auth:
    st.markdown('<p class="nombre-tienda-gigante">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ID DE ADMINISTRADOR")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("ERROR DE CREDENCIALES")
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
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("CERRAR SESIÓN"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULO CARTERA (RECONSTRUIDO TOTALMENTE) ---
    if nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE CARTERA</h1>", unsafe_allow_html=True)
        tab_view, tab_add = st.tabs(["📋 EXPEDIENTES Y PAGOS", "➕ DAR DE ALTA CLIENTE"])
        
        with tab_view:
            if st.session_state.clients_db.empty:
                st.info("No hay clientes registrados.")
            else:
                c_sel = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients_db['NOMBRE'])
                idx = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == c_sel].index[0]
                dat = st.session_state.clients_db.loc[idx]
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #FF8C00;">
                        <p style="color:#FF8C00; font-family:Orbitron;">FICHA TÉCNICA:</p>
                        <p><b>ID:</b> {dat['ID']}</p>
                        <p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p>
                        <p><b>TELÉFONO:</b> {dat['TELEFONO']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_c2:
                    st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
                    abono = st.number_input("REGISTRAR PAGO ($)", min_value=0.0)
                    if st.button("APLICAR ABONO"):
                        st.session_state.clients_db.at[idx, 'DEUDA'] -= abono
                        st.success("Cobro registrado."); st.rerun()
                
                st.markdown("---")
                st.subheader("🛒 Historial de compras")
                hist = st.session_state.sales_db[st.session_state.sales_db['CLIENTE'] == c_sel]
                st.dataframe(hist, use_container_width=True)

        with tab_add:
            st.subheader("Registrar nuevo integrante a la cartera")
            with st.form("new_cl", clear_on_submit=True):
                n_name = st.text_input("NOMBRE COMPLETO")
                n_addr = st.text_input("DIRECCIÓN")
                n_phone = st.text_input("TELÉFONO / WHATSAPP")
                if st.form_submit_button("GUARDAR EN SISTEMA"):
                    new_id = f"JR31-{len(st.session_state.clients_db):03d}"
                    nuevo_cli = pd.DataFrame([{"ID": new_id, "NOMBRE": n_name, "DIRECCION": n_addr, "TELEFONO": n_phone, "DEUDA": 0.0}])
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, nuevo_cli], ignore_index=True)
                    st.success(f"Cliente registrado con ID: {new_id}")
                    st.rerun()

    # --- 7. MÓDULO STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 AÑADIR", "✏️ EDITAR"])
        with tab_a:
            with st.form("add_s", clear_on_submit=True):
                n = st.text_input("PRODUCTO"); s = st.number_input("CANTIDAD", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p}])], ignore_index=True)
        with tab_b:
            if not st.session_state.inv_db.empty:
                ed_it = st.selectbox("EDITAR ARTICULO", st.session_state.inv_db['ARTICULO'])
                idx_e = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed_it].index[0]
                with st.form("edit_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx_e, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx_e, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx_e, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx_e, 'PVP_JR31'] = new_p
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- 8. TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Registre stock primero.")
        else:
            search = st.text_input("🔍 BUSCAR ARTÍCULO")
            filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", filt['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                md = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    t_vta = row['PVP_JR31'] * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "DETALLE": it, "TOTAL": t_vta, "GANANCIA": (row['PVP_JR31']-row['COSTO_TJ'])*qt}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    if md == "CRÉDITO":
                        st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cl, 'DEUDA'] += t_vta
                    st.success("Venta realizada.")

    # --- 9. OTROS ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.metric("VENTAS TOTALES", f"${v:,.2f}")

    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

# --- FOOTER CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
