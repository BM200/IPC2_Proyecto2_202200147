# app/routes.py
from app import app
from flask import render_template, request, redirect, url_for, send_from_directory, flash
import os
import copy # Importante para hacer copias de los planes

# Importamos las clases necesarias del proyecto
from app.services.xml_manager import XMLManager
from app.models.simulador import Simulador
from app.services.report_manager import generar_grafo_tda


# Variable global para almacenar los datos cargados del XML.
datos_cargados = None

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal. Maneja la visualización de la página (GET) y el
    procesamiento de una simulación individual (POST).
    """
    global datos_cargados
    resultados_simulacion = None

    if request.method == 'POST':
        nombre_invernadero_sel = request.form.get('invernadero')
        nombre_plan_sel = request.form.get('plan_riego')

        inv_a_simular = None
        if datos_cargados:
            for invernadero in datos_cargados:
                if invernadero.nombre == nombre_invernadero_sel:
                    inv_a_simular = invernadero
                    break
        
        plan_a_simular_original = None
        if inv_a_simular:
            for plan in inv_a_simular.planes:
                if plan.nombre == nombre_plan_sel:
                    plan_a_simular_original = copy.deepcopy(plan)
                    break

        if inv_a_simular and plan_a_simular_original:
            sim = Simulador(inv_a_simular, plan_a_simular_original)
            sim.ejecutar_simulacion()
            resultados_simulacion = sim.obtener_resultados()
            flash(f"Simulación para '{nombre_plan_sel}' en '{nombre_invernadero_sel}' completada.", "success")

    # Preparación de datos para los menús desplegables en el frontend
    planes_data_json = "{}"
    if datos_cargados:
        json_builder = []
        for invernadero in datos_cargados:
            nombres_planes = [f'"{plan.nombre}"' for plan in invernadero.planes]
            json_builder.append(f'"{invernadero.nombre}": [{",".join(nombres_planes)}]')
        planes_data_json = "{" + ",".join(json_builder) + "}"

    return render_template('index.html',
                           invernaderos=datos_cargados,
                           planes_data_json=planes_data_json,
                           resultados=resultados_simulacion)

@app.route('/cargar', methods=['POST'])
def cargar_archivo():
    """
    Procesa la carga del archivo XML, lo parsea y redirige a la página principal.
    """
    global datos_cargados
    datos_cargados = None

    if 'archivo_xml' not in request.files:
        flash("No se encontró el archivo en la petición.", "error")
        return redirect(url_for('index'))
    
    file = request.files['archivo_xml']
    if file.filename == '':
        flash("No se seleccionó ningún archivo.", "error")
        return redirect(url_for('index'))
    
    uploads_dir = os.path.join(app.root_path, '..', 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        
    ruta_guardado = os.path.join(uploads_dir, file.filename)
    file.save(ruta_guardado)
    
    manejador = XMLManager()
    datos_cargados = manejador.parsear_entrada(ruta_guardado)

    if datos_cargados:
        flash(f"Archivo '{file.filename}' cargado exitosamente.", "success")
    else:
        flash(f"Error al procesar el archivo '{file.filename}'. Revise el formato.", "error")

    return redirect(url_for('index'))

@app.route('/generar-salida', methods=['POST'])
def generar_archivo_salida():
    """
    Ejecuta la simulación para TODOS los planes de TODOS los invernaderos
    cargados y genera el archivo 'salida.xml' para su descarga.
    """
    if not datos_cargados:
        flash("No hay datos cargados para generar el archivo de salida.", "error")
        return redirect(url_for('index'))

    todos_los_resultados = []
    # Itera sobre todos los invernaderos y sus planes, ejecutando una simulación para cada uno.
    for invernadero in datos_cargados:
        for plan in invernadero.planes:
            plan_copiado = copy.deepcopy(plan)
            sim = Simulador(invernadero, plan_copiado)
            sim.ejecutar_simulacion()
            todos_los_resultados.append(sim.obtener_resultados())
    
    # Define el directorio de salida y lo crea si no existe
    output_dir = os.path.join(app.root_path, '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ruta_salida = os.path.join(output_dir, 'salida.xml')
    
    # Llama al XMLManager para generar el archivo con los resultados compilados
    manejador = XMLManager()
    manejador.generar_salida(todos_los_resultados, ruta_salida)
    
    # Envía el archivo generado al usuario para que lo descargue
    return send_from_directory(directory=output_dir, path='salida.xml', as_attachment=True)

@app.route('/reporte-general')
def reporte_general():
    if not datos_cargados:
        flash("Carga un archivo de configuración primero para ver el reporte.", "error")
        return redirect(url_for('index'))

    # La lógica es idéntica a la de 'generar_archivo_salida'
    todos_los_resultados = []
    for invernadero in datos_cargados:
        for plan in invernadero.planes:
            plan_copiado = copy.deepcopy(plan)
            sim = Simulador(invernadero, plan_copiado)
            sim.ejecutar_simulacion()
            todos_los_resultados.append(sim.obtener_resultados())

    # Pasamos la lista completa de resultados a la nueva plantilla
    return render_template('reporte_general.html', lista_resultados=todos_los_resultados)


#////////////////////////////////////////
@app.route('/generar-grafo', methods=['POST'])
def generar_grafo():
    """
    Genera el grafo del TDA para un plan específico y vuelve a mostrar
    la página principal con la imagen del grafo.
    """
    nombre_invernadero_sel = request.form.get('nombre_invernadero')
    nombre_plan_sel = request.form.get('nombre_plan')

    # Reutilizamos los resultados de la simulación anterior si están disponibles
    # Opcional: podrías volver a simular aquí si fuera necesario
    # Por simplicidad, encontraremos el plan original y lo graficaremos.
    
    inv_seleccionado = None
    if datos_cargados:
        for invernadero in datos_cargados:
            if invernadero.nombre == nombre_invernadero_sel:
                inv_seleccionado = invernadero
                break
    
    plan_seleccionado = None
    if inv_seleccionado:
        for plan in inv_seleccionado.planes:
            if plan.nombre == nombre_plan_sel:
                plan_seleccionado = plan
                break

    ruta_del_grafo = None
    if plan_seleccionado:
        # Llamamos a nuestra nueva función para generar el grafo
        ruta_del_grafo = generar_grafo_tda(plan_seleccionado)
        flash("Gráfico del TDA generado exitosamente.", "success")
    else:
        flash("No se pudo encontrar el plan para generar el gráfico.", "error")

    # --- Re-renderizamos la página principal ---
    # Es necesario volver a preparar los datos para la plantilla
    
    planes_data_json = "{}"
    if datos_cargados:
        json_builder = []
        for invernadero in datos_cargados:
            nombres_planes = [f'"{plan.nombre}"' for plan in invernadero.planes]
            json_builder.append(f'"{invernadero.nombre}": [{",".join(nombres_planes)}]')
        planes_data_json = "{" + ",".join(json_builder) + "}"

    # Volvemos a renderizar 'index.html', pero esta vez pasándole la ruta del grafo.
    # El bloque de resultados no se mostrará, pero el del grafo sí.
    # Para que ambos se muestren, necesitaríamos una lógica más compleja de sesión.
    # Por ahora, nos enfocamos en mostrar el grafo.
    return render_template('index.html',
                           invernaderos=datos_cargados,
                           planes_data_json=planes_data_json,
                           # Pasamos la ruta de la imagen a la plantilla
                           grafo_path=ruta_del_grafo)