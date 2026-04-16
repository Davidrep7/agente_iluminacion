from percepcion import Percepcion
from accion import Accion
from motor_inferencia import MotorInferencia

from cpd import elegir_accion, convertir_percepcion


class AgenteIluminacion:
    def __init__(self) -> None:
        self.motor = MotorInferencia()

    def decidir_accion(self, p: Percepcion, usar_cpd_only: bool = False) -> Accion:

        # =========================
        # SOLO REGLAS
        # =========================
        if not usar_cpd_only:
            print("[INFO] Modo determinista (REGLAS)")
            return self.motor.evaluar(p)

        # =========================
        # SOLO CPD
        # =========================
        print("[INFO] Modo probabilístico (CPD)")

        presencia, luz, hora = convertir_percepcion(p)
        resultado, prob = elegir_accion(presencia, luz, hora)

        print(f"[INFO] Acción elegida: {resultado} con probabilidad {prob}")

        # =========================
        # CONVERTIR A OBJETO ACCION
        # =========================
        if resultado == "Encender":
            return Accion("ENCENDER", 100, 0)

        elif resultado == "Ajustar":
            return Accion("AJUSTAR", 50, 0)

        elif resultado == "Apagar":
            return Accion("APAGAR", 0, 0)

        # Caso de seguridad
        return Accion("MANTENER", p.intensidad_actual, 0)