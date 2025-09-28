# app/services/report_manager.py
from graphviz import Digraph
import os
import time # Para añadir un timestamp y evitar problemas de caché del navegador

def generar_grafo_tda(plan_de_riego):
    """
    Genera una imagen PNG que representa el estado actual de la Cola de tareas.
    Devuelve la ruta web a la imagen generada.
    """
    # Creamos un nuevo grafo dirigido. 'LR' significa Left to Right (de izquierda a derecha).
    dot = Digraph(comment='Estado de la Cola de Tareas')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    dot.attr(rankdir='LR')

    # Nodo inicial que representa el "Frente" de la cola.
    dot.node('frente', 'FRENTE', shape='plaintext')
    
    # Recorremos la cola a través de su lista enlazada interna
    nodo_actual = plan_de_riego.secuencia_cola._lista.cabeza
    
    if not nodo_actual:
        # Si la cola está vacía, lo indicamos.
        dot.node('vacia', 'Cola Vacía', fillcolor='lightgrey')
        dot.edge('frente', 'vacia')
    else:
        # El primer nodo (el del frente) se conecta al indicador "FRENTE".
        dot.edge('frente', nodo_actual.dato)
        
        # Recorremos el resto de la lista para crear los nodos y las flechas.
        while nodo_actual and nodo_actual.siguiente:
            dot.edge(nodo_actual.dato, nodo_actual.siguiente.dato)
            nodo_actual = nodo_actual.siguiente

    # --- Guardado del archivo ---
    # La imagen se guardará en la carpeta 'static' para que el navegador pueda acceder a ella.
    output_dir = os.path.join('app', 'static', 'graphs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Renderizamos el grafo. cleanup=True borra el archivo fuente DOT después de crear el PNG.
    # Le añadimos un timestamp al nombre para que cada imagen sea única.
    timestamp = int(time.time())
    ruta_base = os.path.join(output_dir, f'grafo_tda_{timestamp}')
    dot.render(ruta_base, format='png', cleanup=True)
    
    # Devolvemos la RUTA WEB a la imagen.
    return f'static/graphs/grafo_tda_{timestamp}.png'