app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP", layout="wide")

# --- COLORES Y ESTILO (VERDE Y NARANJA) ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { 
        background-color: #FF8C00; color: white; border-radius: 10px; 
        border: none; font-weight: bold; height: 3em; width: 100%;
    }
    .stButton>button:hover { background-color: #2E8B57; color: white; }
    h1, h2, h3 { color: #2E8B57; }
    div[data-testid="stMetricValue"] { color: #FF8C00; }
    .css-1d391kg { background-color: #2E8B57; } 
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (Se guardan mientras la app esté abierta) ---
# En una versión avanzada, estos se guardan en una base de datos nube
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["Fecha", "Producto", "Cant", "Costo USD", "Precio MXN"])
if 'ventas' not in st.session_state:
    st.session_state.ventas = pd.DataFrame(columns=["Fecha", "Cliente", "Producto", "Monto", "Tipo"])
if 'clientes' not in st.session_state:
    st.session_state.clientes = pd.DataFrame([
        {"Nombre": "Publico General", "Deuda": 0.0}
    ])

# --- SISTEMA DE LOGIN ---
if 'sesion' not in st.session_state:
    st.session_state.sesion = False

def login():
    st.title("🍊 JR 31 SHOP - Punto de Venta")
    col1, col2 = st.columns(2)
    with col1:
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if user == "admin_jr31" and pw == "JR31_2024_Chiapas":
                st.session_state.sesion = True
                st.rerun()
            else:
                st.error("Datos incorrectos")

# --- CUERPO DEL PROGRAMA ---
if not st.session_state.sesion:
    login()
else:
    # MENÚ LATERAL
    st.sidebar.title("JR 31 SHOP 🟢")
    opcion = st.sidebar.radio("MENÚ", ["🏠 Inicio", "📦 Compras USA / Inventario", "💰 Nueva Venta", "👥 Clientes y Créditos", "📊 Reportes Excel"])
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.sesion = False
        st.rerun()

    # --- LÓGICA DE LAS SECCIONES ---

    if opcion == "🏠 Inicio":
        st.title("Panel de Control")
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventas Totales", f"${st.session_state.ventas['Monto'].sum():,.2f} MXN")
        col2.metric("Inversión USA", f"${st.session_state.inventario['Costo USD'].sum():,.2f} USD")
        col3.metric("Deuda Clientes", f"${st.session_state.clientes['Deuda'].sum():,.2f} MXN")

        st.subheader("Alertas de Crédito")
        deudores = st.session_state.clientes[st.session_state.clientes['Deuda'] > 0]
        if not deudores.empty:
            st.warning("Clientes con pagos pendientes:")
            st.table(deudores)
        else:
            st.success("No hay deudas pendientes.")

    elif opcion == "📦 Compras USA / Inventario":
        st.header("Entrada de Mercancía (USA)")
        with st.expander("Registrar nueva compra en USA"):
            with st.form("form_inv"):
                f = st.date_input("Fecha")
                p = st.text_input("Nombre del Producto")
                c = st.number_input("Cantidad", min_value=1)
                usd = st.number_input("Costo unitario en USD", min_value=0.0)
                mxn = st.number_input("Precio de Venta en MXN", min_value=0.0)
                if st.form_submit_button("Guardar en Inventario"):
                    nueva_compra = {"Fecha": f, "Producto": p, "Cant": c, "Costo USD": usd, "Precio MXN": mxn}
                    st.session_state.inventario = pd.concat([st.session_state.inventario, pd.DataFrame([nueva_compra])], ignore_index=True)
                    st.success("Guardado correctamente")
        
        st.subheader("Inventario Actual")
        st.dataframe(st.session_state.inventario, use_container_width=True)

    elif opcion == "💰 Nueva Venta":
        st.header("Realizar Venta")
        with st.form("form_venta"):
            cli = st.selectbox("Seleccionar Cliente", st.session_state.clientes['Nombre'])
            prod = st.text_input("Producto vendido")
            monto_v = st.number_input("Monto de la venta (MXN)", min_value=0.0)
            tipo_v = st.radio("Forma de pago", ["Contado", "Crédito"])
            
            if st.form_submit_button("Finalizar Venta"):
                # Registrar venta
                nueva_v = {"Fecha": datetime.now(), "Cliente": cli, "Producto": prod, "Monto": monto_v, "Tipo": tipo_v}
                st.session_state.ventas = pd.concat([st.session_state.ventas, pd.DataFrame([nueva_v])], ignore_index=True)
                
                # Si es crédito, sumar a la deuda del cliente
                if tipo_v == "Crédito":
                    st.session_state.clientes.loc[st.session_state.clientes['Nombre'] == cli, 'Deuda'] += monto_v
                
                st.success(f"Venta registrada a {cli}")

    elif opcion == "👥 Clientes y Créditos":
        st.header("Gestión de Clientes")
        with st.expander("Agregar nuevo cliente"):
            n_cli = st.text_input("Nombre del Cliente")
            if st.button("Registrar Cliente"):
                if n_cli not in st.session_state.clientes['Nombre'].values:
                    st.session_state.clientes = pd.concat([st.session_state.clientes, pd.DataFrame([{"Nombre": n_cli, "Deuda": 0.0}])], ignore_index=True)
                    st.rerun()

        st.subheader("Lista de Clientes y Saldos")
        st.dataframe(st.session_state.clientes, use_container_width=True)

        st.subheader("Abonar Pago")
        c_pago = st.selectbox("Cliente que abona", st.session_state.clientes['Nombre'])
        m_pago = st.number_input("Cantidad a abonar (MXN)", min_value=0.0)
        if st.button("Registrar Abono"):
            st.session_state.clientes.loc[st.session_state.clientes['Nombre'] == c_pago, 'Deuda'] -= m_pago
            st.success("Abono registrado")
            st.rerun()

    elif opcion == "📊 Reportes Excel":
        st.header("Descargar Respaldo")
        st.write("Haz clic en los botones para descargar tu información y guardarla en tu computadora.")
        
        # Botón para Inventario
        buffer_inv = io.BytesIO()
        with pd.ExcelWriter(buffer_inv, engine='openpyxl') as writer:
            st.session_state.inventario.to_excel(writer, index=False)
        st.download_button(label="📥 Descargar Inventario (Excel)", data=buffer_inv.getvalue(), file_name="Inventario_JR31.xlsx")

        # Botón para Ventas
        buffer_ventas = io.BytesIO()
        with pd.ExcelWriter(buffer_ventas, engine='openpyxl') as writer:
            st.session_state.ventas.to_excel(writer, index=False)
        st.download_button(label="📥 Descargar Reporte de Ventas (Excel)", data=buffer_ventas.getvalue(), file_name="Ventas_JR31.xlsx")
