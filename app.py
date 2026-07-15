import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V6.0 (DISEÑO IMPACTANTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    /* FIRMA INFORMATIVA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed;
        bottom: 15px;
        left: 20px;
        color: rgba(46, 139, 87, 0.9);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        z-index: 1000;
        line-height: 1.4;
        font-weight: bold;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 24px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP GIGANTE */
    .logo-text-grande {
        font-family: 'Orbitron', sans-serif; 
        font-size: 6rem; /* TAMAÑO AUMENTADO */
        font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-bottom: 0px;
        filter: drop-shadow(0 0 25px rgba(255,69,0,0.5));
        line-height: 1;
    }

    /* SUBTÍTULO GRANDE */
    .subtitle-grande {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 8px; 
        font-weight: 900;
        font-size: 1.8rem; /* TAMAÑO AUMENTADO */
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Contenedor de Login */
    .login-container {
        background: rgba(27, 38, 59, 0.8);
        padding: 40px;
        border-radius: 25px;
        border: 2px solid #FF4500;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }

    .metric-title { font-family: 'Orbitron'; font-size: 1rem; color: #FF8C00; letter-spacing: 2px; }
    .metric-value { font-family: 'Montserrat'; font-size: 3.5rem; font-weight: 900; color: #FFFFFF; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF4500; }
    .sidebar-brand { color: #FF4500 !important; font-family: 'Orbitron'; font-size: 1.3rem; text-align: center; font-weight: 900; }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 12px !important; border: none !important;
        height: 4em !important; width: 100%; transition: 0.4s;
        font-size: 1.2rem !important;
    }
    .stButton>button:hover { box-shadow: 0 0 30px #2E8B57; transform: scale(1.03); }

    label { color: #FFFFFF !important; font-family: 'Orbitron' !important; font-weight: bold !important; font-size: 1rem !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.log:
    # ELIMINADO EL ESPACIO DEL LOGO Y AUMENTADO EL TAMAÑO DE TEXTO
    st.markdown('<p class="logo-text-grande">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-grande">SISTEMA ERP POS v6.0</p>', unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([0.8, 1, 0.8])
    with col_login:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DATOS INCORRECTOS")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<p class='sidebar-brand'>PUNTO DE VENTA<br>JR31 SHOP</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO ADMIN", type="password")
            if st.button("ACTIVAR ADMIN"):
                if codigo == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR ADMIN"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES MASTER"]
        
        nav = st.radio("SELECCIONE MÓDULO", modulos)
        st.markdown("---")
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0.0
        u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0.0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0.0
        g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0.0

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.markdown(f'<div class="dash-card"><p class="metric-title">VENTAS TOTALES</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d2:
            st.markdown(f'<div class="dash-card"><p class="metric-title">CUENTAS POR COBRAR</p><p class="metric-value" style="color: #FF4500;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d3:
            if st.session_state.es_admin:
                valor_neto = u_tot - g_tot
                st.markdown(f'<div class="dash-card"><p class="metric-title">BALANCE NETO</p><p class="metric-value" style="color: #2E8B57;">${valor_neto:,.0f}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="dash-card"><p class="metric-title">SISTEMA</p><p class="metric-value" style="font-size: 2rem;">VENDEDORA</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Sin inventario cargado.")
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
                    st.success(f"VENTA COMPLETADA: ${t_vta}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        
        with t1:
            cliente_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            
            c_ab1, c_ab2 = st.columns(2)
            c_ab1.markdown(f'<div class="dash-card"><p class="metric-title">SALDO PENDIENTE</p><p class="metric-value">${datos_c["SALDO_DEUDOR"]:,.2f}</p></div>', unsafe_allow_html=True)
            with c_ab2:
                m_pago = st.number_input("REGISTRAR ABONO", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                    st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
                    st.success("Abono aplicado."); st.rerun()

            if not st.session_state.ven.empty:
                st.subheader("🛒 HISTORIAL DE COMPRAS")
                st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f], use_container_width=True)

        with t2:
            n_cli = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR EN CARTERA"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.success("Guardado."); st.rerun()

    # --- 4. GESTIÓN STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>ADMINISTRACIÓN DE STOCK</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("PRODUCTO")
            cant = st.number_input("STOCK INICIAL", min_value=1)
            costo = st.number_input("COSTO ADQ.")
            pvp = st.number_input("PVP")
            if st.form_submit_button("ACTUALIZAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS Y REPORTES (ADMIN) ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>REGISTRO DE GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("IMPORTE")
            if st.form_submit_button("GUARDAR"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    elif nav == "📝 REPORTES MASTER":
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%Y%m%d')}.xlsx")
