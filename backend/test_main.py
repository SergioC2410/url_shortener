from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Importamos tu app y las configuraciones de base de datos
# Asegúrate de que los nombres coincidan con tus archivos (main, database, models)
from main import app, get_db
from database import Base
import models

# 1. Configuración de Base de Datos TEMPORAL (SQLite en memoria)
# Esto evita que borremos o escribamos en tu base de datos real 'sql_app.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos las tablas en la base de datos temporal
Base.metadata.create_all(bind=engine)

# 2. Sobrescribir la dependencia (Dependency Override)
# Le decimos a FastAPI: "Cuando pidas 'get_db', no uses la real, usa esta de prueba"
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Inicializamos el Cliente de Pruebas
client = TestClient(app)

# --- A PARTIR DE AQUÍ SON TUS TESTS ---

def test_crear_url_corta():
    """Prueba que podemos crear una URL corta correctamente"""
    payload = {"target_url": "https://www.google.com"}
    
    # Simulamos una petición POST a tu endpoint de crear
    # NOTA: Revisa si tu ruta es "/url", "/urls" o "/" y ajústalo aquí
    response = client.post("/url", json=payload) 
    
    # ASERCIONES (Las validaciones)
    # 1. Esperamos que el código sea 200 (OK)
    assert response.status_code == 200
    # 2. Esperamos que la respuesta tenga la clave 'url_key'
    assert "key" in response.json()
    # 3. Esperamos que la 'target_url' sea la que enviamos
    assert response.json()["target_url"] == "https://www.google.com"

def test_leer_url_inexistente():
    """Prueba que pasa si pedimos una clave que no existe"""
    response = client.get("/esta-clave-no-existe")
    
    # Debería dar error 404 Not Found
    assert response.status_code == 404