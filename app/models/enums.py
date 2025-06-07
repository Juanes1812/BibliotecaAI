from enum import Enum

class EstadoLibro(str, Enum):
    DISPONIBLE = "disponible"
    RESERVADO = "reservado"
    EN_REPARACION = "en_reparacion"
    PERDIDO = "perdido"