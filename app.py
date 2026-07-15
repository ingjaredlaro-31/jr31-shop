import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-CORPORATE PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    .jared-header {
        position: absolute;
        top: 10px;
        right: 30px;
        color: #2E8B57;
        font-family: 'Orbitron', sans-serif;
        font-size: 18px;
        font-weight: 900;
        text-shadow: 0 0 10px #2E8B57;
        z-index: 1000;
    }

    .logo-text { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; font-weight: 900; background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0px; }
    .carbon-card { background: #1b263b; border-radius: 15px; padding: 25px; border: 1px solid #415a77; box-shadow: 0 10px 30px rgba(0,0,0,0.5); color: white !important; margin-bottom: 15px; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; }
    
    .stButton>button { background: linear-gradient(90deg, #FF4500, #FF8C00) !important; color: white !important; font-family: 'Orbitron' !important; width: 100%; border: none !important; height: 3em !important; border-radius: 8px !important; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 0 15px #2E8B57; }
    
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 3px solid #FF4500; }
    .admin-only { color: #FF4500; font-size: 10px; text-align: center; font-weight: bold; letter-spacing: 1px; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

# --- ESTADO DE SEGURIDAD ---
if 'es_admin' not in st.session_state: st.session_state.es_admin = False
if 'log' not in st.session_state: st.session_state.log = False

# --- ACCESO PRINCIPAL ---
if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; font-weight: bold;'>PREMIUM POS SYSTEM</p>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("ABRIR TERMINAL"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else: st.error("DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron;'>JR 31 MASTER</h2>", unsafe_allow_html=True)
        
        if not st.session_state.es_admin:
            st.markdown("<p class='admin-only'>MODO VENDEDORA</p>", unsafe_allow_html=True)
            codigo_admin = st.text_input("🔓 DESBLOQUEAR INVENTARIO", type="password")
            if st.button("ACTIVAR ADMIN"):
                if codigo_admin == "291329":
                    st.session_state.es_admin = True
                    st.rerun()
                else: st.error("Código Incorrecto")
        else:
            st.success("🔒 MODO ADMINISTRADOR")
            if st.button("BLOQUEAR FUNCIONES"):
                st.session_state.es_admin = False
                st.rerun()

        st.markdown("---")
        modulos = ["🛒 VENTA POS", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.es_admin:
            modulos += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        nav = st.radio("NAVEGACIÓN", modulos)
        st.markdown("---")
        if st.button("SALIR DE LA APP"):
            st.session_state.log = False
            st.session_state.es_admin = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>RENDIMIENTO</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        c1, c2 = st.columns(2)
        c1.metric("VENTAS TOTALES", f"${v_tot:,.2f}")
        
        if st.session_state.es_admin:
            u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
            c2.metric("UTILIDAD NETA", f"${u_tot:,.2f}")
        else:
            c2.info("Cifras de utilidad ocultas para vendedora.")

    # --- 2. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Sin stock disponible.")
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
                    st.success("Venta Exitosa.")

    # --- 3. CARTERA (ACCESO TOTAL VENDEDORA) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>EXPEDIENTES Y ALTAS</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 HISTORIAL Y ABONOS", "👤 REGISTRAR CLIENTE NUEVO"])
        
        with tab1:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            cliente_f = st.selectbox("BUSCAR CLIENTE", st.session_state.cli['NOMBRE'])
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            
            c_c1, c_c2 = st.columns(2)
            c_c1.metric("DEUDA", f"${datos_c['SALDO_DEUDOR']:,.2f}")
            with c_c2:
                m_pago = st.number_input("ABONAR", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    if m_pago > 0:
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                        st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
                        st.success("Pago registrado."); st.rerun()
            
            st.markdown("---")
            st.subheader("📦 Compras")
            st.dataframe(st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f], use_container_width=True)
            st.subheader("💵 Abonos")
            st.dataframe(st.session_state.abonos[st.session_state.abonos['CLIENTE'] == cliente_f], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            n_cli = st.text_input("NOMBRE DEL NUEVO CLIENTE")
            if st.button("DAR DE ALTA"):
                if n_cli:
                    st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                    st.success("Guardado."); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. GESTIÓN STOCK (SOLO ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>STOCK Y PRECIOS</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("ARTÍCULO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO")
            pvp = st.number_input("PRECIO VENTA")
            if st.form_submit_button("ACTUALIZAR INVENTARIO"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
                st.success("Guardado.")
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 5. GASTOS (SOLO ADMIN) ---
    elif nav == "💸 GASTOS" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("g_form"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("REGISTRAR GASTO"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES (SOLO ADMIN) ---
    elif nav == "📝 REPORTES" and st.session_state.es_admin:
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"JR31_MASTER.xlsx")
