import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | Premium Suite", layout="wide", page_icon="🍊")

# --- DISEÑO DE ALTO NIVEL CON TU LOGO ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
    * { font-family: 'Montserrat', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* EFECTO CRISTAL (Glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #1e272e !important;
    }

    /* ESTILO DE TEXTOS */
    label, p, span, .stMarkdown {
        color: #1e272e !important;
        font-weight: 600 !important;
    }
    
    h1, h2, h3 {
        color: #1B5E20 !important;
        font-weight: 900 !important;
    }

    /* BOTONES PREMIUM */
    .stButton>button {
        background: linear-gradient(135deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 15px rgba(255, 69, 0, 0.2) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(27, 94, 32, 0.3) !important;
        background: linear-gradient(135deg, #2E8B57 0%, #1B5E20 100%) !important;
    }

    /* SIDEBAR CUSTOM */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #0D2E11 100%) !important;
        border-right: 8px solid #FF4500;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* CONTENEDOR DE LOGO */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGAR LOGO ---
def mostrar_logo(ancho=200):
    if os.path.exists("logo.png"):
        st.image("logo.png", width=ancho)
    else:
        st.title("🍊 JR 31 SHOP")

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "USD_Unit", "MXN_Total", "Precio_Vta"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Monto", "Metodo"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"Nombre": "Venta de Mostrador", "Deuda": 0.0}])

# --- ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        mostrar_logo(ancho=250)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-size: 1.5rem;'>TERMINAL PRIVADA</h2>", unsafe_allow_html=True)
        
        u = st.text_input("ID de Administrador")
        p = st.text_input("Clave de Acceso", type="password")
        
        if st.button("DESBLOQUEAR SISTEMA"):
            if u == "admin_jr31" and p == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else:
                st.error("Acceso Denegado")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MENÚ CON LOGO ---
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        mostrar_logo(ancho=150)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        nav = st.radio("GESTIÓN EMPRESARIAL", ["📊 Panel de Control", "📦 Logística de Importación", "💸 Terminal de Ventas", "👥 Cartera de Clientes", "📂 Reportes Master"])
        st.markdown("---")
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- CONTENIDO ---
    if nav == "📊 Panel de Control":
        st.title("📊 Resumen Ejecutivo")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("FLUJO DE VENTAS", f"${st.session_state.ven['Monto'].sum():,.2f} MXN")
        c2.metric("CAPITAL USD", f"${st.session_state.inv['USD_Unit'].sum():,.2f} USD")
        c3.metric("DEUDA TOTAL", f"${st.session_state.cli['Deuda'].sum():,.2f} MXN")
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("🚨 Cuentas por Cobrar Pendientes")
        st.dataframe(st.session_state.cli[st.session_state.cli['Deuda'] > 0], use_container_width=True)

    elif nav == "📦 Logística de Importación":
        st.title("📦 Logística e Inventario USA")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("logistica"):
            col_a, col_b = st.columns(2)
            p_n = col_a.text_input("Descripción del Producto")
            p_q = col_b.number_input("Cantidad Recibida", min_value=1)
            p_u = col_a.number_input("Costo Unitario (USD)")
            p_t = col_b.number_input("Tipo de Cambio", value=18.50)
            p_v = col_a.number_input("Precio Venta Sugerido (MXN)")
            if st.form_submit_button("INGRESAR A STOCK"):
                costo_mxn = p_q * p_u * p_t
                nueva_f = pd.DataFrame([{"Producto": p_n, "Stock": p_q, "USD_Unit": p_u, "MXN_Total": costo_mxn, "Precio_Vta": p_v}])
                st.session_state.inv = pd.concat([st.session_state.inv, nueva_f], ignore_index=True)
                st.success("Mercancía registrada en el sistema.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.inv, use_container_width=True)

    elif nav == "💸 Terminal de Ventas":
        st.title("💸 Terminal de Ventas")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c_v1, c_v2 = st.columns(2)
        cli_v = c_v1.selectbox("Seleccionar de Cartera", st.session_state.cli['Nombre'])
        mon_v = c_v2.number_input("Total Transacción (MXN)")
        met_v = c_v1.selectbox("Condición de Pago", ["Contado", "Crédito JR 31"])
        
        if st.button("PROCESAR VENTA"):
            nueva_v = pd.DataFrame([{"Fecha": datetime.now().strftime("%d/%m/%Y"), "Cliente": cli_v, "Monto": mon_v, "Metodo": met_v}])
            st.session_state.ven = pd.concat([st.session_state.ven, nueva_v], ignore_index=True)
            if "Crédito" in met_v:
                st.session_state.cli.loc[st.session_state.cli['Nombre'] == cli_v, 'Deuda'] += mon_v
            st.balloons()
            st.success("Operación Exitosa")
        st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "👥 Cartera de Clientes":
        st.title("👥 Gestión de Cartera")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        with st.form("clientes"):
            n_c = st.text_input("Nombre Completo del Cliente")
            if st.form_submit_button("DAR DE ALTA"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"Nombre": n_c, "Deuda": 0.0}])], ignore_index=True)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.cli, use_container_width=True)

    elif nav == "📂 Reportes Master":
        st.title("📂 Generación de Reportes")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            st.session_state.ven.to_excel(writer, index=False, sheet_name='Ventas')
            st.session_state.inv.to_excel(writer, index=False, sheet_name='Stock')
            st.session_state.cli.to_excel(writer, index=False, sheet_name='Deudores')
        st.download_button(label="📥 DESCARGAR REPORTE MAESTRO (EXCEL)", data=buf.getvalue(), file_name=f"JR31_MASTER_REPORT.xlsx")
        st.markdown('</div>', unsafe_allow_html=True)
