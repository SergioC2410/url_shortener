# URL Shortener API 🔗

# URL Shortener API

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![License](https://img.shields.io/badge/license-MIT-green)

> [🇪🇸 Leer documentación en Español](README.es.md)

A robust and scalable REST API for URL shortening, built with **FastAPI** and **Python**. This project implements modern software engineering practices, including dependency injection, Pydantic schema validation, and SQLAlchemy persistence.

## 🚀 Features

* **URL Shortening:** Generates cryptographically secure unique keys.
* **Redirection:** Efficient handling of HTTP redirects (307).
* **Input Sanitization:** Automatic cleaning and validation of input URLs.
* **Modular Architecture:** Clear separation of concerns (Models, Schemas, CRUD, Routes).
* **Persistence:** Supports SQLite (Dev) and PostgreSQL (Prod).
* **Auto-Documentation:** Integrated Swagger UI and ReDoc.

## 🛠️ Tech Stack

* **Python 3.10+**
* **FastAPI:** High-performance modern web framework.
* **SQLAlchemy:** SQL Toolkit and ORM.
* **Pydantic:** Data validation and settings management.
* **Uvicorn:** Lightning-fast ASGI server.

## 📦 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/tu-usuario/url-shortener.git](https://github.com/tu-usuario/url-shortener.git)
    cd url-shortener
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy
    # Or if you have a requirements file:
    # pip install -r requirements.txt
    ```

4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

## 📖 API Documentation

Once the server is running, you can access the interactive documentation:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🗂️ Project Structure

```text
├── crud.py         # Data access logic (Create, Read)
├── database.py     # DB connection and session configuration
├── main.py         # App endpoints and configuration
├── models.py       # Database Models (SQLAlchemy)
├── schemas.py      # Validation Schemas (Pydantic)
└── README.md       # Documentation