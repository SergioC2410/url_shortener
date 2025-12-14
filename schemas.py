from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict  

# 1. BaseSchema
class URLBase(BaseModel):
    target_url: str = Field(
        ..., 
        title="URL Objetivo", 
        description="La dirección web original a acortar",
        # CAMBIO 1: 'example' ahora va dentro de json_schema_extra
        json_schema_extra={"example": "https://www.google.com"}
    )

class URL(URLBase):
    is_active: bool
    clicks: int

    model_config = ConfigDict(from_attributes=True)
    
# 2. Schema de Creación (Input)
class URLCreate(URLBase):
    """
    Schema para recibir los datos de creación.
    Solo necesitamos la URL original.
    """
    pass

# 3. Schema de Respuesta (Output)
class URLInfo(URLBase):
    """
    Schema para devolver la información al cliente.
    Incluye datos generados por el sistema (key, clicks, status).
    """
    is_active: bool
    clicks: int
    key: str = Field(..., title="Clave Única", description="El código corto generado")
    
    # Optional porque este campo lo calculamos en el código
    url_completa: Optional[str] = Field(None, description="URL corta completa lista para usar")

    # --- AQUÍ ESTÁ EL CAMBIO ---
    # Eliminamos "class Config" y usamos "model_config"
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "target_url": "https://www.google.com",
                "is_active": True,
                "clicks": 0,
                "key": "A8sK2",
                "url_completa": "http://localhost:8000/A8sK2"
            }
        }
    )