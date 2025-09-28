# --- Importación Robusta ---
# Este bloque try-except nos permite ejecutar este archivo directamente para pruebas,
# sin que falle la importación relativa que necesitará Flask.
try:
    # Intenta una importación relativa (para cuando se ejecuta como parte del paquete 'app')
    from ..structures.cola import Cola
except ImportError:
    # Si falla, es porque lo estamos ejecutando directamente.
    # Hacemos una importación directa (asumiendo que la terminal está en la raíz del proyecto).
    import sys
    import os
    # Añadimos la raíz del proyecto al path para encontrar la carpeta 'app'
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from app.structures.cola import Cola


class PlanRiego:
    """
    Representa un plan de riego específico para un invernadero.
    Convierte la secuencia de texto del plan en una Cola de instrucciones.
    """
    def __init__(self, nombre, secuencia_str):
        self.nombre = nombre
        self.secuencia_cola = Cola()
        self._cargar_secuencia(secuencia_str)

    def _cargar_secuencia(self, secuencia_str):
        """
        Método privado para procesar el string de la secuencia y llenar la Cola.
        """
        # Limpiamos espacios en blanco y dividimos el string por la coma.
        pasos = [paso.strip() for paso in secuencia_str.split(',')]
        
        # Encolamos cada paso en nuestra estructura de datos.
        for paso in pasos:
            if paso: # Asegurarnos de no encolar strings vacíos
                self.secuencia_cola.encolar(paso)

    def __str__(self):
        """
        Representación en string para depuración.
        """
        return (f"PlanRiego(Nombre: '{self.nombre}', "
                f"Pasos en cola: {len(self.secuencia_cola)})")

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # String de ejemplo, similar al del archivo XML
    secuencia_ejemplo = "H1-P2, H2-P1, H2-P2, H3-P3, H1-P4"
    
    # Creamos una instancia del plan
    plan_semana_1 = PlanRiego(nombre="Semana 1", secuencia_str=secuencia_ejemplo)
    
    print("Objeto PlanRiego creado:")
    print(plan_semana_1)
    
    print("\nVerificando el contenido de la Cola interna...")
    print(f"El primer paso a ejecutar es: '{plan_semana_1.secuencia_cola.ver_frente()}'")
    
    # Simulamos el procesamiento de dos pasos
    print("\nProcesando primer paso...")
    paso1 = plan_semana_1.secuencia_cola.desencolar()
    print(f"Se procesó: {paso1}")
    
    print("Procesando segundo paso...")
    paso2 = plan_semana_1.secuencia_cola.desencolar()
    print(f"Se procesó: {paso2}")
    
    print("\nEstado actual de la cola:")
    print(f"El siguiente paso a ejecutar es: '{plan_semana_1.secuencia_cola.ver_frente()}'")
    print(f"Pasos restantes: {len(plan_semana_1.secuencia_cola)}")