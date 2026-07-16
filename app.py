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

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Global Background */
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO MONUMENTAL */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    /* MENÚ LATERAL XL */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.6rem !important; font-weight: 900 !important; color: #FFFFFF !important; margin-bottom: 20px !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 10px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 2.8rem; font-weight: 900; color: #FFFFFF; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS (BLINDADA) ---
def init_db():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "TONALA, CHIAPAS", "TELEFONO": "9181255735", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_db()

# --- 4. MOTOR DE PDF PROFESIONAL ---
def create_master_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE GERENCIAL", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Financial Stats
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ESTADO FINANCIERO:", ln=True)
    pdf.set_font("Arial", "", 12)
    v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    u = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
    pdf.cell(0, 10, f"- Ventas Totales: ${v:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Ganancia Real: ${u:,.2f} MXN", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "DETALLE DE STOCK:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, r in st.session_state.inv_db.iterrows():
        pdf.cell(0, 8, f"- {r['ARTICULO']}: {r['STOCK']} pzs en bodega", ln=True)
    
    return pdf.output()

# --- 5. ACCESO ---
if not st.session_state.auth:
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u = st.text_input("ADMIN ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("ACCEDER"):
            if u == "admin_jr31" and p == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 6. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:1.8rem;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            cod = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR ADMIN"):
                if cod == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        m = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: m += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.radio("SISTEMA", m)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MÓDULOS ---

    # --- DASHBOARD DETALLADO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA CORPORATIVO</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_t = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">🛒 VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:5px solid #2E8B57;"><p class="metric-title">💰 GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">👥 CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📦 PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📉 INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">🇺🇸 COSTO USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL VENTA (CARRITO) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        col_l, col_r = st.columns([1, 1.2])
        with col_l:
            srch = st.text_input("🔍 BUSCAR ARTÍCULO")
            f = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(srch, case=False)]
            with st.form("c", clear_on_submit=True):
                it = st.selectbox("PRODUCTO", f['ARTICULO']) if not f.empty else st.selectbox("PRODUCTO", ["N/A"])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("➕ AÑADIR"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
        with col_r:
            if st.session_state.cart:
                df_c = pd.DataFrame(st.session_state.cart)
                st.table(df_c[["ART", "QTY", "SUB"]])
                tt = df_c['SUB'].sum()
                st.markdown(f"## TOTAL: ${tt:,.2f}")
                if st.button("🗑️ VACIAR"): st.session_state.cart = []; st.rerun()
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                if st.button("✅ COBRAR"):
                    uti = sum([(i['PVP']-i['COSTO'])*i['QTY'] for i in st.session_state.cart])
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "TOTAL": tt, "UTILIDAD": uti}])], ignore_index=True)
                    for i in st.session_state.cart: st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                    st.session_state.cart = []; st.balloons(); st.rerun()

    # --- CARTERA (RESTAURADA) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with t1:
            sel = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == sel].iloc[0]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            p = st.number_input("ABONAR")
            if st.button("PAGAR"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == sel, 'DEUDA'] -= p
                st.rerun()
        with t2:
            with st.form("n"):
                name = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": name, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- GESTIÓN STOCK (EDITOR) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        t_a, t_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with t_a:
            with st.form("st"):
                n = st.text_input("ARTICULO"); s = st.number_input("STOCK", min_value=1)
                cu = st.number_input("COSTO USA"); ct = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with t_b:
            if not st.session_state.inv_db.empty:
                it_e = st.selectbox("EDITAR:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it_e].index[0]
                with st.form("e"):
                    n_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    n_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    col_e1, col_e2 = st.columns(2)
                    if col_e1.form_submit_button("💾 ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = n_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = n_p
                        st.rerun()
                    if col_e2.form_submit_button("🗑️ BORRAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.rerun()

    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
                st.rerun()
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

    # --- REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 EXCEL COMPLETO", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%d%m%y')}.xlsx")
        with c_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                st.download_button("📥 DESCARGAR PDF", create_master_pdf(), "JR31_Reporte.pdf")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
