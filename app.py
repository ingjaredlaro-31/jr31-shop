<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JR31 SHOP · Punto de Venta</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --navy:#152238;
    --navy-2:#1E3153;
    --cream:#FBF8F1;
    --paper:#FFFFFF;
    --ink:#1B2333;
    --muted:#6B7386;
    --line:#E7E2D6;
    --gold:#E3A63E;
    --gold-dk:#C88A22;
    --blue:#3A7CA5;
    --green:#3F8F5F;
    --green-bg:#E9F5EE;
    --red:#D6483F;
    --red-bg:#FBEAE8;
    --radius:10px;
    --shadow:0 2px 10px rgba(21,34,56,0.07);
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    font-family:'Inter',sans-serif;
    background:var(--cream);
    color:var(--ink);
    min-height:100vh;
  }
  h1,h2,h3,.brand{font-family:'Space Grotesk',sans-serif;}
  button{font-family:inherit;cursor:pointer;}
  input,select{font-family:inherit;}
  ::-webkit-scrollbar{width:8px;height:8px;}
  ::-webkit-scrollbar-thumb{background:#D8D2C2;border-radius:4px;}

  /* ---------- LOGIN ---------- */
  #login-screen{
    min-height:100vh;display:flex;align-items:center;justify-content:center;
    background:radial-gradient(circle at 20% 20%, #21314F 0%, var(--navy) 55%, #0F1A2C 100%);
    padding:20px;
  }
  .login-card{
    background:var(--paper);
    width:100%;max-width:380px;
    border-radius:16px;
    padding:36px 32px 30px;
    box-shadow:0 20px 60px rgba(0,0,0,0.35);
    text-align:center;
  }
  .login-logo{
    width:64px;height:64px;border-radius:14px;
    background:linear-gradient(135deg, var(--gold) 0%, var(--gold-dk) 100%);
    display:flex;align-items:center;justify-content:center;
    margin:0 auto 16px;color:#1B2333;font-weight:700;font-size:22px;font-family:'Space Grotesk',sans-serif;
  }
  .login-card h1{font-size:22px;margin:0 0 2px;color:var(--navy);letter-spacing:0.3px;}
  .login-card p.sub{color:var(--muted);font-size:13px;margin:0 0 24px;}
  .field{text-align:left;margin-bottom:14px;}
  .field label{display:block;font-size:12.5px;font-weight:600;color:var(--navy-2);margin-bottom:6px;}
  .field input, .field select{
    width:100%;padding:10px 12px;border:1.5px solid var(--line);border-radius:8px;
    font-size:14.5px;background:#FCFBF8;transition:border-color .15s;
  }
  .field input:focus, .field select:focus{outline:none;border-color:var(--gold);background:#fff;}
  .btn{
    border:none;border-radius:8px;padding:11px 18px;font-weight:600;font-size:14px;
    transition:transform .1s, opacity .15s;
  }
  .btn:active{transform:scale(0.98);}
  .btn-primary{background:var(--navy);color:#fff;width:100%;}
  .btn-primary:hover{background:var(--navy-2);}
  .btn-gold{background:var(--gold);color:#241804;}
  .btn-gold:hover{background:var(--gold-dk);}
  .btn-ghost{background:transparent;color:var(--navy);border:1.5px solid var(--line);}
  .btn-ghost:hover{border-color:var(--navy);}
  .btn-danger{background:var(--red-bg);color:var(--red);}
  .btn-danger:hover{background:#f6d6d3;}
  .btn-sm{padding:6px 10px;font-size:12.5px;border-radius:6px;}
  .login-error{
    background:var(--red-bg);color:var(--red);font-size:12.5px;padding:8px 10px;
    border-radius:6px;margin-bottom:14px;display:none;
  }
  .hint-box{
    margin-top:18px;padding:10px 12px;background:#F4F0E4;border-radius:8px;
    font-size:11.5px;color:var(--muted);text-align:left;line-height:1.5;
  }

  /* ---------- APP SHELL ---------- */
  #app{display:none;min-height:100vh;}
  .shell{display:flex;min-height:100vh;}
  .sidebar{
    width:220px;background:var(--navy);color:#EAEBEF;
    display:flex;flex-direction:column;flex-shrink:0;
    position:fixed;top:0;bottom:0;left:0;
  }
  .sidebar .brand-row{
    display:flex;align-items:center;gap:10px;padding:20px 18px 16px;
    border-bottom:1px solid rgba(255,255,255,0.08);
  }
  .brand-row .mark{
    width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--gold),var(--gold-dk));
    display:flex;align-items:center;justify-content:center;font-weight:700;color:#241804;font-size:14px;flex-shrink:0;
  }
  .brand-row .name{font-size:15px;font-weight:700;letter-spacing:0.3px;}
  .brand-row .sub{font-size:10.5px;color:#9AA3B8;}
  .nav{flex:1;padding:14px 10px;overflow-y:auto;}
  .nav button{
    width:100%;text-align:left;background:none;border:none;color:#C7CCDA;
    padding:10px 12px;border-radius:8px;font-size:13.5px;font-weight:500;
    display:flex;align-items:center;gap:10px;margin-bottom:2px;
  }
  .nav button .ic{font-size:15px;width:18px;text-align:center;}
  .nav button:hover{background:rgba(255,255,255,0.06);color:#fff;}
  .nav button.active{background:var(--gold);color:#241804;font-weight:700;}
  .nav .section-label{
    font-size:10px;text-transform:uppercase;letter-spacing:0.8px;color:#6F7893;
    padding:14px 12px 6px;
  }
  .sidebar .user-box{
    padding:14px 16px;border-top:1px solid rgba(255,255,255,0.08);
  }
  .user-box .who{font-size:13px;font-weight:600;}
  .user-box .role{font-size:11px;color:#9AA3B8;margin-bottom:8px;}
  .logout-btn{
    width:100%;background:rgba(255,255,255,0.07);color:#EAEBEF;border:none;
    padding:8px;border-radius:7px;font-size:12.5px;font-weight:600;
  }
  .logout-btn:hover{background:rgba(255,255,255,0.14);}

  .main{margin-left:220px;flex:1;padding:26px 32px 60px;min-width:0;}
  .topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:10px;}
  .topbar h2{font-size:21px;margin:0;color:var(--navy);}
  .topbar .date{font-size:12.5px;color:var(--muted);}

  .view{display:none;}
  .view.active{display:block;animation:fade .18s ease;}
  @keyframes fade{from{opacity:0;transform:translateY(4px);}to{opacity:1;transform:translateY(0);}}

  /* cards / grid */
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:24px;}
  .card{background:var(--paper);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow);border:1px solid var(--line);}
  .card .lbl{font-size:11.5px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:0.4px;}
  .card .val{font-size:24px;font-weight:700;color:var(--navy);margin-top:4px;font-family:'Space Grotesk',sans-serif;}
  .card .val.red{color:var(--red);}
  .card .val.green{color:var(--green);}

  .panel{background:var(--paper);border-radius:12px;box-shadow:var(--shadow);border:1px solid var(--line);padding:20px;margin-bottom:20px;}
  .panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:10px;}
  .panel-head h3{margin:0;font-size:15.5px;color:var(--navy);}

  table{width:100%;border-collapse:collapse;font-size:13px;}
  th{
    text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:0.4px;
    color:var(--muted);padding:9px 10px;border-bottom:2px solid var(--line);font-weight:700;
  }
  td{padding:10px 10px;border-bottom:1px solid #F0ECE0;vertical-align:middle;}
  tr:hover td{background:#FBF9F3;}
  .table-wrap{overflow-x:auto;}
  .badge{padding:3px 9px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block;}
  .badge-green{background:var(--green-bg);color:var(--green);}
  .badge-red{background:var(--red-bg);color:var(--red);}
  .badge-gold{background:#FBF0DA;color:var(--gold-dk);}
  .badge-blue{background:#E7F0F6;color:var(--blue);}
  .badge-gray{background:#EDEDEF;color:#666;}

  .toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
  .search-input{
    padding:9px 12px;border:1.5px solid var(--line);border-radius:8px;font-size:13px;min-width:200px;background:#FCFBF8;
  }
  .search-input:focus{outline:none;border-color:var(--gold);}

  /* modal */
  .overlay{
    display:none;position:fixed;inset:0;background:rgba(15,20,32,0.55);
    align-items:center;justify-content:center;z-index:100;padding:20px;
  }
  .overlay.show{display:flex;}
  .modal{
    background:var(--paper);border-radius:14px;padding:24px;max-width:480px;width:100%;
    max-height:88vh;overflow-y:auto;box-shadow:0 30px 70px rgba(0,0,0,0.3);
  }
  .modal h3{margin:0 0 16px;color:var(--navy);font-size:17px;}
  .modal-actions{display:flex;gap:10px;margin-top:18px;justify-content:flex-end;}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}

  /* POS specific */
  .pos-layout{display:grid;grid-template-columns:1.5fr 1fr;gap:18px;align-items:start;}
  @media(max-width:980px){.pos-layout{grid-template-columns:1fr;}}
  .prod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;max-height:520px;overflow-y:auto;padding-right:4px;}
  .prod-tile{
    background:#fff;border:1.5px solid var(--line);border-radius:10px;padding:10px;cursor:pointer;
    transition:border-color .12s, transform .1s; text-align:left;
  }
  .prod-tile:hover{border-color:var(--gold);transform:translateY(-1px);}
  .prod-tile .pname{font-weight:700;font-size:12.5px;color:var(--navy);line-height:1.25;min-height:32px;}
  .prod-tile .pstock{font-size:10.5px;color:var(--muted);margin-top:4px;}
  .prod-tile .pprice{font-size:13.5px;font-weight:700;color:var(--gold-dk);margin-top:6px;}
  .prod-tile.low{border-color:var(--red);}
  .prod-tile.out{opacity:0.45;cursor:not-allowed;}

  .cart-panel{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:16px;position:sticky;top:20px;}
  .cart-item{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #F0ECE0;gap:8px;}
  .cart-item .nm{font-size:12.5px;font-weight:600;flex:1;}
  .cart-item .qty-ctrl{display:flex;align-items:center;gap:6px;}
  .qty-ctrl button{width:22px;height:22px;border-radius:5px;border:1px solid var(--line);background:#fff;font-weight:700;line-height:1;}
  .cart-item .lp{font-size:12.5px;font-weight:700;width:64px;text-align:right;}
  .empty-cart{color:var(--muted);font-size:12.5px;text-align:center;padding:26px 10px;}
  .cart-total-row{display:flex;justify-content:space-between;font-size:16px;font-weight:700;color:var(--navy);padding-top:10px;margin-top:6px;border-top:2px solid var(--line);}

  .tabs{display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap;}
  .tab-btn{padding:7px 14px;border-radius:20px;border:1.5px solid var(--line);background:#fff;font-size:12.5px;font-weight:600;color:var(--muted);}
  .tab-btn.active{background:var(--navy);color:#fff;border-color:var(--navy);}

  .empty-state{text-align:center;padding:34px 20px;color:var(--muted);font-size:13px;}
  .toast{
    position:fixed;bottom:22px;right:22px;background:var(--navy);color:#fff;padding:12px 18px;
    border-radius:9px;font-size:13px;font-weight:600;box-shadow:0 10px 30px rgba(0,0,0,0.25);
    z-index:200;display:none;
  }
  .toast.err{background:var(--red);}
  .small-note{font-size:11.5px;color:var(--muted);margin-top:6px;}
  .divider{height:1px;background:var(--line);margin:16px 0;}
  .credit-flag{font-weight:700;color:var(--red);}
  @media(max-width:760px){
    .sidebar{width:100%;height:auto;position:relative;flex-direction:row;overflow-x:auto;}
    .sidebar .brand-row{display:none;}
    .nav{display:flex;padding:8px;}
    .nav .section-label{display:none;}
    .user-box{display:none;}
    .main{margin-left:0;padding:18px;}
    .nav button span.lbl-txt{display:none;}
  }
</style>
</head>
<body>

<!-- LOGIN -->
<div id="login-screen">
  <div class="login-card">
    <div class="login-logo">JR</div>
    <h1>JR31 SHOP</h1>
    <p class="sub">Punto de venta · Papelería</p>
    <div class="login-error" id="login-error">Usuario o contraseña incorrectos.</div>
    <div class="field">
      <label>Usuario</label>
      <input id="login-user" type="text" placeholder="tu usuario" autocomplete="username">
    </div>
    <div class="field">
      <label>Contraseña</label>
      <input id="login-pass" type="password" placeholder="••••••••" autocomplete="current-password">
    </div>
    <button class="btn btn-primary" onclick="doLogin()">Entrar</button>
    <div class="hint-box" id="hint-box">Cargando…</div>
  </div>
</div>

<!-- APP -->
<div id="app">
  <div class="shell">
    <div class="sidebar">
      <div class="brand-row">
        <div class="mark">JR</div>
        <div>
          <div class="name">JR31 SHOP</div>
          <div class="sub">Papelería</div>
        </div>
      </div>
      <div class="nav" id="nav-buttons"></div>
      <div class="user-box">
        <div class="who" id="who-name">—</div>
        <div class="role" id="who-role">—</div>
        <button class="logout-btn" onclick="logout()">Cerrar sesión</button>
      </div>
    </div>

    <div class="main">
      <!-- DASHBOARD -->
      <div class="view" id="view-dashboard">
        <div class="topbar"><h2>Panel general</h2><div class="date" id="today-date"></div></div>
        <div class="cards" id="dash-cards"></div>
        <div class="panel">
          <div class="panel-head"><h3>Últimas ventas</h3></div>
          <div class="table-wrap"><table id="dash-recent-table"></table></div>
        </div>
      </div>

      <!-- VENTAS (POS) -->
      <div class="view" id="view-ventas">
        <div class="topbar"><h2>Nueva venta</h2><div class="date" id="clock"></div></div>
        <div class="pos-layout">
          <div class="panel">
            <div class="toolbar" style="margin-bottom:14px;">
              <input class="search-input" id="pos-search" placeholder="Buscar producto…" oninput="renderPosProducts()" style="flex:1;">
              <select class="search-input" id="pos-price-tier" onchange="renderPosProducts()">
                <option value="venta_jr">Precio Venta JR</option>
                <option value="bodega_tj">Precio Bodega TJ</option>
              </select>
            </div>
            <div class="prod-grid" id="pos-product-grid"></div>
          </div>
          <div class="cart-panel">
            <h3 style="margin-top:0;font-size:15px;">Carrito</h3>
            <div id="cart-items"></div>
            <div class="cart-total-row"><span>Total</span><span id="cart-total">$0.00</span></div>
            <div class="divider"></div>
            <div class="field">
              <label>Cliente</label>
              <select id="pos-client" class="search-input" style="width:100%;">
                <option value="">Público general</option>
              </select>
            </div>
            <div class="field">
              <label>Forma de pago</label>
              <select id="pos-payment" class="search-input" style="width:100%;" onchange="togglePosCredit()">
                <option value="contado">Contado</option>
                <option value="credito">Crédito (cliente)</option>
              </select>
            </div>
            <div class="field" id="pos-abono-field" style="display:none;">
              <label>Abono inicial (opcional)</label>
              <input type="number" min="0" step="0.01" id="pos-abono" class="search-input" style="width:100%;" placeholder="0.00">
            </div>
            <button class="btn btn-gold" style="width:100%;margin-top:8px;" onclick="finalizeSale()">Cobrar venta</button>
            <button class="btn btn-ghost" style="width:100%;margin-top:8px;" onclick="clearCart()">Vaciar carrito</button>
          </div>
        </div>
      </div>

      <!-- STOCK -->
      <div class="view" id="view-stock">
        <div class="topbar">
          <h2>Inventario / Stock</h2>
          <button class="btn btn-gold btn-sm" id="btn-new-product" onclick="openProductModal()">+ Nuevo producto</button>
        </div>
        <div class="panel">
          <div class="toolbar" style="margin-bottom:14px;">
            <input class="search-input" id="stock-search" placeholder="Buscar por nombre o categoría…" oninput="renderStockTable()" style="flex:1;">
          </div>
          <div class="table-wrap"><table id="stock-table"></table></div>
        </div>
      </div>

      <!-- COMPRAS -->
      <div class="view" id="view-compras">
        <div class="topbar">
          <h2>Compras</h2>
          <button class="btn btn-gold btn-sm" id="btn-new-purchase" onclick="openPurchaseModal()">+ Registrar compra</button>
        </div>
        <div class="panel">
          <div class="table-wrap"><table id="compras-table"></table></div>
        </div>
      </div>

      <!-- CLIENTES -->
      <div class="view" id="view-clientes">
        <div class="topbar">
          <h2>Clientes y créditos</h2>
          <button class="btn btn-gold btn-sm" onclick="openClientModal()">+ Nuevo cliente</button>
        </div>
        <div class="cards" id="clientes-cards"></div>
        <div class="panel">
          <div class="table-wrap"><table id="clientes-table"></table></div>
        </div>
      </div>

      <!-- CONTROL DE VENTAS -->
      <div class="view" id="view-reportes">
        <div class="topbar"><h2>Control de ventas</h2></div>
        <div class="panel">
          <div class="toolbar" style="margin-bottom:14px;">
            <input type="date" class="search-input" id="rep-from">
            <input type="date" class="search-input" id="rep-to">
            <select class="search-input" id="rep-vendedor"><option value="">Todos los vendedores</option></select>
            <button class="btn btn-ghost btn-sm" onclick="renderReportTable()">Filtrar</button>
          </div>
          <div class="cards" id="rep-cards" style="margin-bottom:16px;"></div>
          <div class="table-wrap"><table id="rep-table"></table></div>
        </div>
      </div>

      <!-- USUARIOS -->
      <div class="view" id="view-usuarios">
        <div class="topbar">
          <h2>Usuarios del sistema</h2>
          <button class="btn btn-gold btn-sm" onclick="openUserModal()">+ Nuevo usuario</button>
        </div>
        <div class="panel">
          <div class="table-wrap"><table id="users-table"></table></div>
        </div>
      </div>

    </div>
  </div>
</div>

<!-- MODALS -->
<div class="overlay" id="modal-product"><div class="modal">
  <h3 id="pm-title">Nuevo producto</h3>
  <input type="hidden" id="pm-id">
  <div class="field"><label>Nombre del producto</label><input id="pm-nombre" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Categoría</label><input id="pm-categoria" class="search-input" style="width:100%;" placeholder="Ej. Cuadernos, Escritura, Oficina…"></div>
  <div class="grid2">
    <div class="field"><label>Stock (cantidad)</label><input type="number" id="pm-stock" class="search-input" style="width:100%;"></div>
    <div class="field"><label>Stock mínimo (alerta)</label><input type="number" id="pm-min" class="search-input" style="width:100%;" value="5"></div>
  </div>
  <div class="divider"></div>
  <div class="field"><label>Precio de compra (USA, USD)</label><input type="number" step="0.01" id="pm-usa" class="search-input" style="width:100%;"></div>
  <div class="grid2">
    <div class="field"><label>Precio de venta JR</label><input type="number" step="0.01" id="pm-jr" class="search-input" style="width:100%;"></div>
    <div class="field"><label>Precio aprox. bodega TJ</label><input type="number" step="0.01" id="pm-tj" class="search-input" style="width:100%;"></div>
  </div>
  <div class="modal-actions">
    <button class="btn btn-ghost" onclick="closeModal('modal-product')">Cancelar</button>
    <button class="btn btn-gold" onclick="saveProduct()">Guardar</button>
  </div>
</div></div>

<div class="overlay" id="modal-purchase"><div class="modal">
  <h3>Registrar compra</h3>
  <div class="field"><label>Producto</label>
    <select id="pu-product" class="search-input" style="width:100%;" onchange="purchaseProductChanged()"></select>
  </div>
  <div class="field"><label>Proveedor</label><input id="pu-proveedor" class="search-input" style="width:100%;" placeholder="Opcional"></div>
  <div class="grid2">
    <div class="field"><label>Cantidad</label><input type="number" id="pu-cantidad" class="search-input" style="width:100%;"></div>
    <div class="field"><label>Costo unitario</label><input type="number" step="0.01" id="pu-costo" class="search-input" style="width:100%;"></div>
  </div>
  <p class="small-note">Esto sumará la cantidad al stock del producto seleccionado automáticamente.</p>
  <div class="modal-actions">
    <button class="btn btn-ghost" onclick="closeModal('modal-purchase')">Cancelar</button>
    <button class="btn btn-gold" onclick="savePurchase()">Registrar</button>
  </div>
</div></div>

<div class="overlay" id="modal-client"><div class="modal">
  <h3>Nuevo cliente</h3>
  <div class="field"><label>Nombre completo</label><input id="cl-nombre" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Teléfono</label><input id="cl-telefono" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Límite de crédito (opcional)</label><input type="number" step="0.01" id="cl-limite" class="search-input" style="width:100%;" placeholder="0.00 = sin límite definido"></div>
  <div class="modal-actions">
    <button class="btn btn-ghost" onclick="closeModal('modal-client')">Cancelar</button>
    <button class="btn btn-gold" onclick="saveClient()">Guardar</button>
  </div>
</div></div>

<div class="overlay" id="modal-abono"><div class="modal">
  <h3>Registrar abono</h3>
  <input type="hidden" id="ab-client-id">
  <p id="ab-client-info" class="small-note"></p>
  <div class="field"><label>Monto del abono</label><input type="number" step="0.01" id="ab-monto" class="search-input" style="width:100%;"></div>
  <div class="modal-actions">
    <button class="btn btn-ghost" onclick="closeModal('modal-abono')">Cancelar</button>
    <button class="btn btn-gold" onclick="saveAbono()">Registrar abono</button>
  </div>
</div></div>

<div class="overlay" id="modal-history"><div class="modal" style="max-width:560px;">
  <h3 id="hist-title">Historial de cliente</h3>
  <div class="table-wrap"><table id="hist-table"></table></div>
  <div class="modal-actions"><button class="btn btn-ghost" onclick="closeModal('modal-history')">Cerrar</button></div>
</div></div>

<div class="overlay" id="modal-user"><div class="modal">
  <h3>Nuevo usuario</h3>
  <div class="field"><label>Nombre completo</label><input id="us-nombre" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Usuario (login)</label><input id="us-username" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Contraseña</label><input id="us-password" class="search-input" style="width:100%;"></div>
  <div class="field"><label>Rol</label>
    <select id="us-role" class="search-input" style="width:100%;">
      <option value="vendedor">Vendedor</option>
      <option value="admin">Administrador</option>
    </select>
  </div>
  <div class="modal-actions">
    <button class="btn btn-ghost" onclick="closeModal('modal-user')">Cancelar</button>
    <button class="btn btn-gold" onclick="saveUser()">Crear usuario</button>
  </div>
</div></div>

<div class="toast" id="toast"></div>

<script>
/* ================= STORAGE / DB ================= */
const DB_KEY = 'jr31-shop-db';
let DB = null;
let currentUser = null;
let cart = []; // {id, nombre, precio, cantidad}

function uid(prefix){ return prefix + '_' + Date.now().toString(36) + Math.random().toString(36).slice(2,7); }

function defaultDB(){
  return {
    users: [
      {id: uid('u'), username:'admin', password:'admin123', nombre:'Administrador', role:'admin'},
      {id: uid('u'), username:'vendedor1', password:'vende123', nombre:'Vendedor 1', role:'vendedor'}
    ],
    products: [],
    sales: [],
    purchases: [],
    clients: []
  };
}

async function loadDB(){
  try{
    const res = await window.storage.get(DB_KEY, true);
    DB = JSON.parse(res.value);
  }catch(e){
    DB = defaultDB();
    await saveDB();
  }
}
async function saveDB(){
  try{
    await window.storage.set(DB_KEY, JSON.stringify(DB), true);
  }catch(e){
    showToast('No se pudo guardar. Revisa tu conexión.', true);
  }
}

function showToast(msg, isErr){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast' + (isErr ? ' err' : '');
  t.style.display = 'block';
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(()=> t.style.display='none', 2600);
}
function money(n){ return '$' + (Number(n)||0).toLocaleString('es-MX',{minimumFractionDigits:2, maximumFractionDigits:2}); }
function fmtDate(d){ const dt = new Date(d); return dt.toLocaleDateString('es-MX',{day:'2-digit',month:'short',year:'numeric'}) + ' ' + dt.toLocaleTimeString('es-MX',{hour:'2-digit',minute:'2-digit'}); }
function todayStr(){ return new Date().toISOString().slice(0,10); }

/* ================= AUTH ================= */
async function doLogin(){
  const u = document.getElementById('login-user').value.trim();
  const p = document.getElementById('login-pass').value;
  const err = document.getElementById('login-error');
  const found = DB.users.find(x=>x.username.toLowerCase()===u.toLowerCase() && x.password===p);
  if(!found){
    err.style.display='block';
    return;
  }
  err.style.display='none';
  currentUser = found;
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  buildNav();
  document.getElementById('who-name').textContent = currentUser.nombre;
  document.getElementById('who-role').textContent = currentUser.role==='admin' ? 'Administrador' : 'Vendedor';
  goTo('dashboard');
}
function logout(){
  currentUser = null;
  cart = [];
  document.getElementById('app').style.display='none';
  document.getElementById('login-screen').style.display='flex';
  document.getElementById('login-user').value='';
  document.getElementById('login-pass').value='';
}

/* ================= NAV ================= */
const NAV_ITEMS = [
  {id:'dashboard', label:'Panel', ic:'◆', roles:['admin','vendedor']},
  {id:'ventas', label:'Vender', ic:'🛒', roles:['admin','vendedor']},
  {id:'stock', label:'Inventario', ic:'📦', roles:['admin','vendedor']},
  {id:'compras', label:'Compras', ic:'🧾', roles:['admin']},
  {id:'clientes', label:'Clientes / Créditos', ic:'👤', roles:['admin','vendedor']},
  {id:'reportes', label:'Control de ventas', ic:'📊', roles:['admin']},
  {id:'usuarios', label:'Usuarios', ic:'🔑', roles:['admin']},
];
function buildNav(){
  const nav = document.getElementById('nav-buttons');
  nav.innerHTML='';
  NAV_ITEMS.filter(i=>i.roles.includes(currentUser.role)).forEach(item=>{
    const b = document.createElement('button');
    b.id = 'nav-'+item.id;
    b.innerHTML = `<span class="ic">${item.ic}</span><span class="lbl-txt">${item.label}</span>`;
    b.onclick = ()=>goTo(item.id);
    nav.appendChild(b);
  });
}
function goTo(view){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));
  document.getElementById('view-'+view).classList.add('active');
  const nb = document.getElementById('nav-'+view);
  if(nb) nb.classList.add('active');
  if(view==='dashboard') renderDashboard();
  if(view==='ventas') renderVentasView();
  if(view==='stock') renderStockTable();
  if(view==='compras') renderComprasView();
  if(view==='clientes') renderClientesView();
  if(view==='reportes') renderReportesView();
  if(view==='usuarios') renderUsersTable();
}

/* ================= DASHBOARD ================= */
function renderDashboard(){
  document.getElementById('today-date').textContent = new Date().toLocaleDateString('es-MX',{weekday:'long', day:'numeric', month:'long', year:'numeric'});
  const today = todayStr();
  const ventasHoy = DB.sales.filter(s=>s.fecha.slice(0,10)===today);
  const totalHoy = ventasHoy.reduce((a,s)=>a+s.total,0);
  const stockBajo = DB.products.filter(p=>p.stock <= (p.min||5));
  const porCobrar = DB.clients.reduce((a,c)=>a+c.saldo,0);

  document.getElementById('dash-cards').innerHTML = `
    <div class="card"><div class="lbl">Ventas de hoy</div><div class="val">${money(totalHoy)}</div></div>
    <div class="card"><div class="lbl"># Ventas hoy</div><div class="val">${ventasHoy.length}</div></div>
    <div class="card"><div class="lbl">Stock bajo</div><div class="val ${stockBajo.length?'red':''}">${stockBajo.length}</div></div>
    <div class="card"><div class="lbl">Por cobrar (créditos)</div><div class="val red">${money(porCobrar)}</div></div>
  `;
  const recent = [...DB.sales].sort((a,b)=>new Date(b.fecha)-new Date(a.fecha)).slice(0,8);
  let html = '<tr><th>Fecha</th><th>Vendedor</th><th>Cliente</th><th>Total</th><th>Pago</th></tr>';
  if(recent.length===0) html += '<tr><td colspan="5" style="text-align:center;color:var(--muted);padding:20px;">Aún no hay ventas registradas.</td></tr>';
  recent.forEach(s=>{
    html += `<tr><td>${fmtDate(s.fecha)}</td><td>${s.vendedorNombre}</td><td>${s.clienteNombre||'Público general'}</td><td>${money(s.total)}</td><td>${s.pago==='credito'?'<span class="badge badge-gold">Crédito</span>':'<span class="badge badge-green">Contado</span>'}</td></tr>`;
  });
  document.getElementById('dash-recent-table').innerHTML = html;
}

/* ================= VENTAS / POS ================= */
function renderVentasView(){
  document.getElementById('clock').textContent = new Date().toLocaleString('es-MX');
  const clientSel = document.getElementById('pos-client');
  clientSel.innerHTML = '<option value="">Público general</option>' + DB.clients.map(c=>`<option value="${c.id}">${c.nombre}${c.saldo>0 ? ' (debe '+money(c.saldo)+')':''}</option>`).join('');
  renderPosProducts();
  renderCart();
}
function renderPosProducts(){
  const q = (document.getElementById('pos-search').value||'').toLowerCase();
  const tier = document.getElementById('pos-price-tier').value;
  const grid = document.getElementById('pos-product-grid');
  const list = DB.products.filter(p=> p.nombre.toLowerCase().includes(q) || (p.categoria||'').toLowerCase().includes(q));
  if(list.length===0){ grid.innerHTML = '<div class="empty-state">No se encontraron productos.</div>'; return; }
  grid.innerHTML = list.map(p=>{
    const price = tier==='venta_jr' ? p.precioJR : p.precioTJ;
    const low = p.stock <= (p.min||5);
    const out = p.stock <= 0;
    return `<button class="prod-tile ${low?'low':''} ${out?'out':''}" ${out?'disabled':''} onclick="addToCart('${p.id}','${tier}')">
      <div class="pname">${p.nombre}</div>
      <div class="pstock">${out?'Sin stock':'Stock: '+p.stock}</div>
      <div class="pprice">${money(price)}</div>
    </button>`;
  }).join('');
}
function addToCart(productId, tier){
  const p = DB.products.find(x=>x.id===productId);
  if(!p) return;
  const price = tier==='venta_jr' ? p.precioJR : p.precioTJ;
  const existing = cart.find(c=>c.id===productId && c.tier===tier);
  const inCartQty = cart.filter(c=>c.id===productId).reduce((a,c)=>a+c.cantidad,0);
  if(inCartQty >= p.stock){ showToast('No hay más stock disponible de este producto.', true); return; }
  if(existing){ existing.cantidad++; }
  else cart.push({id:p.id, nombre:p.nombre, precio:price, tier, cantidad:1, stock:p.stock});
  renderCart();
}
function changeQty(idx, delta){
  cart[idx].cantidad += delta;
  if(cart[idx].cantidad <= 0){ cart.splice(idx,1); }
  else{
    const p = DB.products.find(x=>x.id===cart[idx].id);
    if(p && cart[idx].cantidad > p.stock){ cart[idx].cantidad = p.stock; showToast('Alcanzaste el stock disponible.', true); }
  }
  renderCart();
}
function removeFromCart(idx){ cart.splice(idx,1); renderCart(); }
function clearCart(){ cart=[]; renderCart(); }
function renderCart(){
  const wrap = document.getElementById('cart-items');
  if(cart.length===0){ wrap.innerHTML = '<div class="empty-cart">Selecciona productos para agregarlos aquí.</div>'; }
  else{
    wrap.innerHTML = cart.map((c,i)=>`
      <div class="cart-item">
        <div class="nm">${c.nombre}<div style="font-size:10.5px;color:var(--muted);">${money(c.precio)} c/u</div></div>
        <div class="qty-ctrl">
          <button onclick="changeQty(${i},-1)">−</button>
          <span>${c.cantidad}</span>
          <button onclick="changeQty(${i},1)">+</button>
        </div>
        <div class="lp">${money(c.precio*c.cantidad)}</div>
      </div>
    `).join('');
  }
  const total = cart.reduce((a,c)=>a+c.precio*c.cantidad,0);
  document.getElementById('cart-total').textContent = money(total);
}
function togglePosCredit(){
  const isCredit = document.getElementById('pos-payment').value==='credito';
  document.getElementById('pos-abono-field').style.display = isCredit ? 'block' : 'none';
}
async function finalizeSale(){
  if(cart.length===0){ showToast('Agrega productos al carrito primero.', true); return; }
  const clientId = document.getElementById('pos-client').value;
  const payment = document.getElementById('pos-payment').value;
  const total = cart.reduce((a,c)=>a+c.precio*c.cantidad,0);

  if(payment==='credito' && !clientId){
    showToast('Selecciona un cliente para vender a crédito.', true); return;
  }
  let client = clientId ? DB.clients.find(c=>c.id===clientId) : null;
  let abono = 0;
  if(payment==='credito'){
    abono = parseFloat(document.getElementById('pos-abono').value)||0;
    if(abono > total) abono = total;
  }

  // check stock
  for(const c of cart){
    const p = DB.products.find(x=>x.id===c.id);
    if(!p || p.stock < c.cantidad){ showToast('Stock insuficiente para '+c.nombre, true); return; }
  }
  // deduct stock
  cart.forEach(c=>{
    const p = DB.products.find(x=>x.id===c.id);
    p.stock -= c.cantidad;
  });

  const sale = {
    id: uid('v'),
    fecha: new Date().toISOString(),
    vendedorId: currentUser.id,
    vendedorNombre: currentUser.nombre,
    clienteId: client ? client.id : null,
    clienteNombre: client ? client.nombre : null,
    items: cart.map(c=>({productoId:c.id, nombre:c.nombre, cantidad:c.cantidad, precioUnitario:c.precio, subtotal:c.precio*c.cantidad, tier:c.tier})),
    total,
    pago: payment,
    abonoInicial: abono
  };
  DB.sales.push(sale);

  if(payment==='credito' && client){
    const restante = total - abono;
    client.saldo += restante;
    client.historial = client.historial || [];
    client.historial.push({tipo:'venta', fecha: sale.fecha, monto: total, ventaId: sale.id, nota:'Venta a crédito'});
    if(abono>0) client.historial.push({tipo:'abono', fecha: sale.fecha, monto: abono, nota:'Abono al momento de la venta'});
  }

  await saveDB();
  showToast('Venta registrada correctamente ✔');
  clearCart();
  document.getElementById('pos-abono').value='';
  document.getElementById('pos-payment').value='contado';
  togglePosCredit();
  renderVentasView();
}

/* ================= STOCK ================= */
function renderStockTable(){
  const canEdit = currentUser.role==='admin';
  document.getElementById('btn-new-product').style.display = canEdit ? 'inline-block' : 'none';
  const q = (document.getElementById('stock-search').value||'').toLowerCase();
  const list = DB.products.filter(p=>p.nombre.toLowerCase().includes(q) || (p.categoria||'').toLowerCase().includes(q));
  let html = `<tr><th>Producto</th><th>Categoría</th><th>Stock</th><th>Compra USA</th><th>Venta JR</th><th>Bodega TJ</th>${canEdit?'<th>Acciones</th>':''}</tr>`;
  if(list.length===0) html += `<tr><td colspan="7" style="text-align:center;color:var(--muted);padding:24px;">No hay productos aún. ${canEdit?'Agrega el primero con “+ Nuevo producto”.':''}</td></tr>`;
  list.forEach(p=>{
    const low = p.stock <= (p.min||5);
    html += `<tr>
      <td><strong>${p.nombre}</strong></td>
      <td>${p.categoria||'—'}</td>
      <td>${low? '<span class="badge badge-red">'+p.stock+' bajo</span>' : p.stock}</td>
      <td>$${(p.precioUSA||0).toFixed(2)} USD</td>
      <td>${money(p.precioJR)}</td>
      <td>${money(p.precioTJ)}</td>
      ${canEdit ? `<td>
        <button class="btn btn-ghost btn-sm" onclick="openProductModal('${p.id}')">Editar</button>
        <button class="btn btn-danger btn-sm" onclick="deleteProduct('${p.id}')">Eliminar</button>
      </td>` : ''}
    </tr>`;
  });
  document.getElementById('stock-table').innerHTML = html;
}
function openProductModal(id){
  document.getElementById('pm-title').textContent = id ? 'Editar producto' : 'Nuevo producto';
  document.getElementById('pm-id').value = id||'';
  if(id){
    const p = DB.products.find(x=>x.id===id);
    document.getElementById('pm-nombre').value = p.nombre;
    document.getElementById('pm-categoria').value = p.categoria||'';
    document.getElementById('pm-stock').value = p.stock;
    document.getElementById('pm-min').value = p.min||5;
    document.getElementById('pm-usa').value = p.precioUSA||'';
    document.getElementById('pm-jr').value = p.precioJR||'';
    document.getElementById('pm-tj').value = p.precioTJ||'';
  }else{
    ['pm-nombre','pm-categoria','pm-usa','pm-jr','pm-tj'].forEach(id2=>document.getElementById(id2).value='');
    document.getElementById('pm-stock').value=0;
    document.getElementById('pm-min').value=5;
  }
  document.getElementById('modal-product').classList.add('show');
}
async function saveProduct(){
  const id = document.getElementById('pm-id').value;
  const nombre = document.getElementById('pm-nombre').value.trim();
  if(!nombre){ showToast('Escribe el nombre del producto.', true); return; }
  const data = {
    nombre,
    categoria: document.getElementById('pm-categoria').value.trim(),
    stock: parseFloat(document.getElementById('pm-stock').value)||0,
    min: parseFloat(document.getElementById('pm-min').value)||5,
    precioUSA: parseFloat(document.getElementById('pm-usa').value)||0,
    precioJR: parseFloat(document.getElementById('pm-jr').value)||0,
    precioTJ: parseFloat(document.getElementById('pm-tj').value)||0,
  };
  if(id){
    const p = DB.products.find(x=>x.id===id);
    Object.assign(p, data);
  }else{
    DB.products.push({id: uid('p'), ...data});
  }
  await saveDB();
  closeModal('modal-product');
  renderStockTable();
  showToast('Producto guardado ✔');
}
async function deleteProduct(id){
  if(!confirm('¿Eliminar este producto del inventario?')) return;
  DB.products = DB.products.filter(p=>p.id!==id);
  await saveDB();
  renderStockTable();
}

/* ================= COMPRAS ================= */
function renderComprasView(){
  document.getElementById('btn-new-purchase').style.display = currentUser.role==='admin' ? 'inline-block':'none';
  const list = [...DB.purchases].sort((a,b)=>new Date(b.fecha)-new Date(a.fecha));
  let html = '<tr><th>Fecha</th><th>Producto</th><th>Cantidad</th><th>Costo unit.</th><th>Total</th><th>Proveedor</th></tr>';
  if(list.length===0) html += '<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:24px;">No hay compras registradas.</td></tr>';
  list.forEach(c=>{
    html += `<tr><td>${fmtDate(c.fecha)}</td><td>${c.productoNombre}</td><td>${c.cantidad}</td><td>${money(c.costoUnitario)}</td><td>${money(c.total)}</td><td>${c.proveedor||'—'}</td></tr>`;
  });
  document.getElementById('compras-table').innerHTML = html;
}
function openPurchaseModal(){
  const sel = document.getElementById('pu-product');
  sel.innerHTML = DB.products.map(p=>`<option value="${p.id}">${p.nombre}</option>`).join('') || '<option value="">Agrega productos primero</option>';
  document.getElementById('pu-proveedor').value='';
  document.getElementById('pu-cantidad').value='';
  document.getElementById('pu-costo').value='';
  document.getElementById('modal-purchase').classList.add('show');
}
function purchaseProductChanged(){}
async function savePurchase(){
  const prodId = document.getElementById('pu-product').value;
  const cantidad = parseFloat(document.getElementById('pu-cantidad').value)||0;
  const costo = parseFloat(document.getElementById('pu-costo').value)||0;
  if(!prodId || cantidad<=0){ showToast('Selecciona producto y cantidad válida.', true); return; }
  const p = DB.products.find(x=>x.id===prodId);
  p.stock += cantidad;
  DB.purchases.push({
    id: uid('c'),
    fecha: new Date().toISOString(),
    productoId: prodId,
    productoNombre: p.nombre,
    cantidad,
    costoUnitario: costo,
    total: cantidad*costo,
    proveedor: document.getElementById('pu-proveedor').value.trim()
  });
  await saveDB();
  closeModal('modal-purchase');
  renderComprasView();
  showToast('Compra registrada y stock actualizado ✔');
}

/* ================= CLIENTES ================= */
function renderClientesView(){
  const totalDeuda = DB.clients.reduce((a,c)=>a+c.saldo,0);
  const conDeuda = DB.clients.filter(c=>c.saldo>0).length;
  document.getElementById('clientes-cards').innerHTML = `
    <div class="card"><div class="lbl">Clientes registrados</div><div class="val">${DB.clients.length}</div></div>
    <div class="card"><div class="lbl">Con saldo pendiente</div><div class="val red">${conDeuda}</div></div>
    <div class="card"><div class="lbl">Total por cobrar</div><div class="val red">${money(totalDeuda)}</div></div>
  `;
  let html = '<tr><th>Nombre</th><th>Teléfono</th><th>Saldo pendiente</th><th>Acciones</th></tr>';
  if(DB.clients.length===0) html += '<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:24px;">No hay clientes registrados aún.</td></tr>';
  DB.clients.forEach(c=>{
    html += `<tr>
      <td><strong>${c.nombre}</strong></td>
      <td>${c.telefono||'—'}</td>
      <td>${c.saldo>0 ? '<span class="credit-flag">'+money(c.saldo)+'</span>' : money(0)}</td>
      <td>
        <button class="btn btn-ghost btn-sm" onclick="openHistory('${c.id}')">Historial</button>
        <button class="btn btn-gold btn-sm" onclick="openAbonoModal('${c.id}')">Abonar</button>
        <button class="btn btn-danger btn-sm" onclick="deleteClient('${c.id}')">Eliminar</button>
      </td>
    </tr>`;
  });
  document.getElementById('clientes-table').innerHTML = html;
}
function openClientModal(){
  document.getElementById('cl-nombre').value='';
  document.getElementById('cl-telefono').value='';
  document.getElementById('cl-limite').value='';
  document.getElementById('modal-client').classList.add('show');
}
async function saveClient(){
  const nombre = document.getElementById('cl-nombre').value.trim();
  if(!nombre){ showToast('Escribe el nombre del cliente.', true); return; }
  DB.clients.push({
    id: uid('cl'),
    nombre,
    telefono: document.getElementById('cl-telefono').value.trim(),
    limite: parseFloat(document.getElementById('cl-limite').value)||0,
    saldo: 0,
    historial: []
  });
  await saveDB();
  closeModal('modal-client');
  renderClientesView();
  showToast('Cliente agregado ✔');
}
async function deleteClient(id){
  const c = DB.clients.find(x=>x.id===id);
  if(c.saldo>0){ if(!confirm('Este cliente tiene saldo pendiente de '+money(c.saldo)+'. ¿Eliminar de todas formas?')) return; }
  else if(!confirm('¿Eliminar este cliente?')) return;
  DB.clients = DB.clients.filter(x=>x.id!==id);
  await saveDB();
  renderClientesView();
}
function openAbonoModal(clientId){
  const c = DB.clients.find(x=>x.id===clientId);
  document.getElementById('ab-client-id').value = clientId;
  document.getElementById('ab-client-info').textContent = `${c.nombre} — Saldo actual: ${money(c.saldo)}`;
  document.getElementById('ab-monto').value='';
  document.getElementById('modal-abono').classList.add('show');
}
async function saveAbono(){
  const id = document.getElementById('ab-client-id').value;
  const monto = parseFloat(document.getElementById('ab-monto').value)||0;
  if(monto<=0){ showToast('Ingresa un monto válido.', true); return; }
  const c = DB.clients.find(x=>x.id===id);
  c.saldo = Math.max(0, c.saldo - monto);
  c.historial = c.historial || [];
  c.historial.push({tipo:'abono', fecha: new Date().toISOString(), monto, nota:'Abono registrado por '+currentUser.nombre});
  await saveDB();
  closeModal('modal-abono');
  renderClientesView();
  showToast('Abono registrado ✔');
}
function openHistory(clientId){
  const c = DB.clients.find(x=>x.id===clientId);
  document.getElementById('hist-title').textContent = 'Historial — ' + c.nombre;
  const hist = [...(c.historial||[])].sort((a,b)=>new Date(b.fecha)-new Date(a.fecha));
  let html = '<tr><th>Fecha</th><th>Tipo</th><th>Monto</th><th>Nota</th></tr>';
  if(hist.length===0) html += '<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:16px;">Sin movimientos.</td></tr>';
  hist.forEach(h=>{
    html += `<tr><td>${fmtDate(h.fecha)}</td><td>${h.tipo==='venta'?'<span class="badge badge-gold">Venta</span>':'<span class="badge badge-green">Abono</span>'}</td><td>${money(h.monto)}</td><td>${h.nota||''}</td></tr>`;
  });
  document.getElementById('hist-table').innerHTML = html;
  document.getElementById('modal-history').classList.add('show');
}

/* ================= REPORTES ================= */
function renderReportesView(){
  const vSel = document.getElementById('rep-vendedor');
  const vendedores = [...new Set(DB.sales.map(s=>s.vendedorNombre))];
  vSel.innerHTML = '<option value="">Todos los vendedores</option>' + vendedores.map(v=>`<option value="${v}">${v}</option>`).join('');
  document.getElementById('rep-from').value='';
  document.getElementById('rep-to').value='';
  renderReportTable();
}
function renderReportTable(){
  const from = document.getElementById('rep-from').value;
  const to = document.getElementById('rep-to').value;
  const vend = document.getElementById('rep-vendedor').value;
  let list = [...DB.sales];
  if(from) list = list.filter(s=>s.fecha.slice(0,10) >= from);
  if(to) list = list.filter(s=>s.fecha.slice(0,10) <= to);
  if(vend) list = list.filter(s=>s.vendedorNombre === vend);
  list.sort((a,b)=>new Date(b.fecha)-new Date(a.fecha));

  const total = list.reduce((a,s)=>a+s.total,0);
  const contado = list.filter(s=>s.pago==='contado').reduce((a,s)=>a+s.total,0);
  const credito = list.filter(s=>s.pago==='credito').reduce((a,s)=>a+s.total,0);
  document.getElementById('rep-cards').innerHTML = `
    <div class="card"><div class="lbl">Total en periodo</div><div class="val">${money(total)}</div></div>
    <div class="card"><div class="lbl">Ventas de contado</div><div class="val green">${money(contado)}</div></div>
    <div class="card"><div class="lbl">Ventas a crédito</div><div class="val red">${money(credito)}</div></div>
    <div class="card"><div class="lbl"># de ventas</div><div class="val">${list.length}</div></div>
  `;
  let html = '<tr><th>Fecha</th><th>Vendedor</th><th>Cliente</th><th>Artículos</th><th>Total</th><th>Pago</th></tr>';
  if(list.length===0) html += '<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:24px;">Sin ventas en este periodo.</td></tr>';
  list.forEach(s=>{
    html += `<tr><td>${fmtDate(s.fecha)}</td><td>${s.vendedorNombre}</td><td>${s.clienteNombre||'Público general'}</td><td>${s.items.reduce((a,i)=>a+i.cantidad,0)}</td><td>${money(s.total)}</td><td>${s.pago==='credito'?'<span class="badge badge-gold">Crédito</span>':'<span class="badge badge-green">Contado</span>'}</td></tr>`;
  });
  document.getElementById('rep-table').innerHTML = html;
}

/* ================= USUARIOS ================= */
function renderUsersTable(){
  let html = '<tr><th>Nombre</th><th>Usuario</th><th>Rol</th><th>Acciones</th></tr>';
  DB.users.forEach(u=>{
    html += `<tr>
      <td>${u.nombre}</td>
      <td>${u.username}</td>
      <td>${u.role==='admin' ? '<span class="badge badge-blue">Administrador</span>' : '<span class="badge badge-gray">Vendedor</span>'}</td>
      <td><button class="btn btn-danger btn-sm" onclick="deleteUser('${u.id}')">Eliminar</button></td>
    </tr>`;
  });
  document.getElementById('users-table').innerHTML = html;
}
function openUserModal(){
  document.getElementById('us-nombre').value='';
  document.getElementById('us-username').value='';
  document.getElementById('us-password').value='';
  document.getElementById('us-role').value='vendedor';
  document.getElementById('modal-user').classList.add('show');
}
async function saveUser(){
  const nombre = document.getElementById('us-nombre').value.trim();
  const username = document.getElementById('us-username').value.trim();
  const password = document.getElementById('us-password').value;
  const role = document.getElementById('us-role').value;
  if(!nombre || !username || !password){ showToast('Completa todos los campos.', true); return; }
  if(DB.users.some(u=>u.username.toLowerCase()===username.toLowerCase())){ showToast('Ese usuario ya existe.', true); return; }
  DB.users.push({id: uid('u'), nombre, username, password, role});
  await saveDB();
  closeModal('modal-user');
  renderUsersTable();
  showToast('Usuario creado ✔');
}
async function deleteUser(id){
  const admins = DB.users.filter(u=>u.role==='admin');
  const u = DB.users.find(x=>x.id===id);
  if(u.role==='admin' && admins.length<=1){ showToast('No puedes eliminar al único administrador.', true); return; }
  if(u.id===currentUser.id){ showToast('No puedes eliminar tu propio usuario mientras tienes sesión iniciada.', true); return; }
  if(!confirm('¿Eliminar el usuario "'+u.username+'"?')) return;
  DB.users = DB.users.filter(x=>x.id!==id);
  await saveDB();
  renderUsersTable();
}

/* ================= MODAL HELPERS ================= */
function closeModal(id){ document.getElementById(id).classList.remove('show'); }
document.querySelectorAll('.overlay').forEach(ov=>{
  ov.addEventListener('click', (e)=>{ if(e.target===ov) ov.classList.remove('show'); });
});

/* ================= INIT ================= */
(async function init(){
  await loadDB();
  document.getElementById('hint-box').innerHTML =
    'Usuarios de prueba:<br><strong>Admin:</strong> admin / admin123<br><strong>Vendedor:</strong> vendedor1 / vende123<br>Puedes cambiarlos luego desde “Usuarios”.';
})();
</script>
</body>
</html>
