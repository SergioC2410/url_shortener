import os
import secrets  # Necesario para comparar contraseñas seguramente
import validators
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials # Necesario para el login
from sqlalchemy.orm import Session

# Importaciones locales (tus archivos)
import models, schemas, crud
from database import SessionLocal, engine

# --- CONFIGURACIÓN DE BASE DE DATOS ---
models.Base.metadata.create_all(bind=engine)

# --- INICIALIZACIÓN DE LA APP ---
app = FastAPI(
    title="URL Shortener",
    description="API robusta para acortar URLs y gestionar redirecciones.",
    version="1.0.0"
)

# --- CONFIGURACIÓN DE RUTAS Y ARCHIVOS ESTÁTICOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DEPENDENCIA DE BASE DE DATOS ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- SEGURIDAD (BASIC AUTH) ---
security = HTTPBasic()

def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifica usuario y contraseña.
    Si fallan, lanza un error 401 que pide credenciales de nuevo.
    """
    # CAMBIA ESTO POR TU USUARIO Y CONTRASEÑA PREFERIDOS
    usuario_correcto = "admin"
    password_correcto = "1234"

    # Usamos secrets.compare_digest para evitar ataques de tiempo
    is_user_ok = secrets.compare_digest(credentials.username, usuario_correcto)
    is_pass_ok = secrets.compare_digest(credentials.password, password_correcto)

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# ==========================================
# RUTAS FIJAS (Deben ir PRIMERO)
# ==========================================

@app.get("/")
def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/admin")
def read_admin(username: str = Depends(verificar_admin)): 
    """Panel de Admin: Protegido con contraseña"""
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

@app.get("/urls", response_model=list[schemas.URLInfo])
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), request: Request = None):
    # Nota: También podrías proteger esta ruta con Depends(verificar_admin) si quisieras
    urls = crud.get_urls(db, skip=skip, limit=limit)
    base_url = str(request.base_url)
    for url in urls:
        url.url_completa = f"{base_url}{url.key}"
    return urls

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    # 1. Validación manual extra: Debe tener un punto (ej: .com, .net)
    if "." not in url.target_url:
         raise HTTPException(status_code=400, detail="La URL debe contener un dominio válido (ej: google.com)")

    # 2. Sanitización (agregar http si falta)
    if "http" not in url.target_url:
        url.target_url = "http://" + url.target_url

    # 3. Validación de librería
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="La URL no es válida.")

    # ... el resto del código sigue igual ...
    db_url = crud.create_url(db=db, url=url)
    base_url = str(request.base_url)
    db_url.url_completa = f"{base_url}{db_url.key}"
    return db_url

# ==========================================
# RUTA DINÁMICA (Debe ir AL FINAL)
# ==========================================

@app.get("/{url_key}")
def forward_to_target_url(url_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_key(db, url_key)

    if db_url:
        db_url.clicks += 1
        db.commit()
        db.refresh(db_url)
        return RedirectResponse(db_url.target_url)
    else:
        # Página de Error 404 Personalizada
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