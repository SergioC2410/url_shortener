# 🔗 Shorty | Premium URL Shortener

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-009688)
![Status](https://img.shields.io/badge/Status-Deployed-success)
![Render](https://img.shields.io/badge/Deployed%20on-Render-black)

> **Ver Demo en Producción:** [https://shorty-the-cutter-url.onrender.com/](https://shorty-the-cutter-url.onrender.com/)

¡Hola! Bienvenido a **Shorty**. Esto no es el típico script ; es una aplicación **Full Stack** completa construida desde cero. El objetivo es simple: tomar esas URLs kilométricas y convertirlas en enlaces cortos, limpios y compartibles.

Este proyecto demuestra capacidades reales de ingeniería de software: un backend robusto en Python, un frontend moderno sin dependencias pesadas y un despliegue automatizado en la nube.

---

## 💡 ¿De qué va el proyecto?

Básicamente, le das a Shorty un enlace largo (como un video de YouTube o una ubicación de Maps) y te devuelve una URL única y corta. Pero no se queda ahí.

Integré un **Dashboard de Administración** para monitorear el tráfico. Todo está desplegado en la nube (Render), persistiendo datos en una base de datos real y asegurado con validaciones estrictas.

### Lo más destacado (Highlights):
* **Full Stack & Production Ready:** Desde el modelado de datos en el backend hasta las animaciones CSS en el frontend, todo está conectado y funcionando en vivo.
* **Redirección Inteligente:** Manejo correcto de códigos de estado HTTP (307) para redirecciones temporales.
* **Panel de Admin VIP:** Un dashboard protegido con contraseña para ver métricas (clicks, estado, URLs originales).
* **Validación Robusta:** No puedes romperlo escribiendo "pizza" o enlaces falsos. Usamos `validators` y lógica de sanitización antes de tocar la base de datos.

---

## 🛠️ Bajo el capó (Tech Stack)

### 🏎️ Backend (El Motor)
* **Python 3.10 & FastAPI:** Elegí este stack por su velocidad y su manejo nativo de asincronismo (Async I/O).
* **SQLAlchemy & SQLite:** Para la persistencia de datos. Cada link y cada click quedan registrados.
* **Pydantic:** Para la validación de esquemas de datos. Mantiene la integridad de la API.
* **Seguridad:** Implementación de **HTTP Basic Auth** para proteger las rutas administrativas.

### 🎨 Frontend (La Interfaz)
Aquí decidí irme por **Vanilla JS**. Sin frameworks pesados como React o Angular, solo rendimiento puro y optimizado.

* **HTML5 Semántico:** Estructura limpia y accesible.
* **CSS3 Moderno & Glassmorphism:** Implementé un diseño con efecto "vidrio esmerilado" (frosted glass) para darle un toque premium.
    * *Animaciones:* Transiciones suaves, loaders y efectos hover.
    * *Responsive:* Se adapta perfecto a móvil y desktop.
* **JavaScript (ES6+):**
    * **Async/Await:** Para manejar las peticiones a la API (Fetch) sin bloquear el hilo principal ni congelar la UI.
    * **DOM Manipulation:** Actualización dinámica de la interfaz.
    * **Toast Notifications:** Sistema de notificaciones flotantes custom para feedback de usuario (✅ Éxito / 🚫 Error).
    * **Clipboard API:** Copiado al portapapeles con un solo clic.

---

## 🚀 Cómo correrlo en local

¿Quieres probar el código? Sigue estos pasos:

1.  **Clona el repo:**
    ```bash
    git clone [https://github.com/SergioC2410/url_shortener.git](https://github.com/SergioC2410/url_shortener.git)
    cd url_shortener/backend
    ```

2.  **Configura el Entorno Virtual (venv):**
    ```bash
    # En Windows:
    python -m venv venv
    .\venv\Scripts\activate
    
    # En Mac/Linux:
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Levanta el servidor:**
    ```bash
    uvicorn main:app --reload
    ```
    ¡Listo! Abre `http://127.0.0.1:8000` en tu navegador.

---

## 🕵️ Acceso al Panel de Admin

¿Quieres ver las métricas? Creé un dashboard privado para eso.

* **Ruta:** `/admin` (ej: `https://shorty-the-cutter-url.onrender.com/admin`)
* **Credenciales de Acceso:**
    * User: `admin`
    * Pass: `1234`

---

## 📸 Capturas

| Página Principal | Dashboard de Admin |
| :---: | :---: |
| *UI limpia con Glassmorphism* | *Tabla de estadísticas en tiempo real* |

---

Desarrollado con 💜 y mucho café por **Sergio**.
[Mira mi GitHub](https://github.com/SergioC2410)