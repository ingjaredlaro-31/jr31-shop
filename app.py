import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os
import extra_streamlit_components as stx

# --- 1. CORE ENGINE & ERROR SHIELD ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INITIALIZE ALL DATA STRUCTURES ---
def init_db():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        # Cliente default inicial
        init_c = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "TONALA", "TELEFONO": "9181255735", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, init_c], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_db()

# --- 3. SUPREME EXECUTIVE DESIGN (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* HEADER: ING JARED LARO */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO MONUMENTAL */
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .main-subtitle {
        text-align: center; color: #FFFFFF; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; font-weight: 900; font-size: 2.2rem;
        margin-top: 10px; margin-bottom: 50px; text-shadow: 0 0 15px #2E8B57;
    }

    /* PIE DE PÁGINA CENTRADO SOLICITADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    /* MENU LATERAL XL */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; min-width: 350px !important; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 25px !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 8px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 4. MOTOR PDF ---
def get_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"RESPONSABLE: ING. JARED LARO", ln=True)
    pdf.cell(0, 10, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    return pdf.output()

# --- 5. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 6. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 INICIO / DASHBOARD"): st.session_state.nav_choice = "📊 DASHBOARD"
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CLAVE MAESTRA", type="password")
            if st.button("ACTIVAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SELECCIONE MÓDULO:", menu)
        if st.button("🚪 SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MÓDULOS ---

    # DASHBOARD
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_t = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">COSTO USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # TERMINAL VENTA
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.2])
        with col1:
            search = st.text_input("🔍 BUSCAR ARTÍCULO")
            filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
            with st.form("c"):
                it = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("➕ AÑADIR"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
                    st.rerun()
        with col2:
            if st.session_state.cart:
                df_c = pd.DataFrame(st.session_state.cart)
                st.table(df_c[["ART", "QTY", "SUB"]])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                if st.button("✅ COBRAR"):
                    for i in st.session_state.cart:
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": i['ART'], "CANTIDAD": i['QTY'], "TOTAL": i['SUB'], "UTILIDAD": (i['PVP']-i['COSTO'])*i['QTY']}])], ignore_index=True)
                        st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                    st.session_state.cart = []; st.rerun()

    # CARTERA (RESTAURADA)
    elif nav == "👤 CARTERA":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA Y COBRANZA</h1>", unsafe_allow_html=True)
        tab_v, tab_a = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with tab_v:
            if not st.session_state.clients_db.empty:
                cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
                st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                ab = st.number_input("ABONAR")
                if st.button("PAGAR"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                    st.rerun()
        with tab_a:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # STOCK (EDITABLE Y ELIMINABLE)
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        tab_h, tab_e = st.tabs(["📥 ALTA", "✏️ EDITAR/BORRAR"])
        with tab_h:
            with st.form("stk"):
                a = st.text_input("ARTICULO"); s = st.number_input("STOCK", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with tab_e:
            if not st.session_state.inv_db.empty:
                ed_it = st.selectbox("PRODUCTO:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed_it].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    if st.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
                    if st.form_submit_button("🗑️ ELIMINAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # GASTOS
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": "VARIOS", "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db)

    # REPORTES
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR EXCEL MASTER", buf.getvalue(), "JR31_MASTER.xlsx")

# --- PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
