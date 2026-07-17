import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. INITIALIZE ENGINE & ERROR SHIELD ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", initial_sidebar_state="expanded")

def init_all_data():
    # Database structures with specific column names to avoid KeyErrors
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
    
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        # Default customer
        default_cli = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_cli], ignore_index=True)
    
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'last_ticket' not in st.session_state: st.session_state.last_ticket = None
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_all_data()

# --- 2. SUPREME EXECUTIVE DESIGN (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Background Gradient */
    .stApp { background: radial-gradient(circle at center, #0a2114 0%, #000000 100%); background-attachment: fixed; color: #FFFFFF !important; }
    
    /* Header & Footer Branding */
    .jared-header { position: absolute; top: 15px; right: 40px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000; }
    .footer-centered { text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif; font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%; line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px; }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    /* Monumental Logo Name */
    .logo-giant { font-family: 'Orbitron', sans-serif; font-size: 13vw; font-weight: 900; text-align: center; background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9)); line-height: 0.8; letter-spacing: -10px; text-transform: uppercase; }
    .subtitle-exec { text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; letter-spacing: 15px; font-weight: 400; font-size: 2rem; margin-bottom: 50px; text-transform: uppercase; }

    /* Inputs & Buttons */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }
    .stButton>button { background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important; }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; transform: scale(1.02); }

    /* Sidebar Emojis XL */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 20px !important; }

    /* Metric Cards */
    .exec-card { background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00; margin-bottom: 15px; }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }
    
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. PDF MOTOR ---
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"TOTAL VENTAS: ${v:,.2f} MXN", ln=True)
    return pdf.output()

# --- 4. ACCESS SCREEN ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-exec">SISTEMA DE ADMINISTRACIÓN Y VENTA JR31</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. NAVEGACIÓN LATERAL ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if st.button("🏠 VOLVER A INICIO"): 
            st.session_state.page = "📊 DASHBOARD"
        
        st.markdown("---")
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("MÓDULO:", menu)
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.auth = False
            st.rerun()

    # --- 6. MÓDULOS FUNCIONALES ---

    # --- DASHBOARD PANORÁMICO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_t = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1: st.markdown(f'<div class="exec-card"><p class="metric-title">VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d2: st.markdown(f'<div class="exec-card" style="border-top:5px solid #2E8B57;"><p class="metric-title">GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d3: st.markdown(f'<div class="exec-card"><p class="metric-title">CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        
        col_d4, col_d5, col_d6 = st.columns(3)
        with col_d4: st.markdown(f'<div class="exec-card" style="border-top:5px solid #FFFFFF;"><p class="metric-title">PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d5: st.markdown(f'<div class="exec-card" style="border-top:5px solid #FFFFFF;"><p class="metric-title">INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d6: st.markdown(f'<div class="exec-card" style="border-top:5px solid #FFFFFF;"><p class="metric-title">VALOR USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- STOCK (CON EDITOR Y BORRADO) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        st.subheader("📋 LISTADO ACTUAL")
        st.dataframe(st.session_state.inv_db, use_container_width=True)
        
        t1, t2 = st.tabs(["📥 ALTA", "✏️ EDITAR / BORRAR"])
        with t1:
            with st.form("add_p", clear_on_submit=True):
                col_s1, col_s2 = st.columns(2)
                n = col_s1.text_input("ARTICULO"); s = col_s2.number_input("STOCK", min_value=1)
                cu = col_s1.number_input("COSTO USA"); ct = col_s2.number_input("COSTO TJ"); p = col_s1.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0}])], ignore_index=True)
                    st.rerun()
        with t2:
            if not st.session_state.inv_db.empty:
                it_e = st.selectbox("PRODUCTO:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it_e].index[0]
                with st.form("ed_p"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    b1, b2 = st.columns(2)
                    if b1.form_submit_button("💾 ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
                    if b2.form_submit_button("🗑️ BORRAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.rerun()

    # --- CARTERA CLIENTES ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_c1, t_c2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_c1:
            if not st.session_state.clients_db.empty:
                cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
                st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
                st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
                pago = st.number_input("ABONAR", min_value=0.0)
                if st.button("REGISTRAR PAGO"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= pago
                    st.rerun()
        with t_c2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- TERMINAL VENTA ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        col_v1, col_v2 = st.columns([1, 1.2])
        with col_v1:
            bus = st.text_input("🔍 BUSCAR ARTÍCULO")
            f = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(bus, case=False)]
            with st.form("c"):
                it = st.selectbox("PRODUCTO", f['ARTICULO']) if not f.empty else st.selectbox("PRODUCTO", ["N/A"])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("➕ AÑADIR"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
                    st.rerun()
        with col_v2:
            if st.session_state.cart:
                df_c = pd.DataFrame(st.session_state.cart)
                st.table(df_c[["ART", "QTY", "SUB"]])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                if st.button("✅ FINALIZAR"):
                    for i in st.session_state.cart:
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "ARTICULO": i['ART'], "TOTAL": i['SUB'], "UTILIDAD": (i['PVP']-i['COSTO'])*i['QTY']}])], ignore_index=True)
                        st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                    st.session_state.cart = []; st.balloons(); st.rerun()

    # --- GASTOS Y REPORTES ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            cat = st.selectbox("CAT", ["PALLETS", "OFICINA", "VARIOS"]); con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>AUDITORÍA</h1>", unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.download_button("📥 DESCARGAR EXCEL MASTER", buf.getvalue(), f"JR31_MASTER.xlsx")
        with c_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                st.download_button("📥 DESCARGAR PDF", generate_pdf(), "JR31_Reporte.pdf")

# --- 8. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
