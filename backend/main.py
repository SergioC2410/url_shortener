from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import validators
from fastapi.responses import RedirectResponse, HTMLResponse
# Creamos las tablas al inicio.
# NOTA: En un entorno de producción real, esto se sustituiría por
# migraciones con Alembic para tener control de versiones de la BD.
models.Base.metadata.create_all(bind=engine)

# Inicializamos la app con metadatos para la documentación automática (Swagger)
app = FastAPI(
    title="URL Shortener",
    description="API robusta para acortar URLs y gestionar redirecciones.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" significa "permitir a todo el mundo" (para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    """
    Dependency Injection para la sesión de base de datos.
    
    Usamos 'yield' en lugar de 'return' para pausar la ejecución y permitir
    que el framework use la sesión. El bloque 'finally' asegura que la 
    conexión se cierre SIEMPRE, incluso si ocurre un error en el request.
    Esto evita fugas de conexión (connection leaks).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    """
    Crea una nueva URL corta.
    
    Recibe la URL original, realiza una sanitización básica (añadir http si falta),
    genera una clave única y devuelve la información completa, incluyendo
    la URL acortada construida dinámicamente según el entorno.
    """
    # 1. Sanitización básica de entrada
    # Validamos si el usuario olvidó poner el protocolo.
    if "http" not in url.target_url:
        url.target_url = "http://" + url.target_url
# Si validators dice que no es una URL real, devolvemos error y paramos todo.
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="La URL proporcionada no es válida. Revisa que tenga el formato correcto (ej: google.com).")
    # 2. Delegamos la lógica de persistencia al módulo CRUD
    db_url = crud.create_url(db=db, url=url)

    # 3. Construcción de la respuesta
    # No guardamos el dominio en la BD, lo construimos al vuelo.
    # Esto permite que la API funcione en localhost, staging o producción
    # sin tener que migrar datos.
    base_url = str(request.base_url)
    db_url.url_completa = f"{base_url}{db_url.key}"

    return db_url
@app.get("/urls", response_model=list[schemas.URLInfo])
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), request: Request = None):
    """
    Lista todas las URLs creadas y sus estadísticas (visitas).
    """
    urls = crud.get_urls(db, skip=skip, limit=limit)
    
    # Calculamos la URL completa para cada resultado, igual que al crear
    base_url = str(request.base_url)
    for url in urls:
        url.url_completa = f"{base_url}{url.key}"
        
    return urls

@app.get("/{url_key}")
def forward_to_target_url(url_key: str, db: Session = Depends(get_db)):
    """
    Endpoint de redirección.
    
    Busca la clave en la base de datos y redirige al usuario a la URL original.
    Si la clave no existe, retorna un error 404 estandarizado.
    """
    # 1. Buscamos la URL por su clave única
    db_url = crud.get_url_by_key(db, url_key)

    # 2. Lógica de redirección o error
    if db_url:
        # --- AQUÍ AGREGAMOS LA MAGIA (3 LÍNEAS NUEVAS) ---
        db_url.clicks += 1  # Sumamos 1 a las visitas
        db.commit()         # Guardamos el cambio en la BD
        db.refresh(db_url)  # (Opcional) Refrescamos el dato por si acaso
        # --------------------------------------------------

        return RedirectResponse(db_url.target_url)
    else:
        html_error = f"""
        <html>
            <head>
                <title>Link no encontrado</title>
                <style>
                    body {{ font-family: sans-serif; text-align: center; padding-top: 50px; background: #f9f9f9; }}
                    h1 {{ color: #e74c3c; font-size: 40px; }}
                    p {{ color: #555; font-size: 18px; }}
                    .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }}
                    .btn:hover {{ background: #2980b9; }}
                </style>
            </head>
            <body>
                <h1>⚠️ Ups!</h1>
                <p>El enlace corto <strong>{url_key}</strong> no existe o fue eliminado.</p>
                <a href="/" class="btn">Crear uno nuevo</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html_error, status_code=404)

@app.get("/")
def read_root():
    """
    Health check simple para verificar que la API está viva.
    """
    return {"message": "Bienvenido a la API acortadora de URL de Sergio"}