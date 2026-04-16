import random
import re

# =========================
# TABLA CPD
# =========================
cpd = {
    ("Si", "Baja", "Nocturna"): {
        "Encender": 0.9,
        "Ajustar": 0.1,
        "Apagar": 0.0
    },
    ("Si", "Baja", "Diurna"): {
        "Encender": 0.7,
        "Ajustar": 0.2,
        "Apagar": 0.1
    },
    ("Si", "Media", "Nocturna"): {
        "Encender": 0.4,
        "Ajustar": 0.5,
        "Apagar": 0.1
    },
    ("Si", "Media", "Diurna"): {
        "Encender": 0.2,
        "Ajustar": 0.6,
        "Apagar": 0.2
    },
    ("No", "Alta", "Diurna"): {
        "Encender": 0.0,
        "Ajustar": 0.1,
        "Apagar": 0.9
    },
    ("No", "Media", "Diurna"): {
        "Encender": 0.0,
        "Ajustar": 0.2,
        "Apagar": 0.8
    },
    ("No", "Baja", "Nocturna"): {
        "Encender": 0.05,
        "Ajustar": 0.05,
        "Apagar": 0.9
    }
}

# =========================
# CONVERTIR PERCEPCIÓN
# =========================
def convertir_percepcion(p):
    presencia = "Si" if p.presencia else "No"

    if p.luz_natural < 200:
        luz = "Baja"
    elif p.luz_natural <= 500:
        luz = "Media"
    else:
        luz = "Alta"

    hora = "Diurna" if p.hora_tipo.lower() == "diurna" else "Nocturna"

    return presencia, luz, hora

# =========================
# FUNCIÓN CPD
# =========================
def elegir_accion(presencia, luz, hora):
    clave = (presencia, luz, hora)

    if clave not in cpd:
        return None, 0

    probabilidades = cpd[clave]

    acciones = list(probabilidades.keys())
    pesos = list(probabilidades.values())

    accion = random.choices(acciones, pesos)[0]

    # REGRESA TAMBIÉN LA PROBABILIDAD
    return accion, probabilidades[accion]


# =========================
# MOSTRAR TABLA CPD
# =========================
def mostrar_tabla_cpd() -> None:
    """Muestra la tabla de probabilidades CPD en formato legible."""
    print("\n=== TABLA PROBABILÍSTICA CPD ===")
    if not cpd:
        print("[INFO] No hay reglas probabilísticas definidas.")
        return

    print(f"{'Presencia':<10} {'Luz':<7} {'Hora':<10} {'Encender':>10} {'Ajustar':>10} {'Apagar':>10}")
    print("-" * 60)
    for (presencia, luz, hora), probs in cpd.items():
        print(
            f"{presencia:<10} {luz:<7} {hora:<10} "
            f"{probs.get('Encender', 0):>10.2f} "
            f"{probs.get('Ajustar', 0):>10.2f} "
            f"{probs.get('Apagar', 0):>10.2f}"
        )


def eliminar_regla_cpd() -> None:
    """Elimina una regla de probabilidad CPD por su índice."""
    if not cpd:
        print("\n[INFO] No hay reglas CPD para eliminar.")
        return

    print("\n=== ELIMINAR REGLA PROBABILÍSTICA CPD ===")
    claves = list(cpd.keys())
    for idx, (presencia, luz, hora) in enumerate(claves, 1):
        probs = cpd[(presencia, luz, hora)]
        print(
            f"{idx}. Presencia={presencia}, Luz={luz}, Hora={hora} "
            f"-> Encender={probs.get('Encender', 0):.2f}, "
            f"Ajustar={probs.get('Ajustar', 0):.2f}, "
            f"Apagar={probs.get('Apagar', 0):.2f}"
        )

    try:
        seleccion = int(input("Selecciona el número de la regla CPD a eliminar (0 para cancelar): ").strip())
    except ValueError:
        print("[ERROR] Ingresa un número válido.")
        return

    if seleccion == 0:
        print("Operación cancelada.")
        return

    if 1 <= seleccion <= len(claves):
        clave_eliminar = claves[seleccion - 1]
        del cpd[clave_eliminar]
        print(f"[OK] Regla CPD eliminada: {seleccion}.")
    else:
        print("[ERROR] Índice no válido. No se eliminó ninguna regla.")


# =========================
# AGREGAR NUEVA REGLA CPD
# =========================
def agregar_regla_cpd():
    print("\n=== AGREGAR NUEVA REGLA CPD ===")

    while True:
        presencia_input = input("Presencia (s/n): ").strip().lower()
        if presencia_input in ("s", "n"):
            presencia = "Si" if presencia_input == "s" else "No"
            break
        print("[ERROR] Presencia debe ser 's' o 'n'.")

    while True:
        luz_input = input("Luz (baja/media/alta): ").strip().lower()
        if luz_input in ("baja", "media", "alta"):
            luz = luz_input.capitalize()
            break
        print("[ERROR] Luz debe ser 'baja', 'media' o 'alta'.")

    while True:
        hora_input = input("Hora (diurna/nocturna): ").strip().lower()
        if hora_input in ("diurna", "nocturna"):
            hora = hora_input.capitalize()
            break
        print("[ERROR] Hora debe ser 'diurna' o 'nocturna'.")

    def leer_probabilidad(nombre):
        while True:
            valor_texto = input(f"{nombre}: ").strip()
            if not re.fullmatch(r"\d+(\.\d+)?", valor_texto):
                print(f"[ERROR] {nombre} debe ser un número decimal válido (0.0 - 0.99).")
                continue

            try:
                valor = float(valor_texto)
            except ValueError:
                print(f"[ERROR] {nombre} debe ser un número decimal válido.")
                continue

            if not (0 <= valor < 1):
                print(f"[ERROR] {nombre} debe ser mayor o igual a 0 y menor que 1.")
                continue

            return valor

    print("\nIngresa probabilidades (deben sumar 1):")
    while True:
        p_encender = leer_probabilidad("Encender")
        p_ajustar = leer_probabilidad("Ajustar")
        p_apagar = leer_probabilidad("Apagar")

        total = p_encender + p_ajustar + p_apagar
        if abs(total - 1.0) <= 0.01:
            break

        print("[ERROR] Las probabilidades deben sumar 1. Intenta de nuevo.\n")

    cpd[(presencia, luz, hora)] = {
        "Encender": p_encender,
        "Ajustar": p_ajustar,
        "Apagar": p_apagar
    }

    print("[OK] Regla CPD agregada correctamente")