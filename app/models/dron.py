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

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # Creamos un dron
    dron1 = Dron(id=1, nombre='DR01')
    dron1.asignar_hilera(1)
    
    print("Estado inicial del dron:")
    print(dron1)
    
    # Simulamos algunas acciones
    print("\nSimulando acciones...")
    dron1.estado = "moviendo"
    dron1.posicion_actual = 2
    print("Después de moverse:")
    print(dron1)
    
    dron1.estado = "regando"
    dron1.consumir_recursos(litros_agua=1.0, gramos_fertilizante=100.0)
    print("Después de regar:")
    print(dron1)
    print(f"Total agua consumida: {dron1.litros_agua_consumidos} L")
    print(f"Total fertilizante consumido: {dron1.gramos_fert_consumidos} g")
    
    # Probamos la función de reseteo
    print("\nProbando el reseteo para una nueva simulación...")
    dron1.resetear()
    print("Estado después de resetear:")
    print(dron1)