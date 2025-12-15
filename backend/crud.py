from sqlalchemy.orm import Session
import models, schemas
import secrets
import string

# ==============================================================================
# 1. FUNCIONES DE LECTURA (READ)
# ==============================================================================

def get_url_by_key(db: Session, key: str):
    """
    Busca una URL específica en la base de datos usando su clave única.

    Args:
        db (Session): La sesión de base de datos activa.
        key (str): La clave corta (short key) a buscar.

    Returns:
        models.URLItem | None: El objeto URL si existe, o None si no se encuentra.
    """
    return db.query(models.URLItem).filter(models.URLItem.key == key).first()

def get_urls(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista de todas las URLs guardadas.
    Tiene paginación (skip/limit) por si algún día tienes miles de links.
    """
    return db.query(models.URLItem).offset(skip).limit(limit).all()

# ==============================================================================
# 2. FUNCIONES DE UTILIDAD
# ==============================================================================

def create_random_key(length: int = 5) -> str:
    """
    Genera una cadena alfanumérica aleatoria segura criptográficamente.
    
    Se utiliza 'secrets' en lugar de 'random' para asegurar una menor
    predictibilidad en la generación de claves.

    Args:
        length (int): La longitud deseada de la clave. Por defecto es 5.

    Returns:
        str: La cadena generada.
    """
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

# ==============================================================================
# 3. FUNCIONES DE ESCRITURA (CREATE, UPDATE, DELETE)
# ==============================================================================

def create_url(db: Session, url: schemas.URLCreate) -> models.URLItem:
    """
    Crea una nueva entrada de URL acortada en la base de datos.
    
    Implementa una verificación de colisiones: si la clave generada aleatoriamente
    ya existe (caso muy raro), genera una nueva hasta encontrar una libre.

    Args:
        db (Session): La sesión de base de datos.
        url (schemas.URLCreate): El esquema con la URL original (target_url).

    Returns:
        models.URLItem: La instancia del modelo creada y guardada.
    """
    # Intentamos generar una clave única
    key = create_random_key()
    
    # Programación defensiva: verificamos que la clave no exista ya en la BD
    while get_url_by_key(db, key):
        key = create_random_key()

    # Instanciamos el modelo
    db_url = models.URLItem(target_url=url.target_url, key=key)
    
    try:
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
    except Exception as e:
        # Hacemos rollback en caso de error inesperado para no dejar la sesión sucia
        db.rollback()
        raise e

    return db_url

def update_url(db: Session, db_url: models.URLItem, updates: schemas.URLUpdate):
    """
    Actualiza una URL existente con nuevos datos.
    
    Usa 'exclude_unset=True' para que solo se actualicen los campos que
    el usuario realmente envió (ej: si solo envió is_active, no tocamos target_url).
    """
    update_data = updates.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_url, key, value)

    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def delete_url(db: Session, db_url: models.URLItem):
    """
    Elimina físicamente una URL de la base de datos.
    """
    db.delete(db_url)
    db.commit()
    return True