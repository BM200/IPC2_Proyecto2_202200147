# app/models/dron.py

class Dron:
    """
    Representa a un dron regador.
    Mantiene su estado (posición, recursos consumidos) durante la simulación.
    """
    def __init__(self, id, nombre):
        # Atributos de identificación (no cambian)
        self.id = int(id)
        self.nombre = nombre
        self.hilera_asignada = None # Se asignará después de la creación

        # Atributos de estado (cambian durante la simulación)
        self.posicion_actual = 0
        self.litros_agua_consumidos = 0.0
        self.gramos_fert_consumidos = 0.0
        self.estado = "en_base" # Estados: en_base, moviendo, regando, esperando, regresando, finalizado

    def asignar_hilera(self, hilera_id):
        """
        Asigna el dron a una hilera específica.
        """
        self.hilera_asignada = int(hilera_id)

    def resetear(self):
        """
        Reinicia el estado del dron para una nueva simulación.
        Es crucial para poder ejecutar múltiples planes sin mezclar datos.
        """
        self.posicion_actual = 0
        self.litros_agua_consumidos = 0.0
        self.gramos_fert_consumidos = 0.0
        self.estado = "en_base"
        print(f"Dron {self.nombre} ha sido reseteado a su estado inicial.")

    def consumir_recursos(self, litros_agua, gramos_fertilizante):
        """
        Actualiza los contadores de recursos consumidos.
        """
        self.litros_agua_consumidos += litros_agua
        self.gramos_fert_consumidos += gramos_fertilizante

    def __str__(self):
        """
        Representación en string para depuración.
        """
        return (f"Dron(ID: {self.id}, Nombre: {self.nombre}, "
                f"Hilera: {self.hilera_asignada}, Pos: {self.posicion_actual}, "
                f"Estado: {self.estado})")

