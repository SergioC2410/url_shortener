// Usamos ruta relativa "/url".
// - En local será: http://localhost:8000/url
// - En Render será: https://shorty.com/url
const API_URL = "/url";

async function acortarUrl() {
    const input = document.getElementById("longUrl");
    const resultArea = document.getElementById("result-area");
    const shortLink = document.getElementById("shortLink");
    const btnText = document.getElementById("btn-text");
    const loader = document.getElementById("btn-loader");

    // Limpieza inicial UI
    resultArea.style.display = "none";
    
    // Validación básica
    if (!input.value.trim()) {
        showToast("Por favor, escribe una URL primero.", "error");
        input.focus();
        return;
    }

    // Activar estado de carga
    btnText.style.display = "none";
    loader.style.display = "block";

    try {
        // Petición al Backend
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target_url: input.value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Ocurrió un error desconocido");
        }

        // --- AQUÍ ESTÁ LA MAGIA ---
        // Usamos la URL que el backend calculó (sea localhost o dominio real)
        const fullShortUrl = data.url_completa;
        
        shortLink.href = fullShortUrl;
        shortLink.innerText = fullShortUrl;
        
        resultArea.style.display = "block";
        showToast("¡Enlace acortado con éxito!", "success");
        input.value = ""; 

    } catch (err) {
        console.error(err);
        showToast(err.message, "error");
    } finally {
        // Restaurar botón
        btnText.style.display = "block";
        loader.style.display = "none";
    }
}

function showToast(message, type) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? '✅' : '🚫';
    
    // Usamos template literals para insertar HTML
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-msg">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3500); 
}

function copiarAlPortapapeles() {
    const url = document.getElementById("shortLink").innerText;
    navigator.clipboard.writeText(url).then(() => {
        showToast("URL copiada al portapapeles", "success");
    }).catch(err => {
        showToast("No se pudo copiar", "error");
    });
}