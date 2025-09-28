# app/services/xml_manager.py
import xml.etree.ElementTree as ET

try:
    from ..structures.lista_enlazada import ListaEnlazada
    from ..models.dron import Dron
    from ..models.planta import Planta
    from ..models.plan_riego import PlanRiego
    from ..models.invernadero import Invernadero, Asignacion
    from ..models.simulador import Simulador
except ImportError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from app.structures.lista_enlazada import ListaEnlazada
    from app.models.dron import Dron
    from app.models.planta import Planta
    from app.models.plan_riego import PlanRiego
    from app.models.invernadero import Invernadero, Asignacion
    from app.models.simulador import Simulador


class XMLManager:
    """
    Servicio encargado de leer y escribir archivos XML.
    """
    def parsear_entrada(self, ruta_archivo):
        # (Este método ya es correcto, no necesita cambios)
        try:
            arbol = ET.parse(ruta_archivo)
            raiz = arbol.getroot()
            drones_disponibles = ListaEnlazada()
            for dron_xml in raiz.find('listaDrones'):
                dron = Dron(id=dron_xml.get('id'), nombre=dron_xml.get('nombre'))
                drones_disponibles.insertar_al_final(dron)
            
            invernaderos_configurados = ListaEnlazada()
            for inv_xml in raiz.find('listaInvernaderos'):
                invernadero = Invernadero(inv_xml.get('nombre'), inv_xml.find('numeroHileras').text, inv_xml.find('plantasXhilera').text)
                
                for planta_xml in inv_xml.find('listaPlantas'):
                    planta = Planta(planta_xml.get('posicion'), planta_xml.get('hilera'), planta_xml.text.strip(), planta_xml.get('litrosAgua'), planta_xml.get('gramosFertilizante'))
                    invernadero.agregar_planta(planta)

                for asignacion_xml in inv_xml.find('asignacionDrones'):
                    id_dron_asignado = int(asignacion_xml.get('id'))
                    hilera_asignada = int(asignacion_xml.get('hilera'))
                    
                    for dron_obj in drones_disponibles:
                        if dron_obj.id == id_dron_asignado:
                            invernadero.asignar_dron(dron_obj, hilera_asignada)
                            break
                
                for plan_xml in inv_xml.find('planesRiego'):
                    plan = PlanRiego(plan_xml.get('nombre'), plan_xml.text.strip())
                    invernadero.agregar_plan(plan)
                
                invernaderos_configurados.insertar_al_final(invernadero)
            
            return invernaderos_configurados
        except Exception as e:
            print(f"Error al parsear el archivo de entrada: {e}")
            return None

    def generar_salida(self, lista_resultados, ruta_salida):
        """
        Construye y guarda el archivo salida.xml a partir de una lista de
        resultados pre-calculados por el Simulador.
        """
        root = ET.Element('datosSalida')
        lista_inv_xml = ET.SubElement(root, 'listaInvernaderos')

        resultados_agrupados = {}
        for resultado_plan in lista_resultados:
            nombre_inv = resultado_plan['nombre_invernadero']
            if nombre_inv not in resultados_agrupados:
                resultados_agrupados[nombre_inv] = []
            resultados_agrupados[nombre_inv].append(resultado_plan)

        for nombre_inv, planes_resultados in resultados_agrupados.items():
            inv_xml = ET.SubElement(lista_inv_xml, 'invernadero', {'nombre': nombre_inv})
            # CAMBIO: El nombre de esta etiqueta debe ser 'listaPlanes' según tu HTML, no 'plan'
            lista_planes_xml = ET.SubElement(inv_xml, 'listaPlanes')

            for res in planes_resultados:
                plan_xml = ET.SubElement(lista_planes_xml, 'plan', {'nombre': res['nombre_plan']})
                
                ET.SubElement(plan_xml, 'tiempoOptimoSegundos').text = str(res['tiempo_optimo'])
                ET.SubElement(plan_xml, 'aguaRequeridaLitros').text = str(res['agua_requerida'])
                ET.SubElement(plan_xml, 'fertilizanteRequeridoGramos').text = str(res['fertilizante_requerido'])
                
                eficiencia_xml = ET.SubElement(plan_xml, 'eficienciaDronesRegadores')
                for dron_stat in res['eficiencia_drones']:
                    ET.SubElement(eficiencia_xml, 'dron', {
                        'nombre': dron_stat['nombre'],
                        # CAMBIO CRÍTICO: Convertimos los números a strings con str()
                        'litrosAgua': str(dron_stat['litrosAgua']),
                        'gramosFertilizante': str(dron_stat['gramosFertilizante'])
                    })
                
                instrucciones_xml = ET.SubElement(plan_xml, 'instrucciones')
                for instruccion_segundo in res['instrucciones']:
                    # CAMBIO CRÍTICO: Convertimos el número del segundo a string con str()
                    tiempo_xml = ET.SubElement(instrucciones_xml, 'tiempo', {'segundos': str(instruccion_segundo['segundo'])})
                    for accion_dron in instruccion_segundo['acciones']:
                        ET.SubElement(tiempo_xml, 'dron', {
                            'nombre': accion_dron['nombre'], 
                            'accion': accion_dron['accion']
                        })
        
        arbol = ET.ElementTree(root)
        ET.indent(arbol, space="    ")
        arbol.write(ruta_salida, encoding='UTF-8', xml_declaration=True)
        print(f"Archivo de salida generado exitosamente en: {ruta_salida}")
        return True