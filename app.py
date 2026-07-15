import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP - Premium POS", layout="wide", page_icon="🍊")

# --- DISEÑO "NOVEDOSO" (CSS AVANZADO) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">

    <style>
    /* Fuente Moderna */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo de la App */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Títulos con Estilo */
    h1 {
        color: #1a5e20 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Etiquetas de texto (Labels) */
    label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 5px;
    }

    /* Botones Premium Naranja */
    .stButton>button {
        background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 140, 0, 0.3) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 140, 0, 0.5) !important;
        background: linear-gradient(135deg, #2E8B57 0%, #1a5e20 100%) !important;
    }

    /* Tarjetas Blancas (Cards) */
    div[data-testid="stVerticalBlock"] > div:has(div.stFrame) {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.05);
    }

    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background-color: #1a5e20 !important;
        border-right: 5px solid #FF8C00;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Input Fields */
    input {
        border-radius: 10px !important;
        border: 1px solid #dce1e7 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS ---
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "Costo USD", "Inversión MXN", "Precio Venta"])
if 'ven' not in st.session_state:
    st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Total", "Tipo"])
if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame([{"Nombre": "Público General", "Deuda": 0.0}])

# --- ACCESO / LOGIN ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False

if not st.session_state.ingresado:
    col1, col_login, col2 = st.columns([1, 1.5, 1])
    with col_login:
        st.markdown("<h1 style='text-align: center;'>🍊 JR 31 SHOP</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Premium Management System</p>", unsafe_allow_html=True)
        
        with st.container():
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.button("DESBLOQUEAR SISTEMA"):
                if u == "admin_jr31" and p == "JR31_2024_Chiapas":
                    st.session_state.ingresado = True
                    st.rerun()
                else:
                    st.error("Credenciales Incorrectas")
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>JR 31</h2>", unsafe_allow_html=True)
        st.markdown("---")
        opc = st.radio("NAVEGACIÓN", ["🏠 Dashboard", "📦 Compras / Stock", "💰 Punto de Venta", "👥 Clientes/Crédito", "📊 Reportes"])
        st.markdown("---")
        if st.button("🔒 CERRAR SESIÓN"):
            st.session_state.ingresado = False
            st.rerun()

    # --- DASHBOARD ---
    if opc == "🏠 Dashboard":
        st.title("🚀 Resumen de Negocio")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.metric("VENTAS TOTALES", f"${st.session_state.ven['Total'].sum():,.2f}")
        with c2:
            st.metric("INVERSIÓN USA", f"${st.session_state.inv['Costo USD'].sum():,.2f} USD")
        with c3:
            st.metric("CRÉDITOS ACTIVOS", f"${st.session_state.cli['Deuda'].sum():,.2f}")
        
        st.markdown("### 📋 Deudores Pendientes")
        st.dataframe(st.session_state.cli[st.session_state.cli['Deuda'] > 0], use_container_width=True)

    # --- INVENTARIO ---
    elif opc == "📦 Compras / Stock":
        st.title("📦 Compras USA y Stock")
        with st.expander("➕ REGISTRAR NUEVA ENTRADA DE MERCANCÍA"):
            with st.form("inv_form"):
                p_name = st.text_input("Nombre del Artículo")
                p_qty = st.number_input("Cantidad Comprada", min_value=1)
                p_usd = st.number_input("Costo Unitario (USD)")
                p_tasa = st.number_input("Tipo de Cambio (MXN)", value=18.50)
                p_vta = st.number_input("Precio de Venta Sugerido (MXN)")
                
                if st.form_submit_button("GUARDAR EN NUBE"):
                    inv_mxn = p_qty * p_usd * p_tasa
                    nueva_fila = pd.DataFrame([{"Producto": p_name, "Stock": p_qty, "Costo USD": p_usd, "Inversión MXN": inv_mxn, "Precio Venta": p_vta}])
                    st.session_state.inv = pd.concat([st.session_state.inv, nueva_fila], ignore_index=True)
                    st.success("✅ Stock Actualizado")
        
        st.dataframe(st.session_state.inv, use_container_width=True)

    # --- VENTAS ---
    elif opc == "💰 Punto de Venta":
        st.title("💰 Registrar Venta")
        col_a, col_b = st.columns(2)
        
        cliente_sel = col_a.selectbox("Seleccione Cliente", st.session_state.cli['Nombre'])
        monto_venta = col_b.number_input("Total a Cobrar (MXN)", min_value=0.0)
        tipo_pago = col_a.selectbox("Forma de Pago", ["💵 Contado", "💳 Crédito"])
        
        if st.button("🚀 FINALIZAR Y GENERAR VENTA"):
            nueva_v = pd.DataFrame([{"Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "Cliente": cliente_sel, "Total": monto_venta, "Tipo": tipo_pago}])
            st.session_state.ven = pd.concat([st.session_state.ven, nueva_v], ignore_index=True)
            
            if "Crédito" in tipo_pago:
                st.session_state.cli.loc[st.session_state.cli['Nombre'] == cliente_sel, 'Deuda'] += monto_venta
            
            st.balloons()
            st.success(f"Venta registrada para {cliente_sel}")

    # --- CLIENTES ---
    elif opc == "👥 Clientes/Crédito":
        st.title("👥 Gestión de Clientes")
        with st.form("cli_form"):
            n_clie = st.text_input("Nombre Completo del Cliente")
            if st.form_submit_button("REGISTRAR CLIENTE"):
                st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"Nombre": n_clie, "Deuda": 0.0}])], ignore_index=True)
                st.success("Cliente Agregado")
        
        st.markdown("### 📑 Listado de Saldos y Deudas")
        st.dataframe(st.session_state.cli, use_container_width=True)

    # --- REPORTES ---
    elif opc == "📊 Reportes":
        st.title("📊 Reportes y Respaldo")
        st.write("Genera tu archivo Excel para auditoría o respaldo.")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.ven.to_excel(writer, index=False, sheet_name='Ventas')
            st.session_state.inv.to_excel(writer, index=False, sheet_name='Stock')
            st.session_state.cli.to_excel(writer, index=False, sheet_name='Clientes')
        
        st.download_button(
            label="📥 DESCARGAR EXCEL COMPLETO (JR 31)",
            data=output.getvalue(),
            file_name=f"JR31_SHOP_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )
