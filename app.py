import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-CORPORATE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap');

    .stApp {
        background: radial-gradient(circle, #0d1b2a 0%, #000000 100%);
        color: #e0e1dd !important;
    }

    .ing-signature {
        position: fixed;
        bottom: 10px;
        left: 20px;
        color: #2E8B57;
        font-family: 'Orbitron', sans-serif;
        font-size: 12px;
        letter-spacing: 2px;
        z-index: 999;
        font-weight: bold;
    }

    .logo-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(to right, #FF4500, #FF8C00, #2E8B57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        filter: drop-shadow(0 0 10px rgba(255,69,0,0.3));
        margin-bottom: 0px;
    }

    .carbon-card {
        background: #1b263b;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #415a77;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        margin-bottom: 15px;
        color: white !important;
    }

    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important;
        font-family: 'Orbitron' !important;
        border-radius: 5px !important;
        border: none !important;
        height: 3em !important;
        width: 100%;
    }
    
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #2E8B57; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 3px solid #FF4500; }
    </style>
    <div class="ing-signature">DEVELOPED BY ING. JARED LARO // PRO SYSTEM</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (SUPER BLINDADA) ---
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["ID", "ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
if 'ven' not in st.session_state:
    st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame([{"NOMBRE": "PUBLICO GENERAL", "SALDO_DEUDOR": 0.0}])
if 'gas' not in st.session_state:
    st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

# --- DOBLE CHEQUEO DE COLUMNAS (PARA EVITAR EL KEYERROR) ---
def verificar_columnas():
    columnas_necesarias = ["NOMBRE", "SALDO_DEUDOR"]
    for col in columnas_necesarias:
        if col not in st.session_state.cli.columns:
            st.session_state.cli[col] = 0.0 if col == "SALDO_DEUDOR" else "N/A"

verificar_columnas()

# --- ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px;'>ADMINISTRATION TERMINAL</p>", unsafe_allow_html=True)
    
    col1, col_login, col2 = st.columns([1, 1, 1])
    with col_login:
        st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
        uid = st.text_input("ADMIN ID")
        ukey = st.text_input("ACCESS KEY", type="password")
        if st.button("DESBLOQUEAR"):
            if uid == "admin_jr31" and ukey == "JR31_2024_Chiapas":
                st.session_state.log = True
                st.rerun()
            else:
                st.error("ACCESO DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron;'>MASTER MENU</h2>", unsafe_allow_html=True)
        nav = st.radio("MÓDULOS", ["📊 DASHBOARD", "📦 INVENTARIO", "🛒 VENTA POS", "👤 CARTERA", "💸 GASTOS", "📝 REPORTES"])
        st.markdown("---")
        if st.button("LOGOUT"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>ESTADÍSTICAS</h1>", unsafe_allow_html=True)
        v_totales = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        u_total = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
        g_total = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("VENTAS", f"${v_totales:,.2f}")
        c2.metric("UTILIDAD BRUTA", f"${u_total:,.2f}")
        c3.metric("BALANCE NETO", f"${u_total - g_total:,.2f}")

    # --- 2. INVENTARIO ---
    elif nav == "📦 INVENTARIO":
        st.markdown("<h1 style='font-family: Orbitron;'>STOCK</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            art = st.text_input("ARTICULO")
            cant = st.number_input("CANTIDAD", min_value=1)
            costo = st.number_input("COSTO")
            pvp = st.number_input("PRECIO VENTA")
            if st.form_submit_button("AÑADIR"):
                nuevo = pd.DataFrame([{"ID": len(st.session_state.inv)+1, "ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])
                st.session_state.inv = pd.concat([st.session_state.inv, nuevo], ignore_index=True)
                st.success("STOCK ACTUALIZADO")
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 3. VENTA POS ---
    elif nav == "🛒 VENTA POS":
        st.markdown("<h1 style='font-family: Orbitron;'>PUNTO DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inv.empty:
            st.info("Registre productos en inventario primero.")
        else:
            with st.form("v_form"):
                p_sel = st.selectbox("PRODUCTO", st.session_state.inv['ARTICULO'])
                cliente = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_v = st.number_input("CANTIDAD", min_value=1)
                modo = st.selectbox("MÉTODO", ["CONTADO", "CRÉDITO"])
                if st.form_submit_button("VENDER"):
                    data = st.session_state.inv[st.session_state.inv['ARTICULO'] == p_sel].iloc[0]
                    t_vta = data['PVP'] * cant_v
                    uti = (data['PVP'] - data['COSTO_ADQ']) * cant_v
                    nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CLIENTE": cliente, "ARTICULO": p_sel, "TOTAL": t_vta, "UTILIDAD": uti, "MODO": modo}])
                    st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == p_sel, 'CANTIDAD'] -= cant_v
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente, 'SALDO_DEUDOR'] += t_vta
                    st.success("VENTA REGISTRADA")

    # --- 4. CARTERA (SISTEMA DE SEGURIDAD ACTIVADO) ---
    elif nav == "👤 CARTERA":
        st.markdown("<h1 style='font-family: Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        
        with col_1:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.subheader("NUEVO CLIENTE")
            nombre_n = st.text_input("NOMBRE COMPLETO")
            if st.button("REGISTRAR"):
                if nombre_n:
                    # Agregamos usando nombres de columna exactos
                    st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nombre_n, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                    st.success("LISTO")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_2:
            st.markdown('<div class="carbon-card">', unsafe_allow_html=True)
            st.subheader("ABONOS")
            
            # --- CHEQUEO DE SEGURIDAD ANTES DEL ERROR ---
            verificar_columnas()
            
            # Filtramos solo deudores reales
            deudores_df = st.session_state.cli[st.session_state.cli['SALDO_DEUDOR'] > 0]
            
            if deudores_df.empty:
                st.write("No hay deudas.")
            else:
                c_pago = st.selectbox("CLIENTE", deudores_df['NOMBRE'].tolist())
                m_pago = st.number_input("MONTO ABONO", min_value=0.0)
                if st.button("ABONAR"):
                    st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_pago, 'SALDO_DEUDOR'] -= m_pago
                    st.success("ABONO APLICADO")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.dataframe(st.session_state.cli, use_container_width=True)

    # --- 5. GASTOS ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g_form"):
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                ng = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CONCEPTO": con, "MONTO": mon}])
                st.session_state.gas = pd.concat([st.session_state.gas, ng], ignore_index=True)
        st.table(st.session_state.gas)

    # --- 6. REPORTES ---
    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family: Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
        st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"JR31_LARO.xlsx")
