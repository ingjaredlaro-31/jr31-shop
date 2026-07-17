import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF
import io
 
# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="JR 31 SHOP | ERP by Ing. Jared Laro",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
DB_PATH = "jr31_shop.db"
 
# ============================================================
# 2. CAPA DE PERSISTENCIA (SQLite)
#    -> El inventario, clientes, ventas y gastos ahora se guardan
#       en un archivo de base de datos real (jr31_shop.db), no en
#       memoria. Ya NO se borran al recargar o reiniciar la app.
# ============================================================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
 
 
def init_database():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS inventario (
        ARTICULO TEXT PRIMARY KEY, STOCK INTEGER, COSTO_USA REAL,
        COSTO_TJ REAL, PVP_JR31 REAL, VENDIDOS INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS ventas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, FECHA TEXT, CLIENTE TEXT,
        DETALLE TEXT, TOTAL REAL, UTILIDAD REAL, PAGO TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
        ID TEXT PRIMARY KEY, NOMBRE TEXT, DIRECCION TEXT,
        TELEFONO TEXT, DEUDA REAL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS gastos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, FECHA TEXT,
        CATEGORIA TEXT, CONCEPTO TEXT, MONTO REAL)""")
    cur.execute("SELECT COUNT(*) FROM clientes")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO clientes VALUES (?,?,?,?,?)",
                     ("JR-000", "VENTA MOSTRADOR", "N/A", "N/A", 0.0))
    conn.commit()
    conn.close()
 
 
def load_table(name, cols):
    conn = get_conn()
    try:
        df = pd.read_sql(f"SELECT * FROM {name}", conn)
    except Exception:
        df = pd.DataFrame(columns=cols)
    conn.close()
    if df.empty:
        df = pd.DataFrame(columns=cols)
    return df
 
 
def save_table(df, name):
    conn = get_conn()
    df.to_sql(name, conn, if_exists="replace", index=False)
    conn.close()
 
 
init_database()
 
INV_COLS = ["ARTICULO", "STOCK", "COSTO_USA", "COSTO_TJ", "PVP_JR31", "VENDIDOS"]
VENTAS_COLS = ["ID", "FECHA", "CLIENTE", "DETALLE", "TOTAL", "UTILIDAD", "PAGO"]
CLIENTES_COLS = ["ID", "NOMBRE", "DIRECCION", "TELEFONO", "DEUDA"]
GASTOS_COLS = ["ID", "FECHA", "CATEGORIA", "CONCEPTO", "MONTO"]
 
inv_db = load_table("inventario", INV_COLS)
sales_db = load_table("ventas", VENTAS_COLS)
clients_db = load_table("clientes", CLIENTES_COLS)
expenses_db = load_table("gastos", GASTOS_COLS)
 
if "cart" not in st.session_state:
    st.session_state.cart = []
if "auth" not in st.session_state:
    st.session_state.auth = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
 
# ============================================================
# 3. ESTILO CYBER-LUXURY
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Montserrat:wght@400;700;900&display=swap');
 
    .stApp {
        background: radial-gradient(circle at center, #0a2114 0%, #000000 100%);
        background-attachment: fixed;
        color: #FFFFFF !important;
    }
 
    .jared-header {
        position: absolute; top: 15px; right: 40px;
        color: #2E8B57; font-family: 'Orbitron', sans-serif;
        font-size: 22px; font-weight: 900; text-shadow: 0 0 15px #2E8B57; z-index: 1000;
    }
 
    /* ---- LOGO GIGANTE DE INICIO ---- */
    .logo-wrap { text-align:center; margin-top: 20px; }
    .logo-giant {
        font-family: 'Orbitron', sans-serif;
        font-size: 19vw; font-weight: 900; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 15%, #FF8C00 55%, #FF4500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0; padding: 0; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.9));
        line-height: 0.78; letter-spacing: -1vw; text-transform: uppercase;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { filter: drop-shadow(0 20px 40px rgba(255,140,0,0.25)); }
        50% { filter: drop-shadow(0 20px 55px rgba(46,139,87,0.55)); }
    }
    .logo-sub {
        text-align:center; font-family:'Orbitron', sans-serif; letter-spacing: 8px;
        color:#2E8B57; font-size: 1.3rem; margin-top: -10px; text-shadow: 0 0 12px #2E8B57;
    }
    .logo-tag {
        text-align:center; font-family:'Montserrat', sans-serif; color: rgba(255,255,255,0.55);
        font-size: 0.95rem; margin-top: 6px; letter-spacing: 2px;
    }
    .divider-glow {
        height: 2px; width: 60%; margin: 25px auto;
        background: linear-gradient(90deg, transparent, #FF8C00, #2E8B57, transparent);
    }
 
    .footer-centered {
        text-align: center; color: rgba(255, 255, 255, 0.6); font-family: 'Montserrat', sans-serif;
        font-size: 14px; margin-top: 100px; padding-bottom: 40px; width: 100%;
        line-height: 1.8; border-top: 1px solid rgba(46, 139, 87, 0.2); padding-top: 20px;
    }
    .footer-centered b { color: #2E8B57; font-size: 1.2rem; }
 
    [data-testid="stSidebar"] { background-color: #0b0d17 !important; border-right: 5px solid #FF8C00; }
    div[role="radiogroup"] label { font-size: 1.4rem !important; font-weight: 700; color: #FFFFFF !important; margin-bottom: 14px !important; }
 
    .exec-card {
        background: rgba(255, 255, 255, 0.04); border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border-top: 4px solid #FF8C00;
        margin-bottom: 15px;
    }
    .metric-title { font-family: 'Orbitron'; font-size: 0.85rem; color: #FF8C00; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { font-family: 'Montserrat'; font-size: 2.6rem; font-weight: 900; color: #FFFFFF; }
 
    .low-stock { color: #FF4040 !important; font-weight: 900; }
 
    div[data-baseweb="input"] { background-color: rgba(255, 255, 255, 0.05) !important; border: 2px solid #FF8C00 !important; border-radius: 10px !important; }
    input { color: #FFFFFF !important; font-family: 'Orbitron' !important; }
 
    .stButton>button {
        background: linear-gradient(90deg, #FF4500 0%, #FF8C00 100%) !important;
        color: white !important; font-family: 'Orbitron' !important;
        font-weight: 900 !important; border-radius: 5px !important;
        height: 3.2em !important; width: 100%; transition: 0.4s;
        border: none !important;
    }
    .stButton>button:hover { background: #2E8B57 !important; box-shadow: 0 0 40px #2E8B57 !important; transform: translateY(-2px); }
 
    .cart-item {
        background: rgba(255,255,255,0.05); border-left: 3px solid #2E8B57;
        border-radius: 6px; padding: 10px 14px; margin-bottom: 8px;
        font-family: 'Montserrat'; display:flex; justify-content:space-between;
    }
 
    #MainMenu, footer, header { visibility: hidden; }
    label { color: #FF8C00 !important; font-family: 'Orbitron' !important; font-weight: 900 !important; font-size: 0.9rem !important; text-transform: uppercase;}
    </style>
    <div class="jared-header">ING. JARED LARO</div>
    """, unsafe_allow_html=True)
 
 
# ============================================================
# 4. MOTOR PDF (Ticket de venta)
# ============================================================
def create_pdf(client, items, total, pago):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "JR 31 SHOP", ln=True, align='C')
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, f"Fecha: {datetime.now().strftime('%d/%m/%y %H:%M')}", ln=True, align='C')
    pdf.cell(0, 5, f"Cliente: {client}", ln=True, align='C')
    pdf.cell(0, 5, "-" * 32, ln=True)
    for i in items:
        pdf.cell(0, 5, f"{i['ART']} x{i['QTY']}", ln=True)
        pdf.cell(0, 5, f"   ${i['SUB']:,.2f}", ln=True, align='R')
    pdf.cell(0, 5, "-" * 32, ln=True)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, f"TOTAL: ${total:,.2f}", ln=True, align='R')
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 6, f"Forma de pago: {pago}", ln=True, align='C')
    pdf.cell(0, 8, "¡Gracias por su compra!", ln=True, align='C')
    out = pdf.output()
    return bytes(out)
 
 
# ============================================================
# 5. ACCESO AL SISTEMA
# ============================================================
if not st.session_state.auth:
    st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    st.markdown('<p class="logo-giant">JR 31</p>', unsafe_allow_html=True)
    st.markdown('<p class="logo-sub">S H O P</p>', unsafe_allow_html=True)
    st.markdown('<p class="logo-tag">SISTEMA ERP PROFESIONAL &nbsp;•&nbsp; CHIAPAS, MÉXICO</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
    col_l, col_form, col_r = st.columns([1, 1.3, 1])
    with col_form:
        u_id = st.text_input("ADMIN ID")
        u_pw = st.text_input("CLAVE DE ACCESO", type="password")
        if st.button("ACCEDER"):
            if u_id == "admin_jr31" and u_pw == "JR31_2024_Chiapas":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ACCESO DENEGADO")
else:
    # --- NAVEGACIÓN ---
    with st.sidebar:
        st.markdown("<h1 style='color:#FF8C00; font-family:Orbitron; text-align:center; font-size:2.2rem;'>JR 31</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#2E8B57; font-family:Orbitron; letter-spacing:4px; margin-top:-15px;'>SHOP</p>", unsafe_allow_html=True)
        if not st.session_state.is_admin:
            m_code = st.text_input("🔓 CÓDIGO MAESTRO", type="password")
            if st.button("ACTIVAR ADMIN"):
                if m_code == "291329":
                    st.session_state.is_admin = True
                    st.rerun()
        else:
            st.success("🔒 GERENCIA ACTIVA")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.is_admin = False
                st.rerun()
 
        st.markdown("---")
        menu = ["📊 DASHBOARD", "🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES"]
        if st.session_state.is_admin:
            menu += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        nav = st.sidebar.radio("SISTEMA", menu)
        if st.button("SALIR"):
            st.session_state.auth = False
            st.rerun()
 
    # --- DASHBOARD ---
    if nav == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>PANORAMA COMERCIAL</h1>", unsafe_allow_html=True)
        v_t = sales_db['TOTAL'].sum() if not sales_db.empty else 0
        u_t = sales_db['UTILIDAD'].sum() if not sales_db.empty else 0
        d_t = clients_db['DEUDA'].sum() if not clients_db.empty else 0
        inv_tj = (inv_db['STOCK'] * inv_db['COSTO_TJ']).sum() if not inv_db.empty else 0
        inv_usa = (inv_db['STOCK'] * inv_db['COSTO_USA']).sum() if not inv_db.empty else 0
        pzs = inv_db['STOCK'].sum() if not inv_db.empty else 0
 
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="exec-card"><p class="metric-title">🛒 VENTAS</p><p class="metric-value">${v_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #2E8B57;"><p class="metric-title">💰 GANANCIA</p><p class="metric-value" style="color:#2E8B57;">${u_t:,.0f}</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="exec-card"><p class="metric-title">👥 CARTERA</p><p class="metric-value" style="color:#FF4500;">${d_t:,.0f}</p></div>', unsafe_allow_html=True)
 
        c4, c5, c6 = st.columns(3)
        with c4:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📦 PIEZAS STOCK</p><p class="metric-value">{pzs:,.0f}</p></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">📉 INVERSIÓN TJ</p><p class="metric-value">${inv_tj:,.0f}</p></div>', unsafe_allow_html=True)
        with c6:
            st.markdown(f'<div class="exec-card" style="border-top:4px solid #FFFFFF;"><p class="metric-title">🇺🇸 COSTO USA</p><p class="metric-value">${inv_usa:,.0f}</p></div>', unsafe_allow_html=True)
 
        # --- Novedad: gráfico de ventas y alerta de stock bajo ---
        if not sales_db.empty:
            st.markdown("<h3 style='font-family:Orbitron; color:#FF8C00; margin-top:30px;'>📈 TENDENCIA DE VENTAS</h3>", unsafe_allow_html=True)
            trend = sales_db.groupby("FECHA")["TOTAL"].sum()
            st.bar_chart(trend)
 
        if not inv_db.empty:
            bajo = inv_db[inv_db['STOCK'] <= 3]
            if not bajo.empty:
                st.markdown("<h3 style='font-family:Orbitron; color:#FF4040; margin-top:20px;'>⚠️ STOCK BAJO (≤3 pzs)</h3>", unsafe_allow_html=True)
                st.dataframe(bajo[["ARTICULO", "STOCK"]], use_container_width=True)
 
    # --- TERMINAL VENTA (antes no tenía código, no hacía nada) ---
    elif nav == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
 
        if inv_db.empty:
            st.warning("No hay artículos en inventario. Un administrador debe darlos de alta primero.")
        else:
            col_a, col_b = st.columns([1.4, 1])
            with col_a:
                st.markdown("<h4 style='color:#2E8B57; font-family:Orbitron;'>AGREGAR PRODUCTO</h4>", unsafe_allow_html=True)
                art = st.selectbox("PRODUCTO", inv_db['ARTICULO'])
                fila = inv_db[inv_db['ARTICULO'] == art].iloc[0]
                st.caption(f"Stock disponible: {int(fila['STOCK'])} pzs · PVP: ${fila['PVP_JR31']:,.2f}")
                qty = st.number_input("CANTIDAD", min_value=1, max_value=max(int(fila['STOCK']), 1), value=1)
                if st.button("➕ AGREGAR AL CARRITO"):
                    if qty > fila['STOCK']:
                        st.error("Cantidad supera el stock disponible.")
                    else:
                        st.session_state.cart.append({
                            "ART": art, "QTY": int(qty),
                            "PRECIO": float(fila['PVP_JR31']),
                            "COSTO": float(fila['COSTO_TJ']),
                            "SUB": float(fila['PVP_JR31']) * int(qty)
                        })
                        st.rerun()
 
                st.markdown("<h4 style='color:#2E8B57; font-family:Orbitron; margin-top:20px;'>CARRITO</h4>", unsafe_allow_html=True)
                if not st.session_state.cart:
                    st.info("Carrito vacío.")
                else:
                    for idx, it in enumerate(st.session_state.cart):
                        cc1, cc2 = st.columns([4, 1])
                        with cc1:
                            st.markdown(f'<div class="cart-item"><span>{it["ART"]} x{it["QTY"]}</span><span>${it["SUB"]:,.2f}</span></div>', unsafe_allow_html=True)
                        with cc2:
                            if st.button("❌", key=f"rm_{idx}"):
                                st.session_state.cart.pop(idx)
                                st.rerun()
 
            with col_b:
                st.markdown("<h4 style='color:#FF8C00; font-family:Orbitron;'>COBRO</h4>", unsafe_allow_html=True)
                cliente = st.selectbox("CLIENTE", clients_db['NOMBRE'])
                pago = st.radio("FORMA DE PAGO", ["CONTADO", "CRÉDITO"])
                total = sum(i['SUB'] for i in st.session_state.cart)
                utilidad = sum((i['PRECIO'] - i['COSTO']) * i['QTY'] for i in st.session_state.cart)
                st.metric("TOTAL A COBRAR", f"${total:,.2f}")
 
                if st.button("✅ CONFIRMAR VENTA", disabled=(len(st.session_state.cart) == 0)):
                    # descuenta stock
                    for it in st.session_state.cart:
                        i_idx = inv_db[inv_db['ARTICULO'] == it['ART']].index[0]
                        inv_db.at[i_idx, 'STOCK'] -= it['QTY']
                        inv_db.at[i_idx, 'VENDIDOS'] += it['QTY']
 
                    detalle = ", ".join(f"{i['ART']} x{i['QTY']}" for i in st.session_state.cart)
                    nueva_venta = pd.DataFrame([{
                        "ID": (sales_db['ID'].max() + 1) if not sales_db.empty else 1,
                        "FECHA": datetime.now().strftime("%d/%m/%y"),
                        "CLIENTE": cliente, "DETALLE": detalle,
                        "TOTAL": total, "UTILIDAD": utilidad, "PAGO": pago
                    }])
                    sales_db = pd.concat([sales_db, nueva_venta], ignore_index=True)
 
                    if pago == "CRÉDITO":
                        clients_db.loc[clients_db['NOMBRE'] == cliente, 'DEUDA'] += total
 
                    save_table(inv_db, "inventario")
                    save_table(sales_db, "ventas")
                    save_table(clients_db, "clientes")
 
                    st.session_state.last_ticket = create_pdf(cliente, st.session_state.cart, total, pago)
                    st.session_state.cart = []
                    st.success("Venta registrada correctamente.")
                    st.rerun()
 
                if "last_ticket" in st.session_state and st.session_state.last_ticket:
                    st.download_button("🖨️ DESCARGAR TICKET", st.session_state.last_ticket, "ticket_jr31.pdf")
 
    # --- STOCK ---
    elif nav == "📦 GESTIÓN STOCK" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        t_a, t_b = st.tabs(["📥 ALTA", "✏️ EDITAR / BORRAR"])
        with t_a:
            with st.form("add_f", clear_on_submit=True):
                n = st.text_input("ARTICULO")
                s = st.number_input("CANTIDAD", min_value=1, step=1)
                cu = st.number_input("COSTO USA")
                ct = st.number_input("COSTO TJ")
                p = st.number_input("PVP JR31")
                if st.form_submit_button("GUARDAR"):
                    if n.strip() == "":
                        st.error("El nombre del artículo no puede estar vacío.")
                    elif n in inv_db['ARTICULO'].values:
                        st.error("Ese artículo ya existe. Usa la pestaña EDITAR para modificarlo.")
                    else:
                        nuevo = pd.DataFrame([{
                            "ARTICULO": n, "STOCK": s, "COSTO_USA": cu,
                            "COSTO_TJ": ct, "PVP_JR31": p, "VENDIDOS": 0
                        }])
                        inv_db = pd.concat([inv_db, nuevo], ignore_index=True)
                        save_table(inv_db, "inventario")
                        st.success(f"'{n}' agregado al inventario.")
                        st.rerun()
        with t_b:
            if not inv_db.empty:
                ed_it = st.selectbox("PRODUCTO:", inv_db['ARTICULO'])
                idx = inv_db[inv_db['ARTICULO'] == ed_it].index[0]
                with st.form("ed_f"):
                    new_q = st.number_input("STOCK", value=int(inv_db.at[idx, 'STOCK']))
                    new_p = st.number_input("PVP", value=float(inv_db.at[idx, 'PVP_JR31']))
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("💾 ACTUALIZAR"):
                        inv_db.at[idx, 'STOCK'] = new_q
                        inv_db.at[idx, 'PVP_JR31'] = new_p
                        save_table(inv_db, "inventario")
                        st.rerun()
                    if c2.form_submit_button("🗑️ ELIMINAR"):
                        inv_db = inv_db.drop(idx).reset_index(drop=True)
                        save_table(inv_db, "inventario")
                        st.rerun()
            else:
                st.info("Todavía no hay artículos registrados.")
 
        st.markdown("<h4 style='color:#2E8B57; font-family:Orbitron; margin-top:20px;'>🔎 BUSCAR</h4>", unsafe_allow_html=True)
        busq = st.text_input("Filtrar por nombre de artículo", "")
        tabla = inv_db.copy()
        if busq:
            tabla = tabla[tabla['ARTICULO'].str.contains(busq, case=False, na=False)]
        st.dataframe(tabla, use_container_width=True)
 
    # --- CARTERA ---
    elif nav == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t_v, t_n = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO"])
        with t_v:
            cf = st.selectbox("CLIENTE", clients_db['NOMBRE'])
            dat = clients_db[clients_db['NOMBRE'] == cf].iloc[0]
            st.markdown(f"**ID:** {dat['ID']} | **DIR:** {dat['DIRECCION']} | **TEL:** {dat['TELEFONO']}")
            st.metric("DEUDA", f"${dat['DEUDA']:,.2f}")
            pago = st.number_input("ABONAR", min_value=0.0)
            if st.button("PAGAR"):
                clients_db.loc[clients_db['NOMBRE'] == cf, 'DEUDA'] -= pago
                save_table(clients_db, "clientes")
                st.rerun()
        with t_n:
            with st.form("nc"):
                n = st.text_input("NOMBRE")
                d = st.text_input("DIRECCIÓN")
                t = st.text_input("TELÉFONO")
                if st.form_submit_button("GUARDAR"):
                    nid = f"JR-{len(clients_db):03d}"
                    nuevo = pd.DataFrame([{"ID": nid, "NOMBRE": n, "DIRECCION": d, "TELEFONO": t, "DEUDA": 0.0}])
                    clients_db = pd.concat([clients_db, nuevo], ignore_index=True)
                    save_table(clients_db, "clientes")
                    st.rerun()
 
    # --- GASTOS ---
    elif nav == "💸 GASTOS" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>GASTOS</h1>", unsafe_allow_html=True)
        with st.form("g"):
            cat = st.selectbox("CATEGORÍA", ["RENTA", "SERVICIOS", "TRANSPORTE", "VARIOS"])
            con = st.text_input("CONCEPTO")
            mon = st.number_input("MONTO")
            if st.form_submit_button("GUARDAR"):
                nuevo = pd.DataFrame([{
                    "ID": (expenses_db['ID'].max() + 1) if not expenses_db.empty else 1,
                    "FECHA": datetime.now().strftime("%d/%m/%y"),
                    "CATEGORIA": cat, "CONCEPTO": con, "MONTO": mon
                }])
                expenses_db = pd.concat([expenses_db, nuevo], ignore_index=True)
                save_table(expenses_db, "gastos")
                st.rerun()
        st.dataframe(expenses_db, use_container_width=True)
        if not expenses_db.empty:
            st.metric("TOTAL GASTOS", f"${expenses_db['MONTO'].sum():,.2f}")
 
    # --- REPORTES ---
    elif nav == "📝 REPORTES" and st.session_state.is_admin:
        st.markdown("<h1 style='font-family:Orbitron;'>REPORTES</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            sales_db.to_excel(w, index=False, sheet_name='VENTAS')
            inv_db.to_excel(w, index=False, sheet_name='INVENTARIO')
            clients_db.to_excel(w, index=False, sheet_name='CLIENTES')
            expenses_db.to_excel(w, index=False, sheet_name='GASTOS')
        st.download_button("📥 DESCARGAR EXCEL MAESTRO", buf.getvalue(), "JR31_MASTER.xlsx")
 
# ============================================================
# 6. PIE DE PÁGINA
# ============================================================
st.markdown("""
    <div class="footer-centered">
        <p><b>ING. JARED LARO</b></p>
        <p>ING JARED LARA RODRIGUEZ | 918'125'5735</p>
        <p>SISTEMA ERP JR 31 SHOP - EXCLUSIVE BUSINESS EDITION</p>
    </div>
""", unsafe_allow_html=True)
 
