import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-CORPORATE PREMIUM (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');
    
    /* Fondo General */
    .stApp { background: radial-gradient(circle, #0d1b2a 0%, #000000 100%); color: #e0e1dd !important; }
    
    /* NOMBRE DEL INGENIERO - SUPERIOR DERECHO */
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

    .ing-signature { position: fixed; bottom: 10px; left: 20px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 10px; z-index: 999; opacity: 0.5; }
    
    .logo-text { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; font-weight: 900; background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0px; }
    
    .carbon-card { background: #1b263b; border-radius: 15px; padding: 25px; border: 1px solid #415a77; box-shadow: 0 10px 30px rgba(0,0,0,0.5); color: white !important; }
    
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; }
    
    .stButton>button { background: linear-gradient(90deg, #FF4500, #FF8C00) !important; color: white !important; font-family: 'Orbitron' !important; width: 100%; border: none !important; height: 3em !important; border-radius: 8px !important; box-shadow: 0 0 10px rgba(255,69,0,0.3); }
    
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 0 20px #2E8B57; }
    
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 3px solid #FF4500; }
    </style>
    
    <div class="jared-header">ING. JARED LARO</div>
    <div class="ing-signature">SISTEMA CREADO POR ING. JARED LARO // V3.2 PRO</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS REFORZADA (BLINDAJE TOTAL) ---
def init_db():
    if 'inv' not in st.session_state: 
        st.session_state.inv = pd.DataFrame(columns=["ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
    if 'ven' not in st.session_state: 
        st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    if 'cli' not in st.session_state: 
        st.session_state.cli = pd.DataFrame([{"NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "SALDO_DEUDOR": 0.0}])
    if 'abonos' not in st.session_state: 
        st.session_state.abonos = pd.DataFrame(columns=["FECHA", "CLIENTE", "MONTO"])
    if 'gas' not in st.session_state: 
        st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

init_db()

# --- ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px; font-weight: bold;'>SISTEMA DE GESTIÓN EMPRESARIAL</p>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns([1, 1.2, 1])
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
        nav = st.radio("MÓDULOS DE CONTROL", ["📊 DASHBOARD", "📦 STOCK / INVENTARIO", "🛒 PUNTO DE VENTA", "👤 CARTERA CLIENTES", "💸 GASTOS", "📝 REPORTES"])
        if st.button("CERRAR SESIÓN"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>PANEL DE ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_tot = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        u_tot = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
        g_tot = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("VENTAS TOTALES", f"${v_tot:,.2f}")
        c2.metric("UTILIDAD BRUTA", f"${u_tot:,.2f}")
        c3.metric("GASTOS OPERATIVOS", f"${g_tot:,.2f}")

    # --- 2. STOCK ---
    elif nav == "📦 STOCK / INVENTARIO":
        st.markdown("<h1 style='font-family: Orbitron;'>GESTIÓN DE STOCK</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("NOMBRE DEL ARTICULO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO UNITARIO")
            pvp = st.number_input("PRECIO VENTA")
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
                    
                    # Registro seguro
                    nueva_v = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": c_sel, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])
                    st.session_state.ven = pd.concat([st.session_state.ven, nueva_v], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_sel, 'SALDO_DEUDOR'] += t_vta
                    st.success(f"Venta registrada por ${t_vta}")

    # --- 4. CARTERA (ERROR SOLUCIONADO) ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family: Orbitron;'>EXPEDIENTES Y COBRANZA</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📊 ESTADO DE CUENTA", "👤 NUEVO CLIENTE"])
        
        with tab1:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            cliente_f = st.selectbox("BUSCAR CLIENTE", st.session_state.cli['NOMBRE'])
            
            # Filtro seguro para evitar KeyError
            datos_c = st.session_state.cli[st.session_state.cli['NOMBRE'] == cliente_f]
            if not datos_c.empty:
                deuda_act = datos_c.iloc[0]['SALDO_DEUDOR']
                col_ab1, col_ab2 = st.columns(2)
                col_ab1.metric("SALDO PENDIENTE", f"${deuda_act:,.2f}")
                
                with col_ab2:
                    m_pago = st.number_input("ABONAR A CUENTA ($)", min_value=0.0)
                    if st.button("REGISTRAR PAGO"):
                        if m_pago > 0:
                            st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente_f, 'SALDO_DEUDOR'] -= m_pago
                            nuevo_abono = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cliente_f, "MONTO": m_pago}])
                            st.session_state.abonos = pd.concat([st.session_state.abonos, nuevo_abono], ignore_index=True)
                            st.success("Abono aplicado.")
                            st.rerun()

            st.markdown("---")
            st.subheader(f"🛒 COMPRAS REALIZADAS")
            # SOLUCIÓN AL ERROR: Verificamos si la columna existe antes de filtrar
            if not st.session_state.ven.empty and 'CLIENTE' in st.session_state.ven.columns:
                hist_v = st.session_state.ven[st.session_state.ven['CLIENTE'] == cliente_f]
                st.dataframe(hist_v, use_container_width=True)
            else:
                st.info("Sin registro de compras.")
            
            st.subheader(f"💸 HISTORIAL DE ABONOS")
            if not st.session_state.abonos.empty and 'CLIENTE' in st.session_state.abonos.columns:
                hist_a = st.session_state.abonos[st.session_state.abonos['CLIENTE'] == cliente_f]
                st.dataframe(hist_a, use_container_width=True)
            else:
                st.info("Sin registro de abonos.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            nc = st.text_input("NOMBRE COMPLETO DEL CLIENTE")
            if st.button("DAR DE ALTA EN CARTERA"):
                if nc:
                    st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nc, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                    st.success("Cliente guardado.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. GASTOS ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("g_form"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO ($)")
            if st.form_submit_button("GUARDAR GASTO"):
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
            st.session_state.abonos.to_excel(w, index=False, sheet_name='ABONOS')
        st.download_button("📥 DESCARGAR BASE DE DATOS", buf.getvalue(), f"JR31_LARO_{datetime.now().strftime('%Y%m%d')}.xlsx")
