"""
Módulo: models/sensor_iot.py
Descripción: Clase orientada a objetos que representa un Nodo Sensor IoT (ESP32 + Sensor Ultrasónico HC-SR04)
instalado en un cupo físico de estacionamiento en el Centro Histórico de Santa Marta.
Autor: Jaime Andrés Ruiz Pérez - Ingeniería de Sistemas (Unimagdalena)
"""

import random
import time
from datetime import datetime


class SensorIoT:
    """
    Representa la Capa Física (Dimensión 1 de la Variable Independiente).
    Simula un nodo de hardware IoT ubicado en un cupo individual.
    """

    def __init__(self, id_cupo: str, parqueadero_id: str, ocupado: bool = False):
        self.id_cupo: str = id_cupo
        self.parqueadero_id: str = parqueadero_id
        self.ocupado: bool = ocupado
        self.precision_sensor: float = 97.4  # Indicador operacional (>95%)
        self.ultima_latencia_ms: int = random.randint(85, 210)  # Indicador operacional (<500 ms)
        self.ultima_actualizacion: str = datetime.now().strftime("%H:%M:%S")

    def detectar_cambio_estado(self, nuevo_estado: bool = None) -> dict:
        """
        Cambia el estado del cupo (Libre <-> Ocupado) y calcula la latencia de red hacia la nube.
        """
        inicio = time.perf_counter()
        if nuevo_estado is None:
            self.ocupado = not self.ocupado
        else:
            self.ocupado = nuevo_estado

        # Simulación realista de latencia de transmisión MQTT/HTTP hacia Cloud (< 500 ms)
        latencia_red = random.randint(75, 245)
        fin = time.perf_counter()
        self.ultima_latencia_ms = latencia_red + int((fin - inicio) * 1000)
        self.ultima_actualizacion = datetime.now().strftime("%H:%M:%S")

        return {
            "id_cupo": self.id_cupo,
            "parqueadero_id": self.parqueadero_id,
            "ocupado": self.ocupado,
            "estado_texto": "OCUPADO" if self.ocupado else "DISPONIBLE",
            "latencia_ms": self.ultima_latencia_ms,
            "precision_pct": self.precision_sensor,
            "timestamp": self.ultima_actualizacion,
        }

    def to_dict(self) -> dict:
        """Serializa el objeto SensorIoT a diccionario JSON."""
        return {
            "id_cupo": self.id_cupo,
            "parqueadero_id": self.parqueadero_id,
            "ocupado": self.ocupado,
            "latencia_ms": self.ultima_latencia_ms,
            "precision_pct": self.precision_sensor,
            "ultima_actualizacion": self.ultima_actualizacion,
        }
