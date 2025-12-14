# Acortador de URLs (API)

> [🇬🇧 Read this documentation in English](README.md)

API REST robusta y escalable para acortar URLs, construida con **FastAPI** y **Python**. Este proyecto implementa prácticas de ingeniería de software modernas, incluyendo inyección de dependencias, validación de esquemas con Pydantic y persistencia con SQLAlchemy.

## 🚀 Características

* **Acortado de URLs:** Generación de claves únicas criptográficamente seguras.
* **Redirección:** Manejo eficiente de redirecciones HTTP (307).
* **Sanitización:** Limpieza automática de URLs de entrada.
* **Arquitectura Modular:** Separación clara de responsabilidades (Modelos, Esquemas, CRUD, Rutas).
* **Persistencia:** Compatible con SQLite (Dev) y PostgreSQL (Prod).
* **Documentación Automática:** Swagger UI y ReDoc integrados.

## 🛠️ Tecnologías

* **Python 3.10+**
* **FastAPI:** Framework web moderno de alto rendimiento.
* **SQLAlchemy:** ORM para manejo de base de datos.
* **Pydantic:** Validación de datos y gestión de configuraciones.
* **Uvicorn:** Servidor ASGI.

## 📦 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/url-shortener.git
    cd url-shortener
    ```

2.  **Crear entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install fastapi uvicorn sqlalchemy
    # O si tienes un archivo de requisitos:
    # pip install -r requirements.txt
    ```

4.  **Ejecutar el servidor:**
    ```bash
    uvicorn main:app --reload
    ```
    El servidor iniciará en `http://127.0.0.1:8000`.

## 📖 Documentación de la API

Una vez iniciado el servidor, puedes acceder a la documentación interactiva:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗂️ Estructura del Proyecto

```text
├── crud.py         # Lógica de acceso a datos (Create, Read)
├── database.py     # Configuración de conexión y sesión DB
├── main.py         # Endpoints y configuración de la App
├── models.py       # Modelos de Base de Datos (SQLAlchemy)
├── schemas.py      # Esquemas de Validación (Pydantic)
└── README.md       # Documentación