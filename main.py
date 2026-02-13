import random
import time
import numpy as np
import asyncio
import datetime

class Semaforo:
    VERDE = "🟢 VERDE (Normal)"
    AMARILLO = "🟡 AMARILLO (Advertencia)"
    ROJO = "🔴 ROJO (Crítico)"

def evaluar_semaforo(evento: str, status_code: int, elapsed_time: float) -> str:
    if evento == "Fibrilación Ventricular Grave" or status_code != 200:
        return Semaforo.ROJO
    if elapsed_time > 3:
        return Semaforo.AMARILLO
    return Semaforo.VERDE

def leer_ecg(grave=False):
    if grave:
        return [random.randint(50, 150) + random.randint(-50, 50) for _ in range(100)]
    else:
        return [random.randint(70, 90) for _ in range(100)]

def detectar_fv(ecg_data):
    try:
        cambios = np.diff(ecg_data)
        if max(cambios) > 50:
            return True
    except Exception as e:
        print(f"Error en la detección de fibrilación: {e}")
    return False

def clasificar_evento(ecg_data):
    if detectar_fv(ecg_data):
        return "Fibrilación Ventricular Grave"
    else:
        return "Evento Normal"

async def notificar_hospital(evento):
    try:
        fallo = random.choice([False, False, False, True])
        if fallo:
            raise Exception("Simulación de error de red")
        print(f"Notificación enviada con éxito. Evento: {evento}")
        return 200
    except Exception as e:
        print(f"Error al notificar al hospital: {e}")
        return 500

def recalcular_ruta(gravedad):
    if gravedad == "Fibrilación Ventricular Grave":
        return "Ruta más rápida hacia el hospital de emergencia"
    return "Ruta estándar hacia el hospital"

async def ejecutar_tareas():
    max_iteraciones = 10
    contador = 0

    while contador < max_iteraciones:
        start_time = time.time()

        grave = random.choice([True, False])
        ecg_data = leer_ecg(grave)
        evento = clasificar_evento(ecg_data)
        print(f"\n[{datetime.datetime.now()}] Evento detectado: {evento}")

        status_code = await notificar_hospital(evento)
        if status_code == 200:
            print(f"Notificación OK. Código de estado: {status_code}")
        else:
            print(f"Falló la notificación. Código de estado: {status_code}")

        ruta = recalcular_ruta(evento)
        print(f"Ruta de emergencia: {ruta}")

        elapsed_time = time.time() - start_time

        if elapsed_time > 3:
            print(f"¡Advertencia! Tiempo de respuesta > 3s ({elapsed_time:.2f}s)")

        estado = evaluar_semaforo(evento, status_code, elapsed_time)
        print(f"Semáforo del sistema: {estado} | Tiempo: {elapsed_time:.2f}s")

        contador += 1
        await asyncio.sleep(1)

    print("\nEl sistema ha terminado la ejecución.")

if __name__ == "__main__":
    print("Iniciando el sistema de emergencias médicas...")
    asyncio.run(ejecutar_tareas())
