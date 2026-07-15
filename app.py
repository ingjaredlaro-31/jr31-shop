import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. CORE ENGINE CONFIGURATION ---
st.set_page_config(
    page_title="JR 31 SHOP | EXECUTIVE SYSTEM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SUPREME EXECUTIVE STYLE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #0a2114 0%, #000000 100%); background-attachment: fixed; color: #FFFFFF !important; }
    
    .header-jared { position: absolute; top: 15px; right: 40px; color: #2E8B57; font-family: 'Orbitron', sans-serif; font-size: 26px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000; }

    .shop-logo-giant {
        font-family: 'Orbitron', sans-serif; font-size: 13vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 20%, #FF8C00 60%, #FF4500 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 30px; margin-bottom: -15px; filter: drop-shadow(0 15px 30px rgba(0,0,0,0.9));
        line-height: 0.8; letter-spacing: -10px; text-transform: uppercase;
    }

    .main-subtitle { text-align: center; color: #2E8B57; font-family: 'Orbitron', sans-serif; letter-spacing: 20px; font-weight: 400; font-size: 2.2rem; margin-bottom: 50px; text-transform: uppercase; }

    /* XL INPUTS & BUTTONS */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; margin-bottom: 10px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button { background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; border-radius: 5px !important; height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important; }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    .footer-centered { text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif; font-size: 14px; margin-top: 80px; padding-bottom: 40px; line-height: 1.6; width: 100%; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    
    /* CARDS */
    .metric-card { background: rgba(255,255,255,0.05); padding: 30px; border-radius: 15px; border-top: 5px solid #FF8C00; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .metric-val { font-family: 'Montserrat'; font-size: 3rem; font-weight: 900; color: white; }
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. DATABASE INITIALIZATION ---
if 'inv_db' not in st.session_state:
    st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
if 'sales_db' not in st.session_state:
    st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "MODO"])
if 'client_base' not in st.session_state:
    st.session_state.client_base = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
    default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
    st.session_state.client_base = pd.concat([st.session_state.client_base, default_c], ignore_index=True)
if 'cart' not in st.session_state: st.session_state.cart = []
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# --- 4. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 5. SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 MODO MAESTRO")
            if st.button("CERRAR ADMIN"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- MODULE: DASHBOARD (BUSINESS INTELLIGENCE) ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:3.5rem;'>INTELIGENCIA DE NEGOCIO</h1>", unsafe_allow_html=True)
        
        # CALCULATIONS
        total_inv = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['COSTO']).sum() if not st.session_state.inv_db.empty else 0
        total_vta = (st.session_state.inv_db['STOCK'] * st.session_state.inv_db['PVP']).sum() if not st.session_state.inv_db.empty else 0
        total_stock = st.session_state.inv_db['STOCK'].sum() if not st.session_state.inv_db.empty else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><p style="color:#FF8C00; font-family:Orbitron;">INVERTIDO (COSTO)</p><p class="metric-val">${total_inv:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card" style="border-top:5px solid #2E8B57;"><p style="color:#2E8B57; font-family:Orbitron;">VALOR EN VENTA (PVP)</p><p class="metric-val">${total_vta:,.0f}</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card" style="border-top:5px solid #FFFFFF;"><p style="color:#FFFFFF; font-family:Orbitron;">TOTAL EXISTENCIAS</p><p class="metric-val">{total_stock:,.0f} PZS</p></div>', unsafe_allow_html=True)

    # --- MODULE: POS (TERMINAL VENTA WITH SEARCH BAR) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        
        col_l, col_r = st.columns([1, 1.2])
        with col_l:
            st.subheader("🛍️ Agregar al Ticket")
            if st.session_state.inv_db.empty: st.info("Inventario vacío.")
            else:
                # --- BARRA DE BÚSQUEDA ---
                search_term = st.text_input("🔍 BUSCAR ARTÍCULO", placeholder="Escriba nombre del producto...")
                filtered_df = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'].str.contains(search_term, case=False)]
                
                with st.form("pos_add", clear_on_submit=True):
                    prod_sel = st.selectbox("RESULTADO DE BÚSQUEDA", filtered_df['ARTICULO'])
                    qty_sel = st.number_input("CANTIDAD", min_value=1, step=1)
                    if st.form_submit_button("AÑADIR AL TICKET"):
                        item = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == prod_sel].iloc[0]
                        if qty_sel > item['STOCK']: st.error("Stock insuficiente.")
                        else:
                            st.session_state.cart.append({"ARTICULO": prod_sel, "CANTIDAD": qty_sel, "PVP": item['PVP'], "COSTO": item['COSTO'], "SUBTOTAL": item['PVP']*qty_sel})
                            st.success("Añadido.")

        with col_r:
            st.subheader("🧾 Resumen de Venta")
            if not st.session_state.cart: st.write("Ticket vacío.")
            else:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.table(df_cart[["ARTICULO", "CANTIDAD", "SUBTOTAL"]])
                total_t = df_cart['SUBTOTAL'].sum()
                st.markdown(f"## TOTAL: ${total_t:,.2f}")
                
                rem = st.selectbox("Remover artículo:", range(len(st.session_state.cart)), format_func=lambda x: st.session_state.cart[x]['ARTICULO'])
                if st.button("🗑️ ELIMINAR SELECCIONADO"): st.session_state.cart.pop(rem); st.rerun()
                
                cli_pos = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                if st.button("✅ FINALIZAR Y COBRAR"):
                    profit = sum([(i['PVP'] - i['COSTO']) * i['CANTIDAD'] for i in st.session_state.cart])
                    detail = ", ".join([f"{i['ARTICULO']} (x{i['CANTIDAD']})" for i in st.session_state.cart])
                    
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y %H:%M"), "CLIENTE": cli_pos, "DETALLE": detail, "TOTAL": total_t, "UTILIDAD": profit, "MODO": "CONTADO"}])], ignore_index=True)
                    for i in st.session_state.cart: st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == i['ARTICULO'], 'STOCK'] -= i['CANTIDAD']
                    st.session_state.cart = []; st.balloons(); st.rerun()

    # --- MODULE: STOCK (ADMIN) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GESTIÓN DE STOCK</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 ALTA", "✏️ EDITAR"])
        with tab_a:
            with st.form("add_s", clear_on_submit=True):
                n = st.text_input("PRODUCTO"); s = st.number_input("CANTIDAD", min_value=1); c = st.number_input("COSTO"); p = st.number_input("PVP")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
        st.dataframe(st.session_state.inv_db, use_container_width=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
