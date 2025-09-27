# app/models/invernadero.py

# --- Importación Robusta ---
try:
    from ..structures.lista_enlazada import ListaEnlazada
    from .planta import Planta
    from .dron import Dron
    from .plan_riego import PlanRiego
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from app.structures.lista_enlazada import ListaEnlazada
    from app.models.planta import Planta
    from app.models.dron import Dron
    from app.models.plan_riego import PlanRiego


class Invernadero:
    """
    Representa el invernadero completo. Contiene las hileras de plantas,
    los drones asignados y los planes de riego disponibles.
    """
    def __init__(self, nombre, num_hileras, plantas_por_hilera):
        self.nombre = nombre
        self.num_hileras = int(num_hileras)
        self.plantas_por_hilera = int(plantas_por_hilera)
        
        # Estructura principal: Una lista de listas.
        # Cada elemento de 'hileras' es otra ListaEnlazada que representa una hilera.
        self.hileras = ListaEnlazada()
        for _ in range(self.num_hileras):
            self.hileras.insertar_al_final(ListaEnlazada())
            
        self.drones_asignados = ListaEnlazada()
        self.planes = ListaEnlazada()

    def agregar_planta(self, planta: Planta):
        """
        Agrega un objeto Planta a la hilera correspondiente.
        """
        # Los índices de las listas empiezan en 0, pero las hileras en 1.
        indice_hilera = planta.hilera - 1
        if 0 <= indice_hilera < len(self.hileras):
            hilera_correcta = self.hileras.obtener_por_indice(indice_hilera)
            hilera_correcta.insertar_al_final(planta)
        else:
            print(f"Error: La hilera {planta.hilera} está fuera de rango para la planta {planta.nombre}.")

    def asignar_dron(self, dron: Dron):
        self.drones_asignados.insertar_al_final(dron)

    def agregar_plan(self, plan: PlanRiego):
        self.planes.insertar_al_final(plan)

    def obtener_planta(self, num_hilera, num_posicion):
        """
        Busca y devuelve un objeto Planta específico por su hilera y posición.
        """
        indice_hilera = num_hilera - 1
        if 0 <= indice_hilera < len(self.hileras):
            hilera = self.hileras.obtener_por_indice(indice_hilera)
            actual = hilera.cabeza
            while actual is not None:
                planta = actual.dato
                if planta.posicion == num_posicion:
                    return planta
                actual = actual.siguiente
        return None # No se encontró la planta

    def __str__(self):
        total_plantas = sum(len(h) for h in [self.hileras.obtener_por_indice(i) for i in range(len(self.hileras))])
        return (f"Invernadero(Nombre: '{self.nombre}', "
                f"Drones: {len(self.drones_asignados)}, Plantas: {total_plantas}, "
                f"Planes: {len(self.planes)})")


# --- Bloque de Prueba ---
if __name__ == '__main__':
    # 1. Crear un invernadero de 2 hileras y 2 plantas por hilera
    inv_prueba = Invernadero(nombre="Invernadero Demo", num_hileras=2, plantas_por_hilera=2)
    print(inv_prueba)

    # 2. Crear y agregar plantas
    inv_prueba.agregar_planta(Planta(1, 1, "Tomate", 0.5, 50))
    inv_prueba.agregar_planta(Planta(2, 1, "Lechuga", 0.4, 30))
    inv_prueba.agregar_planta(Planta(1, 2, "Zanahoria", 0.6, 60))
    inv_prueba.agregar_planta(Planta(2, 2, "Pimiento", 0.7, 70))
    
    # 3. Crear, asignar y agregar drones
    dron1 = Dron(1, "DR01")
    dron1.asignar_hilera(1)
    inv_prueba.asignar_dron(dron1)
    
    dron2 = Dron(2, "DR02")
    dron2.asignar_hilera(2)
    inv_prueba.asignar_dron(dron2)

    # 4. Crear y agregar planes de riego
    plan1 = PlanRiego("Diario", "H1-P1,H2-P2")
    inv_prueba.agregar_plan(plan1)

    print("\nEstado del invernadero después de cargarlo:")
    print(inv_prueba)

    # 5. Probar los métodos de obtención
    print("\n--- Probando obtener datos ---")
    planta_buscada = inv_prueba.obtener_planta(num_hilera=2, num_posicion=1)
    if planta_buscada:
        print(f"Planta encontrada: {planta_buscada}")
    else:
        print("No se encontró la planta H2-P1.")