
¡Entendido, Ingeniero Jared Laro! Aquí tienes el sistema completo y definitivo. No le falta ninguna parte. He unido el diseño monumental de la portada con todos los módulos internos (Ventas, Stock, Cartera de Clientes con historial, Gastos y Reportes Excel/PDF).
Este código está diseñado para ser copiado y pegado íntegramente en tu archivo app.py.
1️⃣ REQUISITOS (requirements.txt)
Asegúrate de que este archivo en GitHub tenga estas líneas para que no marque error:
code
Text
streamlit
pandas
openpyxl
fpdf2
2️⃣ CÓDIGO MAESTRO COMPLETO (app.py)
code
Python
import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | SUPREME SYSTEM", layout="wide", page_icon="⚡")

# --- ESTILO LUXURY TITANIUM V15.0 (DISEÑO MONUMENTAL COMPLETO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    /* Fondo Luxury Black */
    .stApp { 
        background: radial-gradient(circle at top, #1e272e 0%, #000000 100%);
        color: #FFFFFF !important; 
    }
    
    /* FIRMA DEL INGENIERO ABAJO */
    .footer-info {
        position: fixed; bottom: 15px; left: 25px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px; z-index: 1000; line-height: 1.4; font-weight: 700;
        letter-spacing: 1px;
    }

    /* NOMBRE SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 26px; font-weight: 900; 
        text-shadow: 0 0 10px rgba(46, 139, 87, 0.8); z-index: 1000;
    }

    /* EL NOMBRE GIGANTE JR 31 SHOP */
    .nombre-tienda-gigante {
        font-family: 'Orbitron', sans-serif;
        font-size: 12vw;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 10%, #FF8C00 50%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
        margin-bottom: -15px;
        filter: drop-shadow(0 15px 25px rgba(0,0,0,0.9));
        line-height: 0.9;
        text-transform: uppercase;
    }

    .subtitulo-elegante {
        text-align: center; color: #2E8B57; 
        font-family: 'Montserrat', sans-serif; 
        letter-spacing: 15px; font-weight: 100;
        font-size: 1.6rem; margin-bottom: 50px;
        text-transform: uppercase; opacity: 0.9;
    }

    /* INPUTS DE ACCESO */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid #444 !important;
    }
    
    input {
        color: #FF8C00 !important;
        font-size: 1.4rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    /* BOTÓN ACCEDER ELEGANTE */
    .stButton>button {
        background: transparent !important;
        color: #FFFFFF !important; 
        font-family: 'Orbitron' !important;
        font-weight: 400 !important; 
        border-radius: 5px !important; 
        border: 1px solid #FF8C00 !important;
        height: 3.8em !important; width: 100%; 
        font-size: 1.6rem !important;
        letter-spacing: 5px; margin-top: 20px;
        text-transform: uppercase;
        box-shadow: inset 0 0 10px rgba(255, 140, 0, 0.1);
    }
    .stButton>button:hover { 
        background: #FF8C00 !important; color: #000000 !important; font-weight: 900 !important;
        box-shadow: 0 0 40px rgba(255, 140, 0, 0.6) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF8C00; }
    
    /* CARDS DASHBOARD */
    .dash-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px; padding: 35px;
        border-top: 5px solid #FF8C00;
        text-align: center; box-shadow: 0 15px 30px rgba(0,0,0,0.5);
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.9rem !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE BASES DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- FUNCIÓN GENERAR PDF ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(0, 20, "JR 31 SHOP - REPORTE MAESTRO", ln=True, align='C')
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f"Generado por: Ing. Jared Laro | {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    v_total = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"RESUMEN FINANCIERO", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"- Ventas Totales: ${v_total:,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Utilidad Real: ${st.session_state.ven['UTILIDAD'].sum():,.2f} MXN", ln=True)
    pdf.cell(0, 10, f"- Cartera Pendiente: ${st.session_state.cli['SALDO_DEUDOR'].sum():,.2f} MXN", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ESTADO DE INVENTARIO", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, r in st.session_state.inv.iterrows():
        pdf.cell(0, 8, f"{r['ARTICULO']}: {r['CANTIDAD']} unidades | PVP: ${r['PVP']}", ln=True)
    
    return pdf.output()

# --- LÓGICA DE ACCESO ---
if not st.session_state.log:
    st.markdown('<p class="nombre-tienda-gigante">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo-elegante">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("Acceso Inválido")
else:
    # --- MENÚ INTERIOR ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.5rem; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            cod = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if cod == "291329": st.session_state.es_admin = True; st.rerun()
        else:
            st.success("🔒 MODO ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.es_admin = False; st.rerun()
        
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.sidebar.radio("MENÚ", modulos)
        if st.button("SALIR DEL SISTEMA"): st.session_state.log = False; st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>DASHBOARD OPERATIVO</h1>", unsafe_allow_html=True)
        v = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="dash-card"><p style="color:#FF8C00; font-family:Orbitron;">VENTAS TOTALES</p><p style="font-size:5rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="dash-card"><p style="color:#2E8B57; font-family:Orbitron;">CARTERA CLIENTES</p><p style="font-size:5rem; font-weight:900;">${d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family:Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty:
            st.info("Registre productos en inventario primero.")
        else:
            with st.form("venta_form"):
                p_sel = st.selectbox("SELECCIONE PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("COMPLETAR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    total_v = data['PVP'] * cant_v
                    utilidad = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": total_v, "UTILIDAD": utilidad, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += total_v
                    st.success(f"Venta registrada: ${total_v}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE CLIENTES</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t1:
            c_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.cli['NOMBRE'])
            dat = st.session_state.cli[st.session_state.cli['NOMBRE'] == c_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${dat['SALDO_DEUDOR']:,.2f}")
            abono = st.number_input("REGISTRAR ABONO", min_value=0.0)
            if st.button("PAGAR"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_f, 'SALDO_DEUDOR'] -= abono
                st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_f, "MONTO": abono}])], ignore_index=True)
                st.rerun()
            
            st.subheader("Historial de Compras")
            if not st.session_state.ven.empty:
                st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == c_f], use_container_width=True)

        with t2:
            n_c = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_c, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()

    # --- 4. GESTIÓN STOCK (PROTEGIDO) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("inv_form", clear_on_submit=True):
            a = st.text_input("ARTÍCULO")
            c = st.number_input("CANTIDAD", min_value=1)
            cost = st.number_input("COSTO ADQUISICIÓN")
            pvp = st.number_input("PRECIO VENTA")
            if st.form_submit_button("AÑADIR A STOCK"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": a, "CANTIDAD": c, "COSTO_ADQ": cost, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS (PROTEGIDO) ---
    elif nav == "💸 GASTOS" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES (PROTEGIDO) ---
    elif nav == "📝 REPORTES" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
                st.session_state.inv.to_excel(w, index=False, sheet_name='STOCK')
            st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%d%m%Y')}.xlsx")
        with c_r2:
            if st.button("📄 GENERAR PDF MAESTRO"):
                pdf_bytes = generar_pdf()
                st.download_button("📥 DESCARGAR PDF", pdf_bytes, f"Reporte_JR31_{datetime.now().strftime('%d%m%Y')}.pdf", mime="application/pdf")
