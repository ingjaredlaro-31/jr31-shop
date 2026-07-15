import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN ESTRUCTURAL ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- DISEÑO DE VANGUARDIA (CSS PERSONALIZADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@300;700;900&display=swap');
    
    /* Fondo General */
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    /* FIRMA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed; bottom: 15px; left: 20px;
        color: #2E8B57; font-family: 'Montserrat', sans-serif;
        font-size: 11px; z-index: 1000; line-height: 1.4; font-weight: 900;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 22px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO TIPO BRANDING */
    .logo-branding {
        font-family: 'Orbitron', sans-serif; font-size: 4.5rem; font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 20px; filter: drop-shadow(0 0 15px rgba(255,69,0,0.4));
    }

    /* TARJETAS DEL DASHBOARD */
    .dash-card {
        background: rgba(27, 38, 59, 0.7); border-radius: 20px; padding: 30px;
        border-top: 5px solid #FF4500; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center; margin-bottom: 20px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 2px; }
    .metric-value { font-family: 'Montserrat'; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; }

    /* BOTONES */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 12px !important; border: none !important;
        height: 3.5em !important; width: 100%; transition: 0.4s; font-size: 1.2rem !important;
    }
    .stButton>button:hover { box-shadow: 0 0 30px #2E8B57; transform: translateY(-3px); }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF4500; }
    
    /* INPUTS */
    input { background-color: #1b263b !important; color: #FFFFFF !important; border: 1px solid #415a77 !important; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: bold !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (BLINDAJE TOTAL) ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- FUNCIÓN GENERADORA DE PDF ---
def exportar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(255, 69, 0) # Naranja
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE DE OPERACIONES", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87) # Verde
    pdf.cell(0, 10, f"Desarrollado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Resumen
    v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
    u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
    g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "RESUMEN FINANCIERO:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Total Ventas: ${v_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"Utilidad Bruta: ${u_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"Gastos Registrados: ${g_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"Balance de Caja: ${u_tot - g_tot:,.2f} MXN", ln=True)
    pdf.ln(10)
    
    # Stock
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "ESTADO DE INVENTARIO ACTUAL:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, r in st.session_state.inv.iterrows():
        pdf.cell(0, 7, f"- {r['ARTICULO']}: {r['CANTIDAD']} pzs | Precio: ${r['PVP']}", ln=True)
    
    return pdf.output()

# --- SISTEMA DE ACCESO ---
if not st.session_state.log:
    col_logo_l, col_logo_c, col_logo_r = st.columns([0.1, 2, 0.1])
    with col_logo_c:
        if os.path.exists("logo.png"): st.image("logo.png", width=650)
        else: st.markdown('<p class="logo-branding">JR 31 SHOP</p>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px; font-weight: bold;'>BUSINESS TERMINAL v10.0</p>", unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div style="background: rgba(27, 38, 59, 0.8); padding: 35px; border-radius: 25px; border: 2px solid #FF4500;">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<p style='color: #FF4500; font-family: Orbitron; font-size: 1.5rem; text-align: center;'>PUNTO DE VENTA<br>JR 31 SHOP</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if codigo == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO ACTIVO")
            if st.button("BLOQUEAR PRIVILEGIOS"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES MAESTROS"]
        
        nav = st.radio("SISTEMA", modulos)
        st.markdown("---")
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>ESTADÍSTICAS OPERATIVAS</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        col_d1, col_d2 = st.columns(2)
        with col_d1: st.markdown(f'<div class="dash-card"><p class="metric-title">FLUJO DE VENTAS</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d2: st.markdown(f'<div class="dash-card"><p class="metric-title">CUENTAS POR COBRAR</p><p class="metric-value" style="color: #FF4500;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)
        
        if st.session_state.es_admin:
            u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
            g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
            st.markdown(f'<div class="dash-card"><p class="metric-title">BALANCE NETO (UTILIDAD - GASTOS)</p><p class="metric-value" style="color: #2E8B57;">${u_tot - g_tot:,.2f}</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE COBRO</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Inventario sin existencias. Contactar al Ing. Jared.")
        else:
            with st.form("venta_form"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("TIPO DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("CONCLUIR OPERACIÓN"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    total = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": total, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += total
                    st.success(f"Venta registrada por ${total}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>EXPEDIENTES Y ALTAS</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 ESTADO DE CUENTA", "👤 NUEVO CLIENTE"])
        with tab1:
            c_sel_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            dat_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == c_sel_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${dat_c['SALDO_DEUDOR']:,.2f}")
            abono = st.number_input("REGISTRAR ABONO", min_value=0.0)
            if st.button("APLICAR PAGO"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel_f, 'SALDO_DEUDOR'] -= abono
                st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel_f, "MONTO": abono}])], ignore_index=True)
                st.rerun()
            
            st.markdown("### Historial de Movimientos")
            # Blindaje contra error de tabla vacía
            if not st.session_state.ven.empty:
                st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == c_sel_f], use_container_width=True)

        with tab2:
            nom_n = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR EN CARTERA"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nom_n, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.success("Guardado con éxito.")

    # --- 4. STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("inv"):
            a = st.text_input("ARTICULO")
            c = st.number_input("CANTIDAD", min_value=1)
            cost = st.number_input("COSTO ADQUISICIÓN")
            pvp = st.number_input("PRECIO VENTA AL PÚBLICO")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": a, "CANTIDAD": c, "COSTO_ADQ": cost, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS (ADMIN) ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("gas"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES (ADMIN) ---
    elif nav == "📝 REPORTES MAESTROS":
        st.markdown("<h1 style='font-family: Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        st.markdown('<div style="background: #1b263b; padding: 30px; border-radius: 20px;">', unsafe_allow_html=True)
        
        # EXCEL
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
            st.session_state.inv.to_excel(w, index=False, sheet_name='INVENTARIO')
        st.download_button("📥 DESCARGAR MASTER EXCEL", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%d%m%Y')}.xlsx")
        
        st.markdown("---")
        
        # PDF
        if st.button("📄 GENERAR PDF EJECUTIVO"):
            pdf_data = exportar_pdf()
            st.download_button("📥 DESCARGAR REPORTE PDF", data=pdf_data, file_name=f"Reporte_JR31_{datetime.now().strftime('%d%m%Y')}.pdf", mime="application/pdf")
        
        st.markdown('</div>', unsafe_allow_html=True)
