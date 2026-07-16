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

# --- 2. DISEÑO SUPREME EXECUTIVE (CSS PERSONALIZADO) ---
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

    /* PIE DE PÁGINA CENTRADO */
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; letter-spacing: 2px; }

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

    /* MENÚ LATERAL - LETRAS MÁS GRANDES Y PROFESIONALES */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF8C00;
    }
    /* Estilo para los nombres de los módulos */
    div[role="radiogroup"] label {
        font-size: 1.8rem !important; /* LETRAS MUCHO MÁS GRANDES */
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin-bottom: 20px !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    div[role="radiogroup"] label:hover { color: #FF8C00 !important; }

    /* INPUTS Y BOTONES GIGANTES */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.5em !important; width: 100%; transition: 0.5s;
        font-size: 1.8rem !important; text-transform: uppercase;
    }

    .executive-card {
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; padding: 35px;
        border-top: 6px solid #FF8C00; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS (BLINDADA) ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "MODO"])
if 'clients_db' not in st.session_state:
    st.session_state.clients_db = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    default_c = pd.DataFrame([{"ID": "JR31-001", "NOMBRE": "VENTA MOSTRADOR", "DIRECCION": "TONALA, CHIAPAS", "TELEFONO": "9181255735", "DEUDA": 0.0}])
    st.session_state.clients_db = pd.concat([st.session_state.clients_db, default_c], ignore_index=True)
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])

if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. FUNCIÓN GENERADORA DE REPORTES PDF ---
def generate_professional_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Ejecutivo
    pdf.set_fill_color(10, 33, 18) # Verde profundo
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 10, "JR 31 SHOP", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "AUDITORIA Y CONTROL DE OPERACIONES", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"REPORTE GENERADO EL: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(0, 10, f"RESPONSABLE: ING. JARED LARA RODRIGUEZ", ln=True)
    pdf.ln(5)
    
    # Resumen Financiero
    pdf.set_fill_color(255, 140, 0) # Naranja
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, " BALANCE FINANCIERO ", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 12)
    v_total = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
    u_total = st.session_state.sales_db['UTILIDAD'].sum() if not st.session_state.sales_db.empty else 0
    g_total = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
    
    pdf.cell(0, 10, f"- Ventas Totales: ${v_total:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Ganancia Bruta: ${u_total:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Gastos Operativos: ${g_total:,.2f} MXN", ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"- BALANCE NETO: ${u_total - g_total:,.2f} MXN", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, " ESTADO DE INVENTARIO ", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    for _, r in st.session_state.inv_db.iterrows():
        pdf.cell(0, 8, f"{r['ARTICULO']} | Stock: {r['STOCK']} | PVP: ${r['PVP_JR31']}", ln=True)
        
    return pdf.output()

# --- 5. ACCESO AL SISTEMA ---
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
            else: st.error("DENEGADO")
else:
    # --- 6. MENÚ LATERAL XL ---
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

    # --- 7. MÓDULO REPORTES (CENTRO DE AUDITORÍA) ---
    if nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CENTRO DE AUDITORÍA Y REPORTES</h1>", unsafe_allow_html=True)
        
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            st.markdown('<div class="executive-card">', unsafe_allow_html=True)
            st.subheader("📊 Reporte en Excel")
            st.write("Base de datos completa de ventas, inventario y clientes.")
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.sales_db.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inv_db.to_excel(w, index=False, sheet_name='INVENTARIO')
                st.session_state.clients_db.to_excel(w, index=False, sheet_name='CARTERA')
            st.download_button("📥 DESCARGAR EXCEL MAESTRO", buf.getvalue(), f"JR31_LARO_MASTER_{datetime.now().strftime('%d%m%y')}.xlsx")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c_r2:
            st.markdown('<div class="executive-card">', unsafe_allow_html=True)
            st.subheader("📄 Reporte Ejecutivo PDF")
            st.write("Documento formal con balance de ganancias y estado de stock.")
            if st.button("🛠️ GENERAR PDF"):
                pdf_output = generate_professional_pdf()
                st.download_button("📥 DESCARGAR PDF AHORA", pdf_output, f"Reporte_Gerencial_JR31.pdf", "application/pdf")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🔍 Auditoría de Ventas (Historial)")
        st.dataframe(st.session_state.sales_db, use_container_width=True)

    # --- OTROS MÓDULOS ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv_db.empty: st.info("Sin stock.")
        else:
            with st.form("pos"):
                it = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                cl = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
                qt = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("VENDER"):
                    row = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == it].iloc[0]
                    total = row['PVP_JR31'] * qt
                    uti = (row['PVP_JR31'] - row['COSTO_TJ']) * qt
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cl, "DETALLE": it, "TOTAL": total, "UTILIDAD": uti, "MODO": "CONTADO"}])], ignore_index=True)
                    st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == it, 'STOCK'] -= qt
                    st.success(f"Venta registrada: ${total}")

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        tab_v, tab_a = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with tab_v:
            c_sel = st.selectbox("CLIENTE", st.session_state.clients_db['NOMBRE'])
            idx = st.session_state.clients_db[st.session_state.clients_db['NOMBRE'] == c_sel].index[0]
            dat = st.session_state.clients_db.loc[idx]
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            abono = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.clients_db.at[idx, 'DEUDA'] -= abono
                st.rerun()
        with tab_a:
            with st.form("nc"):
                n = st.text_input("NOMBRE"); d = st.text_input("DIRECCIÓN"); t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR31-{len(st.session_state.clients_db):03d}"
                    st.session_state.clients_db = pd.concat([st.session_state.clients_db, pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])], ignore_index=True)
                    st.rerun()

    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.markdown(f'<div class="executive-card"><p class="metric-title">VENTAS ACUMULADAS</p><p class="metric-val">${v:,.2f}</p></div>', unsafe_allow_html=True)

    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk"):
            a = st.text_input("ARTÍCULO"); s = st.number_input("CANTIDAD", min_value=1); c_u = st.number_input("COSTO USA"); c_t = st.number_input("COSTO TJ"); p = st.number_input("PVP JR31")
            if st.form_submit_button("AÑADIR"):
                st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO_USA": c_u, "COSTO_TJ": c_t, "PVP_JR31": p}])], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            cat = st.selectbox("TIPO", ["PALLETS", "OFICINA", "VARIOS"]); con = st.text_input("CONCEPTO"); mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.dataframe(st.session_state.expenses_db, use_container_width=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
