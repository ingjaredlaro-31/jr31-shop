import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import os

# --- 1. INITIALIZE SESSION STATES (LOGIC IN ENGLISH) ---
def init_system():
    if 'inv_db' not in st.session_state:
        st.session_state.inv_db = pd.DataFrame(columns=["ARTICULO", "STOCK", "COSTO", "PVP"])
    if 'sales_db' not in st.session_state:
        st.session_state.sales_db = pd.DataFrame(columns=["FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "MODO"])
    if 'client_base' not in st.session_state:
        st.session_state.client_base = pd.DataFrame(columns=["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"])
        default_c = pd.DataFrame([{"ID": "JR31-000", "NOMBRE": "VENTA MOSTRADOR (EFECTIVO)", "DIRECCION": "N/A", "TELEFONO": "N/A", "DEUDA": 0.0}])
        st.session_state.client_base = pd.concat([st.session_state.client_base, default_c], ignore_index=True)
    if 'expenses_db' not in st.session_state:
        st.session_state.expenses_db = pd.DataFrame(columns=["FECHA", "CATEGORIA", "CONCEPTO", "MONTO"])
    if 'cart' not in st.session_state:
        st.session_state.cart = [] # Temporary list for the salesperson
    if 'auth' not in st.session_state: st.session_state.auth = False
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False

init_system()

# --- 2. SUPREME LUXURY STYLE (CSS) ---
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

    /* XL INPUTS */
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; height: 75px !important; margin-bottom: 10px !important; }
    input { color: #FFFFFF !important; font-size: 1.8rem !important; font-family: 'Orbitron' !important; text-align: center !important; }

    .stButton>button { background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important; color: white !important; font-family: 'Orbitron' !important; font-weight: 900 !important; border-radius: 5px !important; height: 3.5em !important; width: 100%; transition: 0.5s; font-size: 1.8rem !important; }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 60px #2E8B57 !important; }

    .footer-centered { text-align: center; color: rgba(255, 255, 255, 0.5); font-family: 'Montserrat', sans-serif; font-size: 14px; margin-top: 80px; padding-bottom: 40px; line-height: 1.6; width: 100%; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px; }

    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 1rem !important; text-transform: uppercase;}
    
    /* CART STYLE */
    .cart-box { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px dashed #2E8B57; }
    </style>
    <div class="header-jared">ING. JARED LARO</div>
    """, unsafe_allow_html=True)

# --- 3. ACCESS CONTROL ---
if not st.session_state.auth:
    st.markdown('<p class="shop-logo-giant">JR 31 SHOP</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">SISTEMA DE ADMINISTRACIÓN Y VENTA</p>', unsafe_allow_html=True)
    col_l, col_form, col_r = st.columns([1, 1.4, 1])
    with col_form:
        u_id = st.text_input("USUARIO ADMIN")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else: st.error("DENEGADO")
else:
    # --- 4. NAVIGATION ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center;'>JR 31 SHOP</h1>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("DESBLOQUEAR ADMIN"):
                if m_code == "291329": st.session_state.is_admin = True; st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"): st.session_state.is_admin = False; st.rerun()

        st.markdown("---")
        menu = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.is_admin: menu += ["📦 GESTIÓN STOCK", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"): st.session_state.auth = False; st.rerun()

    # --- MODULE 1: TERMINAL VENTA (WITH CART EDITING) ---
    if nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        
        col_inv, col_cart = st.columns([1, 1.2])
        
        with col_inv:
            st.subheader("🛍️ Agregar al Ticket")
            if st.session_state.inv_db.empty:
                st.info("No hay productos en inventario.")
            else:
                with st.form("add_to_cart", clear_on_submit=True):
                    prod_name = st.selectbox("PRODUCTO", st.session_state.inv_db['ARTICULO'])
                    qty_add = st.number_input("CANTIDAD", min_value=1, step=1)
                    if st.form_submit_button("➕ AGREGAR AL TICKET"):
                        item_data = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == prod_name].iloc[0]
                        if qty_add > item_data['STOCK']:
                            st.error(f"Stock insuficiente. Solo hay {item_data['STOCK']}")
                        else:
                            st.session_state.cart.append({
                                "ARTICULO": prod_name,
                                "CANTIDAD": qty_add,
                                "PVP": item_data['PVP'],
                                "COSTO": item_data['COSTO'],
                                "SUBTOTAL": item_data['PVP'] * qty_add
                            })
                            st.success(f"{prod_name} añadido.")

        with col_cart:
            st.subheader("🧾 Resumen del Ticket")
            if not st.session_state.cart:
                st.write("Ticket vacío.")
            else:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.table(df_cart[["ARTICULO", "CANTIDAD", "SUBTOTAL"]])
                
                total_ticket = df_cart['SUBTOTAL'].sum()
                st.markdown(f"### TOTAL A COBRAR: **${total_ticket:,.2f}**")
                
                # --- VENDEDORA PUEDE REMOVER COSAS ---
                item_to_remove = st.selectbox("REMOVER ARTÍCULO DEL TICKET", range(len(st.session_state.cart)), format_func=lambda x: st.session_state.cart[x]['ARTICULO'])
                if st.button("🗑️ QUITAR DEL TICKET"):
                    st.session_state.cart.pop(item_to_remove)
                    st.rerun()
                
                st.markdown("---")
                client_pos = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                pay_mode = st.selectbox("MÉTODO DE PAGO", ["CONTADO", "CRÉDITO"])
                
                if st.button("✅ FINALIZAR Y COBRAR"):
                    # Process Sale
                    total_profit = sum([(i['PVP'] - i['COSTO']) * i['CANTIDAD'] for i in st.session_state.cart])
                    detalle_str = ", ".join([f"{i['ARTICULO']} (x{i['CANTIDAD']})" for i in st.session_state.cart])
                    
                    new_sale = pd.DataFrame([{
                        "FECHA": datetime.now().strftime("%d/%m/%y %H:%M"),
                        "CLIENTE": client_pos,
                        "DETALLE": detalle_str,
                        "TOTAL": total_ticket,
                        "UTILIDAD": total_profit,
                        "MODO": pay_mode
                    }])
                    st.session_state.sales_db = pd.concat([st.session_state.sales_db, new_sale], ignore_index=True)
                    
                    # Subtract Stock
                    for item in st.session_state.cart:
                        st.session_state.inv_db.loc[st.session_state.inv_db['ARTICULO'] == item['ARTICULO'], 'STOCK'] -= item['CANTIDAD']
                    
                    # Update Debt
                    if pay_mode == "CRÉDITO":
                        st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == client_pos, 'DEUDA'] += total_ticket
                    
                    st.session_state.cart = [] # Clear cart
                    st.balloons()
                    st.success("Venta completada con éxito.")
                    st.rerun()

    # --- MODULE 2: GESTIÓN STOCK (ADMIN CAN DELETE) ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>CONTROL DE INVENTARIO</h1>", unsafe_allow_html=True)
        tab_a, tab_b = st.tabs(["📥 AGREGAR", "🔧 MODIFICAR / ELIMINAR"])
        
        with tab_a:
            with st.form("add_stock", clear_on_submit=True):
                n = st.text_input("NOMBRE"); s = st.number_input("CANTIDAD", min_value=1); c = st.number_input("COSTO"); p = st.number_input("PVP")
                if st.form_submit_button("GUARDAR"):
                    st.session_state.inv_db = pd.concat([st.session_state.inv_db, pd.DataFrame([{"ARTICULO": n, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
                    st.rerun()

        with tab_b:
            if not st.session_state.inv_db.empty:
                item_edit = st.selectbox("SELECCIONAR ARTÍCULO", st.session_state.inv_db['ARTICULO'])
                idx = st.session_state.inv_db[st.session_state.inv_db['ARTICULO'] == item_edit].index[0]
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    new_p = st.number_input("NUEVO PVP", value=float(st.session_state.inv_db.at[idx, 'PVP']))
                    if st.button("ACTUALIZAR PRECIO"):
                        st.session_state.inv_db.at[idx, 'PVP'] = new_p
                        st.success("Precio actualizado.")
                
                with col_e2:
                    st.markdown("### ⚠️ ZONA DE PELIGRO")
                    if st.button("🗑️ ELIMINAR DEL INVENTARIO"):
                        st.session_state.inv_db = st.session_state.inv_db.drop(idx).reset_index(drop=True)
                        st.warning("Artículo eliminado.")
                        st.rerun()
        
        st.dataframe(st.session_state.inv_db, use_container_width=True)

    # --- MODULE 3: REPORTES (ADMIN CAN DELETE SALES) ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>AUDITORÍA</h1>", unsafe_allow_html=True)
        
        if not st.session_state.sales_db.empty:
            st.subheader("Historial de Ventas")
            st.dataframe(st.session_state.sales_db, use_container_width=True)
            
            # --- GERENCIA PUEDE BORRAR VENTAS MAL REGISTRADAS ---
            sale_to_del = st.selectbox("ANULAR VENTA POR FECHA/CLIENTE", range(len(st.session_state.sales_db)), format_func=lambda x: f"{st.session_state.sales_db.iloc[x]['FECHA']} - {st.session_state.sales_db.iloc[x]['CLIENTE']}")
            if st.button("❌ ANULAR VENTA SELECCIONADA"):
                st.session_state.sales_db = st.session_state.sales_db.drop(sale_to_del).reset_index(drop=True)
                st.error("Venta anulada del sistema.")
                st.rerun()
        else:
            st.info("No hay registros de ventas.")

    # --- OTHERS ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        cl_sel = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
        dat = st.session_state.client_base[st.session_state.client_base['NOMBRE'] == cl_sel].iloc[0]
        st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
        ab = st.number_input("ABONAR", min_value=0.0)
        if st.button("APLICAR PAGO"):
            st.session_state.client_base.loc[st.session_state.client_base['NOMBRE'] == cl_sel, 'DEUDA'] -= ab
            st.rerun()

    elif nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>DASHBOARD</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_db['TOTAL'].sum() if not st.session_state.sales_db.empty else 0
        st.markdown(f'<div style="background:rgba(255,255,255,0.05); padding:50px; text-align:center; border-top:5px solid #FF8C00;"><p style="font-family:Orbitron; font-size:2rem; color:#FF8C00;">VENTAS TOTALES</p><p style="font-size:7rem; font-weight:900;">${v:,.0f}</p></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
