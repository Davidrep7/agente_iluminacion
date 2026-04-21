from cpd import agregar_regla_cpd, eliminar_regla_cpd, mostrar_tabla_cpd
from percepcion import Percepcion
from agente import AgenteIluminacion

def obtener_datos() -> Percepcion | None:
    """Solicita datos al usuario y crea una Percepcion si son válidos."""
    try:
        print("\n--- Ingresa los datos de la percepción ---")
        
        # Luz natural
        while True:
            luz = int(input("Luz natural (lux): "))
            if luz >= 0:
                break
            print("[ERROR] La luz natural no puede ser negativa.")
        
        presencia_input = input("¿Hay presencia? (s/n): ").strip().lower()
        presencia = presencia_input == 's'
            
        # Hora
        while True:
            hora = input("Tipo de hora (diurna/nocturna): ").strip().lower()
            if hora in ("diurna", "nocturna"):
                break
            print("[ERROR] Ingresa 'diurna' o 'nocturna'")
        
        # Intensidad actual
        while True:
            intensidad = int(input("Intensidad actual (0-100%): "))
            if 0 <= intensidad <= 100:
                break
            print("[ERROR] La intensidad debe estar entre 0 y 100.")
        
        percepcion = Percepcion(luz, presencia, hora, intensidad)
        
        if percepcion.es_valida():
            return percepcion
        else:
            return None
    
    except ValueError:
        print("Error: ingresa números válidos.")
        return None


def mostrar_menu() -> str:
    """Muestra el menú principal y retorna la opción seleccionada."""
    print("\n" + "="*60)
    print("SISTEMA DE AGENTE DE ILUMINACIÓN INTELIGENTE")
    print("="*60)
    print("1. Procesar percepción CPD (probabilístico)")
    print("2. Agregar regla probabilística (CPD)")
    print("3. Mostrar tabla probabilística CPD")
    print("4. Eliminar regla probabilística CPD")
    print("5. Salir")
    print("="*60)
    return input("Selecciona una opción (1-5): ").strip()


def procesar_percepcion(agente: AgenteIluminacion) -> None:
    percepcion = obtener_datos()
    if percepcion is None:
        return

    print(f"\n[PERCEPCIÓN]")
    print(f"  Luz: {percepcion.luz_natural} lux")
    print(f"  Presencia: {'Sí' if percepcion.presencia else 'No'}")
    print(f"  Hora: {percepcion.hora_tipo}")
    print(f"  Intensidad actual: {percepcion.intensidad_actual}%\n")

    print("[MODO] Probabilístico (CPD)")

    accion = agente.decidir_accion(percepcion, usar_cpd_only=True)

    print("\n[RESULTADO]")
    accion.ejecutar()


def main() -> None:
    agente = AgenteIluminacion()

    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            procesar_percepcion(agente)

        elif opcion == "2":
            agregar_regla_cpd()
            
        elif opcion == "3":
            mostrar_tabla_cpd()

        elif opcion == "4":
            eliminar_regla_cpd()

        elif opcion == "5":
            print("\n¡Adios!")
            break

        else:
            print("[ERROR] Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()