from percepcion import Percepcion
from accion import Accion
from cpd import elegir_accion, convertir_percepcion


class AgenteIluminacion:
    def __init__(self) -> None:
        pass

    def decidir_accion(self, p: Percepcion, usar_cpd_only: bool = False) -> Accion:

        # =========================
        # MODO CPD (PROBABILÍSTICO)
        # =========================
        print("[INFO] Modo probabilístico (CPD)")

        presencia, luz, hora = convertir_percepcion(p)
        resultado, prob = elegir_accion(presencia, luz, hora)

        print(f"[INFO] Acción elegida: {resultado} (probabilidad: {prob})")

        return Accion(resultado.upper(), None, 0)