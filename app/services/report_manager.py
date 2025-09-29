from graphviz import Digraph
import os
import time

def generar_grafo_tda(lista_tareas_en_t, tiempo_t):
    """
    Genera una imagen PNG a partir de una LISTA DE STRINGS que representa
    el estado de la cola en un tiempo 't'.
    """
    dot = Digraph(comment=f'Estado de la Cola en t={tiempo_t}')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    dot.attr(rankdir='LR')
    dot.attr(label=f'Estado de la Cola de Tareas en t={tiempo_t}s', labelloc='t', fontsize='16')

    dot.node('frente', 'FRENTE', shape='plaintext')
    
    if not lista_tareas_en_t:
        dot.node('vacia', 'Cola Vacía', fillcolor='lightgrey')
        dot.edge('frente', 'vacia')
    else:
        dot.edge('frente', lista_tareas_en_t[0])
        for i in range(len(lista_tareas_en_t) - 1):
            dot.edge(lista_tareas_en_t[i], lista_tareas_en_t[i+1])

    output_dir = os.path.join('app', 'static', 'graphs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = int(time.time())
    nombre_archivo_png = f'grafo_tda_{timestamp}.png'
    nombre_archivo_base = f'grafo_tda_{timestamp}'
    ruta_base_sin_extension = os.path.join(output_dir, nombre_archivo_base)

    dot.render(ruta_base_sin_extension, format='png', cleanup=True)
    
    return f'graphs/{nombre_archivo_png}'