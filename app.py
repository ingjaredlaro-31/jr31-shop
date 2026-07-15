import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V7.0 (ULTRA IMPACTO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    
    /* Fondo General */
    .stApp { 
        background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); 
        color: #e0e1dd !important; 
    }
    
    /* FIRMA INFORMATIVA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed;
        bottom: 15px;
        left: 20px;
        color: #2E8B57;
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        z-index: 1000;
        line-height: 1.4;
        font-weight: 900;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; 
        text-shadow: 0 0 20px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP - TAMAÑO MONUMENTAL */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif; 
        font-size: 9rem; /* TAMAÑO MEGA GIGANTE */
        font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-top: 50px;
        margin-bottom: 0px;
        filter: drop-shadow(0 0 30px rgba(255,69,0,0.6));
        line-height: 1;
        letter-spacing: -5px;
    }

    /* SUBTÍTULO SISTEMA - TAMAÑO GRANDE */
    .subtitle-grande {
        text-align: center; 
        color: #FFFFFF; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 12px; 
        font-weight: 900;
        font-size: 2.5rem; /* MUCHO MÁS GRANDE */
        margin-top: 10px;
        margin-bottom: 50px;
        text-shadow: 0 0 10px #2E8B57;
    }

    /* Contenedor de Login Estilizado (Sin rectángulo superior) */
    .login-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 69, 0, 0.3);
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }

    /* Botón Desbloquear */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 15px !important; border: none !important;
        height: 4.5em !important; width: 100%; transition: 0.5s;
        font-size: 1.4rem !important;
        margin-top: 20px;
    }
    .stButton>button:hover { box-shadow: 0 0 40px #2E8B57; transform: scale(1.05); }

    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.2rem !important; }
    
    input { 
        background-color: #1b263b !important; 
        color: #FFFFFF !important; 
        border: 2px solid #415a77 !important; 
        font-size: 1.2rem !important;
        border-radius: 10px !important;
    }

    /* Estilo Dashboard */
    .dash-card {
        background: rgba(27, 38, 59, 0.8);
        border-radius: 25px; padding: 35px;
        border-left: 8px solid #FF4500;
        text-align: center;
    }
    .metric-value { font-family: 'Montserrat'; font-size: 4rem; font-weight: 900; color: #FFFFFF; }
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

# --- PANTALLA DE ACCESO (SIN RECTÁNGULOS VACÍOS) ---
if not st.session_state.log:
    # EL TEXTO AHORA ES GIGANTE Y SIN CAJAS ARRIBA
    st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-grande">SISTEMA ERP POS v7.0</p>', unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([0.8, 1, 0.8])
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
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
        st.markdown("<h1 style='color: #FF4500; font-family: Orbitron; font-size: 1.5rem;'>PUNTO DE VENTA<br>JR 31 SHOP</h1>", unsafe_allow_html=True)
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
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- CONTENIDO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="dash-card"><p style="color:#FF8C00; font-family:Orbitron;">VENTAS TOTALES</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="dash-card"><p style="color:#FF4500; font-family:Orbitron;">POR COBRAR</p><p class="metric-value">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Inventario vacío.")
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

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        cliente_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
        datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
        st.markdown(f'<div class="dash-card"><p style="color:#FF8C00; font-family:Orbitron;">DEUDA ACTUAL</p><p class="metric-value">${datos_c["SALDO_DEUDOR"]:,.2f}</p></div>', unsafe_allow_html=True)
        
        m_pago = st.number_input("ABONAR", min_value=0.0)
        if st.button("APLICAR PAGO"):
            st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
            st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
            st.rerun()

    elif nav == "📦 GESTIÓN STOCK":
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("inv"):
            art = st.text_input("PRODUCTO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO")
            pvp = st.number_input("PRECIO")
            if st.form_submit_button("ACTUALIZAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)
