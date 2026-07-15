import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO "TECH-PREMIUM" (CSS AVANZADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Righteous&family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');

    /* Fondo Oscuro Total */
    .stApp {
        background: radial-gradient(circle, #0d1b2a 0%, #000000 100%);
        color: #e0e1dd !important;
    }

    /* FIRMA DEL INGENIERO */
    .ing-signature {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: #FF8C00;
        font-family: 'Orbitron', sans-serif;
        font-size: 10px;
        letter-spacing: 2px;
        z-index: 999;
    }

    /* LOGO TIPO BRANDING */
    .logo-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255,69,0,0.5));
        margin-bottom: 0px;
    }

    /* TARJETAS DE CARBONO (No borrosas) */
    .carbon-card {
        background: #1b263b;
        border-left: 5px solid #FF4500;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    /* INPUTS MODERNOS */
    input {
        background-color: #0d1b2a !important;
        color: #FF8C00 !important;
        border: 1px solid #2E8B57 !important;
        border-radius: 5px !important;
    }

    /* BOTONES DE PODER */
    .stButton>button {
        background: #FF4500 !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
        border: none !important;
        padding: 15px !important;
        width: 100%;
        border-radius: 5px !important;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(255,69,0,0.4);
    }
    .stButton>button:hover {
        background: #2E8B57 !important;
        box-shadow: 0 0 20px rgba(46,139,87,0.8);
        transform: translateY(-2px);
    }

    /* SIDEBAR PROFESIONAL */
    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 2px solid #FF4500;
    }

    /* MÉTRICAS NEÓN */
    [data-testid="stMetricValue"] {
        color: #2E8B57 !important;
        font-family: 'Orbitron', sans-serif;
    }
    </style>
    <div class="ing-signature">SISTEMA DESARROLLADO POR EL ING. JARED LARO © 2024</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (BLINDADA CONTRA ERRORES) ---
if 'inv' not in st.session_state: 
    st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "INVERSION_ADQ", "VALOR_VENTA"])
if 'ven' not in st.session_state: 
    st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO", "MODO"])
if 'cli' not in st.session_state: 
    st.session_state.cli = pd.DataFrame([{"NOMBRE": "PUBLICO GENERAL", "SALDO_DEUDOR": 0.0}])

# --- SISTEMA DE ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron;'>CONTROL DE OPERACIONES COMERCIALES</p>", unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1, 1])
    with col_login:
        st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: white;'>AUTENTICACIÓN REQUERIDA</h4>", unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("DESBLOQUEAR"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else:
                st.error("ACCESO DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 10px;'>ING. JARED LARO | SOFTWARE DIVISION</p>", unsafe_allow_html=True)

else:
    # --- MENÚ DE NAVEGACIÓN ORIGINAL ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron;'>JR 31 PANEL</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 10px;'>ING. JARED LARO v2.1</p>", unsafe_allow_html=True)
        st.markdown("---")
        nav = st.sidebar.selectbox("MÓDULOS", ["📊 ESTADÍSTICAS", "📦 ENTRADA DE PRODUCTO", "🛒 PUNTO DE VENTA", "👤 CARTERA CLIENTES", "📝 REPORTES"])
        st.markdown("---")
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.log = False
            st.rerun()

    # --- 1. ESTADÍSTICAS (DASHBOARD) ---
    if nav == "📊 ESTADÍSTICAS":
        st.markdown("<h1 style='font-family: Orbitron;'>INTELIGENCIA DE NEGOCIO</h1>", unsafe_allow_html=True)
        
        # FIX ERROR: Verificamos si la columna existe antes de sumar
        ventas_totales = st.session_state.ven['MONTO'].sum() if not st.session_state.ven.empty else 0.0
        inversion_total = st.session_state.inv['INVERSION_ADQ'].sum() if not st.session_state.inv.empty else 0.0
        deuda_total = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0.0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.metric("INGRESOS VENTAS", f"${ventas_totales:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.metric("INVERSIÓN EN STOCK", f"${inversion_total:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.metric("CUENTAS POR COBRAR", f"${deuda_total:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. ENTRADA DE PRODUCTO (ANTES LOGÍSTICA USA) ---
    elif nav == "📦 ENTRADA DE PRODUCTO":
        st.markdown("<h1 style='font-family: Orbitron;'>REGISTRO DE MERCANCÍA</h1>", unsafe_allow_html=True)
        with st.form("entrada_form"):
            col_a, col_b = st.columns(2)
            art = col_a.text_input("DESCRIPCIÓN DEL ARTÍCULO")
            cant = col_b.number_input("CANTIDAD", min_value=1)
            inv_adq = col_a.number_input("INVERSIÓN DE ADQUISICIÓN (PAGADO)")
            v_vta = col_b.number_input("VALOR DE VENTA ESPERADO")
            if st.form_submit_button("REGISTRAR EN SISTEMA"):
                nueva_f = pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "INVERSION_ADQ": inv_adq, "VALOR_VENTA": v_vta}])
                st.session_state.inv = pd.concat([st.session_state.inv, nueva_f], ignore_index=True)
                st.success("DATOS INDEXADOS CORRECTAMENTE")
        st.table(st.session_state.inv)

    # --- 3. PUNTO DE VENTA ---
    elif nav == "🛒 PUNTO DE VENTA":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        with st.form("venta_form"):
            cliente = st.selectbox("SELECCIONAR CLIENTE", st.session_state.cli['NOMBRE'])
            monto_v = st.number_input("MONTO DE OPERACIÓN", min_value=0.0)
            modo_v = st.selectbox("MÉTODO DE PAGO", ["CONTADO", "CRÉDITO"])
            if st.form_submit_button("FINALIZAR TRANSACCIÓN"):
                nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CLIENTE": cliente, "MONTO": monto_v, "MODO": modo_v}])
                st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
                if modo_v == "CRÉDITO":
                    st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente, 'SALDO_DEUDOR'] += monto_v
                st.success("TRANSACCIÓN COMPLETADA")

    # --- 4. CARTERA CLIENTES ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>GESTIÓN DE CARTERA</h1>", unsafe_allow_html=True)
        nc = st.text_input("NOMBRE COMPLETO DEL CLIENTE")
        if st.button("DAR DE ALTA"):
            st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nc, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
            st.rerun()
        st.dataframe(st.session_state.cli, use_container_width=True)

    # --- 5. REPORTES ---
    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family: Orbitron;'>EXPORTACIÓN DE DATOS</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv.to_excel(w, index=False, sheet_name='INVENTARIO')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR MASTER REPORT EXCEL", buf.getvalue(), "REPORTE_JR31_LARO.xlsx")
