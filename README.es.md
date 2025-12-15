# 🔗 Shorty | URL Shortener Premium

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Alto%20Rendimiento-009688)
![Status](https://img.shields.io/badge/Status-Live%20%26%20Kicking-success)
![Render](https://img.shields.io/badge/Deploy%20en-Render-black)

> **Ver Demo en Producción:** [https://shorty-the-cutter-url.onrender.com/](https://shorty-the-cutter-url.onrender.com/)

Bienvenido a **Shorty**. Este proyecto representa una **aplicación Full Stack** completa, desarrollada desde cero con enfoque en la eficiencia y la seguridad. El objetivo principal es la conversión de URLs extensas en enlaces cortos, limpios y eficientes para su distribución.

Este proyecto demuestra un dominio en la integración de un **backend robusto** basado en Python (FastAPI) con un **frontend moderno** (Vanilla JS/CSS), totalmente desplegado en un entorno de producción en la nube.

---

## 💡 Propósito del Proyecto (Product Mindset)

El sistema ofrece una solución de acortamiento de URLs con capacidad de **auditoría y seguimiento**. Tras generar un enlace corto, la plataforma monitorea y registra el número de clicks que recibe, ofreciendo métricas básicas en tiempo real desde un dashboard privado.

### Aspectos Técnicos Destacados (Highlights):
* **Arquitectura Full Stack:** Integración coherente y modular del API (backend), la base de datos y la interfaz de usuario (frontend).
* **Redirección Estándar:** Implementación de redirecciones HTTP 307 (Temporal Redirect) y manejo de errores 404 con páginas personalizadas.
* **Dashboard Asegurado:** Panel de administración protegido mediante **Autenticación Básica HTTP (Basic Auth)** para acceder a las estadísticas.
* **Validación de Integridad:** Uso de validadores estrictos para garantizar que solo se procesen URLs válidas, rechazando entradas malformadas.

---

## 📐 Diseño y Prototipado (Design-to-Code Blueprint)

Antes de iniciar el desarrollo del código, se definió la estructura de la Interfaz de Usuario (UI) y el flujo de usuario (UX) mediante un prototipo en Figma. Este **mockup de alta fidelidad** sirvió como *blueprint* esencial para asegurar una arquitectura de la información clara y la posterior traducción a un producto final *pixel-perfect*.

* **Ver el Prototipo en Figma:** [Wireframe: URL Shortener](https://www.figma.com/design/a4PYuK2S0dJIH3yEOYqUUp/Wireframe-URL-Shortener?node-id=0-1&p=f&t=yiobX4dwB1bvFjlo-0)

---

## 🛠️ Stack Tecnológico (Under the Hood)

### 🏎️ Backend (El Servidor)
* **Python 3.10 & FastAPI:** Elegido por su rendimiento asíncrono y la generación automática de documentación Swagger/ReDoc.
* **SQLAlchemy & SQLite:** Utilizado como ORM para la capa de persistencia de datos y gestión del esquema.
* **Pydantic:** Garantiza la validación y tipado de los datos entrantes y salientes de la API (schemas).
* **Despliegue (Render):** Configuración de variables de entorno y comandos de *start* para el entorno de producción.

### 🎨 Frontend (La Interfaz)
La implementación se realizó con **Vanilla JavaScript** para maximizar el rendimiento y minimizar la dependencia de librerías externas.

* **Maquetación:** Estructura HTML5 Semántica y diseño **Responsive** (Media Queries).
* **Estilización:** Uso de CSS3 avanzado, incluyendo el efecto **Glassmorphism** y animaciones para un *look & feel* moderno.
* **JavaScript (ES6+):**
    * **Asincronismo:** Uso de `fetch` con `async/await` para peticiones no bloqueantes a la API.
    * **DOM:** Manipulación directa del DOM para una interfaz reactiva.
    * **Features:** Implementación de la **Clipboard API** para la función de copiar y un sistema de **Toast Notifications** para feedback de usuario.

---

## 🚀 Guía de Instalación Local

Para ejecutar el servicio en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/SergioC2410/url_shortener.git](https://github.com/SergioC2410/url_shortener.git)
    cd url_shortener/backend
    ```

2.  **Configurar y Activar el Entorno Virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciar el servidor Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    Accede a `http://127.0.0.1:8000`.

---

## 🕵️ Credenciales de Acceso al Dashboard

El panel de administración se encuentra protegido en la ruta `/admin`.

* **URL de Acceso:** `/admin` (ej: `https://shorty-the-cutter-url.onrender.com/admin`)
* **Credenciales (Demo):**
    * Usuario: `admin`
    * Contraseña: `1234`

---

## 📸 Screenshots

| Página Principal | Dashboard de Administración |
| :---: | :---: |
| *UI con énfasis en la usabilidad y diseño* | *Métricas clave para la auditoría de enlaces* |

---

[Ver en GitHub](https://github.com/SergioC2410)
