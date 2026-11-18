"""
Archivo Principal: app.py
Descripción: Servidor Backend HTTP/REST orientado a objetos que conecta los módulos POO
(models.SensorIoT, models.Parqueadero y services.GestorParqueoCloud) con la interfaz UI/UX.
Autor: Jaime Andrés Ruiz Pérez - Ingeniería de Sistemas (Universidad del Magdalena)
"""

import json
import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from services.gestor_parqueo_cloud import GestorParqueoCloud

# Instancia global del servicio en la nube (Patrón Singleton / POO)
gestor_cloud = GestorParqueoCloud()


class SmartParkAPIHandler(SimpleHTTPRequestHandler):
    """
    Controlador HTTP orientado a objetos que sirve la aplicación web y expone
    los endpoints REST para consultar y actualizar los sensores IoT en tiempo real.
    """

    def do_GET(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == "/api/estado":
            self._send_json(gestor_cloud.obtener_estado_completo())
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == "/api/sensor/toggle":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            id_parqueadero = data.get("id_parqueadero")
            id_cupo = data.get("id_cupo")

            try:
                gestor_cloud.procesar_evento_sensor(id_parqueadero, id_cupo)
                self._send_json(gestor_cloud.obtener_estado_completo())
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
        else:
            self._send_json({"error": "Endpoint no encontrado"}, status=404)

    def _send_json(self, payload: dict, status: int = 200):
        response = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        # Silenciar logs repetitivos de consola para mantener limpia la terminal
        pass


def iniciar_servidor(puerto: int = 8080):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    servidor = HTTPServer(("127.0.0.1", puerto), SmartParkAPIHandler)
    url = f"http://127.0.0.1:{puerto}/index.html"
    print("=" * 72)
    print("  PROTOTIPO FUNCIONAL: SMARTPARK CENTRO HISTÓRICO DE SANTA MARTA")
    print("  Arquitectura Modular POO en Python + Simulación IoT en Tiempo Real")
    print("  Estudiante: Jaime Andrés Ruiz Pérez | Ingeniería de Sistemas")
    print("=" * 72)
    print(f"  -> Servidor Cloud activo en: {url}")
    print("  -> Presiona Ctrl + C para detener el servidor.")
    print("=" * 72)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
