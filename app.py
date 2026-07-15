import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="JR 31 SHOP | BY ING. JARED LARO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO SUPREME CYBER-EXECUTIVE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@100;400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important; 
    }

    .header-jared {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 28px; font-weight: 900; 
        text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }

    .footer-info {
        position: fixed; bottom: 20px; left: 30px;
        color: rgba(255, 255, 255, 0.4);
        font-family: 'Montserrat', sans-serif;
        font-size: 12px; z-index: 1000; line-height: 1.6; font-weight: 900;
    }

    /* NOMBRE DE TIENDA MONUMENTAL (LOGIN) */
    .monumental-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 15vw;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: -15px;
        filter: drop-shadow(0 15px 35px rgba(0,0,0,1));
        line-height: 0.8;
        letter-spacing: -10px;
        text-transform: uppercase;
    }

    /* INPUTS GIGANTES */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #FF8C00 !important;
        border-radius: 10px !important;
        height: 80px !important;
    }
    
    input {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-family: 'Orbitron', sans-serif !important;
        text-align: center !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 4em !important; width: 100%; transition: 0.5s;
        font-size: 2rem !important;
        text-transform: uppercase;
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.4) !important;
    }

    /* DASHBOARD CARDS */
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px; padding: 30px;
        border-top: 5px solid #FF8C00;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
    }
    .metric-value { font-family: 'Orbitron', sans-serif; font-size: 4rem; font-weight: 900; color: #FFFFFF; }

    [data-testid="stSidebar"] {
        background-color: #0b0d17 !important;
        border-right: 5px solid #FF4500;
    }

    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    </style>
    
    <div class="header-jared">ING. JARED LARO</div>
    <div class="footer-info">
        ING JARED LARA RODRIGUEZ | 918'125'5735<br>
        SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION
    </div>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE DATOS ---
if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
if 'sales_history' not in st.session_state:
    st.session_state.sales_history = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'client_base' not in st.session_state:
    st.session_state.client_base = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR", "DEUDA": 0.0}])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'admin_privileges' not in st.session_state: st.session_state.admin_privileges = False

# --- 4. CONTROL DE ACCESO ---
if not st.session_state.authenticated:
    st.markdown('<p class="monumental-logo">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; font-family:Orbitron; letter-spacing:10px;">ACCESO AL SISTEMA</h2>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.2, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("ACCESS KEY", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 MASTER</h1>", unsafe_allow_html=True)
        if not st.session_state.admin_privileges:
            code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR PRIVILEGIOS"):
                if code == "291329":
                    st.session_state.admin_privileges = True
                    st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.admin_privileges = False
                st.rerun()

        st.markdown("---")
        menu_options = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.admin_privileges:
            menu_options += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        choice = st.radio("SELECCIONE MÓDULO", menu_options)
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.authenticated = False
            st.rerun()

    # --- 6. MÓDULOS ---

    # --- DASHBOARD ---
    if choice == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_history['TOTAL'].sum() if not st.session_state.sales_history.empty else 0
        g = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="metric-container"><p style="color:#FF8C00; font-family:Orbitron;">INGRESOS TOTALES</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-container" style="border-top:5px solid #FF4500;"><p style="color:#FF4500; font-family:Orbitron;">EGRESOS TOTALES</p><p class="metric-value" style="color:#FF4500;">${g:,.0f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL VENTA ---
    elif choice == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory_db.empty: st.info("Sin inventario.")
        else:
            with st.form("pos"):
                art = st.selectbox("PRODUCTO", st.session_state.inventory_db['ARTICULO'])
                cli = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qty = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("FINALIZAR VENTA"):
                    row = st.session_state.inventory_db[st.session_state.inventory_db['ARTICULO'] == art].iloc[0]
                    total = row['PVP'] * qty
                    st.session_state.sales_history = pd.concat([st.session_state.sales_history, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli, "ARTICULO": art, "TOTAL": total, "UTILIDAD": (row['PVP']-row['COSTO'])*qty, "MODO": "CONTADO"}])], ignore_index=True)
                    st.session_state.inventory_db.loc[st.session_state.inventory_db['ARTICULO'] == art, 'STOCK'] -= qty
                    st.success(f"Venta registrada: ${total}")

    # --- CARTERA ---
    elif choice == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t2:
            n_name = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"NOMBRE": n_name, "DEUDA": 0.0}])], ignore_index=True)
                st.success("Guardado.")

    # --- GESTIÓN STOCK ---
    elif choice == "📦 GESTIÓN STOCK" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a = st.text_input("ARTICULO")
            s = st.number_input("STOCK", min_value=1)
            c = st.number_input("COSTO")
            p = st.number_input("PVP")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory_db, use_container_width=True)

    # --- MÓDULO CORREGIDO: GASTOS ---
    elif choice == "💸 GASTOS" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CONTROL DE EGRESOS Y LOGÍSTICA</h1>", unsafe_allow_html=True)
        
        # Resumen Rápido de Gastos
        total_gastado = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        st.markdown(f'<div class="metric-container" style="border-top:5px solid #2E8B57; margin-bottom:40px;"><p style="color:#2E8B57; font-family:Orbitron;">TOTAL GASTOS OPERATIVOS</p><p class="metric-value" style="color:#2E8B57;">${total_gastado:,.2f}</p></div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1, 1.5])
        
        with col_g1:
            st.markdown("### 📥 REGISTRAR GASTO")
            with st.form("form_gastos", clear_on_submit=True):
                cat_g = st.selectbox("CATEGORÍA", ["PALLETS", "OFICINA", "LOGÍSTICA", "SERVICIOS", "VARIOS"])
                con_g = st.text_input("CONCEPTO (Ej. Compra de tarimas, papelería...)")
                mon_g = st.number_input("MONTO DEL GASTO ($)", min_value=0.1, step=1.0)
                if st.form_submit_button("GUARDAR GASTO EN SISTEMA"):
                    nuevo_gasto = pd.DataFrame([{
                        "FECHA": datetime.now().strftime("%d/%m/%Y"),
                        "CATEGORIA": cat_g,
                        "CONCEPTO": con_g,
                        "MONTO": mon_g
                    }])
                    st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, nuevo_gasto], ignore_index=True)
                    st.success("✅ Gasto registrado correctamente.")
                    st.rerun()

        with col_g2:
            st.markdown("### 📋 HISTORIAL DE GASTOS")
            if not st.session_state.expenses_db.empty:
                st.dataframe(st.session_state.expenses_db, use_container_width=True)
            else:
                st.info("No hay gastos registrados en este periodo.")

    # --- REPORTES ---
    elif choice == "📝 REPORTES" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_history.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.expenses_db.to_excel(w, index=False, sheet_name='GASTOS')
        st.download_button("📥 DESCARGAR REPORTE EXCEL", buf.getvalue(), f"JR31_LARO_MASTER.xlsx")
