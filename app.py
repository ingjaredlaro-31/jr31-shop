import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V11.0 (MONUMENTAL Y LIMPIO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Montserrat:wght@700;900&display=swap');
    
    /* Fondo General Profundo */
    .stApp { 
        background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); 
        color: #e0e1dd !important; 
    }
    
    /* FIRMA INFORMATIVA INFERIOR IZQUIERDA */
    .footer-info {
        position: fixed; bottom: 15px; left: 20px;
        color: #2E8B57; font-family: 'Montserrat', sans-serif;
        font-size: 14px; z-index: 1000; line-height: 1.4; font-weight: 900;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 32px; font-weight: 900; 
        text-shadow: 0 0 20px #2E8B57; z-index: 1000;
    }

    /* LOGO JR 31 SHOP - TAMAÑO MONUMENTAL SIN RECTÁNGULOS */
    .logo-monumental {
        font-family: 'Orbitron', sans-serif; 
        font-size: 10rem; /* TAMAÑO MÁXIMO */
        font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-top: 40px;
        margin-bottom: 0px;
        filter: drop-shadow(0 0 35px rgba(255,69,0,0.6));
        line-height: 1; letter-spacing: -5px;
    }

    /* SUBTÍTULO SISTEMA GRANDE */
    .subtitle-grande {
        text-align: center; 
        color: #FFFFFF; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 5px; 
        font-weight: 900;
        font-size: 2.2rem; /* MUCHO MÁS GRANDE */
        margin-top: 5px;
        margin-bottom: 50px;
        text-shadow: 0 0 15px #2E8B57;
    }

    /* Estilo de Inputs (Sin cajas que encierren) */
    label { 
        color: #FF8C00 !important; 
        font-family: 'Orbitron' !important; 
        font-weight: 900 !important; 
        font-size: 1.4rem !important; 
        margin-bottom: 15px !important;
    }

    input {
        background-color: rgba(27, 38, 59, 0.9) !important;
        color: #FFFFFF !important;
        border: 2px solid #FF4500 !important;
        font-size: 1.6rem !important;
        border-radius: 15px !important;
        height: 60px !important;
    }

    /* BOTÓN ACCEDER IMPACTANTE */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 15px !important; border: none !important;
        height: 4em !important; width: 100%; transition: 0.5s;
        font-size: 2rem !important; /* BOTÓN GIGANTE */
        margin-top: 40px;
        box-shadow: 0 10px 40px rgba(255, 69, 0, 0.5) !important;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 60px #2E8B57 !important; 
        transform: scale(1.05); 
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# --- PANTALLA DE ACCESO (VANGUARDIA) ---
if not st.session_state.log:
    # ELIMINADOS LOS RECTÁNGULOS, SÓLO CONTENIDO PURO
    if os.path.exists("logo.png"):
        col_img_l, col_img_c, col_img_r = st.columns([0.5, 2, 0.5])
        with col_img_c:
            st.image("logo.png", use_column_width=True)
    else:
        st.markdown('<p class="logo-monumental">JR 31 SHOP</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle-grande">SISTEMA DE ADMINISTRACIÓN Y VENTA JR31</p>', unsafe_allow_html=True)
    
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
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
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron; text-align: center;'>JR 31 MASTER</h2>", unsafe_allow_html=True)
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
        
        nav = st.radio("SELECCIONE MÓDULO", modulos)
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        c1, c2 = st.columns(2)
        with c1: 
            st.markdown(f'<div style="background: rgba(27, 38, 59, 0.8); border-radius: 20px; padding: 30px; border-left: 10px solid #FF8C00; text-align: center;"><p style="color:#FF8C00; font-family:Orbitron; font-size: 1.5rem;">VENTAS</p><p style="font-family: Montserrat; font-size: 4rem; font-weight: 900; color: white;">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: 
            st.markdown(f'<div style="background: rgba(27, 38, 59, 0.8); border-radius: 20px; padding: 30px; border-left: 10px solid #FF4500; text-align: center;"><p style="color:#FF4500; font-family:Orbitron; font-size: 1.5rem;">CARTERA</p><p style="font-family: Montserrat; font-size: 4rem; font-weight: 900; color: white;">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Registre inventario primero.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success(f"OPERACIÓN EXITOSA: ${t_vta}")

    # --- 3. CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with t1:
            cliente_f = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            st.metric("DEUDA ACTUAL", f"${datos_c['SALDO_DEUDOR']:,.2f}")
            m_a = st.number_input("ABONAR", min_value=0.0)
            if st.button("ABONAR A CUENTA"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_a
                st.rerun()
        with t2:
            n = st.text_input("NOMBRE")
            if st.button("GUARDAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()

    # --- 4. GESTIÓN STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("inv"):
            art = st.text_input("PRODUCTO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO")
            pvp = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)
