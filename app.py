import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP", layout="wide")

# --- COLORES JR 31 SHOP (VERDE Y NARANJA) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .stButton>button { 
        background-color: #FF8C00; color: white; border-radius: 12px; 
        border: none; font-weight: bold; height: 3em; width: 100%;
    }
    .stButton>button:hover { background-color: #2E8B57; }
    h1, h2, h3 { color: #2E8B57; font-family: 'Arial'; }
    .css-1d391kg { background-color: #2E8B57 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL ---
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "Costo_USD", "Precio_MXN"])
if 'ven' not in st.session_state:
    st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Total", "Metodo"])
if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame([{"Nombre": "Público General", "Deuda": 0.0}])

# --- LOGIN ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False

if not st.session_state.ingresado:
    st.title("🍊 JR 31 SHOP - Punto de Venta")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("ACCEDER"):
        if u == "admin_jr31" and p == "JR31_2024_Chiapas":
            st.session_state.ingresado = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
else:
    # --- MENÚ PRINCIPAL ---
    st.sidebar.title("JR 31 SHOP 🟢")
    opc = st.sidebar.radio("Navegar", ["🏠 Inicio", "📦 Compras USA", "💰 Ventas", "👥 Clientes / Créditos", "📊 Reportes"])
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.ingresado = False
        st.rerun()

    if opc == "🏠 Inicio":
        st.title("Bienvenido a JR 31 SHOP")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ventas", f"${st.session_state.ven['Total'].sum():,.2f}")
        c2.metric("Inversión USA", f"${st.session_state.inv['Costo_USD'].sum():,.2f} USD")
        c3.metric("Deuda Clientes", f"${st.session_state.cli['Deuda'].sum():,.2f}")
        
        st.subheader("⚠️ Alerta de Créditos Pendientes")
        deudores = st.session_state.cli[st.session_state.cli['Deuda'] > 0]
        st.table(deudores)

    elif opc == "📦 Compras USA":
        st.header("Registrar Compra en USA")
        with st.form("compras"):
            prod = st.text_input("Producto")
            cant = st.number_input("Cantidad", min_value=1)
            cusd = st.number_input("Costo unitario (USD)")
            pmxn = st.number_input("Precio de venta (MXN)")
            if st.form_submit_button("Guardar en Inventario"):
                nuevo = pd.DataFrame([{"Producto": prod, "Stock": cant, "Costo_USD": cusd, "Precio_MXN": pmxn}])
                st.session_state.inv = pd.concat([st.session_state.inv, nuevo], ignore_index=True)
                st.success("Guardado")
        st.dataframe(st.session_state.inv)

    elif opc == "💰 Ventas":
        st.header("Nueva Venta")
        cliente_v = st.selectbox("Cliente", st.session_state.cli['Nombre'])
        monto_v = st.number_input("Monto Total (MXN)")
        metodo_v = st.selectbox("Método", ["Contado", "Crédito"])
        if st.button("Finalizar Venta"):
            nueva_v = pd.DataFrame([{"Fecha": datetime.now(), "Cliente": cliente_v, "Total": monto_v, "Metodo": metodo_v}])
            st.session_state.ven = pd.concat([st.session_state.ven, nueva_v], ignore_index=True)
            if metodo_v == "Crédito":
                st.session_state.cli.loc[st.session_state.cli['Nombre'] == cliente_v, 'Deuda'] += monto_v
            st.success("Venta Registrada")

    elif opc == "👥 Clientes / Créditos":
        st.header("Control de Clientes")
        n_cli = st.text_input("Nuevo Cliente")
        if st.button("Agregar"):
            st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"Nombre": n_cli, "Deuda": 0.0}])], ignore_index=True)
        st.dataframe(st.session_state.cli)

    elif opc == "📊 Reportes":
        st.header("Descargar Datos")
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.ven.to_excel(writer, index=False, sheet_name='Ventas')
        st.download_button("📥 Descargar Excel de Ventas", buffer, "Reporte_JR31.xlsx")
