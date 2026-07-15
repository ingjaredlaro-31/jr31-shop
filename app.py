import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ING. JARED LARO | BUSINESS INTELLIGENCE", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V4.0 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    /* Branding Superior Derecho */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 22px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* Logo Principal Estilo Logo */
    .logo-text {
        font-family: 'Orbitron', sans-serif; font-size: 4rem; font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 20px; filter: drop-shadow(0 0 20px rgba(255,69,0,0.4));
    }

    /* Tarjetas del Dashboard (Novedosas) */
    .dash-card {
        background: rgba(27, 38, 59, 0.6);
        border-radius: 20px; padding: 30px;
        border-top: 4px solid #FF4500;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center; transition: 0.3s;
    }
    .dash-card:hover { border-top: 4px solid #2E8B57; transform: translateY(-5px); }

    /* Métricas Gigantes */
    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; }
    .metric-value { font-family: 'Montserrat'; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; }

    /* Estilo Sidebar */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #2E8B57; }
    .sidebar-title { color: #FF4500 !important; font-family: 'Orbitron'; font-size: 1.5rem; text-align: center; font-weight: 900; }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 10px !important; border: none !important;
        height: 3.5em !important; width: 100%; transition: 0.4s;
    }
    .stButton>button:hover { box-shadow: 0 0 25px #2E8B57; transform: scale(1.02); }

    /* Input Fields */
    input { background-color: #0d1b2a !important; color: #FF8C00 !important; border: 1px solid #415a77 !important; font-weight: bold !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS BLINDADA ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px;'>SISTEMA ERP DESARROLLADO POR ING. JARED LARO</p>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1, 1])
    with col_login:
        st.markdown('<div style="background: #1b263b; padding: 30px; border-radius: 20px; border: 1px solid #FF4500;">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<p class='sidebar-title'>ING. JARED LARO</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO ADMIN", type="password")
            if st.button("ACTIVAR PRIVILEGIOS"):
                if codigo == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
        else:
            st.success("🔒 ADMIN ACTIVO")
            if st.button("CERRAR SESIÓN ADMIN"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES MASTER"]
        
        nav = st.radio("SISTEMA DE NAVEGACIÓN", modulos)
        st.markdown("---")
        if st.button("SALIR DE LA APP"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD NOVEDOSO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA DE NEGOCIO</h1>", unsafe_allow_html=True)
        
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0.0
        u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0.0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0.0
        g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0.0

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.markdown(f'<div class="dash-card"><p class="metric-title">VENTAS BRUTAS</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d2:
            st.markdown(f'<div class="dash-card"><p class="metric-title">CARTERA POR COBRAR</p><p class="metric-value" style="color: #FF4500;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d3:
            valor_neto = u_tot - g_tot
            color_neto = "#2E8B57" if valor_neto >= 0 else "#FF4500"
            st.markdown(f'<div class="dash-card"><p class="metric-title">UTILIDAD NETA</p><p class="metric-value" style="color: {color_neto};">${valor_neto:,.0f}</p></div>', unsafe_allow_html=True)

        if st.session_state.es_admin:
            st.markdown("### 📊 RESUMEN OPERATIVO")
            st.dataframe(st.session_state.ven.tail(10), use_container_width=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Inventario vacío.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("MODO PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success("OPERACIÓN EXITOSA")

    # --- 3. CARTERA (ERROR CORREGIDO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ REGISTRAR CLIENTE"])
        
        with t1:
            cliente_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            
            c_ab1, c_ab2 = st.columns(2)
            c_ab1.markdown(f'<div class="dash-card"><p class="metric-title">DEUDA ACTUAL</p><p class="metric-value">${datos_c["SALDO_DEUDOR"]:,.2f}</p></div>', unsafe_allow_html=True)
            with c_ab2:
                m_pago = st.number_input("REGISTRAR ABONO", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                    st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
                    st.rerun()

            st.markdown("### 🛒 COMPRAS REALIZADAS")
            # --- BLINDAJE ANTI-ERROR ---
            if not st.session_state.ven.empty:
                historial = st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f]
                if not historial.empty:
                    st.dataframe(historial, use_container_width=True)
                else:
                    st.info("Este cliente no tiene compras registradas.")
            else:
                st.info("No hay ventas en la base de datos todavía.")

        with t2:
            n_cli = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR CLIENTE"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.success("CLIENTE AÑADIDO")

    # --- 4. GESTIÓN STOCK (SOLO ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("ARTÍCULO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO ADQUISICIÓN")
            pvp = st.number_input("PVP")
            if st.form_submit_button("ACTUALIZAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS Y REPORTES ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    elif nav == "📝 REPORTES MASTER":
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR EXCEL MASTER", buf.getvalue(), f"JR31_MASTER_LARO.xlsx")
