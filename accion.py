from dataclasses import dataclass

@dataclass(frozen=True)
class Accion:
    tipo: str
    intensidad: int | None = 0
    delay: int = 0  # segundos

    def ejecutar(self) -> None:
        if self.delay > 0:
            mins = self.delay // 60
            secs = self.delay % 60

            if self.intensidad is None:
                # CPD
                if mins > 0 and secs == 0:
                    print(f"Acción: {self.tipo} después de {mins} min")
                else:
                    print(f"Acción: {self.tipo} después de {self.delay} s")
            else:
                return None

        else:
            if self.intensidad is None:
                # CPD
                print(f"Acción: {self.tipo}")
            else:
                return None