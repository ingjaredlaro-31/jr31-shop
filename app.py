import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | ELITE BUSINESS", layout="wide", page_icon="⚡")

# --- ESTILO LUXURY PLATINUM V13.0 (IMPACTO TOTAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@300;800;900&display=swap');
    
    /* Fondo Dark Luxury Profesional */
    .stApp { 
        background: radial-gradient(circle at center, #1e272e 0%, #050505 100%);
        color: #FFFFFF !important; 
    }
    
    /* FIRMA DEL INGENIERO - ELEGANTE ABAJO */
    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 14px; z-index: 1000; line-height: 1.5; font-weight: 800;
        letter-spacing: 1px;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #FF8C00; font-family: 'Orbitron', sans-serif;
        font-size: 32px; font-weight: 900; 
        text-shadow: 0 0 15px rgba(255, 140, 0, 0.6); z-index: 1000;
    }

    /* JR 31 SHOP - TAMAÑO MONUMENTAL SIN RECUADROS */
    .logo-supreme {
        font-family: 'Orbitron', sans-serif; 
        font-size: 11vw; /* OCUPA CASI TODO EL ANCHO */
        font-weight: 900;
        background: linear-gradient(180deg, #FFFFFF 30%, #FF8C00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-top: 20px;
        margin-bottom: -10px;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.8));
        line-height: 0.9;
        letter-spacing: -5px;
    }

    .subtitle-supreme {
        text-align: center; 
        color: #2E8B57; 
        font-family: 'Orbitron', sans-serif; 
        letter-spacing: 15px; 
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 60px;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(46, 139, 87, 0.5);
    }

    /* Campos de Acceso - Grandes y Limpios */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid #444 !important;
        height: 70px !important;
    }
    
    input {
        color: white !important;
        font-size: 1.8rem !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-align: center !important;
    }

    /* BOTÓN ACCEDER - PODER TOTAL */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border-radius: 20px !important; 
        border: none !important;
        height: 4.5em !important; 
        width: 100%; 
        transition: 0.4s;
        font-size: 2.2rem !important; /* TEXTO MUY GRANDE */
        margin-top: 40px;
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.4) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 60px rgba(46, 139, 87, 0.8) !important; 
        background: #2E8B57 !important;
        transform: scale(1.02);
    }

    /* Eliminar espacios extra de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .css-1offfwp { padding: 0 !important; }
    
    label { 
        color: #FF8C00 !important; 
        font-family: 'Montserrat' !important; 
        font-weight: 900 !important; 
        font-size: 1.3rem !important; 
        text-transform: uppercase;
    }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | CONTACTO: 918'125'5735<br>
        PROYECTO DESARROLLADO PARA USO COMERCIAL EXCLUSIVO DE JR 31 SHOP
    </div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- PANTALLA DE ACCESO ---
if not st.session_state.log:
    # EL LOGO AHORA ES TEXTO MONUMENTAL O IMAGEN PURA
    if os.path.exists("logo.png"):
        col_img_l, col_img_c, col_img_r = st.columns([0.2, 2, 0.2])
        with col_img_c:
            st.image("logo.png", use_column_width=True)
    else:
        st.markdown('<p class="logo-supreme">JR 31 SHOP</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle-supreme">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    
    # LOGIN CENTER
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        uid = st.text_input("USUARIO ADM")
        ukey = st.text_input("CONTRASEÑA", type="password")
        if st.button("ACCEDER"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("ACCESO DENEGADO")
else:
    # --- INTERFAZ INTERNA ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; font-size:1.5rem; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("---")
        if not st.session_state.es_admin:
            cod = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if cod == "291329": st.session_state.es_admin = True; st.rerun()
        else:
            st.success("🔒 ADMIN ACTIVO")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.es_admin = False; st.rerun()
        
        mod = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin: mod += ["📦 GESTIÓN STOCK", "📝 REPORTES"]
        nav = st.sidebar.radio("MENÚ PRINCIPAL", mod)
        if st.button("SALIR DEL SISTEMA"): st.session_state.log = False; st.rerun()

    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="background:rgba(255,140,0,0.1); border:2px solid #FF8C00; border-radius:20px; padding:40px; text-align:center;"><p style="font-family:Orbitron; font-size:1.5rem; color:#FF8C00;">TOTAL VENTAS</p><p style="font-size:5rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="background:rgba(46,139,87,0.1); border:2px solid #2E8B57; border-radius:20px; padding:40px; text-align:center;"><p style="font-family:Orbitron; font-size:1.5rem; color:#2E8B57;">EN CARTERA</p><p style="font-size:5rem; font-weight:900;">${d:,.0f}</p></div>', unsafe_allow_html=True)

    # --- VENTA ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family:Orbitron;'>NUEVA VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Inventario sin productos registrados.")
        else:
            with st.form("venta_pos"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("MÉTODO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR TRANSACCIÓN"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    total = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": total, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO": st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += total
                    st.success(f"VENTA COMPLETADA: ${total}")

    # --- STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO MAESTRO</h1>", unsafe_allow_html=True)
        with st.form("inv"):
            a = st.text_input("ARTÍCULO")
            c = st.number_input("CANTIDAD", min_value=1)
            ca = st.number_input("COSTO ADQUISICIÓN")
            pv = st.number_input("PRECIO VENTA")
            if st.form_submit_button("REGISTRAR"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": a, "CANTIDAD": c, "COSTO_ADQ": ca, "PVP": pv}])], ignore_index=True)
        st.dataframe(st.session_state.inv, use_container_width=True)
