class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0
        self._iter_nodo = None # Atributo para la iteración

    def insertar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.longitud += 1

    def obtener_por_indice(self, indice):
        if indice < 0 or indice >= self.longitud:
            return None
        actual = self.cabeza
        contador = 0
        while contador < indice:
            actual = actual.siguiente
            contador += 1
        return actual.dato

    def recorrer_y_mostrar(self):
        if self.cabeza is None:
            print("La lista está vacía.")
            return
        actual = self.cabeza
        print("Contenido de la lista:")
        while actual is not None:
            print(f"[{actual.dato}] -> ", end="")
            actual = actual.siguiente
        print("None")
        
    def __len__(self):
        return self.longitud

    # --- NUEVOS MÉTODOS PARA HACERLA ITERABLE ---
    def __iter__(self):
        """
        Prepara la lista para ser iterada. Se llama al inicio de un bucle for.
        """
        self._iter_nodo = self.cabeza
        return self

    def __next__(self):
        """
        Devuelve el siguiente elemento en la iteración.
        """
        if self._iter_nodo is None:
            # Fin de la iteración
            raise StopIteration
        else:
            # Devolvemos el dato actual y avanzamos al siguiente nodo
            dato_actual = self._iter_nodo.dato
            self._iter_nodo = self._iter_nodo.siguiente
            return dato_actual

# --- El bloque de prueba sigue igual ---
if __name__ == '__main__':
    lista_de_drones = ListaEnlazada()
    lista_de_drones.insertar_al_final('DR01')
    lista_de_drones.insertar_al_final('DR02')
    lista_de_drones.insertar_al_final('DR03')
    
    print("Probando el nuevo comportamiento iterable con un bucle for:")
    for dron in lista_de_drones:
        print(f"- {dron}")

    print("\nLa funcionalidad anterior sigue intacta:")
    lista_de_drones.recorrer_y_mostrar()