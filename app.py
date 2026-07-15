import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | MANAGEMENT SYSTEM", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-CORPORATE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    .ing-signature { position: fixed; bottom: 10px; left: 20px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 12px; z-index: 999; font-weight: bold; }
    .logo-text { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; font-weight: 900; background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0px; }
    .carbon-card { background: #1b263b; border-radius: 15px; padding: 20px; border: 1px solid #415a77; margin-bottom: 15px; color: white !important; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; }
    .stButton>button { background: linear-gradient(90deg, #FF4500, #FF8C00) !important; color: white !important; font-family: 'Orbitron' !important; width: 100%; border: none !important; height: 3em !important; border-radius: 8px !important; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #2E8B57; }
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 3px solid #FF4500; }
    </style>
    <div class="ing-signature">SYSTEM ARCHITECT: ING. JARED LARO // VERSION 3.0</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS REFORZADA ---
def init_db():
    if 'inv' not in st.session_state: st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
    if 'ven' not in st.session_state: st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    if 'cli' not in st.session_state: st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
    if 'abonos' not in st.session_state: st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'gas' not in st.session_state: st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

init_db()

# --- ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px;'>SISTEMA DE CONTROL CHIAPAS</p>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1, 1])
    with col_login:
        st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
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
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron;'>JR 31 MASTER</h2>", unsafe_allow_html=True)
        nav = st.radio("MÓDULOS", ["📊 DASHBOARD", "📦 STOCK / INVENTARIO", "🛒 PUNTO DE VENTA", "👤 CARTERA CLIENTES", "💸 GASTOS", "📝 REPORTES"])
        if st.button("SALIR"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>ESTADO FINANCIERO</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
        g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("VENTAS TOTALES", f"${v_tot:,.2f}")
        c2.metric("UTILIDAD BRUTA", f"${u_tot:,.2f}")
        c3.metric("BALANCE NETO", f"${u_tot - g_tot:,.2f}")

    # --- 2. STOCK ---
    elif nav == "📦 STOCK / INVENTARIO":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE MERCANCÍA</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("NOMBRE DEL ARTICULO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO DE ADQUISICIÓN")
            pvp = st.number_input("PRECIO DE VENTA")
            if st.form_submit_button("REGISTRAR ARTICULO"):
                st.session_state.inv = pd.concat([st.session_state.inv, pd.DataFrame([{"ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])], ignore_index=True)
                st.success("STOK ACTUALIZADO")
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 3. VENTA ---
    elif nav == "🛒 PUNTO DE VENTA":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty: st.warning("Registre productos primero.")
        else:
            with st.form("venta"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                c_sel = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("TIPO DE PAGO", ["EFECTIVO/CONTADO", "CRÉDITO"])
                if st.form_submit_button("FINALIZAR VENTA"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    
                    st.session_state.ven = pd.concat([st.session_state.ven, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success(f"Venta Exitosa por ${t_vta}")

    # --- 4. CARTERA DETALLADA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA Y EXPEDIENTES</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📊 EXPEDIENTE POR CLIENTE", "👤 ALTA DE CLIENTES"])
        
        with tab1:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            cliente_f = st.selectbox("SELECCIONAR CLIENTE PARA VER HISTORIAL", st.session_state.cli['NOMBRE'])
            
            # Datos del cliente seleccionado
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f].iloc[0]
            
            c_c1, c_c2 = st.columns(2)
            c_c1.metric("DEUDA ACTUAL", f"${datos_c['SALDO_DEUDOR']:,.2f}")
            
            # Sección de Abonos
            with c_c2:
                m_pago = st.number_input("REGISTRAR ABONO ($)", min_value=0.0)
                if st.button("APLICAR PAGO"):
                    if m_pago > 0:
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                        st.session_state.abonos = pd.concat([st.session_state.abonos, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])], ignore_index=True)
                        st.success("Abono registrado.")
                        st.rerun()
            
            st.markdown("---")
            st.subheader(f"📦 HISTORIAL DE COMPRAS: {cliente_f}")
            historial_v = st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f]
            if historial_v.empty: st.info("Este cliente no tiene compras registradas.")
            else: st.dataframe(historial_v, use_container_width=True)
            
            st.subheader(f"💵 HISTORIAL DE ABONOS: {cliente_f}")
            historial_a = st.session_state.abonos[st.session_state.abonos['CLIENTE'] == cliente_f]
            if historial_a.empty: st.info("No hay abonos registrados.")
            else: st.dataframe(historial_a, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.subheader("REGISTRAR NUEVO CLIENTE")
            n_cli = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR EN CARTERA"):
                if n_cli:
                    st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": n_cli, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                    st.success("Añadido.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.dataframe(st.session_state.cli, use_container_width=True)

    # --- 5. GASTOS ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("g_form"):
            con = st.text_input("CONCEPTO DE GASTO")
            mon = st.number_input("MONTO ($)")
            if st.form_submit_button("REGISTRAR GASTO"):
                st.session_state.gas = pd.concat([st.session_state.gas, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CONCEPTO": con, "MONTO": mon}])], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES ---
    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family: Orbitron;'>MASTER REPORT</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv.to_excel(w, index=False, sheet_name='STOCK')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
            st.session_state.abonos.to_excel(w, index=False, sheet_name='HISTORIAL_ABONOS')
        st.download_button("📥 DESCARGAR BASE DE DATOS EXCEL", buf.getvalue(), f"JR31_MASTER_{datetime.now().strftime('%Y%m%d')}.xlsx")
