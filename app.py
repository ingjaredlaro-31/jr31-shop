import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- 1. CONFIGURACIÓN DE MOTOR ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INICIALIZACIÓN DE DATOS (PROTECCIÓN TOTAL) ---
def init_system_data():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "MARGEN"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default], ignore_index=True)
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_system_data()

# --- 3. ESTILO SUPREME EXECUTIVE (CSS) ---
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
    .logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 11vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    /* MENU LATERAL XL */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 400px !important; }
    div[role="radiogroup"] label { font-size: 1.8rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 4. ACCESO AL SISTEMA ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA DE ADMINISTRACIÓN Y VENTA</h2>', unsafe_allow_html=True)
    
    # OPCION DE CARGAR INVENTARIO SI SE BORRÓ
    with st.expander("📥 RESTAURAR MI INVENTARIO (SUBIR ARCHIVO)"):
        file_up = st.file_uploader("Suba su respaldo anterior", type="xlsx")
        if file_up:
            try:
                data_restored = pd.read_excel(file_up, sheet_name=None)
                st.session_state.inv_db = data_restored.get('INVENTARIO', st.session_state.inv_db)
                st.session_state.clients_db = data_restored.get('CLIENTES', st.session_state.clients_db)
                st.success("¡DATOS RESTAURADOS EXITOSAMENTE!")
            except: st.error("Archivo no compatible.")

    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>MENU</h1>", unsafe_allow_html=True)
        if st.button("🏠 DASHBOARD / INICIO"): st.rerun()
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💾 RESPALDO"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 6. MÓDULOS ---

    # --- TERMINAL VENTA (INTERFAZ PROFESIONAL) ---
    if nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        col_pos1, col_pos2 = st.columns([1, 1.3])
        
        with col_pos1:
            st.subheader("🛍️ Añadir al Ticket")
            if st.session_state.inv_db.empty: st.info("Registre productos en Gestión Stock.")
            else:
                bus_art = st.text_input("🔍 BUSCAR ARTÍCULO")
                filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(bus_art, case=False)]
                with st.form("cart"):
                    it = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
                    qt = st.number_input("CANTIDAD", min_value=1)
                    if st.form_submit_button("➕ AÑADIR"):
                        data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                        st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
                        st.rerun()

        with col_pos2:
            st.subheader("🧾 Detalle de Cobro")
            if st.session_state.cart:
                df_c = pd.DataFrame(st.session_state.cart)
                st.table(df_c[["ART", "QTY", "SUB"]])
                total_t = df_c['SUB'].sum()
                st.markdown(f"## TOTAL A COBRAR: ${total_t:,.2f}")
                
                if st.button("🧹 VACIAR TICKET"): st.session_state.cart = []; st.rerun()
                
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                mo = st.selectbox("MÉTODO PAGO", ["CONTADO", "CRÉDITO"])
                if st.button("✅ FINALIZAR Y ACTUALIZAR"):
                    # Registrar ventas
                    for i in st.session_state.cart:
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": i['ART'], "CANTIDAD": i['QTY'], "TOTAL": i['SUB'], "UTILIDAD": (i['PVP']-i['COSTO'])*i['QTY']}])], ignore_index=True)
                        st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                    
                    if mo == "CRÉDITO":
                        idx_c = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cl].index[0]
                        st.session_state.clients_db.at[idx_c, 'DEUDA'] += total_t
                    
                    st.session_state.cart = []; st.balloons(); st.rerun()

    # --- CARTERA (CON DATOS COMPLETOS) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"""<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border-left: 5px solid #FF8C00;'>
            <p><b>ID:</b> {dat['ID']}</p><p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p><p><b>TELÉFONO:</b> {dat['TELEFONO']}</p></div>""", unsafe_allow_html=True)
            st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.success("Pago registrado."); st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR CLIENTE"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.success("Añadido."); st.rerun()

    # --- DASHBOARD ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        p = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:5px solid #2E8B57;"><p class="metric-title">GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d:,.0f}</p></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:5px solid #FFFFFF;"><p class="metric-title">STOCK</p><p class="metric-value">{p:,.0f}</p></div>', unsafe_allow_html=True)

    # --- RESPALDO (PARA QUE NUNCA SE PIERDA NADA) ---
    elif nav == "💾 RESPALDO" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE RESPALDO</h1>", unsafe_allow_html=True)
        st.info("Descargue su base de datos al final de cada día para guardarla en su celular o computadora.")
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.inv_db.to_excel(w, index=False, sheet_name='INVENTARIO')
            st.session_state.clients_db.to_excel(w, index=False, sheet_name='CLIENTES')
        st.download_button("📥 DESCARGAR MI BASE DE DATOS (EXCEL)", buf.getvalue(), f"Base_JR31_{datetime.now().strftime('%d%m%y')}.xlsx")

    # --- STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk"):
            a = st.text_input("PRODUCTO"); s = st.number_input("STOCK", min_value=1)
            cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
            if st.form_submit_button("GUARDAR"):
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p}])], ignore_index=True)
                st.success("Guardado."); st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
