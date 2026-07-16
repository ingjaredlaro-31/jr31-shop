import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="JR 31 SHOP | SUPREME ERP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    /* TOP RIGHT HEADER: THE ENGINEER */
    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP MONUMENTAL */
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    /* SIDEBAR STYLE & ICONS */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.7rem !important; font-weight: 900; color: #FFFFFF !important; margin-bottom: 20px !important; }

    /* DASHBOARD CARDS */
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* FOOTER CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }

    /* XL INPUTS */
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

# --- 3. DATA REPAIR & INITIALIZATION (ENGLISH BACKEND) ---
def maintenance_db():
    inv_cols = ["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"]
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=inv_cols)
    else:
        for col in inv_cols:
            if col not in st.session_state.inv_db.columns: st.session_state.inv_db[col] = 0.0

    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD"])
    
    if 'clients_db' not in st.session_state:
        st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": "JR-000", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])], ignore_index=True)
    
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'last_ticket' not in st.session_state: st.session_state.last_ticket = None
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

maintenance_db()

# --- 4. PDF TICKET GENERATOR ---
def create_ticket(client, items, total):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "JR 31 SHOP", ln=True, align='C')
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, f"Fecha: {datetime.now().strftime('%d/%m/%y %H:%M')}", ln=True, align='C')
    pdf.cell(0, 5, f"Cliente: {client}", ln=True)
    pdf.cell(0, 5, "-"*30, ln=True)
    for i in items:
        pdf.cell(0, 5, f"{i['ART']} x{i['QTY']} - ${i['SUB']}", ln=True)
    pdf.cell(0, 5, "-"*30, ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 10, f"TOTAL: ${total:,.2f}", ln=True, align='R')
    return pdf.output()

# --- 5. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px; color:#2E8B57;">SISTEMA ERP PROFESIONAL</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 6. SIDEBAR ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR GERENCIA"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- 7. MODULES ---

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        u_t = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
        d_t = st.session_state.clients_db['DEUDA'].sum() if not st.session_state.clients_db.empty else 0
        inv_tj = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_TJ']).sum() if not st.session_state.inv_db.empty else 0
        inv_usa = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO_USA']).sum() if not st.session_state.inv_db.empty else 0
        pzs = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="exec-card"><p class="metric-title">🛒 VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">💰 GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="exec-card"><p class="metric-title">👥 CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
        
        c4, c5, c6 = st.columns(3)
        with c4: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📦 PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📉 INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">🇺🇸 VALOR USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)

    # --- STOCK (CORREGIDO: EDITAR Y ELIMINAR ACTIVADO) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE INVENTARIO</h1>", unsafe_allow_html=True)
        t_add, t_edit = st.tabs(["📥 ALTA DE PRODUCTO", "✏️ EDITAR O ELIMINAR"])
        
        with t_add:
            with st.form("add", clear_on_submit=True):
                col1, col2 = st.columns(2)
                n = col1.text_input("ARTICULO")
                s = col2.number_input("STOCK", min_value=1)
                cu = col1.number_input("COSTO USA")
                ct = col2.number_input("COSTO TJ")
                p = col1.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO_USA": cu, "COSTO_TJ": ct, "PVP_JR31": p}])], ignore_index=True)
                    st.success("Registrado."); st.rerun()

        with t_edit:
            if not st.session_state.inv_db.empty:
                art_e = st.selectbox("PRODUCTO A MODIFICAR", st.session_state.inv_db['ARTICULO'])
                idx_e = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == art_e].index[0]
                with st.form("edit_stock"):
                    st.subheader(f"Editando: {art_e}")
                    col_e1, col_e2 = st.columns(2)
                    new_q = col_e1.number_input("NUEVO STOCK", value=int(st.session_state.inv_db.at[idx_e, 'STOCK']))
                    new_cu = col_e2.number_input("NUEVO COSTO USA", value=float(st.session_state.inv_db.at[idx_e, 'COSTO_USA']))
                    new_ct = col_e1.number_input("NUEVO COSTO TJ", value=float(st.session_state.inv_db.at[idx_e, 'COSTO_TJ']))
                    new_p = col_e2.number_input("NUEVO PVP", value=float(st.session_state.inv_db.at[idx_e, 'PVP_JR31']))
                    
                    b_upd, b_del = st.columns(2)
                    if b_upd.form_submit_button("💾 ACTUALIZAR"):
                        st.session_state.inv_db.at[idx_e, 'STOCK'] = new_q
                        st.session_state.inv_db.at[idx_e, 'COSTO_USA'] = new_cu
                        st.session_state.inv_db.at[idx_e, 'COSTO_TJ'] = new_ct
                        st.session_state.inv_db.at[idx_e, 'PVP_JR31'] = new_p
                        st.success("Actualizado."); st.rerun()
                    if b_del.form_submit_button("🗑️ ELIMINAR ARTÍCULO"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx_e).reset_index(drop=True)
                        st.warning("Borrado."); st.rerun()
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- TERMINAL VENTA (CON CARRITO Y TICKET) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        col_l, col_r = st.columns([1, 1.2])
        with col_l:
            search = st.text_input("🔍 BUSCAR ARTÍCULO")
            filt = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search, case=False)]
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", filt['ARTICULO']) if not filt.empty else st.selectbox("PRODUCTO", ["N/A"])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("➕ AÑADIR"):
                    data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    st.session_state.cart.append({"ART": it, "QTY": qt, "PVP": data['PVP_JR31'], "COSTO": data['COSTO_TJ'], "SUB": data['PVP_JR31']*qt})
                    st.rerun()
        with col_r:
            if st.session_state.cart:
                df_c = pd.DataFrame(st.session_state.cart)
                st.table(df_c[["ART", "QTY", "SUB"]])
                t_val = df_c['SUB'].sum()
                st.markdown(f"## TOTAL: ${t_val:,.2f}")
                
                if st.button("🧹 VACIAR TICKET"): st.session_state.cart = []; st.rerun()
                
                cli_v = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                if st.button("✅ FINALIZAR Y GENERAR TICKET"):
                    for i in st.session_state.cart:
                        st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli_v, "ARTICULO": i['ART'], "CANTIDAD": i['QTY'], "TOTAL": i['SUB'], "UTILIDAD": (i['PVP']-i['COSTO'])*i['QTY']}])], ignore_index=True)
                        st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ART'], 'STOCK'] -= i['QTY']
                    st.session_state.last_ticket = {"cli": cli_v, "items": st.session_state.cart, "tot": t_val}
                    st.session_state.cart = []; st.rerun()
            
            if st.session_state.last_ticket:
                t_bytes = create_ticket(st.session_state.last_ticket['cli'], st.session_state.last_ticket['items'], st.session_state.last_ticket['tot'])
                st.download_button("📥 DESCARGAR TICKET PDF", t_bytes, "ticket.pdf", "application/pdf")
                if st.button("NUEVA VENTA"): st.session_state.last_ticket = None; st.rerun()

    # --- CARTERA (CON DATOS COMPLETOS) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_v, t_a = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t_v:
            cf = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            dat = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"""<div style='border:1px solid #FF8C00; padding:20px; border-radius:10px;'>
            <p><b>ID:</b> {dat['ID']}</p><p><b>DIR:</b> {dat['DIRECCION']}</p><p><b>TEL:</b> {dat['TELEFONO']}</p></div>""", unsafe_allow_html=True)
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            ab = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients_db.loc[st.session_state.clients_db['NOMBRE'] == cf, 'DEUDA'] -= ab
                st.rerun()
        with t_a:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIR"); t = st.text_input("TEL")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    # --- GASTOS Y REPORTES ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.expenses_db)

    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv_db.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR EXCEL MASTER", buf.getvalue(), "JR31_MASTER.xlsx")

# --- 8. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
