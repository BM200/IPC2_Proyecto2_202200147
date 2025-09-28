
class Planta:
    """
    Representa una planta individual en el invernadero.
    Contiene sus características y posición.
    """
    def __init__(self, posicion, hilera, nombre, litros_agua, gramos_fertilizante):
        self.posicion = int(posicion)
        self.hilera = int(hilera)
        self.nombre = nombre
        self.litros_agua = float(litros_agua)
        self.gramos_fertilizante = float(gramos_fertilizante)

    def __str__(self):
        """
        Devuelve una representación en string del objeto Planta.
        Es muy útil para la depuración, ya que puedes hacer print(objeto_planta).
        """
        return (f"Planta(Nombre: {self.nombre}, Pos: H{self.hilera}-P{self.posicion}, "
                f"Agua: {self.litros_agua}L, Fert: {self.gramos_fertilizante}g)")

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # Creamos dos instancias de la clase Planta
    planta_cipres = Planta(
        posicion=1, 
        hilera=1, 
        nombre="ciprés", 
        litros_agua=1, 
        gramos_fertilizante=100
    )
    
    planta_italiano = Planta(
        posicion=2, 
        hilera=1, 
        nombre="ciprés italiano", 
        litros_agua=1.5, 
        gramos_fertilizante=120
    )
    
    # Usamos el método __str__ implícitamente al imprimir los objetos
    print("Se han creado los siguientes objetos Planta:")
    print(planta_cipres)
    print(planta_italiano)
    
    # Accedemos a sus atributos
    print(f"\nEl fertilizante requerido por el {planta_italiano.nombre} es de {planta_italiano.gramos_fertilizante} gramos.")