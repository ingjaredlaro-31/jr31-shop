import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. INITIALIZE ALL SESSION STATES (BLINDAJE TOTAL) ---
def init_all_session_states():
    # Database structures
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"])
    
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "MODO"])
    
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA", "LIMITE"])
        default_cli = pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0, "LIMITE": 0.0}])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_cli], ignore_index=True)
    
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []
        
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_all_session_states()

# --- 2. SUPREME EXECUTIVE DESIGN (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    /* Global Deep Background */
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

    /* MONUMENTAL SHOP NAME */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .main-subtitle { 
        text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 20px; font-weight: 400; font-size: 2.2rem; margin-bottom: 50px; text-transform: uppercase;
    }

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 80px; padding-bottom: 40px; width: 100%;
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

# --- 3. PDF ENGINE ---
def get_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE MAESTRO DE OPERACIONES", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Propiedad de Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"TOTAL VENTAS: ${v:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"TOTAL EN CARTERA: ${st.session_state.clients_db['DEUDA'].sum():,.2f} MXN", ln=True)
    
    pdf.ln(10)
    pdf.cell(0, 10, "DETALLE DE STOCK:", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, r in st.session_state.inv_db.iterrows():
        pdf.cell(0, 8, f"- {r['ARTICULO']}: {r['STOCK']} pzs en existencia", ln=True)
    
    return pdf.output()

# --- 4. LOGIN SCREEN ---
if not st.session_state.auth:
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
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
    # --- 5. SIDEBAR NAVIGATION ---
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
        if st.button("SALIR"):
            st.session_state.auth = False
            st.rerun()

    # --- 6. MODULES ---

    # --- TERMINAL VENTA (CON CARRITO Y BÚSQUEDA) ---
    if nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Primero cargue inventario en GESTIÓN STOCK.")
        else:
            col_pos_l, col_pos_r = st.columns([1, 1.2])
            with col_pos_l:
                search_vta = st.text_input("🔍 BUSCAR ARTÍCULO")
                filtered_inv = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search_vta, case=False)]
                with st.form("add_cart", clear_on_submit=True):
                    it_sel = st.selectbox("RESULTADO", filtered_inv['ARTICULO'])
                    it_qty = st.number_input("CANTIDAD", min_value=1)
                    if st.form_submit_button("➕ AGREGAR AL TICKET"):
                        data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it_sel].iloc[0]
                        st.session_state.cart.append({"ART": it_sel, "QTY": it_qty, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*it_qty})
            
            with col_pos_r:
                st.subheader("🧾 Ticket Actual")
                if st.session_state.cart:
                    df_cart = pd.DataFrame(st.session_state.cart)
                    st.table(df_cart[["ART", "QTY", "SUB"]])
                    t_ticket = df_cart['SUB'].sum()
                    st.markdown(f"## TOTAL: ${t_ticket:,.2f}")
                    
                    rem = st.selectbox("Remover artículo:", range(len(st.session_state.cart)), format_func=lambda x: st.session_state.cart[x]['ART'])
                    if st.button("🗑️ QUITAR"): st.session_state.cart.pop(rem); st.rerun()
                    
                    cli_vta = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                    modo_p = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                    if st.button("✅ FINALIZAR"):
                        uti = sum([(i['PVP'] - i['COSTO']) * i['QTY'] for i in st.session_state.cart])
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli_vta, "TOTAL": t_ticket, "UTILIDAD": uti, "MODO": modo_p}])], ignore_index=True)
                        for i in st.session_state.cart: st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                        if modo_p == "CRÉDITO": st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cli_vta, 'DEUDA'] += t_ticket
                        st.session_state.cart = []; st.balloons(); st.rerun()

    # --- CARTERA CLIENTES (EXPEDIENTE COMPLETO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA Y EXPEDIENTES</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            cl_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cl_f].iloc[0]
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                st.markdown(f"""<div style='border:1px solid #FF8C00; padding:20px; border-radius:10px;'>
                <p><b>ID:</b> {dat['ID']}</p><p><b>DIRECCIÓN:</b> {dat['DIRECCION']}</p><p><b>TELÉFONO:</b> {dat['TELEFONO']}</p></div>""", unsafe_allow_html=True)
            with col_ex2:
                st.metric("DEUDA ACTUAL", f"${dat['DEUDA']:,.2f}")
                abono = st.number_input("REGISTRAR ABONO", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cl_f, 'DEUDA'] -= abono
                    st.rerun()
        with t2:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO"); l = st.number_input("LÍMITE CRÉDITO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0, "LIMITE": l}])], ignore_index=True)
                    st.rerun()

    # --- STOCK (ADMIN CON EDITOR) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE STOCK</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR/BORRAR"])
        with tab_a:
            with st.form("add_s", clear_on_submit=True):
                col_s1, col_s2 = st.columns(2)
                art_n = col_s1.text_input("ARTICULO")
                art_q = col_s2.number_input("STOCK", min_value=1)
                art_u = col_s1.number_input("COSTO USA (USD)")
                art_t = col_s2.number_input("COSTO TJ (PESOS)")
                art_p = col_s1.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": art_n, "STOCK": art_q, "COSTO_USA": art_u, "COSTO_TJ": art_t, "PVP_JR31": art_p, "VENDIDOS": 0}])], ignore_index=True)
        with tab_b:
            if not st.session_state.inv_db.empty:
                ed_it = st.selectbox("MODIFICAR:", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == ed_it].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(st.session_state.inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(st.session_state.inv_db.at[idx, 'PVP_JR31']))
                    b1, b2 = st.columns(2)
                    if b1.form_submit_button("ACTUALIZAR"):
                        st.session_state.inv_db.at[idx, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx, 'PVP_JR31'] = new_p
                        st.rerun()
                    if b2.form_submit_button("🗑️ BORRAR"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- DASHBOARD ---
    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        inv_val = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="executive-card"><p class="metric-title">VENTAS ACUMULADAS</p><p class="metric-val">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="executive-card"><p class="metric-title">INVERSIÓN EN STOCK</p><p class="metric-val">${inv_val:,.0f}</p></div>', unsafe_allow_html=True)

    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            c = st.selectbox("CAT", ["PALLETS", "OFICINA", "VARIOS"]); con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": c, "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.expenses_db)

    # --- REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        if st.button("📄 GENERAR PDF MAESTRO"):
            st.download_button("📥 DESCARGAR PDF", get_pdf_report(), "JR31_Reporte.pdf")
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
        st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), "JR31_Ventas.xlsx")

# --- 8. PIE DE PÁGINA CENTRADO ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
