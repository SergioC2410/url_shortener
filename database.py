import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Intentamos obtener la URL de la base de datos de las variables de entorno.
# Si no existe (estamos en local), usamos SQLite por defecto para desarrollo rápido.
# Esto es crucial para despliegues en producción (ej: Render, Railway, AWS).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Configuración de argumentos de conexión
# 'check_same_thread': False es necesario SOLO para SQLite en FastAPI,
# ya que cada petición puede correr en un hilo distinto.
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Creación del motor (Engine)
# Nota: echo=True (comentado) sirve para ver los SQL logs en consola al depurar.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
    # echo=True 
)

# Configuración de la sesión
# autocommit=False: Queremos control total sobre cuándo se guardan los datos.
# autoflush=False: Evita que SQLAlchemy mande datos a la DB antes de que estemos listos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
Base = declarative_base()