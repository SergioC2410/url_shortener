import os
import secrets
import re
import asyncio
import httpx
import socket
from typing import Optional
from urllib.parse import urlparse
import validators
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

# Importaciones locales
import models, schemas, crud
from database import SessionLocal, engine

# ==============================================================================
# 1. CONFIGURACIÓN INICIAL
# ==============================================================================

# Crear tablas en la BD
models.Base.metadata.create_all(bind=engine)

# Definir rutas de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(
    title="URL Shortener",
    description="API para acortar URLs (Rama Prueba-Internet)",
    version="1.2.0"
)

# ==============================================================================
# 1.1 CONFIGURACIÓN DE VALIDACIÓN MEJORADA
# ==============================================================================

# Configuración para verificación de URLs
VALIDATE_URLS = os.getenv("VALIDATE_URLS", "True").lower() == "true"
VALIDATION_TIMEOUT = 5  # segundos
MAX_URL_LENGTH = 2048

# Lista de TLDs válidos (se puede expandir)
VALID_TLDS = {
    'com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 
    'arpa', 'ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 
    'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 
    'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 
    'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 
    'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 
    'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 
    'co', 'cr', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 
    'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 
    'eh', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 
    'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 
    'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 
    'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 
    'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 
    'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 
    'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 
    'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 
    'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 
    'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 
    'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 
    'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 
    'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 
    'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 
    'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 
    'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 
    'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 
    'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 
    'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 
    'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 
    'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 
    'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 
    'vu', 'wf', 'ws', 'ye', 'yt', 'za', 'zm', 'zw'
}

# Dominios bloqueados (ejemplos comunes)
BLOCKED_DOMAINS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "192.168.",
    "10.",
    "172.16.",
    "172.17.",
    "172.18.",
    "172.19.",
    "172.20.",
    "172.21.",
    "172.22.",
    "172.23.",
    "172.24.",
    "172.25.",
    "172.26.",
    "172.27.",
    "172.28.",
    "172.29.",
    "172.30.",
    "172.31.",
]

# ==============================================================================
# 1.2 FUNCIONES DE VALIDACIÓN MEJORADAS
# ==============================================================================

def validar_formato_url(url: str) -> tuple[bool, str]:
    """Valida el formato básico de una URL de manera estricta"""
    # Validación de longitud
    if len(url) > MAX_URL_LENGTH:
        return False, f"La URL es demasiado larga (máximo {MAX_URL_LENGTH} caracteres)"
    
    # Eliminar protocolo si existe para analizar el dominio
    clean_url = url.lower()
    if clean_url.startswith(('http://', 'https://')):
        clean_url = clean_url.split('://', 1)[1]
    
    # Eliminar ruta y parámetros si existen
    domain_part = clean_url.split('/')[0]
    
    # Verificar que tenga al menos un punto
    if '.' not in domain_part:
        return False, "El dominio debe contener un punto (ej: ejemplo.com)"
    
    # Dividir dominio para analizar
    domain_parts = domain_part.split('.')
    
    # Verificar que haya al menos 2 partes después del último punto
    if len(domain_parts) < 2:
        return False, "Dominio incompleto (ej: ejemplo.com)"
    
    # Verificar cada parte del dominio
    for part in domain_parts:
        if not part:
            return False, "Parte del dominio vacía"
        if len(part) < 1:  # No permitir partes de dominio vacías
            return False, "Parte del dominio demasiado corta"
        if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', part):
            return False, f"Parte del dominio inválida: '{part}'"
    
    # Verificar el TLD (extensión del dominio)
    tld = domain_parts[-1].lower()
    if tld not in VALID_TLDS:
        return False, f"Extensión de dominio no válida: '.{tld}'"
    
    # Verificar que el dominio principal (sin TLD) no sea demasiado corto
    main_domain = domain_parts[-2] if len(domain_parts) >= 2 else ''
    if len(main_domain) < 2 and main_domain not in {'co', 'ac', 'go', 'or', 'ne', 'com'}:
        return False, "Nombre de dominio principal demasiado corto"
    
    # Patrón regex más estricto para URL completa
    patron_url = re.compile(
        r'^(https?://)?'  # http:// o https:// (opcional)
        r'([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+'  # dominio
        r'[A-Za-z]{2,}'  # extensión de dominio (al menos 2 caracteres)
        r'(:[0-9]{1,5})?'  # puerto opcional
        r'(/.*)?$',  # ruta opcional
        re.IGNORECASE
    )
    
    if not patron_url.match(url):
        return False, "Formato de URL inválido"
    
    return True, ""

def validar_dominio(url: str) -> tuple[bool, str]:
    """Valida que el dominio no sea local, privado o sospechoso"""
    try:
        parsed = urlparse(url)
        if not parsed.hostname:
            return False, "URL sin dominio válido"
        
        hostname = parsed.hostname.lower()
        
        # Verificar dominios bloqueados
        for blocked in BLOCKED_DOMAINS:
            if hostname.startswith(blocked):
                return False, f"Dominio no permitido: {hostname}"
        
        # Verificar si es IP
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname):
            octetos = list(map(int, hostname.split('.')))
            # IPs privadas
            if octetos[0] == 10:
                return False, "IP privada (10.x.x.x) no permitida"
            elif octetos[0] == 172 and 16 <= octetos[1] <= 31:
                return False, "IP privada (172.16-31.x.x) no permitida"
            elif octetos[0] == 192 and octetos[1] == 168:
                return False, "IP privada (192.168.x.x) no permitida"
        
        # Verificar que el dominio tenga al menos 2 partes separadas por punto
        if hostname.count('.') < 1:
            return False, "Dominio debe tener al menos un punto separador"
        
        # Verificar que no sea solo un TLD (como "com" o "org")
        domain_parts = hostname.split('.')
        if len(domain_parts) < 2:
            return False, "Dominio incompleto"
        
        # Verificar que el último segmento (TLD) tenga al menos 2 caracteres
        tld = domain_parts[-1]
        if len(tld) < 2:
            return False, "Extensión de dominio demasiado corta"
        
        # Verificar dominio principal
        main_domain = domain_parts[-2]
        if len(main_domain) < 2:
            return False, "Nombre de dominio principal demasiado corto"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validando dominio: {str(e)}"

async def verificar_resolucion_dns(hostname: str) -> tuple[bool, str]:
    """Verifica que el dominio se pueda resolver a través de DNS"""
    try:
        # Usar asyncio para resolver DNS
        loop = asyncio.get_event_loop()
        try:
            # Intentar resolver IPv4
            await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
            return True, ""
        except socket.gaierror:
            # Intentar resolver IPv6
            try:
                await loop.getaddrinfo(hostname, None, family=socket.AF_INET6)
                return True, ""
            except socket.gaierror:
                return False, f"No se pudo resolver el dominio '{hostname}'"
    except Exception as e:
        return False, f"Error resolviendo DNS: {str(e)}"

async def verificar_url_accesible(url: str) -> tuple[bool, str]:
    """Verifica que la URL sea accesible haciendo una petición HEAD"""
    if not VALIDATE_URLS:
        return True, ""
    
    try:
        # Primero verificar DNS
        parsed = urlparse(url)
        dns_ok, dns_msg = await verificar_resolucion_dns(parsed.hostname)
        if not dns_ok:
            return False, dns_msg
        
        async with httpx.AsyncClient(
            timeout=VALIDATION_TIMEOUT,
            follow_redirects=True,
            verify=False,  # Para testing, en producción debería ser True
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        ) as client:
            
            # Intentar con HEAD primero (más liviano)
            try:
                response = await client.head(url, allow_redirects=True)
                if response.status_code < 400:
                    return True, ""
                elif response.status_code == 405:
                    # Si HEAD no está permitido, intentar con GET
                    try:
                        response = await client.get(url, timeout=VALIDATION_TIMEOUT)
                        if response.status_code < 400:
                            return True, ""
                        else:
                            return False, f"URL devolvió código {response.status_code}"
                    except httpx.HTTPError:
                        # Si GET también falla, aceptar la URL pero con advertencia
                        return True, f"URL parece existir pero no se pudo verificar completamente"
                else:
                    return False, f"URL devolvió código {response.status_code}"
                    
            except httpx.HTTPError as head_error:
                # Si HEAD falla, intentar con GET
                try:
                    response = await client.get(url, timeout=VALIDATION_TIMEOUT)
                    if response.status_code < 400:
                        return True, ""
                    else:
                        return False, f"URL devolvió código {response.status_code}"
                except httpx.HTTPError as get_error:
                    return False, f"No se pudo acceder a la URL: {str(get_error)}"
                    
    except httpx.TimeoutException:
        # Si hay timeout, puede que el sitio sea lento, pero aceptamos la URL
        return True, "Verificación timeout - URL aceptada con precaución"
    except Exception as e:
        return False, f"Error verificando URL: {str(e)}"

async def validar_url_completa(url: str) -> tuple[bool, str]:
    """Valida una URL completamente: formato, dominio y accesibilidad"""
    
    # Paso 1: Verificar formato básico
    if not url:
        return False, "La URL no puede estar vacía"
    
    # Eliminar espacios
    url = url.strip()
    
    # Paso 2: Asegurar que tenga protocolo
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Paso 3: Validar con validators (biblioteca existente)
    if not validators.url(url):
        return False, "Formato de URL inválido. Ejemplo: https://ejemplo.com"
    
    # Paso 4: Validar formato con nuestra función más estricta
    formato_ok, formato_msg = validar_formato_url(url)
    if not formato_ok:
        return False, formato_msg
    
    # Paso 5: Validar dominio
    dominio_valido, mensaje_dominio = validar_dominio(url)
    if not dominio_valido:
        return False, mensaje_dominio
    
    # Paso 6: Verificar DNS (esto es crítico para saber si el dominio existe)
    parsed = urlparse(url)
    dns_ok, dns_msg = await verificar_resolucion_dns(parsed.hostname)
    if not dns_ok:
        return False, f"El dominio no existe o no se puede resolver: {dns_msg}"
    
    # Paso 7: Verificar que sea accesible (opcional pero recomendado)
    if VALIDATE_URLS:
        accesible, mensaje_acceso = await verificar_url_accesible(url)
        if not accesible:
            # No rechazamos inmediatamente, damos una advertencia
            print(f"Advertencia: {mensaje_acceso}")
            # Podemos decidir si rechazar o aceptar con advertencia
            # Por ahora aceptamos pero registramos la advertencia
    
    return True, url

# ==============================================================================
# 2. ARCHIVOS ESTÁTICOS
# ==============================================================================

if not os.path.exists(FRONTEND_DIR):
    raise RuntimeError(f"No se encuentra la carpeta frontend en: {FRONTEND_DIR}")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 3. FUNCIONES DE AYUDA (DEPENDENCIAS)
# ==============================================================================

def get_db():
    """Gestiona la conexión a la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBasic()

def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Valida usuario y contraseña del administrador."""
    user_ok = secrets.compare_digest(credentials.username, "admin")
    pass_ok = secrets.compare_digest(credentials.password, "1234")

    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def obtener_base_url(request: Request) -> str:
    """
    Detecta si estamos en Render (Internet) o en Local.
    Usa la variable de entorno DOMAIN si existe.
    """
    domain = os.getenv("DOMAIN")
    if domain:
        return domain.rstrip("/") + "/"
    return str(request.base_url)

# ==============================================================================
# 4. RUTAS DE VISTAS (HTML)
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Sirve la página principal."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/admin", response_class=HTMLResponse)
def read_admin(username: str = Depends(verificar_admin)): 
    """Sirve el panel de admin (protegido)."""
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

# ==============================================================================
# 5. RUTAS DE LA API (LÓGICA) - VALIDACIÓN MEJORADA
# ==============================================================================

@app.get("/urls", response_model=list[schemas.URLInfo])
def read_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), request: Request = None):
    """Devuelve el historial de URLs."""
    urls = crud.get_urls(db, skip=skip, limit=limit)
    base_url = obtener_base_url(request)
    
    for url in urls:
        url.url_completa = f"{base_url}{url.key}"
        
    return urls

@app.post("/url", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    """Crea un nuevo enlace corto con validación mejorada."""
    
    # Validación mejorada
    if not url.target_url or url.target_url.strip() == "":
        raise HTTPException(status_code=400, detail="La URL no puede estar vacía")
    
    # Validar URL completamente
    valida, resultado = await validar_url_completa(url.target_url)
    
    if not valida:
        raise HTTPException(status_code=400, detail=resultado)
    
    # Si la validación devolvió la URL con protocolo, la actualizamos
    if isinstance(resultado, str) and resultado.startswith(('http://', 'https://')):
        url.target_url = resultado
    
    # Guardar en BD
    db_url = crud.create_url(db=db, url=url)
    
    # Respuesta con URL completa
    base_url = obtener_base_url(request)
    db_url.url_completa = f"{base_url}{db_url.key}"
    
    return db_url

# ==============================================================================
# 6. REDIRECCIÓN Y OPERACIONES CRUD
# ==============================================================================

@app.put("/urls/{url_key}", response_model=schemas.URLInfo)
async def update_url_endpoint(url_key: str, updates: schemas.URLUpdate, db: Session = Depends(get_db)):
    """Edita una URL existente con validación mejorada."""
    db_url = crud.get_url_by_key(db, url_key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    
    # Si intentan cambiar la URL objetivo, la validamos de nuevo
    if updates.target_url:
        if not updates.target_url or updates.target_url.strip() == "":
            raise HTTPException(status_code=400, detail="La URL no puede estar vacía")
        
        # Validar URL completamente
        valida, resultado = await validar_url_completa(updates.target_url)
        
        if not valida:
            raise HTTPException(status_code=400, detail=resultado)
        
        # Si la validación devolvió la URL con protocolo, la actualizamos
        if isinstance(resultado, str) and resultado.startswith(('http://', 'https://')):
            updates.target_url = resultado

    return crud.update_url(db, db_url, updates)

@app.delete("/urls/{url_key}")
def delete_url_endpoint(url_key: str, db: Session = Depends(get_db)):
    """Elimina una URL."""
    db_url = crud.get_url_by_key(db, url_key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    
    crud.delete_url(db, db_url)
    return {"detail": "URL eliminada correctamente"}

@app.get("/{url_key}")
def forward_to_target_url(url_key: str, db: Session = Depends(get_db)):
    """Redirige al enlace original."""
    if url_key == "static":
        return HTMLResponse(status_code=404)

    db_url = crud.get_url_by_key(db, url_key)

    if db_url:
        db_url.clicks += 1
        db.commit()
        return RedirectResponse(db_url.target_url)
    else:
        # Error 404 Personalizado
        html_error = f"""
        <html>
            <head>
                <title>No encontrado</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: sans-serif; text-align: center; padding-top: 50px; background: #f9f9f9; }}
                    h1 {{ color: #e74c3c; }}
                    .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #6366f1; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>⚠️ Enlace no encontrado</h1>
                <p>El código <strong>{url_key}</strong> no existe.</p>
                <a href="/" class="btn">Crear nuevo</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html_error, status_code=404)

# ==============================================================================
# 7. ENDPOINTS DE DIAGNÓSTICO
# ==============================================================================

@app.get("/api/health")
def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return {
        "status": "ok",
        "version": "1.2.0",
        "features": {
            "url_validation": VALIDATE_URLS,
            "max_url_length": MAX_URL_LENGTH
        }
    }

@app.post("/api/validate-url")
async def validate_url_external(url: schemas.URLCreate):
    """Endpoint para validar una URL sin crear un enlace."""
    if not url.target_url or url.target_url.strip() == "":
        return {"valid": False, "message": "La URL no puede estar vacía"}
    
    valida, resultado = await validar_url_completa(url.target_url)
    
    if valida:
        return {
            "valid": True,
            "message": "URL válida",
            "normalized_url": resultado if isinstance(resultado, str) else url.target_url
        }
    else:
        return {
            "valid": False,
            "message": resultado,
            "normalized_url": None
        }