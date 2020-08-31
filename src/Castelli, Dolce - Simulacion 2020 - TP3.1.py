from random import random,seed
from numpy import log, average, median, std, bincount, array, insert
import matplotlib.pyplot as plt
from datetime import datetime
from tabulate import tabulate

class Queue_mm1():

    def __init__(self, num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT, cola_maxima = None):
        self.num_events = num_events
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required
        self.Q_LIMIT = Q_LIMIT
        self.parameter_lambda = 1 / self.mean_interarrival
        self.parameter_mu = 1 / self.mean_service
        self.cola_maxima = cola_maxima

        self.inicializar()

    def inicializar(self):
        self.time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.time_last_event = 0.0

        self.nums_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0

        self.time_next_event = [0.0,0.0,0.0]
        self.time_next_event[1] = self.time + self.expon(mean_interarrival)
        self.time_next_event[2] = 10 ** 30
        self.time_arrival = [0.0 for i in range(self.Q_LIMIT + 1)]

        self.min_time_next_event = 0.0
        self.next_event_type = 0

        self.clientes_denegados = 0

        self.qdet = []
        self.qdet.append(self.area_num_in_q)
    
    def timing(self):
        self.min_time_next_event = 10 ** 29
        self.next_event_type = 0

        for i in range(self.num_events + 1):
            if self.time_next_event[i] < self.min_time_next_event and i != 0:
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        if self.next_event_type == 0:
            print('Lista vacia en tiempo ' + str(self.time))
            exit()

        self.time = self.min_time_next_event

        
    def arrive(self):
        self.time_next_event[1] = self.time + self.expon(self.mean_interarrival)

        if self.server_status == 1:
            self.num_in_q += 1

            #Si es mm1k y la cola está llena
            if (self.cola_maxima and self.num_in_q > self.cola_maxima):
                self.clientes_denegados += 1
            else:
                self.time_arrival[self.num_in_q] = self.time

        else:
            self.delay = 0.0
            self.total_of_delays += self.delay

            self.nums_custs_delayed += 1
            self.server_status = 1
            self.time_next_event[2] = self.time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[2] = 10**30
        else:
            self.num_in_q -= 1
            self.delay = self.time - self.time_arrival[1]
            self.total_of_delays += self.delay

            self.nums_custs_delayed += 1
            self.time_next_event[2] = self.time + self.expon(self.mean_service)

            for i in range(self.num_in_q):
                self.time_arrival[i] = self.time_arrival[i + 1]


    def update_time_avg_stats(self):
        self.time_since_last_event = self.time - self.time_last_event
        self.time_last_event = self.time


        self.qdet.append(self.num_in_q * self.time_since_last_event / self.time)
        self.area_num_in_q += self.num_in_q * self.time_since_last_event
        self.area_server_status += self.server_status * self.time_since_last_event

    def expon(self, mean):
        u = random()
        return -mean * log(u)

    def simmulate(self, cant_simulaciones):

        metricas_simulacion = []
        frecuencias_cola = []
        frecuencias_sistema = []

        

        for i in range(cant_simulaciones):

            historico_cola_simulacion = []
            historico_sistema_simuacion = []
            if i % 10 == 0:
                print('Simulado ' + str(i) + '/' + str(cant_simulaciones))

            seed(datetime.now())
            self.inicializar()

            historico_cola_simulacion.append(0)
            historico_sistema_simuacion.append(0)

            while(self.nums_custs_delayed < self.num_delays_required):
                self.timing()
                self.update_time_avg_stats()

                if self.next_event_type == 1:
                    self.arrive()
                elif self.next_event_type == 2:
                    self.depart()

                #Para calcular la probabilidad de n clientes en cola
                historico_cola_simulacion.append(self.num_in_q)

                if self.server_status == 1:
                    historico_sistema_simuacion.append(self.num_in_q + 1)
                else:
                    historico_sistema_simuacion.append(self.num_in_q)


            metricas = self.calcula_metricas()
            metricas_simulacion.append(metricas)

            frecuencias_cola_iteracion = [0 for i in range(7)]
            frecuencias_sistema_iteracion = [0 for i in range(7)]
            
            #Cuenta ocurrencias hasta 5, la siguiente será de cualquier numero mayor a 5
            for i in range(6):
                frecuencias_cola_iteracion[i] = historico_cola_simulacion.count(i) #/ len(historico_cola_simulacion)
            
            frecuencias_cola_iteracion[6] = sum(i > 5 for i in historico_cola_simulacion)

            #Cuenta ocurrencias hasta 5, la siguiente será de cualquier numero mayor a 5
            for i in range(6):
                frecuencias_sistema_iteracion[i] = historico_sistema_simuacion.count(i) #/ len(historico_sistema_simuacion)
            
            frecuencias_sistema_iteracion[6] = sum(i > 5 for i in historico_sistema_simuacion)

            #Añade las frecuencias de la corrida a las generales
            frecuencias_cola.append(frecuencias_cola_iteracion)
            frecuencias_sistema.append(frecuencias_sistema_iteracion)


        return self.devuelve_metricas(metricas_simulacion), frecuencias_cola, frecuencias_sistema

    def calcula_metricas(self):

        metricas = {}

        promedio_clientes_cola = self.area_num_in_q / self.time
        promedio_clientes_sistema = promedio_clientes_cola + self.parameter_lambda / self.parameter_mu
        tiempo_promedio_cola = self.total_of_delays / self.nums_custs_delayed
        tiempo_promedio_sistema = tiempo_promedio_cola + 1 / self.parameter_mu
        utilizacion_servidor = self.area_server_status / self.time

        if self.cola_maxima is not None:
            denegacion_servicio = self.clientes_denegados / promedio_clientes_sistema

        metricas['promedio_clientes_cola'] = promedio_clientes_cola
        metricas['promedio_clientes_sistema'] = promedio_clientes_sistema
        metricas['tiempo_promedio_cola'] = tiempo_promedio_cola
        metricas['tiempo_promedio_sistema'] = tiempo_promedio_sistema
        metricas['utilizacion_servidor'] = utilizacion_servidor

        if self.cola_maxima is not None:
            metricas['denegacion_servicio'] = denegacion_servicio

        return metricas

    def obtiene_acumulados(self,metrica):
        acum = 0
        metrics = []

        for i,val in enumerate(metrica,start=1):
            acum += val 
            metrics.append(acum/i)
    
        return metrics 

    def obtiene_promedio_metricas(self,metricas):
        clientes_cola = average(metricas['clientes_cola_avg'])
        clientes_sistema = average(metricas['clientes_sistema_avg'])
        tiempo_promedio_cola = average(metricas['tiempo_promedio_cola_avg'])
        tiempo_promedio_sistema = average(metricas['tiempo_promedio_sistema_avg'])
        utilizacion_servidor = average(metricas['utilizacion_servidor_avg'])

        if self.cola_maxima is not None:
            denegacion_servicio = average(metricas['denegacion_servicio_avg'])
            graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor,denegacion_servicio]
        else:
            graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]

        return graficas

    def obtiene_metricas_promedio(self,metricas):
        clientes_cola = metricas['clientes_cola_avg']
        clientes_sistema = metricas['clientes_sistema_avg']
        tiempo_promedio_cola = metricas['tiempo_promedio_cola_avg']
        tiempo_promedio_sistema = metricas['tiempo_promedio_sistema_avg']
        utilizacion_servidor = metricas['utilizacion_servidor_avg']

        graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]


        return graficas

    def obtiene_metricas_acumuladas(self, metricas):
        clientes_cola = self.obtiene_acumulados(metricas['clientes_cola_avg'])
        clientes_sistema = self.obtiene_acumulados(metricas['clientes_sistema_avg'])
        tiempo_promedio_cola = self.obtiene_acumulados(metricas['tiempo_promedio_cola_avg'])
        tiempo_promedio_sistema = self.obtiene_acumulados(metricas['tiempo_promedio_sistema_avg'])
        utilizacion_servidor = self.obtiene_acumulados(metricas['utilizacion_servidor_avg'])

        graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]

        return graficas
 
    def devuelve_metricas(self, metricas_simulacion):
        
        clientes_cola = []
        clientes_sistema = []
        tiempo_promedio_cola = []
        tiempo_promedio_sistema = []
        utilizacion_servidor = []
        denegacion_servicio = []
        
        for m in metricas_simulacion:
            clientes_cola.append(m['promedio_clientes_cola'])
            clientes_sistema.append(m['promedio_clientes_sistema'])
            tiempo_promedio_cola.append(m['tiempo_promedio_cola'])
            tiempo_promedio_sistema.append(m['tiempo_promedio_sistema'])
            utilizacion_servidor.append(m['utilizacion_servidor'])

            if self.cola_maxima is not None:
                denegacion_servicio.append(m['denegacion_servicio'])

        clientes_cola_avg = clientes_cola
        clientes_sistema_avg = clientes_sistema
        tiempo_promedio_cola_avg = tiempo_promedio_cola
        tiempo_promedio_sistema_avg = tiempo_promedio_sistema
        utilizacion_servidor_avg = utilizacion_servidor

        if self.cola_maxima is not None:
            denegacion_servicio_avg = denegacion_servicio

        metricas = {}
        metricas['clientes_cola_avg'] = clientes_cola_avg
        metricas['clientes_sistema_avg'] = clientes_sistema_avg 
        metricas['tiempo_promedio_cola_avg'] = tiempo_promedio_cola_avg 
        metricas['tiempo_promedio_sistema_avg'] = tiempo_promedio_sistema_avg 
        metricas['utilizacion_servidor_avg'] = utilizacion_servidor_avg 

        if self.cola_maxima is not None:
            metricas['denegacion_servicio_avg'] = denegacion_servicio_avg 

        return metricas

    def obtiene_promedios_frecuencias(self, frecuencias_cola, frecuencias_sistema):
        frecuencias_cola_calc = []
        frecuencias_sistema_calc = []
        frecuencias_cola_grafica = []
        frecuencias_sistema_grafica = []
        cantidades = [i for i in range(7)]
        
        for i in range(7):
            suma = 0
            for iteracion in frecuencias_cola:
                suma += iteracion[i]
            promedio = round(suma / len(frecuencias_cola))

            frecuencias_cola_calc.append(promedio)

        for i in range(7):
            suma = 0
            for iteracion in frecuencias_sistema:
                suma += iteracion[i]
            promedio = round(suma / len(frecuencias_sistema))

            frecuencias_sistema_calc.append(promedio)

        array_cola = array(frecuencias_cola_calc)
        array_sistema = array(frecuencias_sistema_calc)

        frecuencias_cola_grafica = array_cola / float(array_cola.sum())
        frecuencias_sistema_grafica = array_sistema / float(array_sistema.sum())

        return frecuencias_cola_grafica, frecuencias_sistema_grafica

    def grafica_metricas(self, metricas, acumulados=False):
        
        titulos = ['Clientes promedio en cola', 'Clientes promedio en sistema', 'Tiempo promedio en cola', 'Tiempo promedio en sistema', 'Utilizacion del servidor']

        if acumulados:
            graficas = self.obtiene_metricas_acumuladas(metricas)
            title = 'Simulación MM1 | Métricas Acumuladas | λ =' + str(self.parameter_lambda) + ', μ = ' + str(self.parameter_mu)
            acum_text = 'acum_'
        else:
            graficas = self.obtiene_metricas_promedio(metricas)
            title = 'Simulación MM1 | λ =' + str(self.parameter_lambda) + ', μ = ' + str(self.parameter_mu)
            acum_text = ''

        

        fig, axs = plt.subplots(3, 2, constrained_layout=True)
        fig.suptitle(title)

        cont = 0
        a = 0
        ax = plt.Subplot 

        x_axis = [i for i in range(1,11)]

        for i, grafica in enumerate(graficas,start=0):
            
            if cont == 2:
                cont = 0
                a += 1

            ax = axs[a][cont]
            ax.set_xticks(x_axis)
            ax.plot(x_axis,grafica)
            ax.hlines(average(grafica), 1, len(grafica), colors='r', linestyles="dashed", lw=1)
            ax.set_xlabel("Cantidad de simulaciones")

            if a == 0:
                y_label = 'Clientes (cantidad)'
            elif a == 1:
                y_label = 'Tiempo (m)'
            elif a == 2 and cont == 0:
                y_label = 'Utilización (%)'
            
            ax.set_ylabel(y_label)
            ax.set_title(titulos[i])        
        

            cont += 1   
        
        win_manager = plt.get_current_fig_manager()
        win_manager.window.state('zoomed')
        
        plt.savefig('grafica_metricas_mm1_lambda_' + str(self.parameter_lambda) + '_mu_' + acum_text + str(self.parameter_mu) +'.png')
        plt.show()


    def grafica_mm1k(self, promedios_simulacion, tamaños_cola):

        title = 'Simulación MM1K | Métricas λ =' + str(self.parameter_lambda) + ', μ = ' + str(self.parameter_mu)
        titulos = ['Clientes promedio en cola', 'Clientes promedio en sistema', 'Tiempo promedio en cola', 'Tiempo promedio en sistema', 'Utilizacion del servidor', 'Denegación de servicio']

        #Transponer los promedios
        promedios_simulacion = array(promedios_simulacion).T

        fig, axs = plt.subplots(3, 2, constrained_layout=True)
        fig.suptitle(title)

        cont = 0
        a = 0
        ax = plt.Subplot 

        x_axis = [i for i in range(1,7)]

        for i, grafica in enumerate(promedios_simulacion,start=0):
            
            if cont == 2:
                cont = 0
                a += 1

            ax = axs[a][cont]
            ax.set_xticks(tamaños_cola)
            ax.bar(tamaños_cola, grafica)
            ax.set_xlabel("Longitud máxima de cola")

            if a == 0:
                y_label = 'Clientes (cantidad)'
            elif a == 1:
                y_label = 'Tiempo (m)'
            elif a == 2 and cont == 0:
                y_label = 'Utilización (%)'
            
            ax.set_ylabel(y_label)
            ax.set_title(titulos[i])

            cont += 1   

        win_manager = plt.get_current_fig_manager()
        win_manager.window.state('zoomed')
        
        plt.savefig("grafica_mm1k_lambda_" + str(self.parameter_lambda) + '_mu_' + str(self.parameter_mu) +".png")
        plt.show()

    def grafica_cant_clientes(self, frecuencias_cola_grafica, frecuencias_sistema_grafica ):
        title = 'Simulación MM1 | λ =' + str(self.parameter_lambda) + ', μ = ' + str(self.parameter_mu)

        titulos = ['Cantidad de clientes en cola', 'Cantidad de clientes en sistema']

        fig, axs = plt.subplots(1, 2, constrained_layout=True)
        fig.suptitle(title)

        cont = 0
        ax = plt.Subplot 

        x_axis = [i for i in range(7)]

        for i, grafica in enumerate((frecuencias_cola_grafica, frecuencias_sistema_grafica), start=0):

            ax = axs[cont]
            ax.set_xticks(x_axis)

            ax.bar(x_axis, grafica)

            ax.set_xlabel('Cantidad de clientes')
            ax.set_ylabel('Probabilidad')
            ax.set_title(titulos[i]) 

            cont += 1   

        win_manager = plt.get_current_fig_manager()
        win_manager.window.state('zoomed')
        
        plt.savefig("grafica_frecuencias_lambda_" + str(self.parameter_lambda) + '_mu_' + str(self.parameter_mu) +".png")
        plt.show()

    def reporte_metricas(self,metricas):
        print('REPORT ')
        
        #Tiempo total de la simulación
        print('Time simulation ended ' + str(self.time))

        m1 = metricas['clientes_cola_avg']
        m2 = metricas['clientes_sistema_avg']
        m3 = metricas['tiempo_promedio_cola_avg']
        m4 = metricas['tiempo_promedio_sistema_avg']
        m5 = metricas['utilizacion_servidor_avg']

        leyendas = ['Metrica', 'Media', 'Mediana', 'Desvio Estandar']
        promedio_clientes_cola = [ 'Promedio clientes en cola',  str(round(average(m1),3)), str(round(median(m1),3)), str(round(std(m1),3)) ]
        promedio_clientes_sistema = [ 'Promedio de clientes en sistema', str(round(average(m2),3)), str(round(median(m2),3)), str(round(std(m2),3)) ]
        tiempo_promedio_cola = [ 'Tiempo promedio en cola', str(round(average(m3),3)), str(round(median(m3),3)), str(round(std(m3),3)) ]
        tiempo_promedio_sistema = [ 'Tiempo promedio en sistema', str(round(average(m4),3)), str(round(median(m4),3)), str(round(std(m4),3)) ]
        utilizacion_servidor = [ 'Utilizacion del servidor', str(round(average(m5),3)), str(round( median(m5),3)), str(round(std(m5),3)) ]

        reporte = [promedio_clientes_cola, promedio_clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]
        
        #Informa estadísticos en forma tabular
        print(tabulate(reporte, headers=leyendas))

        #Guarda en un archivo la secuencia generada (para visualizar el patrón)
        with open('resultados_metricas.txt', 'a') as file:
            file.write('MU: ' + str(self.parameter_mu) + ' | LAMBDA: ' + str(self.parameter_lambda))
            file.write('\n')
            file.write(tabulate(reporte, headers=leyendas, tablefmt='latex'))
            file.writelines('\n\n')

    def reporte_frecuencias(self, frecuencias_cola_grafica, frecuencias_sistema_grafica ):
        
        print('REPORTE FRECUENCIAS')
                
        leyendas = [str(i) for i in range(7)]
        frecuencias_cola_rep = frecuencias_cola_grafica.tolist()
        frecuencias_sistema_rep = frecuencias_sistema_grafica.tolist()
        leyendas.insert(0, 'Métrica')
        frecuencias_cola_rep.insert(0, 'Clientes en cola')
        frecuencias_sistema_rep.insert(0, 'Clientes en sistema')
        
        reporte = [frecuencias_cola_rep, frecuencias_sistema_rep]
        #Informa estadísticos en forma tabular
        print(tabulate(reporte, headers=leyendas))

        #Guarda en un archivo la secuencia generada (para visualizar el patrón)
        with open('resultados_metricas_frecuencias.txt', 'a') as file:
            file.write('MU: ' + str(self.parameter_mu) + ' | LAMBDA: ' + str(self.parameter_lambda))
            file.write('\n')
            file.write(tabulate(reporte, headers=leyendas, tablefmt='latex'))
            file.writelines('\n\n')


if __name__ == "__main__":

    #PARAMETROS
    num_events = 2
    mean_service = 0.5
    num_delays_required = 1000
    Q_LIMIT = 100000

    tamaños_cola = [0,2,5,10,50]
    par_mu = 1/mean_service
    tasas_arribos_relativas = [0.25, 0.5, 0.75, 1, 1.25]
    tasas_arribos = [t*par_mu for t in tasas_arribos_relativas]

    cant_simulaciones = 10

    #Simulaciones mm1
    for t in tasas_arribos:
        mean_interarrival = 1/t
        mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT)
        metricas, frecuencias_cola, frecuencias_sistema = mm1.simmulate(cant_simulaciones)

        # Métricas promedios
        mm1.grafica_metricas(metricas)
        mm1.reporte_metricas(metricas)

        # Métricas promedios acumulados
        mm1.grafica_metricas(metricas,True)

    
        # Gráficas Frecuencias
        frecuencias_cola_grafica, frecuencias_sistema_grafica = mm1.obtiene_promedios_frecuencias(frecuencias_cola, frecuencias_sistema)
        mm1.reporte_frecuencias(frecuencias_cola_grafica, frecuencias_sistema_grafica)
        mm1.grafica_cant_clientes(frecuencias_cola_grafica, frecuencias_sistema_grafica)
        

    #Simulaciones mm1k
    for t in tasas_arribos:
        mean_interarrival = 1/t
        
        promedios_simulacion = []
        
        for limite in tamaños_cola:
            mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT, cola_maxima=limite)
            metricas, frecuencias_cola, frecuencias_sistema = mm1.simmulate(cant_simulaciones)

            #Obtiene
            promedio_metricas = mm1.obtiene_promedio_metricas(metricas)
            promedios_simulacion.append(promedio_metricas)

        # Métricas promedios
        mm1.grafica_mm1k(promedios_simulacion, tamaños_cola)