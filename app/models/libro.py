from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import EstadoLibro 

class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(300), nullable=False)
    autor = Column(String(800), nullable=False)
    isbn = Column(String(20), unique=True, index=True)
    estado = Column(Enum(EstadoLibro), default=EstadoLibro.DISPONIBLE)
    
    # Relación con reservas
    reservas = relationship("Reserva", back_populates="libro")

class Reserva(Base):
    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey('libros.id'), nullable=False)
    usuario_email = Column(String(100), nullable=False)
    fecha_reserva = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    
    # Relación con libro
    libro = relationship("Libro", back_populates="reservas")