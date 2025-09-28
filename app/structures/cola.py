# app/structures/cola.py

# Importamos las clases del archivo vecino.
from .lista_enlazada import Nodo, ListaEnlazada

class Cola:
    """
    Implementación de una estructura de datos tipo Cola (Queue).
    Utiliza el principio FIFO (First-In, First-Out).
    Está construida sobre nuestra propia ListaEnlazada.
    """
    def __init__(self):
        """
        Inicializa la cola vacía.
        """
        self._lista = ListaEnlazada()

    def encolar(self, dato):
        """
        Añade un elemento al final de la cola.
        Corresponde a insertar al final de nuestra lista enlazada.
        """
        self._lista.insertar_al_final(dato)

    def desencolar(self):
        """
        Elimina y devuelve el elemento del frente de la cola.
        Corresponde a obtener y eliminar la cabeza de la lista enlazada.
        """
        if self.esta_vacia():
            return None
        
        # Obtenemos el dato de la cabeza.
        dato_a_devolver = self._lista.cabeza.dato
        
        # Movemos la cabeza al siguiente nodo, eliminando el primero.
        self._lista.cabeza = self._lista.cabeza.siguiente
        self._lista.longitud -= 1
        
        return dato_a_devolver

    def ver_frente(self):
        """
        Devuelve el elemento del frente de la cola sin eliminarlo.
        """
        if self.esta_vacia():
            return None
        return self._lista.cabeza.dato

    def esta_vacia(self):
        """
        Verifica si la cola no tiene elementos.
        """
        return self._lista.cabeza is None

    def __len__(self):
        """
        Permite usar la función len() sobre la cola.
        """
        return len(self._lista)

    def recorrer_y_mostrar(self):
        """
        Método auxiliar para visualizar el contenido de la cola.
        """
        if self.esta_vacia():
            print("La cola está vacía.")
        else:
            print("Frente -> ", end="")
            self._lista.recorrer_y_mostrar()


# --- Bloque de Prueba ---
if __name__ == '__main__':
    plan_de_riego = Cola()
    
    print("Encolando los pasos del plan de riego...")
    plan_de_riego.encolar('H1-P2')
    plan_de_riego.encolar('H2-P1')
    plan_de_riego.encolar('H2-P2')
    
    plan_de_riego.recorrer_y_mostrar()
    print(f"Longitud de la cola: {len(plan_de_riego)}")
    
    print("\nProcesando el primer paso...")
    primer_paso = plan_de_riego.desencolar()
    print(f"Paso a ejecutar: {primer_paso}") # Debería ser 'H1-P2'
    
    print("Estado de la cola después de desencolar:")
    plan_de_riego.recorrer_y_mostrar()
    
    print(f"\nEl siguiente paso en el frente es: {plan_de_riego.ver_frente()}") # Debería ser 'H2-P1'
    
    print("\nDesencolando todos los elementos...")
    plan_de_riego.desencolar()
    plan_de_riego.desencolar()
    
    if plan_de_riego.esta_vacia():
        print("La cola ahora está vacía.")