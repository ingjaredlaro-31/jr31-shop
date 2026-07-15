import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP | BY ING. JARED LARO", layout="wide", page_icon="⚡")

# --- ESTILO CYBER-CORPORATE (CSS ACTUALIZADO) ---
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
    }

    /* Estilo para los textos de los formularios */
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-size: 0.8rem !important; }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF4500, #FF8C00) !important;
        color: white !important;
        font-family: 'Orbitron' !important;
        border-radius: 5px !important;
        border: none !important;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #2E8B57;
    }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 3px solid #FF4500; }
    </style>
    <div class="ing-signature">DEVELOPED BY ING. JARED LARO // PRO-EDITION 2024</div>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (BLINDADA) ---
def init_data():
    if 'inv' not in st.session_state:
        st.session_state.inv = pd.DataFrame(columns=["ID", "ARTICULO", "CANTIDAD", "COSTO_ADQ", "PVP"])
    if 'ven' not in st.session_state:
        st.session_state.ven = pd.DataFrame(columns=["FECHA", "CLIENTE", "ARTICULO", "TOTAL", "UTILIDAD", "MODO"])
    if 'cli' not in st.session_state:
        st.session_state.cli = pd.DataFrame([{"NOMBRE": "PUBLICO GENERAL", "SALDO_DEUDOR": 0.0}])
    if 'gas' not in st.session_state:
        st.session_state.gas = pd.DataFrame(columns=["FECHA", "CONCEPTO", "MONTO"])

init_data()

# --- ACCESO ---
if 'log' not in st.session_state: st.session_state.log = False

if not st.session_state.log:
    st.markdown('<p class="logo-text">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2E8B57; font-family: Orbitron; letter-spacing: 5px;'>INTELIGENCIA DE MERCADO</p>", unsafe_allow_html=True)
    
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
                st.error("DENEGADO")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- MENÚ ---
    with st.sidebar:
        st.markdown("<h2 style='color: #FF4500; font-family: Orbitron;'>MASTER MENU</h2>", unsafe_allow_html=True)
        nav = st.radio("MÓDULOS", ["📊 DASHBOARD", "📦 INVENTARIO", "🛒 PUNTO DE VENTA", "👤 CARTERA", "💸 GASTOS", "📝 REPORTES"])
        st.markdown("---")
        if st.button("LOGOUT"):
            st.session_state.log = False
            st.rerun()

    # --- 1. DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family: Orbitron;'>ANÁLISIS DE RENDIMIENTO</h1>", unsafe_allow_html=True)
        
        v_totales = st.session_state.ven['TOTAL'].sum() if not st.session_state.ven.empty else 0
        u_total = st.session_state.ven['UTILIDAD'].sum() if not st.session_state.ven.empty else 0
        g_total = st.session_state.gas['MONTO'].sum() if not st.session_state.gas.empty else 0
        balance = u_total - g_total

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("VENTAS TOTALES", f"${v_totales:,.2f}")
        c2.metric("UTILIDAD BRUTA", f"${u_total:,.2f}")
        c3.metric("GASTOS OPERATIVOS", f"${g_total:,.2f}", delta_color="inverse")
        c4.metric("BALANCE NETO", f"${balance:,.2f}")

        st.markdown("### 📋 ÚLTIMOS MOVIMIENTOS")
        st.dataframe(st.session_state.ven.tail(5), use_container_width=True)

    # --- 2. INVENTARIO ---
    elif nav == "📦 INVENTARIO":
        st.markdown("<h1 style='font-family: Orbitron;'>CONTROL DE STOCK</h1>", unsafe_allow_html=True)
        with st.form("inv_form"):
            col_a, col_b = st.columns(2)
            art = col_a.text_input("NOMBRE DEL PRODUCTO")
            cant = col_b.number_input("CANTIDAD", min_value=1)
            costo = col_a.number_input("COSTO UNITARIO ADQUISICIÓN")
            pvp = col_b.number_input("PRECIO VENTA AL PÚBLICO")
            if st.form_submit_button("REGISTRAR ARTÍCULO"):
                nuevo = pd.DataFrame([{"ID": len(st.session_state.inv)+1, "ARTICULO": art, "CANTIDAD": cant, "COSTO_ADQ": costo, "PVP": pvp}])
                st.session_state.inv = pd.concat([st.session_state.inv, nuevo], ignore_index=True)
                st.success("STOCK ACTUALIZADO")
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- 3. PUNTO DE VENTA (ERROR CORREGIDO) ---
    elif nav == "🛒 PUNTO DE VENTA":
        st.markdown("<h1 style='font-family: Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        
        if st.session_state.inv.empty:
            st.warning("⚠️ No hay productos en inventario para vender.")
        else:
            with st.form("venta_form"):
                prod_sel = st.selectbox("PRODUCTO A VENDER", st.session_state.inv['ARTICULO'])
                # Obtenemos datos del producto seleccionado
                prod_data = st.session_state.inv[st.session_state.inv['ARTICULO'] == prod_sel].iloc[0]
                
                cliente = st.selectbox("CLIENTE", st.session_state.cli['NOMBRE'])
                cant_vta = st.number_input("CANTIDAD", min_value=1, max_value=int(prod_data['CANTIDAD']))
                modo = st.selectbox("MÉTODO", ["CONTADO", "CRÉDITO"])
                
                if st.form_submit_button("CONCLUIR VENTA"):
                    total_vta = prod_data['PVP'] * cant_vta
                    utilidad = (prod_data['PVP'] - prod_data['COSTO_ADQ']) * cant_vta
                    
                    # Registrar venta
                    nv = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CLIENTE": cliente, "ARTICULO": prod_sel, "TOTAL": total_vta, "UTILIDAD": utilidad, "MODO": modo}])
                    st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
                    
                    # Descontar Inventario
                    st.session_state.inv.loc[st.session_state.inv['ARTICULO'] == prod_sel, 'CANTIDAD'] -= cant_vta
                    
                    # Cargar deuda si es crédito
                    if modo == "CRÉDITO":
                        st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == cliente, 'SALDO_DEUDOR'] += total_vta
                    
                    st.success(f"VENTA REALIZADA: ${total_vta}")

    # --- 4. CARTERA CLIENTES ---
    elif nav == "👤 CARTERA":
        st.markdown("<h1 style='font-family: Orbitron;'>GESTIÓN DE CRÉDITOS</h1>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("NUEVO CLIENTE")
            nc = st.text_input("NOMBRE")
            if st.button("REGISTRAR"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"NOMBRE": nc, "SALDO_DEUDOR": 0.0}])], ignore_index=True)
                st.rerun()
        with col_c2:
            st.subheader("PAGAR / ABONAR DEUDA")
            c_pago = st.selectbox("CLIENTE DEUDOR", st.session_state.cli[st.session_state.cli['SALDO_DEUDOR'] > 0]['NOMBRE'] if not st.session_state.cli.empty else ["N/A"])
            m_pago = st.number_input("MONTO ABONO", min_value=0.0)
            if st.button("APLICAR PAGO"):
                st.session_state.cli.loc[st.session_state.cli['NOMBRE'] == c_pago, 'SALDO_DEUDOR'] -= m_pago
                st.success("PAGO APLICADO")
                st.rerun()
        st.dataframe(st.session_state.cli, use_container_width=True)

    # --- 5. GASTOS ---
    elif nav == "💸 GASTOS":
        st.markdown("<h1 style='font-family: Orbitron;'>GASTOS OPERATIVOS</h1>", unsafe_allow_html=True)
        with st.form("gastos_f"):
            concepto = st.text_input("CONCEPTO (Renta, Comida, Flete, etc.)")
            m_gasto = st.number_input("MONTO", min_value=0.0)
            if st.form_submit_button("REGISTRAR GASTO"):
                ng = pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%Y"), "CONCEPTO": concepto, "MONTO": m_gasto}])
                st.session_state.gas = pd.concat([st.session_state.gas, ng], ignore_index=True)
                st.success("GASTO REGISTRADO")
        st.table(st.session_state.gas)

    # --- 6. REPORTES ---
    elif nav == "📝 REPORTES":
        st.markdown("<h1 style='font-family: Orbitron;'>EXPORTAR BASE DE DATOS</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.inv.to_excel(w, index=False, sheet_name='INVENTARIO')
            st.session_state.cli.to_excel(w, index=False, sheet_name='CARTERA')
            st.session_state.gas.to_excel(w, index=False, sheet_name='GASTOS')
        st.download_button("📥 DESCARGAR MASTER REPORT", buf.getvalue(), f"JR31_LARO_{datetime.now().strftime('%Y%m%d')}.xlsx")
