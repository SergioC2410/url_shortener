const API_URL = "http://localhost:8000/urls";

async function cargarDatos() {
    const tableBody = document.getElementById("table-body");
    
    try {
        // 1. Pedimos los datos al Backend (que ya lee la base de datos)
        const response = await fetch(API_URL);
        const urls = await response.json();

        // 2. Limpiamos la tabla por si acaso
        tableBody.innerHTML = "";

        // 3. Rellenamos la tabla
        urls.forEach(url => {
            const row = document.createElement("tr");
            
            // Formatear fecha (opcional, si el backend la envía)
            // const fecha = new Date(url.created_at).toLocaleDateString();

            row.innerHTML = `
                <td>
                    <div style="font-weight:600;">${url.key}</div>
                </td>
                <td class="link-cell" style="max-width: 300px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                    <a href="${url.target_url}" target="_blank" title="${url.target_url}">${url.target_url}</a>
                </td>
                <td class="link-cell">
                    <a href="${url.url_completa}" target="_blank">${url.url_completa}</a>
                </td>
                <td class="clicks-cell">${url.clicks} 🖱️</td>
                <td style="text-align:center;">
                    <span class="status-badge ${url.is_active ? 'status-active' : 'status-inactive'}">
                        ${url.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Error cargando datos:", error);
        tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Error cargando datos. Asegúrate de que el Backend esté corriendo.</td></tr>`;
    }
}

// Cargar datos apenas entremos a la página
document.addEventListener("DOMContentLoaded", cargarDatos);