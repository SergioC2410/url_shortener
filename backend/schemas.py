from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# ==============================================================================
# 1. ESQUEMA BASE (SHARED)
# ==============================================================================

class URLBase(BaseModel):
    """
    Propiedades compartidas que toda URL debe tener.
    Se usa como base para evitar repetir código en los otros esquemas.
    """
    target_url: str = Field(
        ..., 
        title="URL Objetivo", 
        description="La dirección web original a la que queremos redirigir",
        # En Pydantic v2, los ejemplos van dentro de 'json_schema_extra'
        json_schema_extra={"example": "https://www.google.com"}
    )

# ==============================================================================
# 2. ESQUEMAS DE ENTRADA (INPUTS)
# ==============================================================================

class URLCreate(URLBase):
    """
    Datos necesarios para CREAR una nueva URL corta.
    Hereda de URLBase, por lo que solo exige 'target_url'.
    """
    pass

class URLUpdate(BaseModel):
    """
    Datos para EDITAR una URL existente.
    Todos los campos son opcionales porque el usuario puede querer
    cambiar solo el link, solo el estado, o ambos.
    """
    target_url: Optional[str] = Field(None, description="Nueva dirección web (opcional)")
    is_active: Optional[bool] = Field(None, description="Activar o desactivar el enlace")

# ==============================================================================
# 3. ESQUEMAS DE SALIDA (OUTPUTS)
# ==============================================================================

class URLInfo(URLBase):
    """
    Schema completo para devolver información al cliente (Frontend).
    Incluye datos de la DB (clicks, estado) y datos calculados (url_completa).
    """
    id: int
    is_active: bool
    clicks: int
    key: str = Field(..., title="Clave Única", description="El código corto generado (ej: AbC12)")
    
    # Campo calculado: No se guarda en la DB, se genera al vuelo en el main.py
    url_completa: Optional[str] = Field(None, description="URL corta completa lista para compartir")

    # Configuración del Modelo (Pydantic v2)
    model_config = ConfigDict(
        # 'from_attributes=True' permite a Pydantic leer datos de SQLAlchemy
        from_attributes=True,
        
        # Ejemplo para la documentación automática (Swagger UI)
        json_schema_extra={
            "example": {
                "target_url": "https://www.google.com",
                "is_active": True,
                "clicks": 42,
                "key": "A8sK2",
                "url_completa": "https://tu-dominio.com/A8sK2"
            }
        }
    )