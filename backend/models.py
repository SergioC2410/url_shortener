from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class URLItem(Base):
    """
    Modelo de Base de Datos para las URLs acortadas.
    
    Representa la tabla 'urls' en la base de datos.
    Incluye campos de auditoría (created_at) y control (is_active)
    que generalmente se omiten en tutoriales básicos pero son
    vitales en producción.
    """
    __tablename__ = "urls"

    # Identificador único
    id = Column(Integer, primary_key=True, index=True)

    # Datos principales
    # nullable=False asegura integridad a nivel de base de datos
    target_url = Column(String, index=True, nullable=False) 
    key = Column(String, unique=True, index=True, nullable=False)

    # Analytics y Control
    clicks = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)  # Permite desactivar links sin borrarlos

    # Auditoría (Timestamps)
    # server_default=func.now() delega la hora a la DB, no a la aplicación,
    # lo cual es más preciso y evita problemas de zona horaria del servidor de Python.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        """
        Representación en string del objeto para depuración.
        Ayuda mucho cuando haces print(mi_objeto) en la consola.
        """
        return f"<URLItem(key='{self.key}', target='{self.target_url}', active={self.is_active})>"