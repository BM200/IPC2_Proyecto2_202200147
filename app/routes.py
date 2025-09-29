# app/routes.py
from app import app
from flask import render_template, request, redirect, url_for, send_from_directory, flash, session
import os
import copy

from app.services.xml_manager import XMLManager
from app.models.simulador import Simulador
from app.services.report_manager import generar_grafo_tda

datos_cargados = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global datos_cargados
    
    if request.method == 'POST':
        # Limpia datos de un grafo anterior al iniciar una nueva simulación
        if 'grafo_path' in session: session.pop('grafo_path')
        if 'tiempo_solicitado' in session: session.pop('tiempo_solicitado')

        nombre_invernadero_sel = request.form.get('invernadero')
        nombre_plan_sel = request.form.get('plan_riego')
        
        inv_a_simular, plan_a_simular_original = None, None
        if datos_cargados:
            for invernadero in datos_cargados:
                if invernadero.nombre == nombre_invernadero_sel:
                    inv_a_simular = invernadero
                    break
        if inv_a_simular:
            for plan in inv_a_simular.planes:
                if plan.nombre == nombre_plan_sel:
                    plan_a_simular_original = copy.deepcopy(plan)
                    break
        
        if inv_a_simular and plan_a_simular_original:
            sim = Simulador(inv_a_simular, plan_a_simular_original)
            sim.ejecutar_simulacion()
            resultados = sim.obtener_resultados()
            session['resultados_simulacion'] = resultados
            flash("Simulación completada.", "success")
        
        return redirect(url_for('index'))

    planes_data_json = "{}"
    if datos_cargados:
        json_builder = []
        for invernadero in datos_cargados:
            nombres_planes = [f'"{plan.nombre}"' for plan in invernadero.planes]
            json_builder.append(f'"{invernadero.nombre}": [{",".join(nombres_planes)}]')
        planes_data_json = "{" + ",".join(json_builder) + "}"
    
    resultados_guardados = session.get('resultados_simulacion')
    grafo_guardado = session.get('grafo_path')
    tiempo_guardado = session.get('tiempo_solicitado')

    return render_template('index.html',
                           invernaderos=datos_cargados,
                           planes_data_json=planes_data_json,
                           resultados=resultados_guardados,
                           grafo_path=grafo_guardado,
                           tiempo_solicitado=tiempo_guardado)

@app.route('/cargar', methods=['POST'])
def cargar_archivo():
    global datos_cargados
    session.clear()
    datos_cargados = None
    if 'archivo_xml' not in request.files:
        flash("No se encontró el archivo.", "error")
        return redirect(url_for('index'))
    file = request.files['archivo_xml']
    if file.filename == '':
        flash("No se seleccionó archivo.", "error")
        return redirect(url_for('index'))
    uploads_dir = os.path.join(app.root_path, '..', 'uploads')
    if not os.path.exists(uploads_dir): os.makedirs(uploads_dir)
    ruta_guardado = os.path.join(uploads_dir, file.filename)
    file.save(ruta_guardado)
    manejador = XMLManager()
    datos_cargados = manejador.parsear_entrada(ruta_guardado)
    if datos_cargados: flash(f"Archivo '{file.filename}' cargado.", "success")
    else: flash(f"Error al procesar '{file.filename}'.", "error")
    return redirect(url_for('index'))

@app.route('/generar-salida', methods=['POST'])
def generar_archivo_salida():
    if not datos_cargados:
        flash("No hay datos cargados para generar salida.", "error")
        return redirect(url_for('index'))
    todos_los_resultados = []
    for invernadero in datos_cargados:
        for plan in invernadero.planes:
            plan_copiado = copy.deepcopy(plan)
            sim = Simulador(invernadero, plan_copiado)
            sim.ejecutar_simulacion()
            todos_los_resultados.append(sim.obtener_resultados())
    output_dir = os.path.join(app.root_path, '..', 'output')
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    ruta_salida = os.path.join(output_dir, 'salida.xml')
    manejador = XMLManager()
    manejador.generar_salida(todos_los_resultados, ruta_salida)
    return send_from_directory(directory=output_dir, path='salida.xml', as_attachment=True)

@app.route('/reporte-general')
def reporte_general():
    if not datos_cargados:
        flash("Carga un archivo para ver el reporte.", "error")
        return redirect(url_for('index'))
    todos_los_resultados = []
    for invernadero in datos_cargados:
        for plan in invernadero.planes:
            plan_copiado = copy.deepcopy(plan)
            sim = Simulador(invernadero, plan_copiado)
            sim.ejecutar_simulacion()
            todos_los_resultados.append(sim.obtener_resultados())
    return render_template('reporte_general.html', lista_resultados=todos_los_resultados)

@app.route('/generar-grafo', methods=['POST'])
def generar_grafo():
    resultados = session.get('resultados_simulacion')
    if not resultados:
        flash("Ejecuta una simulación primero.", "error")
        return redirect(url_for('index'))

    tiempo_t = int(request.form.get('tiempo_t', 0))
    session['tiempo_solicitado'] = tiempo_t

    historial_cola = resultados.get('historial_cola')

    if historial_cola and 0 <= tiempo_t < len(historial_cola):
        cola_en_t = historial_cola[tiempo_t]
        ruta_relativa_grafo = generar_grafo_tda(cola_en_t, tiempo_t)
        session['grafo_path'] = url_for('static', filename=ruta_relativa_grafo)
        flash(f"Gráfico del TDA en t={tiempo_t}s generado.", "success")
    else:
        flash(f"El tiempo {tiempo_t}s está fuera de rango.", "error")
        if 'grafo_path' in session: session.pop('grafo_path')
        
    return redirect(url_for('index'))