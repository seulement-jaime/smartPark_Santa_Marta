"""
Módulo: models/parqueadero.py
Descripción: Clase orientada a objetos que representa un Parqueadero Formal dentro del polígono
del Centro Histórico de Santa Marta (Muestra piloto n1 = 3 parqueaderos).
Autor: Jaime Andrés Ruiz Pérez - Ingeniería de Sistemas (Unimagdalena)
"""

from typing import List, Dict
from models.sensor_iot import SensorIoT


class Parqueadero:
    """
    Representa una unidad de infraestructura de estacionamiento formal y gestiona
    su colección de objetos SensorIoT (Composición POO).
    """

    def __init__(
        self,
        id_parqueadero: str,
        nombre: str,
        direccion: str,
        latitud: float,
        longitud: float,
        tarifa_hora_cop: int,
        total_cupos: int,
        ocupados_iniciales: int,
    ):
        self.id_parqueadero: str = id_parqueadero
        self.nombre: str = nombre
        self.direccion: str = direccion
        self.latitud: float = latitud
        self.longitud: float = longitud
        self.tarifa_hora_cop: int = tarifa_hora_cop
        self.sensores: List[SensorIoT] = []

        # Inicializar los nodos IoT de cada cupo
        for i in range(1, total_cupos + 1):
            codigo_cupo = f"{self.id_parqueadero}-C{i:02d}"
            esta_ocupado = i <= ocupados_iniciales
            self.sensores.append(SensorIoT(codigo_cupo, self.id_parqueadero, esta_ocupado))

    @property
    def total_cupos(self) -> int:
        return len(self.sensores)

    @property
    def cupos_ocupados(self) -> int:
        return sum(1 for s in self.sensores if s.ocupado)

    @property
    def cupos_disponibles(self) -> int:
        return self.total_cupos - self.cupos_ocupados

    @property
    def porcentaje_ocupacion(self) -> float:
        if self.total_cupos == 0:
            return 0.0
        return round((self.cupos_ocupados / self.total_cupos) * 100, 1)

    @property
    def estado_alerta(self) -> str:
        """Retorna el semáforo de disponibilidad para la interfaz UI/UX."""
        if self.cupos_disponibles == 0:
            return "COMPLETO"
        elif self.cupos_disponibles <= 2:
            return "POCOS_CUPOS"
        return "DISPONIBLE"

    def cambiar_estado_cupo(self, id_cupo: str) -> Dict:
        """Busca un sensor específico por su ID y conmuta su estado."""
        for sensor in self.sensores:
            if sensor.id_cupo == id_cupo:
                return sensor.detectar_cambio_estado()
        raise ValueError(f"No se encontró el cupo {id_cupo} en {self.nombre}")

    def to_dict(self) -> Dict:
        """Serializa el parqueadero y todos sus sensores para la API en la nube."""
        return {
            "id": self.id_parqueadero,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "tarifa_hora_cop": self.tarifa_hora_cop,
            "total_cupos": self.total_cupos,
            "cupos_ocupados": self.cupos_ocupados,
            "cupos_disponibles": self.cupos_disponibles,
            "porcentaje_ocupacion": self.porcentaje_ocupacion,
            "estado_alerta": self.estado_alerta,
            "sensores": [s.to_dict() for s in self.sensores],
        }
