import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="JR 31 SHOP - Punto de Venta", layout="wide", page_icon="🍊")

# --- DISEÑO PROFESIONAL MEJORADO ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    h1, h2, h3 { color: #1a5e20 !important; font-family: 'Arial'; }
    
    /* Color de las etiquetas (Labels) para que sean visibles */
    label { color: #333333 !important; font-weight: bold !important; }

    /* Botones Naranja JR31 */
    .stButton>button {
        background-color: #FF8C00;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    .stButton>button:hover { background-color: #2E8B57; }

    /* Sidebar Verde JR31 */
    [data-testid="stSidebar"] { background-color: #1a5e20; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (Persistencia en Sesión) ---
if 'inv' not in st.session_state:
    st.session_state.inv = pd.DataFrame(columns=["Producto", "Stock", "Costo USD", "Inversión MXN", "Precio Venta"])
if 'ven' not in st.session_state:
    st.session_state.ven = pd.DataFrame(columns=["Fecha", "Cliente", "Total", "Tipo"])
if 'cli' not in st.session_state:
    st.session_state.cli = pd.DataFrame([{"Nombre": "Público General", "Deuda": 0.0}])

# --- SISTEMA DE ACCESO ---
if 'ingresado' not in st.session_state:
    st.session_state.ingresado = False

if not st.session_state.ingresado:
    st.title("🍊 JR 31 SHOP")
    st.subheader("Inicie sesión para administrar su tienda")
    
    col_l, col_r = st.columns(2)
    with col_l:
        u = st.text_input("Usuario Administrador")
        p = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if u == "admin_jr31" and p == "JR31_2024_Chiapas":
                st.session_state.ingresado = True
                st.rerun()
            else:
                st.error("❌ Datos incorrectos")
else:
    # --- MENÚ LATERAL ---
    with st.sidebar:
        st.header("MENÚ JR 31")
        opc = st.radio("Ir a:", ["📊 Resumen", "📦 Inventario USA", "💰 Vender", "👥 Clientes", "📥 Reportes"])
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state.ingresado = False
            st.rerun()

    # --- LÓGICA DE SECCIONES ---
    if opc == "📊 Resumen":
        st.title("📊 Resumen de JR 31 SHOP")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ventas Totales", f"${st.session_state.ven['Total'].sum():,.2f}")
        c2.metric("Inversión (USD)", f"${st.session_state.inv['Costo USD'].sum():,.2f}")
        c3.metric("Deuda de Clientes", f"${st.session_state.cli['Deuda'].sum():,.2f}")
        
        st.subheader("Deudores Actuales")
        st.table(st.session_state.cli[st.session_state.cli['Deuda'] > 0])

    elif opc == "📦 Inventario USA":
        st.title("📦 Compras USA")
        with st.form("inv_form"):
            prod = st.text_input("Nombre del Producto")
            cant = st.number_input("Cantidad", min_value=1)
            cusd = st.number_input("Costo Unitario (USD)")
            tasa = st.number_input("Tipo de Cambio (MXN)", value=18.50)
            p_vta = st.number_input("Precio de Venta (MXN)")
            if st.form_submit_button("GUARDAR EN INVENTARIO"):
                inv_mxn = cusd * tasa * cant
                nuevo = pd.DataFrame([{"Producto": prod, "Stock": cant, "Costo USD": cusd, "Inversión MXN": inv_mxn, "Precio Venta": p_vta}])
                st.session_state.inv = pd.concat([st.session_state.inv, nuevo], ignore_index=True)
                st.success("Producto Registrado")
        st.dataframe(st.session_state.inv)

    elif opc == "💰 Vender":
        st.title("💰 Registrar Venta")
        clie = st.selectbox("Cliente", st.session_state.cli['Nombre'])
        mont = st.number_input("Monto Total (MXN)")
        tipo = st.selectbox("Forma de Pago", ["Contado", "Crédito"])
        if st.button("REGISTRAR VENTA"):
            nv = pd.DataFrame([{"Fecha": datetime.now(), "Cliente": clie, "Total": mont, "Tipo": tipo}])
            st.session_state.ven = pd.concat([st.session_state.ven, nv], ignore_index=True)
            if tipo == "Crédito":
                st.session_state.cli.loc[st.session_state.cli['Nombre'] == clie, 'Deuda'] += mont
            st.success("Venta Exitosa")

    elif opc == "👥 Clientes":
        st.title("👥 Clientes")
        n_c = st.text_input("Nombre del Cliente Nuevo")
        if st.button("Agregar Cliente"):
            st.session_state.cli = pd.concat([st.session_state.cli, pd.DataFrame([{"Nombre": n_c, "Deuda": 0.0}])], ignore_index=True)
        st.dataframe(st.session_state.cli)

    elif opc == "📥 Reportes":
        st.title("📥 Descargar Reportes")
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.ven.to_excel(w, index=False, sheet_name='Ventas')
        st.download_button("Descargar Excel de Ventas", buf.getvalue(), "Reporte_JR31.xlsx")
