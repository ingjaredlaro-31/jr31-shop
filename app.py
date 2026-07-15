import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-PREMIUM V8.0 (DISEÑO LIMPIO E IMPACTANTE) ---
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
        position: fixed;
        bottom: 15px;
        left: 20px;
        color: #2E8B57;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        z-index: 1000;
        line-height: 1.4;
        font-weight: 900;
    }

    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
    .jared-header {
        position: absolute; top: 10px; right: 30px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 30px; font-weight: 900; 
        text-shadow: 0 0 20px #2E8B57; z-index: 1000;
    }

    /* ESTILO DE ETIQUETAS Y TEXTO GRANDE */
    label { 
        color: #FF8C00 !important; 
        font-family: 'Orbitron' !important; 
        font-weight: 900 !important; 
        font-size: 1.3rem !important; /* LETRAS MÁS GRANDES */
        margin-bottom: 10px !important;
    }

    input {
        background-color: #1b263b !important;
        color: #FFFFFF !important;
        border: 2px solid #FF4500 !important;
        font-size: 1.5rem !important; /* TEXTO DE INPUT MÁS GRANDE */
        border-radius: 12px !important;
        height: 50px !important;
    }

    /* BOTÓN ACCEDER GIGANTE */
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important; 
        font-family: 'Orbitron' !important;
        font-weight: 900 !important; 
        border-radius: 15px !important; 
        border: none !important;
        height: 4em !important; 
        width: 100%; 
        transition: 0.5s;
        font-size: 1.8rem !important; /* BOTÓN MÁS GRANDE */
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(255, 69, 0, 0.4) !important;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 50px #2E8B57 !important; 
        transform: scale(1.05); 
    }

    /* DASHBOARD Y TARJETAS */
    .dash-card {
        background: rgba(27, 38, 59, 0.9);
        border-radius: 25px; padding: 40px;
        border-left: 10px solid #FF4500;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .metric-value { 
        font-family: 'Montserrat'; 
        font-size: 5rem; /* NÚMEROS GIGANTES */
        font-weight: 900; 
        color: #FFFFFF; 
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF4500; }
    
    /* Quitamos cualquier contenedor fantasma */
    .css-1offfwp { padding: 0 !important; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ 918'125'5735<br>
        APP CREADA Y DESARROLLADA PARA USO COMERCIAL POR EL ING JR 31
    </div>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA MOSTRAR LOGO SIN RECTÁNGULOS ---
def mostrar_logo_limpio():
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=False, width=600) # LOGO EN GRANDE
    else:
        st.markdown("<h1 style='text-align: center; font-family: Orbitron; font-size: 6rem; background: linear-gradient(to right, #FF4500, #FF8C00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>JR 31 SHOP</h1>", unsafe_allow_html=True)

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
    # ELIMINADO EL RECTÁNGULO, SOLO LOGO O TEXTO
    col_l, col_c, col_r = st.columns([0.5, 2, 0.5])
    with col_c:
        mostrar_logo_limpio()
        st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 10px; font-weight: 900; font-size: 2rem;'>SISTEMA ERP POS v8.0</p>", unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        # Aquí solo los inputs y el botón, sin cajas extra
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
        if os.path.exists("logo.png"):
            st.image("logo.png", width=150)
        st.markdown("<p style='color: #FF4500; font-family: Orbitron; font-size: 1.5rem; text-align: center;'>JR 31 SHOP</p>", unsafe_allow_html=True)
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
        
        nav = st.radio("MÓDULOS", modulos)
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- CONTENIDO DINÁMICO ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron; text-align: center;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        d_tot = st.session_state.cli['SALDO_DEUDOR'].sum() if not st.session_state.cli.empty else 0
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="dash-card"><p style="color:#FF8C00; font-family:Orbitron; font-size: 1.5rem;">VENTAS TOTALES</p><p class="metric-value">${v_tot:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="dash-card"><p style="color:#FF4500; font-family:Orbitron; font-size: 1.5rem;">CARTERA VENCIDA</p><p class="metric-value">${d_tot:,.0f}</p></div>', unsafe_allow_html=True)

    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("ALERTA: Inventario vacío.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("CONCLUIR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success(f"OPERACIÓN EXITOSA: ${t_vta}")

    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE CARTERA</h1>", unsafe_allow_html=True)
        cliente_f = st.selectbox("SELECCIONAR CLIENTE", st.session_state.cli['NOMBRE'])
        datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
        st.markdown(f'<div class="dash-card"><p style="color:#FF8C00; font-family:Orbitron; font-size: 1.5rem;">DEUDA ACTUAL</p><p class="metric-value">${datos_c["SALDO_DEUDOR"]:,.2f}</p></div>', unsafe_allow_html=True)
        
        m_pago = st.number_input("REGISTRAR ABONO", min_value=0.0)
        if st.button("APLICAR PAGO"):
            st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
            st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
            st.rerun()
