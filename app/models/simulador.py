# app/models/simulador.py
import copy

class Simulador:
    def __init__(self, invernadero_original, plan_original):
        self.invernadero = copy.deepcopy(invernadero_original)
        self.plan = plan_original
        self.tiempo_total = 0
        self.instrucciones_por_tiempo = []
        self.asignaciones_activas = self._determinar_asignaciones_activas()
        self.historial_cola = []

    def _parsear_paso(self, paso_str):
        partes = paso_str.split('-')
        hilera = int(partes[0].replace('H', ''))
        posicion = int(partes[1].replace('P', ''))
        return hilera, posicion

    def _determinar_asignaciones_activas(self):
        hileras_con_tareas = set()
        for tarea in self.plan.secuencia_cola._lista:
            h, _ = self._parsear_paso(tarea)
            hileras_con_tareas.add(h)
        
        asignaciones_activas = []
        for asignacion in self.invernadero.asignaciones_drones:
            if asignacion.hilera in hileras_con_tareas:
                asignacion.dron.resetear()
                asignaciones_activas.append(asignacion)
        return asignaciones_activas

    def _buscar_proxima_tarea_para_hilera(self, hilera_id):
        for tarea in self.plan.secuencia_cola._lista:
            h_tarea, _ = self._parsear_paso(tarea)
            if h_tarea == hilera_id:
                return tarea
        return None

    def ejecutar_simulacion(self):
        cola_tareas = self.plan.secuencia_cola
        
        # Guardamos una representación simple de la cola (lista de strings)
        tareas_actuales_lista = [tarea for tarea in cola_tareas._lista]
        self.historial_cola.append(tareas_actuales_lista)

        while not cola_tareas.esta_vacia():
            self.tiempo_total += 1
            dron_ha_regado_este_segundo = False
            acciones_del_segundo = []
            tarea_principal_str = cola_tareas.ver_frente()
            h_principal, pos_principal = self._parsear_paso(tarea_principal_str)

            for asignacion in self.asignaciones_activas:
                dron = asignacion.dron
                accion_info = {'nombre': dron.nombre, 'accion': "Fin"}

                if dron.estado == 'finalizado':
                    acciones_del_segundo.append(accion_info)
                    continue

                tarea_personal_str = self._buscar_proxima_tarea_para_hilera(asignacion.hilera)

                if not tarea_personal_str:
                    dron.estado = 'finalizado'
                    acciones_del_segundo.append(accion_info)
                    continue

                h_personal, pos_personal = self._parsear_paso(tarea_personal_str)

                if (tarea_personal_str == tarea_principal_str and
                    dron.posicion_actual == pos_personal and
                    not dron_ha_regado_este_segundo):
                    accion_info['accion'] = "Regar"
                    dron_ha_regado_este_segundo = True
                elif dron.posicion_actual < pos_personal:
                    dron.posicion_actual += 1
                    accion_info['accion'] = f"Adelante(H{asignacion.hilera}P{dron.posicion_actual})"
                elif dron.posicion_actual > pos_personal:
                    dron.posicion_actual -= 1
                    accion_info['accion'] = f"Atrás(H{asignacion.hilera}P{dron.posicion_actual})"
                else:
                    accion_info['accion'] = "Esperar"
                
                acciones_del_segundo.append(accion_info)

            if dron_ha_regado_este_segundo:
                cola_tareas.desencolar()
                planta_regada = self.invernadero.obtener_planta(h_principal, pos_principal)
                if planta_regada:
                    for asignacion in self.asignaciones_activas:
                        if asignacion.hilera == h_principal:
                            asignacion.dron.consumir_recursos(planta_regada.litros_agua, planta_regada.gramos_fertilizante)
                            break
            
            self.instrucciones_por_tiempo.append({
                'segundo': self.tiempo_total,
                'acciones': acciones_del_segundo
            })
            
            # Guardamos la representación simple de la cola en cada paso
            tareas_actuales_lista = [tarea for tarea in cola_tareas._lista]
            self.historial_cola.append(tareas_actuales_lista)

    def obtener_resultados(self):
        stats_drones_activos = []
        for asignacion in self.asignaciones_activas:
            stats_drones_activos.append({
                'nombre': asignacion.dron.nombre,
                'litrosAgua': round(asignacion.dron.litros_agua_consumidos, 2),
                'gramosFertilizante': round(asignacion.dron.gramos_fert_consumidos, 2)
            })
        
        agua_total = sum(d['litrosAgua'] for d in stats_drones_activos)
        fert_total = sum(d['gramosFertilizante'] for d in stats_drones_activos)

        # El diccionario de resultados ahora es 100% serializable a JSON
        return {
            'nombre_invernadero': self.invernadero.nombre,
            'nombre_plan': self.plan.nombre,
            'tiempo_optimo': self.tiempo_total,
            'agua_requerida': round(agua_total, 2),
            'fertilizante_requerido': round(fert_total, 2),
            'eficiencia_drones': stats_drones_activos,
            'instrucciones': self.instrucciones_por_tiempo,
            'historial_cola': self.historial_cola
        }