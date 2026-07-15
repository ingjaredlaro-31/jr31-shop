import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V10.0 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    .jared-header { position: absolute; top: 10px; right: 30px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900; text-shadow: 0 0 20px #2E8B57; z-index: 1000; }
    .footer-info { position: fixed; bottom: 15px; left: 20px; color: #2E8B57; font-family: 'Montserrat', sans-serif; font-size: 13px; z-index: 1000; font-weight: 900; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.2rem !important; }
    .stButton>button { background: linear-gradient(90deg, #FF4500, #FF8C00) !important; color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; border-radius: 12px !important; height: 3.5em !important; width: 100%; font-size: 1.3rem !important; }
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF4500; }
    .dash-card { background: rgba(27, 38, 59, 0.9); border-radius: 20px; padding: 30px; border-left: 10px solid #FF4500; text-align: center; }
    .metric-value { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">ING JARED LARA RODRIGUEZ 918'125'5735<br>APP CREADA PARA USO COMERCIAL POR EL ING JR 31</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- FUNCIÓN GENERADORA DE PDF MASTER ---
def generar_pdf_master():
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 69, 0) # Naranja
    pdf.cell(0, 10, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(0, 100, 0) # Verde
    pdf.cell(0, 10, f"Generado por: Ing. Jared Laro - {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Resumen Financiero
    v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
    u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
    g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
    d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. RESUMEN FINANCIERO", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"- Ventas Totales Brutas: ${v_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Utilidad Bruta: ${u_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Gastos Operativos: ${g_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Utilidad Neta (Caja): ${u_tot - g_tot:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Total Pendiente en Cartera: ${d_tot:,.2f} MXN", ln=True)
    pdf.ln(5)
    
    # Inventario
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "2. ESTADO DE INVENTARIO", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for idx, row in st.session_state.inv.iterrows():
        pdf.cell(0, 8, f"{row['ARTICULO']}: {row['CANTIDAD']} unidades | PVP: ${row['PVP']}", ln=True)
    
    return pdf.output()

# --- LÓGICA DE ACCESO ---
if not st.session_state.log:
    col_l, col_c, col_r = st.columns([0.1, 2, 0.1])
    with col_c:
        if os.path.exists("logo.png"): st.image("logo.png", width=600)
        else: st.markdown("<h1 style='text-align: center; font-family: Orbitron; font-size: 6rem; background: linear-gradient(to right, #FF4500, #FF8C00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; font-size: 2rem; font-weight: 900;'>BUSINESS TERMINAL v10.0</p>", unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<p style='color: #FF4500; font-family: Orbitron; font-size: 1.5rem; text-align: center;'>PUNTO DE VENTA<br>JR 31 SHOP</p>", unsafe_allow_html=True)
        st.markdown("---")
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO ADMIN", type="password")
            if st.button("ACTIVAR ADMIN"):
                if codigo == "291329": st.session_state.es_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO"); 
            if st.button("CERRAR ADMIN"): st.session_state.es_admin = False; st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin: modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES MASTER"]
        nav = st.radio("MÓDULOS", modulos)
        if st.button("SALIR DE LA APP"): st.session_state.log = False; st.rerun()

    # --- CONTENIDO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="dash-card"><p style="color:#FF8C00;">VENTAS</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="dash-card"><p style="color:#FF4500;">CARTERA</p><p class="metric-value">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL</h1>", unsafe_allow_html=True)
        with st.form("v"):
            p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'] if not st.session_state.inv.empty else ["Vacío"])
            c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            cant = st.number_input("CANTIDAD", min_value=1)
            modo = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
            if st.form_submit_button("VENDER"):
                data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                t_v = data['PVP'] * cant
                uti = (data['PVP'] - data['COSTO_ADQ']) * cant
                st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_v, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant
                if modo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_v
                st.success("Venta Exitosa")

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with tab1:
            cliente_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${datos_c['SALDO_DEUDOR']:,.2f}")
            m_a = st.number_input("ABONAR", min_value=0.0)
            if st.button("REGISTRAR ABONO"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_a
                st.rerun()
        with tab2:
            n = st.text_input("NOMBRE")
            if st.button("GUARDAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()

    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("s"):
            n_p = st.text_input("NOMBRE")
            c_p = st.number_input("CANTIDAD", min_value=1)
            cost_p = st.number_input("COSTO")
            pvp_p = st.number_input("PVP")
            if st.form_submit_button("GUARDAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": n_p, "CANTIDAD": c_p, "COSTO_ADQ": cost_p, "PVP": pvp_p}])], ignore_index=True)
                st.success("Guardado")
        st.dataframe(st.session_state.inv)

    elif nav == "📝 REPORTES MASTER" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES Y EXPORTACIÓN</h1>", unsafe_allow_html=True)
        st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
        
        # BOTÓN PARA PDF
        st.subheader("📄 Reporte Ejecutivo en PDF")
        if st.button("GENERAR PDF RESUMEN"):
            pdf_data = generar_pdf_master()
            st.download_button(label="📥 DESCARGAR PDF AHORA", data=pdf_data, file_name=f"Reporte_JR31_{datetime.now().strftime('%d%m%Y')}.pdf", mime="application/pdf")
            st.success("PDF generado con éxito.")

        st.markdown("---")
        
        # BOTÓN PARA EXCEL (Existente)
        st.subheader("Excel Completo")
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv.to_excel(w, index=False, sheet_name='STOCK')
        st.download_button("📥 DESCARGAR MASTER EXCEL", buf.getvalue(), "JR31_MASTER.xlsx")
        st.markdown('</div>', unsafe_allow_html=True)
