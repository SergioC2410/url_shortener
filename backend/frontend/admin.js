/* =============================================
   CONSTANTES Y CONFIGURACIÓN
   ============================================= */
const API_ENDPOINTS = {
    GET_ALL: "/urls",       // Obtener todas las URLs
    CREATE: "/url",         // Crear nueva URL
    UPDATE: "/urls/{key}",  // Actualizar URL existente
    DELETE: "/urls/{key}"   // Eliminar URL
};

const SORT_OPTIONS = {
    DATE_DESC: "date_desc",     // Más recientes primero
    DATE_ASC: "date_asc",       // Más antiguos primero
    CLICKS_DESC: "clicks_desc", // Más visitados
    CLICKS_ASC: "clicks_asc",   // Menos visitados
    ALPHA_ASC: "alpha_asc"      // Orden alfabético
};

/* =============================================
   ESTADO GLOBAL DE LA APLICACIÓN
   ============================================= */
let appState = {
    urls: [],               // Todos los enlaces cargados
    filteredUrls: [],       // Enlaces filtrados y ordenados
    isEditing: false,       // Modo edición vs creación
    currentEditKey: null,   // Clave del enlace siendo editado
    isLoading: false,       // Estado de carga
    searchTerm: "",         // Término de búsqueda actual
    sortBy: SORT_OPTIONS.DATE_DESC  // Orden actual
};

/* =============================================
   ELEMENTOS DEL DOM (CACHE)
   ============================================= */
const DOM = {
    tableBody: document.getElementById("table-body"),
    searchInput: document.getElementById("searchInput"),
    sortSelect: document.getElementById("sortSelect"),
    modal: document.getElementById("modal"),
    modalTitle: document.getElementById("modal-title"),
    editKeyInput: document.getElementById("edit-key"),
    editUrlInput: document.getElementById("edit-url"),
    editActiveCheckbox: document.getElementById("edit-active"),
    statusGroup: document.getElementById("status-group"),
    saveButton: document.getElementById("btn-save"),
    modalForm: document.getElementById("modal-form")
};

/* =============================================
   FUNCIONES DE UTILIDAD
   ============================================= */

/**
 * Formatea una fecha para mostrar en consola
 */
function formatDate(dateString) {
    if (!dateString) return "Fecha desconocida";
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return dateString;
    }
}

/**
 * Valida si una URL es válida
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Muestra u oculta el indicador de carga
 */
function setLoading(isLoading) {
    appState.isLoading = isLoading;
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.id !== 'btn-save') {
            button.disabled = isLoading;
        }
    });
}

/**
 * Muestra un mensaje de notificación
 */
function showNotification(message, type = 'info') {
    // Crear notificación si no existe
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        document.body.appendChild(notification);
    }

    // Configurar colores según tipo
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };

    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    notification.style.transform = 'translateX(0)';

    // Auto-ocultar después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(120%)';
    }, 3000);
}

/* =============================================
   FUNCIONES DE LA API
   ============================================= */

/**
 * Carga todos los enlaces desde el servidor
 */
async function loadUrls() {
    setLoading(true);
    
    try {
        // Mostrar estado de carga en la tabla
        DOM.tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    <div class="loading-spinner">⏳ Cargando enlaces...</div>
                </td>
            </tr>
        `;

        const response = await fetch(API_ENDPOINTS.GET_ALL);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const data = await response.json();
        appState.urls = data;
        
        // Actualizar la vista
        filterAndSortUrls();
        showNotification(`${data.length} enlaces cargados`, 'success');
        
    } catch (error) {
        console.error('Error al cargar URLs:', error);
        
        // Mostrar error en la tabla
        DOM.tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center error-message">
                    ❌ Error al cargar los datos. 
                    <button onclick="loadUrls()" style="margin-left: 10px; padding: 5px 10px;">
                        Reintentar
                    </button>
                </td>
            </tr>
        `;
        
        showNotification('Error al cargar enlaces', 'error');
        
    } finally {
        setLoading(false);
    }
}

/**
 * Guarda un enlace (crea o actualiza)
 */
async function saveUrl(urlData, isEdit = false) {
    const endpoint = isEdit 
        ? API_ENDPOINTS.UPDATE.replace('{key}', urlData.key)
        : API_ENDPOINTS.CREATE;

    const method = isEdit ? 'PUT' : 'POST';

    try {
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(urlData)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || 'Error en la operación');
        }

        const result = await response.json();
        showNotification(isEdit ? 'Enlace actualizado' : 'Enlace creado', 'success');
        await loadUrls(); // Recargar la lista
        
        return result;
        
    } catch (error) {
        console.error('Error al guardar:', error);
        showNotification(`Error: ${error.message}`, 'error');
        throw error;
    }
}

/**
 * Elimina un enlace
 */
async function deleteUrl(key) {
    if (!key) return;

    try {
        const endpoint = API_ENDPOINTS.DELETE.replace('{key}', key);
        const response = await fetch(endpoint, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Error al eliminar');
        }

        showNotification('Enlace eliminado', 'success');
        await loadUrls(); // Recargar la lista
        
    } catch (error) {
        console.error('Error al eliminar:', error);
        showNotification('Error al eliminar el enlace', 'error');
    }
}

/* =============================================
   FILTRADO Y ORDENAMIENTO
   ============================================= */

/**
 * Filtra y ordena los enlaces según los criterios actuales
 */
function filterAndSortUrls() {
    const { urls, searchTerm, sortBy } = appState;
    
    // 1. Filtrar
    let filtered = urls.filter(url => {
        const searchLower = searchTerm.toLowerCase();
        return url.key.toLowerCase().includes(searchLower) || 
               url.target_url.toLowerCase().includes(searchLower);
    });

    // 2. Ordenar
    filtered.sort((a, b) => {
        switch (sortBy) {
            case SORT_OPTIONS.DATE_ASC:
                // Más antiguos primero (nota: usando fallback de fecha mínima)
                const dateA = new Date(a.created_at || '1970-01-01').getTime();
                const dateB = new Date(b.created_at || '1970-01-01').getTime();
                return dateA - dateB;
                
            case SORT_OPTIONS.DATE_DESC:
                // Más recientes primero
                const dateC = new Date(b.created_at || '1970-01-01').getTime();
                const dateD = new Date(a.created_at || '1970-01-01').getTime();
                return dateC - dateD;
                
            case SORT_OPTIONS.CLICKS_ASC:
                return (a.clicks || 0) - (b.clicks || 0);
                
            case SORT_OPTIONS.CLICKS_DESC:
                return (b.clicks || 0) - (a.clicks || 0);
                
            case SORT_OPTIONS.ALPHA_ASC:
                return (a.key || '').localeCompare(b.key || '');
                
            default:
                return 0;
        }
    });

    appState.filteredUrls = filtered;
    renderTable();
}

/**
 * Aplica filtros (llamado desde eventos)
 */
function applyFilters() {
    appState.searchTerm = DOM.searchInput.value;
    appState.sortBy = DOM.sortSelect.value;
    filterAndSortUrls();
}

/* =============================================
   RENDERIZADO DE LA TABLA
   ============================================= */

/**
 * Renderiza la tabla con los enlaces filtrados
 */
function renderTable() {
    const { filteredUrls } = appState;
    const tableBody = DOM.tableBody;

    if (filteredUrls.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    <div class="empty-state">
                        📭 No se encontraron enlaces
                        ${appState.searchTerm ? ` para "${appState.searchTerm}"` : ''}
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = '';

    filteredUrls.forEach((url, index) => {
        const row = document.createElement('tr');
        
        // Animación escalonada
        row.className = 'animate-row';
        row.style.animationDelay = `${index * 0.03}s`;

        // URL completa (corto)
        const shortUrl = `${window.location.origin}/${url.key}`;

        row.innerHTML = `
            <td>
                <div class="url-key" title="Creado: ${formatDate(url.created_at)}">
                    <strong>${url.key}</strong>
                </div>
            </td>
            <td class="original-url-cell">
                <a href="${url.target_url}" 
                   target="_blank" 
                   rel="noopener noreferrer"
                   title="${url.target_url}">
                    ${truncateText(url.target_url, 50)}
                </a>
            </td>
            <td class="short-url-cell">
                <a href="${shortUrl}" 
                   target="_blank" 
                   rel="noopener noreferrer"
                   title="${shortUrl}"
                   onclick="copyToClipboard('${shortUrl}', event)">
                    ${shortUrl.replace(/^https?:\/\//, '')}
                </a>
                <button class="copy-btn" onclick="copyToClipboard('${shortUrl}')" title="Copiar">
                    📋
                </button>
            </td>
            <td class="clicks-cell" title="Total de visitas">
                <span class="clicks-count">${url.clicks || 0}</span>
            </td>
            <td class="status-cell">
                <span class="status-badge ${url.is_active ? 'status-active' : 'status-inactive'}">
                    ${url.is_active ? '✅ Activo' : '⛔ Inactivo'}
                </span>
            </td>
            <td class="actions-cell">
                <div class="action-buttons">
                    <button class="action-btn btn-edit" 
                            onclick="prepareEdit('${url.key}')"
                            title="Editar enlace">
                        ✏️
                    </button>
                    <button class="action-btn btn-delete" 
                            onclick="confirmDelete('${url.key}')"
                            title="Eliminar enlace">
                        🗑️
                    </button>
                </div>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

/**
 * Trunca texto muy largo
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Copia texto al portapapeles
 */
function copyToClipboard(text, event = null) {
    if (event) event.preventDefault();
    
    navigator.clipboard.writeText(text)
        .then(() => showNotification('Enlace copiado al portapapeles', 'success'))
        .catch(err => {
            console.error('Error al copiar:', err);
            showNotification('Error al copiar', 'error');
        });
}

/* =============================================
   GESTIÓN DEL MODAL
   ============================================= */

/**
 * Abre el modal en modo creación
 */
function openCreateModal() {
    appState.isEditing = false;
    appState.currentEditKey = null;
    
    DOM.modalTitle.textContent = 'Crear Nuevo Enlace';
    DOM.editKeyInput.value = '';
    DOM.editUrlInput.value = '';
    DOM.editActiveCheckbox.checked = true;
    DOM.statusGroup.style.display = 'none'; // Ocultar estado al crear
    
    // Resetear validación
    DOM.editUrlInput.classList.remove('invalid');
    DOM.modal.showModal();
    DOM.editUrlInput.focus();
}

/**
 * Prepara el modal para editar un enlace
 */
function prepareEdit(key) {
    const url = appState.urls.find(u => u.key === key);
    if (!url) return;

    appState.isEditing = true;
    appState.currentEditKey = key;
    
    DOM.modalTitle.textContent = `Editar: ${key}`;
    DOM.editKeyInput.value = key;
    DOM.editUrlInput.value = url.target_url;
    DOM.editActiveCheckbox.checked = url.is_active !== false; // Default true
    DOM.statusGroup.style.display = 'block'; // Mostrar estado al editar
    
    DOM.modal.showModal();
    DOM.editUrlInput.focus();
}

/**
 * Cierra el modal
 */
function closeModal() {
    DOM.modal.close();
    DOM.modalForm.reset();
}

/**
 * Guarda los cambios (crea o edita)
 */
async function saveChanges() {
    const url = DOM.editUrlInput.value.trim();
    const isActive = DOM.editActiveCheckbox.checked;
    const isEditing = appState.isEditing;
    const key = appState.currentEditKey;

    // Validaciones
    if (!url) {
        DOM.editUrlInput.classList.add('invalid');
        showNotification('Por favor, ingresa una URL', 'warning');
        DOM.editUrlInput.focus();
        return;
    }

    if (!isValidUrl(url)) {
        DOM.editUrlInput.classList.add('invalid');
        showNotification('URL inválida. Asegúrate de incluir http:// o https://', 'warning');
        DOM.editUrlInput.focus();
        return;
    }

    // Preparar datos
    const urlData = {
        target_url: url
    };

    if (isEditing) {
        urlData.key = key;
        urlData.is_active = isActive;
    }

    // Mostrar estado de guardado
    DOM.saveButton.disabled = true;
    DOM.saveButton.innerHTML = '<span class="spinner"></span> Guardando...';

    try {
        await saveUrl(urlData, isEditing);
        closeModal();
    } catch (error) {
        // El error ya fue manejado en saveUrl
    } finally {
        DOM.saveButton.disabled = false;
        DOM.saveButton.textContent = 'Guardar';
    }
}

/* =============================================
   CONFIRMACIÓN DE ELIMINACIÓN
   ============================================= */

/**
 * Muestra confirmación antes de eliminar
 */
function confirmDelete(key) {
    const url = appState.urls.find(u => u.key === key);
    if (!url) return;

    // Crear modal de confirmación personalizado
    const modal = document.createElement('dialog');
    modal.className = 'confirm-modal';
    modal.innerHTML = `
        <div class="confirm-content">
            <h3>¿Eliminar enlace?</h3>
            <p>Código: <strong>${key}</strong></p>
            <p>URL: ${truncateText(url.target_url, 60)}</p>
            <p>Visitas: ${url.clicks || 0}</p>
            <p class="warning-text">⚠️ Esta acción no se puede deshacer.</p>
            <div class="confirm-actions">
                <button class="btn-cancel" onclick="this.closest('dialog').close()">Cancelar</button>
                <button class="btn-danger" onclick="executeDelete('${key}')">Eliminar</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.showModal();

    // Remover el modal después de cerrar
    modal.addEventListener('close', () => {
        modal.remove();
    });
}

/**
 * Ejecuta la eliminación después de confirmar
 */
function executeDelete(key) {
    document.querySelector('.confirm-modal')?.close();
    deleteUrl(key);
}

/* =============================================
   INICIALIZACIÓN Y EVENT LISTENERS
   ============================================= */

/**
 * Inicializa la aplicación
 */
function initApp() {
    // Configurar event listeners
    DOM.searchInput.addEventListener('input', debounce(applyFilters, 300));
    DOM.sortSelect.addEventListener('change', applyFilters);
    
    // Eventos del modal
    DOM.modal.addEventListener('click', (event) => {
        if (event.target === DOM.modal) {
            closeModal();
        }
    });

    DOM.modal.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    });

    // Evento del formulario
    DOM.modalForm.addEventListener('submit', (event) => {
        event.preventDefault();
        saveChanges();
    });

    // Validación en tiempo real
    DOM.editUrlInput.addEventListener('input', () => {
        DOM.editUrlInput.classList.remove('invalid');
    });

    // Cargar datos iniciales
    loadUrls();
}

/**
 * Debounce para optimizar eventos frecuentes
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* =============================================
   EXPOSICIÓN GLOBAL DE FUNCIONES
   ============================================= */
// Solo exponer las funciones necesarias para eventos HTML
window.abrirModalCrear = openCreateModal;
window.aplicarFiltros = applyFilters;
window.cerrarModal = closeModal;
window.guardarCambios = saveChanges;
window.prepararEdicion = prepareEdit;
window.eliminarUrl = confirmDelete;
window.copyToClipboard = copyToClipboard;

/* =============================================
   INICIALIZAR AL CARGAR EL DOM
   ============================================= */
document.addEventListener('DOMContentLoaded', initApp);