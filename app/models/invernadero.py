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

#creamos una clase de ayuda. 
class Asignacion:
    """Almacena la relacion entre un dron y la hilera a la que está asignado"""
    def __init__(self, dron, hilera):
        self.dron = dron
        self.hilera = int(hilera)


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
        
        #Se almacena objetos asignacion 
        self.asignaciones_drones = ListaEnlazada()
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

    def asignar_dron(self, dron: Dron, hilera_id:int):

        nueva_asignacion = Asignacion(dron, hilera_id)
        self.asignaciones_drones.insertar_al_final(nueva_asignacion)

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
                f"Drones: {len(self.drones_asignaciones_drones)}, Plantas: {total_plantas}, "
                f"Planes: {len(self.planes)})")


