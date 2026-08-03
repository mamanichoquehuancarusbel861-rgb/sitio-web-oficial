// CONFIGURACIÓN DE LA API FLASK
const API_BASE = 'http://127.0.0.1:5000/api';

let currentModule = 'productos';
let editingId = null;

// BANCO DE IMÁGENES / RUTAS (Reemplaza estas URLs con las rutas de tus propias imágenes localmente o URLs)
const DEMO_IMAGES = {
  productos: [
   'img/productos/producto1.jpg',
    'img/productos/producto2.jpg',
    'img/productos/producto3.jpg',
    'img/productos/producto4.jpg',
    'img/productos/producto5.jpg',
    'img/productos/producto6.jpg',
    'img/productos/producto7.jpg',
    'img/productos/producto8.jpg',
    'img/productos/producto9.jpg',
    'img/productos/producto10.jpg',
    'img/productos/producto11.jpg',
    'img/productos/producto12.jpg',
    'img/productos/producto13.jpg',
    'img/productos/producto14.jpg',
    'img/productos/producto15.jpg'
  ],
  empleados: [
    'img/empleados/empleado1.jpg',
    'img/empleados/empleado2.jpg',
    'img/empleados/empleado3.jpg',
    'img/empleados/empleado4.jpg',
    'img/empleados/empleado5.jpg'
  ],
  avatars: {
    mujer: 'https://cdn-icons-png.flaticon.com/512/4140/4140047.png',
    hombre: 'https://cdn-icons-png.flaticon.com/512/4140/4140061.png'
  }
};

// FUNCIÓN PARA OBTENER AVATAR SEGÚN EL NOMBRE DEL CLIENTE (MUJER / HOMBRE)
function obtenerAvatarPorNombre(nombreCompleto = '') {
  if (!nombreCompleto) return DEMO_IMAGES.avatars.hombre;

  const primerNombre = nombreCompleto.trim().split(' ')[0].toLowerCase();
  
  // Lista común de nombres femeninos y regla de terminación en 'a'
  const nombresFemeninos = [
    'maria', 'maría', 'ana', 'lucia', 'lucía', 'carmen', 'laura', 'sofia', 'sofía', 
    'elena', 'patricia', 'martha', 'marta', 'rosa', 'andrea', 'diana', 'paula', 
    'claudia', 'monica', 'mónica', 'beatriz', 'vanessa', 'jessica', 'gabriela', 
    'carla', 'valeria', 'camila', 'daniela', 'fernanda', 'luisa', 'guadalupe'
  ];

  const esMujer = nombresFemeninos.includes(primerNombre) || 
                  (primerNombre.endsWith('a') && !['joshua', 'luca', 'sasha'].includes(primerNombre));

  return esMujer ? DEMO_IMAGES.avatars.mujer : DEMO_IMAGES.avatars.hombre;
}

// ESQUEMA DE CADA MÓDULO (Estructura, campos y renderizado)
const MODULE_CONFIG = {
  productos: {
    title: 'Gestión de Productos',
    endpoint: '/productos',
    idField: 'id_producto',
    columns: ['Producto', 'Marca', 'P. Compra', 'P. Venta', 'Stock', 'id_categoria', 'id_proveedor', 'Acciones'],
    renderRow: (item, idx) => {
      // Usa item.imagen si existe en la API, o tus propias imágenes por defecto
      const imgProducto = item.imagen || DEMO_IMAGES.productos[idx % DEMO_IMAGES.productos.length] || DEMO_IMAGES.productos[0];

      return `
        <td>
          <div class="tbl-user-cell">
            <span class="img-number">${idx + 1}.</span>
            <img src="${imgProducto}" class="tbl-img" alt="Producto" ondblclick="openImageModal(this.src)">
            <div>
              <strong>${item.nombre || 'Producto sin nombre'}</strong>
              <div style="font-size:0.75rem; color:var(--text-muted);">${item.codigo || '#PROD'}</div>
            </div>
          </div>
        </td>
        <td><span class="badge-pill">${item.marca || 'Genérico'}</span></td>
        <td>S/ ${parseFloat(item.precio_compra || 0).toFixed(2)}</td>
        <td style="color:var(--accent-green); font-weight:600;">S/ ${parseFloat(item.precio_venta || item.precio || 0).toFixed(2)}</td>
        <td><strong>${item.stock || 0}</strong> und</td>
      `;
    },
    formHTML: (data = {}) => `
      <div class="form-group"><label>Código:</label><input type="text" id="inp_codigo" value="${data.codigo || ''}" required></div>
      <div class="form-group"><label>Nombre del Producto:</label><input type="text" id="inp_nombre" value="${data.nombre || ''}" required></div>
      <div class="form-group"><label>Marca:</label><input type="text" id="inp_marca" value="${data.marca || ''}"></div>
      <div class="form-group"><label>Precio Compra (S/):</label><input type="number" step="0.01" id="inp_pcompra" value="${data.precio_compra || ''}"></div>
      <div class="form-group"><label>Precio Venta (S/):</label><input type="number" step="0.01" id="inp_pventa" value="${data.precio_venta || data.precio || ''}"></div>
      <div class="form-group"><label>Stock:</label><input type="number" id="inp_stock" value="${data.stock || 10}"></div>
    `,
    getFormData: () => ({
      codigo: document.getElementById('inp_codigo').value,
      nombre: document.getElementById('inp_nombre').value,
      marca: document.getElementById('inp_marca').value,
      precio_compra: parseFloat(document.getElementById('inp_pcompra').value) || 0,
      precio_venta: parseFloat(document.getElementById('inp_pventa').value) || 0,
      stock: parseInt(document.getElementById('inp_stock').value) || 0
    })
  },

  clientes: {
    title: 'Gestión de Clientes',
    endpoint: '/clientes',
    idField: 'id_cliente',
    columns: ['Cliente', 'DNI / RUC', 'Teléfono', 'Dirección', 'Acciones'],
    renderRow: (item, idx) => {
      const nombreCompleto = `${item.nombres || item.nombre || ''} ${item.apellidos || ''}`;
      // Genera avatar de mujer u hombre según el nombre
      const avatarCliente = obtenerAvatarPorNombre(item.nombres || item.nombre);

      return `
        <td>
          <div class="tbl-user-cell">
            <span class="img-number">${idx + 1}.</span>
            <img src="${avatarCliente}" class="tbl-img" alt="Avatar Cliente" ondblclick="openImageModal(this.src)">
            <div>
              <strong>${nombreCompleto}</strong>
            </div>
          </div>
        </td>
        <td>${item.dni || item.ruc || '-'}</td>
        <td>${item.telefono || '-'}</td>
        <td>${item.direccion || 'Sin dirección'}</td>
      `;
    },
    formHTML: (data = {}) => `
      <div class="form-group"><label>Nombres:</label><input type="text" id="inp_nom" value="${data.nombres || ''}" required></div>
      <div class="form-group"><label>Apellidos / Razón Social:</label><input type="text" id="inp_ape" value="${data.apellidos || ''}"></div>
      <div class="form-group"><label>DNI o RUC:</label><input type="text" id="inp_doc" value="${data.dni || ''}"></div>
      <div class="form-group"><label>Teléfono:</label><input type="text" id="inp_tel" value="${data.telefono || ''}"></div>
    `,
    getFormData: () => ({
      nombres: document.getElementById('inp_nom').value,
      apellidos: document.getElementById('inp_ape').value,
      dni: document.getElementById('inp_doc').value,
      telefono: document.getElementById('inp_tel').value
    })
  },

  categorias: {
    title: 'Categorías de Productos',
    endpoint: '/categorias',
    idField: 'id_categoria',
    columns: ['ID', 'Categoría', 'Descripción', 'Acciones'],
    renderRow: (item) => `
      <td><strong>#${item.id_categoria || item.id}</strong></td>
      <td><span class="badge-pill">${item.nombre}</span></td>
      <td>${item.descripcion || 'Sin descripción'}</td>
    `,
    formHTML: (data = {}) => `
      <div class="form-group"><label>Nombre Categoría:</label><input type="text" id="inp_cat_nom" value="${data.nombre || ''}" required></div>
      <div class="form-group"><label>Descripción:</label><input type="text" id="inp_cat_desc" value="${data.descripcion || ''}"></div>
    `,
    getFormData: () => ({
      nombre: document.getElementById('inp_cat_nom').value,
      descripcion: document.getElementById('inp_cat_desc').value
    })
  },

  proveedores: {
    title: 'Proveedores Registrados',
    endpoint: '/proveedores',
    idField: 'id_proveedor',
    columns: ['ID', 'Razón Social', 'RUC', 'Contacto', 'Acciones'],
    renderRow: (item) => `
      <td><strong>#${item.id_proveedor || item.id}</strong></td>
      <td><strong>${item.razon_social || item.nombre}</strong></td>
      <td>${item.ruc || '-'}</td>
      <td>${item.telefono || item.contacto || '-'}</td>
    `,
    formHTML: (data = {}) => `
      <div class="form-group"><label>Razón Social:</label><input type="text" id="inp_prov_rs" value="${data.razon_social || ''}" required></div>
      <div class="form-group"><label>RUC:</label><input type="text" id="inp_prov_ruc" value="${data.ruc || ''}"></div>
      <div class="form-group"><label>Teléfono:</label><input type="text" id="inp_prov_tel" value="${data.telefono || ''}"></div>
    `,
    getFormData: () => ({
      razon_social: document.getElementById('inp_prov_rs').value,
      ruc: document.getElementById('inp_prov_ruc').value,
      telefono: document.getElementById('inp_prov_tel').value
    })
  },

  empleados: {
    title: 'Personal / Empleados',
    endpoint: '/empleados',
    idField: 'id_empleado',
    columns: ['Empleado', 'Cargo', 'DNI', 'Acciones'],
    renderRow: (item, idx) => {
      // Usa item.imagen si existe en la API, o tus propias imágenes de empleados por defecto
      const imgEmpleado = item.imagen || DEMO_IMAGES.empleados[idx % DEMO_IMAGES.empleados.length] || DEMO_IMAGES.empleados[0];

      return `
        <td>
          <div class="tbl-user-cell">
            <span class="img-number">${idx + 1}.</span>
            <img src="${imgEmpleado}" class="tbl-img" alt="Empleado" ondblclick="openImageModal(this.src)">
            <strong>${item.nombres || item.nombre} ${item.apellidos || ''}</strong>
          </div>
        </td>
        <td><span class="badge-pill">${item.cargo || 'Personal'}</span></td>
        <td>${item.dni || '-'}</td>
      `;
    },
    formHTML: (data = {}) => `
      <div class="form-group"><label>Nombres:</label><input type="text" id="inp_emp_nom" value="${data.nombres || ''}" required></div>
      <div class="form-group"><label>Cargo:</label><input type="text" id="inp_emp_cargo" value="${data.cargo || ''}"></div>
      <div class="form-group"><label>DNI:</label><input type="text" id="inp_emp_dni" value="${data.dni || ''}"></div>
    `,
    getFormData: () => ({
      nombres: document.getElementById('inp_emp_nom').value,
      cargo: document.getElementById('inp_emp_cargo').value,
      dni: document.getElementById('inp_emp_dni').value
    })
  },

  ventas: {
    title: 'Historial de Ventas',
    endpoint: '/ventas',
    idField: 'id_venta',
    columns: ['ID Venta', 'Fecha', 'Cliente ID', 'Monto Total', 'Acciones'],
    renderRow: (item) => `
      <td><strong>Venta #${item.id_venta || item.id}</strong></td>
      <td>${item.fecha || 'Hoy'}</td>
      <td>Cliente #${item.id_cliente || 1}</td>
      <td style="color:var(--accent-green); font-weight:600;">S/ ${parseFloat(item.total || 0).toFixed(2)}</td>
    `,
    formHTML: (data = {}) => `
      <div class="form-group"><label>ID Cliente:</label><input type="number" id="inp_vta_cli" value="${data.id_cliente || 1}"></div>
      <div class="form-group"><label>Total (S/):</label><input type="number" step="0.01" id="inp_vta_tot" value="${data.total || 0}"></div>
    `,
    getFormData: () => ({
      id_cliente: parseInt(document.getElementById('inp_vta_cli').value),
      total: parseFloat(document.getElementById('inp_vta_tot').value)
    })
  },

  detalle_ventas: {
    title: 'Detalle de Ventas',
    endpoint: '/detalle_ventas',
    idField: 'id_detalle',
    columns: ['ID Detalle', 'Venta ID', 'Producto ID', 'Cantidad', 'Subtotal', 'Acciones'],
    renderRow: (item) => {
        const idDet = item.id_detalle || item.id || 'N/A';
        const idVta = item.id_venta || '-';
        const idProd = item.id_producto || '-';
        const cant = item.cantidad || 1;
        const sub = item.subtotal || (cant * (item.precio || 10));

        return `
            <td><strong>#${idDet}</strong></td>
            <td>Venta #${idVta}</td>
            <td>Producto #${idProd}</td>
            <td><strong>${cant}</strong> und</td>
            <td style="color:var(--accent-green); font-weight:600;">S/ ${parseFloat(sub).toFixed(2)}</td>
        `;
    },
    formHTML: (data = {}) => `
      <div class="form-group"><label>ID Venta:</label><input type="number" id="inp_det_vta" value="${data.id_venta || 1}" required></div>
      <div class="form-group"><label>ID Producto:</label><input type="number" id="inp_det_prod" value="${data.id_producto || 1}" required></div>
      <div class="form-group"><label>Cantidad:</label><input type="number" id="inp_det_cant" value="${data.cantidad || 1}" required></div>
      <div class="form-group"><label>Subtotal (S/):</label><input type="number" step="0.01" id="inp_det_sub" value="${data.subtotal || 10.00}"></div>
    `,
    getFormData: () => ({
      id_venta: parseInt(document.getElementById('inp_det_vta').value),
      id_producto: parseInt(document.getElementById('inp_det_prod').value),
      cantidad: parseInt(document.getElementById('inp_det_cant').value),
      subtotal: parseFloat(document.getElementById('inp_det_sub').value)
    })
  }
};

// INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', () => {
  loadModule(currentModule);
});

// CAMBIAR PESTAÑA / MÓDULO
function switchCollection(moduleName, btnElement) {
  currentModule = moduleName;
  document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
  btnElement.classList.add('active');
  loadModule(moduleName);
}

// 🟢 FUNCION DE NOTIFICACION DE EXITO / ERROR
function showNotification(message, type = 'success') {
  const toast = document.getElementById('toast-notification');
  const msgEl = document.getElementById('toast-message');
  const iconEl = document.getElementById('toast-icon');

  if (type === 'success') {
    toast.style.borderColor = 'rgba(16, 185, 129, 0.4)';
    toast.style.background = 'rgba(16, 185, 129, 0.15)';
    iconEl.innerHTML = '✔';
    iconEl.style.color = '#10b981';
  } else if (type === 'error') {
    toast.style.borderColor = 'rgba(239, 68, 68, 0.4)';
    toast.style.background = 'rgba(239, 68, 68, 0.15)';
    iconEl.innerHTML = '✖';
    iconEl.style.color = '#ef4444';
  } else {
    toast.style.borderColor = 'rgba(59, 130, 246, 0.4)';
    toast.style.background = 'rgba(59, 130, 246, 0.15)';
    iconEl.innerHTML = 'ℹ';
    iconEl.style.color = '#3b82f6';
  }

  msgEl.innerText = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// 🔄 FUNCION PARA ACTUALIZAR DATOS MANUALMENTE O AUTOMÁTICAMENTE
async function refreshData() {
  await loadModule(currentModule);
  showNotification('Datos actualizados exitosamente.', 'info');
}

// CARGAR DATOS DESDE LA API FLASK
async function loadModule(moduleName) {
  const config = MODULE_CONFIG[moduleName];
  document.getElementById('view-title').innerText = config.title;
  document.getElementById('kpi-active-module').innerText = config.title.replace('Gestión de ', '');
  
  // Renderizar cabecera de la tabla
  const theadRow = document.getElementById('table-head-row');
  theadRow.innerHTML = config.columns.map(col => `<th>${col}</th>`).join('');

  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:30px; color:var(--text-muted);">Cargando datos...</td></tr>';

  try {
    const res = await fetch(`${API_BASE}${config.endpoint}`);
    if (!res.ok) throw new Error('Error al conectar');
    
    const data = await res.json();
    document.getElementById('kpi-count').innerText = data.length;

    if (data.length === 0) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:30px; color:var(--text-muted);">No hay registros encontrados. ¡Añade uno nuevo!</td></tr>';
      return;
    }

    tbody.innerHTML = data.map((item, index) => {
      const itemId = item[config.idField] || item.id;
      return `
        <tr>
          ${config.renderRow(item, index)}
          <td>
            <div class="action-group">
              <button class="btn-icon btn-edit" onclick="openModalForEdit(${itemId})">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button class="btn-icon btn-delete" onclick="deleteRecord(${itemId})">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');

  } catch (err) {
    console.error(err);
    tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding:30px; color:var(--accent-red);">Error al conectar con la API en 127.0.0.1:5000</td></tr>`;
  }
}

// VISUALIZADOR DE IMAGEN EN TAMAÑO GRANDE
function openImageModal(src) {
  const highResSrc = src.replace('w=100', 'w=800');
  document.getElementById('modal-img-preview').src = highResSrc;
  document.getElementById('image-modal').classList.add('active');
}

function closeImageModal() {
  document.getElementById('image-modal').classList.remove('active');
}

// CONTROL DE MODAL (NUEVO / EDITAR)
function openModal() {
  editingId = null;
  const config = MODULE_CONFIG[currentModule];
  document.getElementById('modal-title').innerText = `Nuevo en ${config.title}`;
  document.getElementById('modal-method-tag').innerText = 'POST';
  document.getElementById('modal-method-tag').style.background = 'rgba(16, 185, 129, 0.2)';
  document.getElementById('form-fields').innerHTML = config.formHTML();
  document.getElementById('form-modal').classList.add('active');
}

async function openModalForEdit(id) {
  editingId = id;
  const config = MODULE_CONFIG[currentModule];
  document.getElementById('modal-title').innerText = `Editar ID #${id}`;
  document.getElementById('modal-method-tag').innerText = 'PUT';
  document.getElementById('modal-method-tag').style.background = 'rgba(249, 115, 22, 0.2)';

  try {
    const res = await fetch(`${API_BASE}${config.endpoint}/${id}`);
    const data = await res.json();
    document.getElementById('form-fields').innerHTML = config.formHTML(data);
    document.getElementById('form-modal').classList.add('active');
  } catch (e) {
    showNotification('No se pudo obtener el registro para editar.', 'error');
  }
}

function closeModal() {
  document.getElementById('form-modal').classList.remove('active');
}

// GUARDAR / ACTUALIZAR (POST & PUT CON NOTIFICACIÓN DE ÉXITO)
async function handleFormSubmit(event) {
  event.preventDefault();
  const config = MODULE_CONFIG[currentModule];
  const payload = config.getFormData();

  const url = editingId ? `${API_BASE}${config.endpoint}/${editingId}` : `${API_BASE}${config.endpoint}`;
  const method = editingId ? 'PUT' : 'POST';

  try {
    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      closeModal();
      await loadModule(currentModule);
      
      // Muestra la notificación correspondiente
      if (editingId) {
        showNotification('Se editó exitosamente.', 'success');
      } else {
        showNotification('Se agregó exitosamente.', 'success');
      }
    } else {
      showNotification('Ocurrió un problema al guardar el registro.', 'error');
    }
  } catch (e) {
    showNotification('Error al comunicar con la API Flask.', 'error');
  }
}

// ELIMINAR (DELETE CON NOTIFICACIÓN DE ÉXITO)
async function deleteRecord(id) {
  if (!confirm(`¿Estás seguro de eliminar el registro #${id}?`)) return;
  const config = MODULE_CONFIG[currentModule];

  try {
    const res = await fetch(`${API_BASE}${config.endpoint}/${id}`, { method: 'DELETE' });
    if (res.ok) {
      await loadModule(currentModule);
      showNotification('Se eliminó exitosamente.', 'success');
    } else {
      showNotification('No se pudo eliminar el registro.', 'error');
    }
  } catch (e) {
    showNotification('Error al conectar con la API.', 'error');
  }
}