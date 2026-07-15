import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN ESTRUCTURAL ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V10.0 (DISEÑO FINAL DE ÉLITE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@300;700;900&display=swap');
    
    /* Fondo General Profundo */
    .stApp { 
        background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); 
        color: #e0e1dd !important; 
    }
    
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
        font-size: 24px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP MONUMENTAL (SIN RECTÁNGULOS) */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif; 
        font-size: 8rem; font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 30px; margin-bottom: 0px;
        filter: drop-shadow(0 0 25px rgba(255,69,0,0.5));
        line-height: 1; letter-spacing: -5px;
    }

    .subtitle-grande {
        text-align: center; color: #FFFFFF; font-family: 'Orbitron', sans-serif; 
        letter-spacing: 10px; font-weight: 900; font-size: 2.2rem;
        margin-top: 10px; margin-bottom: 40px; text-shadow: 0 0 10px #2E8B57;
    }

    /* TARJETAS DEL DASHBOARD */
    .dash-card {
        background: rgba(27, 38, 59, 0.7); border-radius: 25px; padding: 35px;
        border-left: 10px solid #FF4500; box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        text-align: center; margin-bottom: 20px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; }
    .metric-value { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }

    /* BOTONES */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 12px !important; border: none !important;
        height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.3rem !important;
    }
    .stButton>button:hover { box-shadow: 0 0 40px #2E8B57; transform: scale(1.02); }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF4500; }
    
    /* INPUTS */
    input { background-color: #1b263b !important; color: #FFFFFF !important; border: 2px solid #415a77 !important; font-size: 1.2rem !important; border-radius: 10px !important; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (SUPER BLINDADA) ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- FUNCIÓN GENERADORA DE PDF MAESTRO ---
def exportar_pdf_maestro():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 15, "JR 31 SHOP - REPORTE GERENCIAL", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(46, 139, 87)
    pdf.cell(0, 10, f"Desarrollado por Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
    u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
    g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
    d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 10, "1. BALANCE FINANCIERO:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"- Total Ventas: ${v_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"- Utilidad Real (Ganancia): ${u_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"- Gastos Operativos: ${g_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"- Utilidad Neta (Caja): ${u_tot - g_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 8, f"- Cuentas por Cobrar (Cartera): ${d_tot:,.2f} MXN", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. INVENTARIO ACTUAL:", ln=True)
    pdf.set_font("Arial", "", 10)
    for i, r in st.session_state.inv.iterrows():
        pdf.cell(0, 7, f"- {r['ARTICULO']}: {r['CANTIDAD']} pzs | PVP: ${r['PVP']}", ln=True)
    
    return pdf.output()

# --- PANTALLA DE ACCESO ---
if not st.session_state.log:
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-grande">SISTEMA ERP POS v10.0</p>', unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div style="background: rgba(27, 38, 59, 0.8); padding: 40px; border-radius: 25px; border: 2px solid #FF4500;">', unsafe_allow_html=True)
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
        if os.path.exists("logo.png"): st.image("logo.png", width=200)
        st.markdown("<p style='color: #FF4500; font-family: Orbitron; font-size: 1.2rem; text-align: center;'>PUNTO DE VENTA<br>JR 31 SHOP</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO ADMIN", type="password")
            if st.button("DESBLOQUEAR MAESTRO"):
                if codigo == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.radio("SISTEMA", modulos)
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="dash-card"><p class="metric-title">VENTAS TOTALES</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="dash-card"><p class="metric-title">CARTERA VENCIDA</p><p class="metric-value" style="color: #FF4500;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)
        
        if st.session_state.es_admin:
            u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
            g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
            st.markdown(f'<div class="dash-card"><p class="metric-title">UTILIDAD NETA (BALANCE)</p><p class="metric-value" style="color: #2E8B57;">${u_tot - g_tot:,.2f}</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Aviso: El inventario está vacío.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success("VENTA REGISTRADA")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 EXPEDIENTES", "👤 NUEVO CLIENTE"])
        with tab1:
            cliente_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${datos_c['SALDO_DEUDOR']:,.2f}")
            m_abono = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR PAGO"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_abono
                st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_abono}])], ignore_index=True)
                st.rerun()
            
            st.subheader("Historial de Compras")
            if not st.session_state.ven.empty:
                st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f], use_container_width=True)
            else: st.info("Sin ventas registradas.")

        with tab2:
            n_cli = st.text_input("NOMBRE")
            if st.button("GUARDAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()

    # --- 4. GESTIÓN STOCK (SOLO ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>ALTA DE MERCANCÍA</h1>", unsafe_allow_html=True)
        with st.form("inv_form", clear_on_submit=True):
            a_p = st.text_input("ARTICULO")
            c_p = st.number_input("CANTIDAD", min_value=1)
            cost_p = st.number_input("COSTO ADQUISICIÓN")
            pvp_p = st.number_input("PVP (VENTA)")
            if st.form_submit_button("GUARDAR EN STOCK"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": a_p, "CANTIDAD": c_p, "COSTO_ADQ": cost_p, "PVP": pvp_p}])], ignore_index=True)
                st.success("Guardado.")
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS (SOLO ADMIN) ---
    elif nav == "💸 GASTOS" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR GASTO"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES (SOLO ADMIN) ---
    elif nav == "📝 REPORTES" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>EXPORTACIÓN</h1>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inv.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 DESCARGAR EXCEL COMPLETO", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%Y%m%d')}.xlsx")
        
        with col_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                pdf_data = exportar_pdf_maestro()
                st.download_button("📥 DESCARGAR PDF RESUMEN", data=pdf_data, file_name=f"Reporte_JR31_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf")
