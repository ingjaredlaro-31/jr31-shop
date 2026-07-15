")
            if st.button("CERRAR PRIVILEGIOS"):
                st.session_state.admin_privileges = False
                st.rerun()

        st.markdown("---")
        menu_options = ["🛒 TERMINAL VENTA", "👤 CARTERA CLIENTES", "📊 DASHBOARD"]
        if st.session_state.admin_privileges:
            menu_options += ["📦 GESTIÓN STOCK", "💸 GASTOS", "📝 REPORTES"]
        
        choice = st.radio("SELECCIONE MÓDULO", menu_options)
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.authenticated = False
            st.rerun()

    # --- 6. MÓDULOS ---

    # --- DASHBOARD ---
    if choice == "📊 DASHBOARD":
        st.markdown("<h1 style='font-family:Orbitron; text-align:center; font-size:4rem;'>INTELIGENCIA COMERCIAL</h1>", unsafe_allow_html=True)
        v = st.session_state.sales_history['TOTAL'].sum() if not st.session_state.sales_history.empty else 0
        g = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="metric-container"><p style="color:#FF8C00; font-family:Orbitron;">INGRESOS TOTALES</p><p class="metric-value">${v:,.0f}</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-container" style="border-top:5px solid #FF4500;"><p style="color:#FF4500; font-family:Orbitron;">EGRESOS TOTALES</p><p class="metric-value" style="color:#FF4500;">${g:,.0f}</p></div>', unsafe_allow_html=True)

    # --- TERMINAL VENTA ---
    elif choice == "🛒 TERMINAL VENTA":
        st.markdown("<h1 style='font-family:Orbitron;'>TERMINAL DE VENTA</h1>", unsafe_allow_html=True)
        if st.session_state.inventory_db.empty: st.info("Sin inventario.")
        else:
            with st.form("pos"):
                art = st.selectbox("PRODUCTO", st.session_state.inventory_db['ARTICULO'])
                cli = st.selectbox("CLIENTE", st.session_state.client_base['NOMBRE'])
                qty = st.number_input("CANTIDAD", min_value=1)
                if st.form_submit_button("FINALIZAR VENTA"):
                    row = st.session_state.inventory_db[st.session_state.inventory_db['ARTICULO'] == art].iloc[0]
                    total = row['PVP'] * qty
                    st.session_state.sales_history = pd.concat([st.session_state.sales_history, pd.DataFrame([{"FECHA": datetime.now().strftime("%d/%m/%y"), "CLIENTE": cli, "ARTICULO": art, "TOTAL": total, "UTILIDAD": (row['PVP']-row['COSTO'])*qty, "MODO": "CONTADO"}])], ignore_index=True)
                    st.session_state.inventory_db.loc[st.session_state.inventory_db['ARTICULO'] == art, 'STOCK'] -= qty
                    st.success(f"Venta registrada: ${total}")

    # --- CARTERA ---
    elif choice == "👤 CARTERA CLIENTES":
        st.markdown("<h1 style='font-family:Orbitron;'>CARTERA</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 EXPEDIENTES", "➕ NUEVO CLIENTE"])
        with t2:
            n_name = st.text_input("NOMBRE COMPLETO")
            if st.button("GUARDAR"):
                st.session_state.client_base = pd.concat([st.session_state.client_base, pd.DataFrame([{"NOMBRE": n_name, "DEUDA": 0.0}])], ignore_index=True)
                st.success("Guardado.")

    # --- GESTIÓN STOCK ---
    elif choice == "📦 GESTIÓN STOCK" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron;'>INVENTARIO</h1>", unsafe_allow_html=True)
        with st.form("stk", clear_on_submit=True):
            a = st.text_input("ARTICULO")
            s = st.number_input("STOCK", min_value=1)
            c = st.number_input("COSTO")
            p = st.number_input("PVP")
            if st.form_submit_button("ACTUALIZAR STOCK"):
                st.session_state.inventory_db = pd.concat([st.session_state.inventory_db, pd.DataFrame([{"ARTICULO": a, "STOCK": s, "COSTO": c, "PVP": p}])], ignore_index=True)
        st.dataframe(st.session_state.inventory_db, use_container_width=True)

    # --- MÓDULO CORREGIDO: GASTOS ---
    elif choice == "💸 GASTOS" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron; text-align:center;'>CONTROL DE EGRESOS Y LOGÍSTICA</h1>", unsafe_allow_html=True)
        
        # Resumen Rápido de Gastos
        total_gastado = st.session_state.expenses_db['MONTO'].sum() if not st.session_state.expenses_db.empty else 0
        st.markdown(f'<div class="metric-container" style="border-top:5px solid #2E8B57; margin-bottom:40px;"><p style="color:#2E8B57; font-family:Orbitron;">TOTAL GASTOS OPERATIVOS</p><p class="metric-value" style="color:#2E8B57;">${total_gastado:,.2f}</p></div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns([1, 1.5])
        
        with col_g1:
            st.markdown("### 📥 REGISTRAR GASTO")
            with st.form("form_gastos", clear_on_submit=True):
                cat_g = st.selectbox("CATEGORÍA", ["PALLETS", "OFICINA", "LOGÍSTICA", "SERVICIOS", "VARIOS"])
                con_g = st.text_input("CONCEPTO (Ej. Compra de tarimas, papelería...)")
                mon_g = st.number_input("MONTO DEL GASTO ($)", min_value=0.1, step=1.0)
                if st.form_submit_button("GUARDAR GASTO EN SISTEMA"):
                    nuevo_gasto = pd.DataFrame([{
                        "FECHA": datetime.now().strftime("%d/%m/%Y"),
                        "CATEGORIA": cat_g,
                        "CONCEPTO": con_g,
                        "MONTO": mon_g
                    }])
                    st.session_state.expenses_db = pd.concat([st.session_state.expenses_db, nuevo_gasto], ignore_index=True)
                    st.success("✅ Gasto registrado correctamente.")
                    st.rerun()

        with col_g2:
            st.markdown("### 📋 HISTORIAL DE GASTOS")
            if not st.session_state.expenses_db.empty:
                st.dataframe(st.session_state.expenses_db, use_container_width=True)
            else:
                st.info("No hay gastos registrados en este periodo.")

    # --- REPORTES ---
    elif choice == "📝 REPORTES" and st.session_state.admin_privileges:
        st.markdown("<h1 style='font-family:Orbitron;'>CENTRO DE AUDITORÍA</h1>", unsafe_allow_html=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.sales_history.to_excel(w, index=False, sheet_name='VENTAS')
            st.session_state.expenses_db.to_excel(w, index=False, sheet_name='GASTOS')
        st.download_button("📥 DESCARGAR REPORTE EXCEL", buf.getvalue(), f"JR31_LARO_MASTER.xlsx")
