import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V5.0 (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    /* FIRMA INFORMATIVA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed;
        bottom: 15px;
        left: 20px;
        color: rgba(46, 139, 87, 0.8);
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        z-index: 1000;
        line-height: 1.4;
        font-weight: bold;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 20px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    /* Logo Principal */
    .logo-text {
        font-family: 'Orbitron', sans-serif; font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 10px; filter: drop-shadow(0 0 15px rgba(255,69,0,0.3));
    }

    /* Cards del Dashboard */
    .dash-card {
        background: rgba(27, 38, 59, 0.6);
        border-radius: 20px; padding: 25px;
        border-top: 4px solid #FF4500;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        text-align: center; margin-bottom: 15px;
    }

    .metric-title { font-family: 'Orbitron'; font-size: 0.9rem; color: #FF8C00; letter-spacing: 2px; }
    .metric-value { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: #FFFFFF; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 4px solid #FF4500; }
    .sidebar-brand { color: #FF4500 !important; font-family: 'Orbitron'; font-size: 1.2rem; text-align: center; font-weight: 900; letter-spacing: 1px; }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 10px !important; border: none !important;
        height: 3.2em !important; width: 100%; transition: 0.4s;
    }
    .stButton>button:hover { box-shadow: 0 0 20px #2E8B57; transform: scale(1.02); }
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
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px; font-weight: bold;'>SISTEMA ERP POS v5.0</p>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1, 1])
    with col_login:
        st.markdown('<div style="background: #1b263b; padding: 30px; border-radius: 20px; border: 1px solid #FF4500;">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("ACCESO DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<p class='sidebar-brand'>PUNTO DE VENTA<br>JR31 SHOP</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.es_admin:
            codigo = st.text_input("🔓 CÓDIGO ADMIN", type="password")
            if st.button("DESBLOQUEAR PRIVILEGIOS"):
                if codigo == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
        else:
            st.success("🔒 ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES MASTER"]
        
        nav = st.radio("SISTEMA", modulos)
        st.markdown("---")
        if st.button("SALIR DE LA APP"):
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
            st.markdown(f'<div class="dash-card"><p class="metric-title">PENDIENTE COBRO</p><p class="metric-value" style="color: #FF4500;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with col_d3:
            if st.session_state.es_admin:
                valor_neto = u_tot - g_tot
                st.markdown(f'<div class="dash-card"><p class="metric-title">BALANCE NETO</p><p class="metric-value" style="color: #2E8B57;">${valor_neto:,.0f}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="dash-card"><p class="metric-title">ESTADO</p><p class="metric-value" style="font-size: 1.5rem;">VENDEDORA ACTIVA</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Aviso: El inventario está vacío. Notificar al Administrador.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR TRANSACCIÓN"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success(f"Venta registrada con éxito: ${t_vta}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        
        with t1:
            cliente_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            
            c_ab1, c_ab2 = st.columns(2)
            c_ab1.markdown(f'<div class="dash-card"><p class="metric-title">SALDO PENDIENTE</p><p class="metric-value">${datos_c["SALDO_DEUDOR"]:,.2f}</p></div>', unsafe_allow_html=True)
            with c_ab2:
                m_pago = st.number_input("REGISTRAR ABONO", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                    st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
                    st.success("Abono aplicado exitosamente."); st.rerun()

            if not st.session_state.ven.empty:
                st.subheader("🛒 HISTORIAL DE COMPRAS")
                st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f], use_container_width=True)

        with t2:
            n_cli = st.text_input("NOMBRE COMPLETO DEL CLIENTE")
            if st.button("GUARDAR EN CARTERA"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.success("Cliente registrado."); st.rerun()

    # --- 4. GESTIÓN STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>ADMINISTRACIÓN DE INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("NOMBRE DEL PRODUCTO")
            cant = st.number_input("CANTIDAD INICIAL", min_value=1)
            costo = st.number_input("COSTO DE ADQUISICIÓN")
            pvp = st.number_input("PRECIO VENTA PÚBLICO")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS Y REPORTES (ADMIN) ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>REGISTRO DE GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            con = st.text_input("CONCEPTO (Renta, Luz, Envíos, etc.)")
            mon = st.number_input("IMPORTE DEL GASTO")
            if st.form_submit_button("GUARDAR GASTO"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    elif nav == "📝 REPORTES MASTER":
        st.markdown("<h1 style='font-family: Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
            st.session_state.inv.to_excel(w, index=False, sheet_name='INVENTARIO')
            st.session_state.abonos.to_excel(w, index=False, sheet_name='ABONOS')
            st.session_state.gas.to_excel(w, index=False, sheet_name='GASTOS')
        st.download_button("📥 DESCARGAR REPORTE MAESTRO EXCEL", buf.getvalue(), f"JR31_MASTER_LARO_{datetime.now().strftime('%Y%m%d')}.xlsx")
