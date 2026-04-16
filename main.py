from cpd import agregar_regla_cpd, eliminar_regla_cpd, mostrar_tabla_cpd
from percepcion import Percepcion
from agente import AgenteIluminacion
from accion import Accion
from regla import Regla

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
        
        # Validar la percepción usando el método es_valida()
        if percepcion.es_valida():
            return percepcion
        else:
            return None
    
    except ValueError:
        print("Error: ingresa números válidos.")
        return None

def crear_regla(agente: AgenteIluminacion) -> None:
    """Permite al usuario crear una nueva regla inteligente con condiciones personalizadas."""
    try:
        print("\n" + "="*60)
        print("CREAR NUEVA REGLA INTELIGENTE")
        print("="*60)
        
        # 1. Nombre de la regla
        nombre = input("\nNombre de la regla: ").strip()
        if not nombre:
            print("[ERROR] El nombre no puede estar vacío.")
            return
        
        # 1.5. Prioridad de la regla
        print("\nPrioridad de la regla (0-10, donde 10 es máxima prioridad):")
        try:
            prioridad = int(input("Prioridad: ").strip())
            if not (0 <= prioridad <= 10):
                print("[ERROR] La prioridad debe estar entre 0 y 10.")
                return
        except ValueError:
            print("[ERROR] Ingresa un número válido para la prioridad.")
            return
        
        # 2. Condiciones de la regla
        print("\n--- CONDICIONES DE LA REGLA ---")
        
        # Luz natural
        print("\n1. Luz natural:")
        luz_min = None
        luz_max = None
        luz_tipo = None  # 'rango', 'menor', 'mayor', o None (cualquiera)
        
        print("   Opciones: (1) Rango  (2) Menor que  (3) Mayor que  (4) Cualquiera")
        luz_op = input("   Selecciona (1-4): ").strip()
        
        if luz_op == '1':
            try:
                luz_min = int(input("   Luz mínima (lux): "))
                luz_max = int(input("   Luz máxima (lux): "))
                if luz_min > luz_max:
                    print("[ERROR] Luz mínima no puede ser mayor que máxima.")
                    return
                luz_tipo = 'rango'
            except ValueError:
                print("[ERROR] Ingresa números válidos.")
                return
        elif luz_op == '2':
            try:
                luz_max = int(input("   Luz menor que (lux): "))
                luz_tipo = 'menor'
            except ValueError:
                print("[ERROR] Ingresa un número válido.")
                return
        elif luz_op == '3':
            try:
                luz_min = int(input("   Luz mayor que (lux): "))
                luz_tipo = 'mayor'
            except ValueError:
                print("[ERROR] Ingresa un número válido.")
                return
        
        # Intensidad actual
        print("\n2. Intensidad actual:")
        intensidad_cond = None
        intensidad_valor = None
        print("   Opciones: (1) Menor que  (2) Mayor que  (3) Igual a  (4) Cualquiera")
        intensidad_op = input("   Selecciona (1-4): ").strip()
        if intensidad_op in ['1', '2', '3']:
            try:
                intensidad_valor = int(input("   Intensidad (0-100): "))
                if not (0 <= intensidad_valor <= 100):
                    print("[ERROR] Intensidad debe estar entre 0 y 100.")
                    return
                intensidad_cond = intensidad_op
            except ValueError:
                print("[ERROR] Ingresa un número válido.")
                return
        
        # Presencia
        print("\n3. Presencia:")
        presencia_cond = None
        print("   Opciones: (1) Sí  (2) No  (3) Cualquiera")
        presencia_op = input("   Selecciona (1-3): ").strip()
        if presencia_op == '1':
            presencia_cond = True
        elif presencia_op == '2':
            presencia_cond = False
        
        # Hora
        print("\n4. Tipo de hora:")
        hora_cond = None
        print("   Opciones: (1) Diurna  (2) Nocturna  (3) Cualquiera")
        hora_op = input("   Selecciona (1-3): ").strip()
        if hora_op == '1':
            hora_cond = "diurna"
        elif hora_op == '2':
            hora_cond = "nocturna"
        
        # 3. Acción
        print("\n--- ACCIÓN DE LA REGLA ---")
        print("Tipos de acción: ENCENDER, APAGAR, AJUSTAR, MANTENER")
        tipo_accion = input("Tipo de acción: ").strip().upper()
        
        if tipo_accion not in ["ENCENDER", "APAGAR", "AJUSTAR", "MANTENER"]:
            print("[ERROR] Tipo de acción no válido.")
            return
        
        intensidad_accion = 0
        if tipo_accion in ["ENCENDER", "AJUSTAR"]:
            try:
                intensidad_accion = int(input("Intensidad resultante (0-100): "))
                if not (0 <= intensidad_accion <= 100):
                    print("[ERROR] Intensidad debe estar entre 0 y 100.")
                    return
            except ValueError:
                print("[ERROR] Intensidad debe ser un número.")
                return
        
        delay = 0
        agregar_delay = input("¿Agregar delay? (s/n): ").strip().lower()
        if agregar_delay == 's':
            try:
                delay = int(input("Delay en segundos: "))
            except ValueError:
                print("[ERROR] Delay debe ser un número.")
                return
        
        # 4. Crear la condición dinámica
        def crear_condicion(luz_tipo, luz_min, luz_max, intensidad_cond, intensidad_valor, presencia_cond, hora_cond):
            def condicion(p: Percepcion) -> bool:
                # Verificar luz natural
                if luz_tipo == 'rango':
                    if not (luz_min <= p.luz_natural <= luz_max):
                        return False
                elif luz_tipo == 'menor':
                    if p.luz_natural >= luz_max:
                        return False
                elif luz_tipo == 'mayor':
                    if p.luz_natural <= luz_min:
                        return False
                
                # Verificar intensidad actual
                if intensidad_cond is not None and intensidad_valor is not None:
                    if intensidad_cond == '1':  # Menor que
                        if p.intensidad_actual >= intensidad_valor:
                            return False
                    elif intensidad_cond == '2':  # Mayor que
                        if p.intensidad_actual <= intensidad_valor:
                            return False
                    elif intensidad_cond == '3':  # Igual a
                        if p.intensidad_actual != intensidad_valor:
                            return False
                
                # Verificar presencia
                if presencia_cond is not None:
                    if p.presencia != presencia_cond:
                        return False
                
                # Verificar hora
                if hora_cond is not None:
                    if p.hora_tipo.strip().lower() != hora_cond:
                        return False
                
                return True
            return condicion
        
        # Crear la regla
        nueva_regla = Regla(
            nombre=nombre,
            condicion=crear_condicion(luz_tipo, luz_min, luz_max, intensidad_cond, intensidad_valor, presencia_cond, hora_cond),
            accion=lambda p: Accion(tipo_accion, intensidad_accion, delay),
            prioridad=prioridad
        )
        
        agente.motor.agregar_regla(nueva_regla)
        
        # Mostrar confirmación
        print(f"\n{'='*60}")
        print(f"✓ REGLA CREADA: {nombre}")
        print(f"Prioridad: {prioridad}/10")
        print(f"{'='*60}")
        print("CONDICIONES:")
        if luz_tipo == 'rango':
            print(f"  • Luz natural: {luz_min}-{luz_max} lux")
        elif luz_tipo == 'menor':
            print(f"  • Luz natural: menor que {luz_max} lux")
        elif luz_tipo == 'mayor':
            print(f"  • Luz natural: mayor que {luz_min} lux")
        else:
            print(f"  • Luz natural: Cualquiera")
        if intensidad_cond is not None and intensidad_valor is not None:
            op_str = "menor que" if intensidad_cond == '1' else "mayor que" if intensidad_cond == '2' else "igual a"
            print(f"  • Intensidad actual: {op_str} {intensidad_valor}%")
        if presencia_cond is not None:
            print(f"  • Presencia: {'Sí' if presencia_cond else 'No'}")
        if hora_cond is not None:
            print(f"  • Hora: {hora_cond.capitalize()}")
        print("\nACCIÓN:")
        print(f"  • Tipo: {tipo_accion} -> {intensidad_accion}%" + (f" (delay: {delay}s)" if delay > 0 else ""))
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"[ERROR] No se pudo crear la regla: {e}")

def eliminar_regla(agente: AgenteIluminacion) -> None:
    """Permite al usuario seleccionar y eliminar una regla del motor de inferencia."""
    reglas = agente.motor.obtener_reglas_ordenadas()
    if not reglas:
        print("\n[INFO] No hay reglas para eliminar.")
        return

    print("\n" + "="*60)
    print("ELIMINAR REGLA")
    print("="*60)
    for idx, regla in enumerate(reglas, 1):
        print(f"{idx}. [{regla.prioridad}/10] {regla.nombre}")

    try:
        seleccion = int(input("Selecciona el número de la regla a eliminar (0 para cancelar): ").strip())
    except ValueError:
        print("[ERROR] Ingresa un número válido.")
        return

    if seleccion == 0:
        print("Operación cancelada.")
        return

    if agente.motor.eliminar_regla_por_indice(seleccion):
        print(f"\n[OK] Regla eliminada (posición {seleccion}).")
    else:
        print("[ERROR] Índice no válido. No se eliminó ninguna regla.")


def mostrar_menu() -> str:
    """Muestra el menú principal y retorna la opción seleccionada."""
    print("\n" + "="*60)
    print("SISTEMA DE AGENTE DE ILUMINACIÓN INTELIGENTE")
    print("="*60)
    print("1. Ver reglas existentes")
    print("2. Crear nueva regla")
    print("3. Eliminar regla")
    print("4. Procesar percepción")
    print("5. Procesar percepción CPD (probabilístico)")
    print("6. Agregar regla probabilística (CPD)")
    print("7. Mostrar tabla probabilística CPD")
    print("8. Eliminar regla probabilística CPD")
    print("9. Salir")
    print("="*60)
    return input("Selecciona una opción (1-9): ").strip()


def procesar_percepcion(agente: AgenteIluminacion, usar_cpd_only: bool = False) -> None:
    percepcion = obtener_datos()
    if percepcion is None:
        return

    print(f"  Luz: {percepcion.luz_natural} lux | Presencia: {'Sí' if percepcion.presencia else 'No'} | Hora: {percepcion.hora_tipo} | Intensidad: {percepcion.intensidad_actual}%")
    print()

    accion = agente.decidir_accion(percepcion, usar_cpd_only=usar_cpd_only)
    accion.ejecutar()


def main() -> None:
    agente = AgenteIluminacion()

    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            agente.motor.listar_reglas()
        
        elif opcion == "2":
            crear_regla(agente)
        
        elif opcion == "3":
            eliminar_regla(agente)

        elif opcion == "4":
            procesar_percepcion(agente, usar_cpd_only=False)

        elif opcion == "5":
            procesar_percepcion(agente, usar_cpd_only=True)
            
        elif opcion == "6":
            agregar_regla_cpd()

        elif opcion == "7":
            mostrar_tabla_cpd()

        elif opcion == "8":
            eliminar_regla_cpd()

        elif opcion == "9":
            print("\n¡Adios!")
            break

        else:
            print("[ERROR] Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()