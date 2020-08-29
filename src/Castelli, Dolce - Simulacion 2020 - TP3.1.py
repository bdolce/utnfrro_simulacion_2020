from enum import Enum
from random import random,seed
from numpy import log, average, mean, median, std
import matplotlib.pyplot as plt
import statistics as stats
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
        self.cantidad_n_clientes_en_cola = [0.0 for i in range(7)]
        self.cantidad_n_clientes_en_sistema = [0.0 for i in range(7)]

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

    def calcula_probabilidad_n_cola(self,n):
        prob = []
        ro = self.parameter_lambda / self.parameter_mu

        for i in range(n+1):
            if i == 0:
                prob.append(1-ro**2)
            else:
                prob.append(ro**(i+1) * (1-ro))

        return prob

    def calcula_probabilidad_n_sistema(self,n):
        prob = []
        self.parameter_lambda = 1 * self.parameter_mu
        ro = self.parameter_lambda / self.parameter_mu

        for i in range(n+1):
            a = ro**i * (1-ro)
            prob.append(a)
        
        return prob

    def calcula_probabilidad_denegacion_servicio(self,n):
        suma = 0
        self.parameter_lambda = 1 * self.parameter_mu
        ro = self.parameter_lambda / self.parameter_mu

        for i in range(n+1):
            suma += ro**(i+1)

        prob = ro - ((1-ro) * suma )
        
        return prob

    def grafica_prob(self, lista):

        plt.hist(lista)
        plt.ylabel('')
        
        win_manager = plt.get_current_fig_manager()
        win_manager.window.state('zoomed')
        
        #plt.savefig("Grafica largo de semilla " + str(longitudes[l]) +".png")
        plt.show()

    def calcula_metricas(self):

        metricas = {}

        promedio_clientes_cola = self.area_num_in_q / self.time
        promedio_clientes_sistema = promedio_clientes_cola + self.parameter_lambda / self.parameter_mu
        tiempo_promedio_cola = self.total_of_delays / self.nums_custs_delayed
        tiempo_promedio_sistema = tiempo_promedio_cola + 1 / self.parameter_mu
        utilizacion_servidor = self.area_server_status / self.time
        denegacion_servicio = self.clientes_denegados / promedio_clientes_sistema

       # prob_n_cola = self.calcula_probabilidad_n_cola(n=5)
       # prob_n_sistema = self.calcula_probabilidad_n_sistema(n=5)
       # prob_den_servicio = self.calcula_probabilidad_denegacion_servicio(n=50)

        metricas['promedio_clientes_cola'] = promedio_clientes_cola
        metricas['promedio_clientes_sistema'] = promedio_clientes_sistema
        metricas['tiempo_promedio_cola'] = tiempo_promedio_cola
        metricas['tiempo_promedio_sistema'] = tiempo_promedio_sistema
        metricas['utilizacion_servidor'] = utilizacion_servidor
        metricas['denegacion_servicio'] = denegacion_servicio

        return metricas

    def reporte_metricas(self,metricas):
        print('REPORT ')
        
        #Tiempo total de la simulación
        print('Time simulation ended ' + str(self.time))

        m1 = metricas['clientes_cola_avg']
        m2 = metricas['clientes_sistema_avg']
        m3 = metricas['tiempo_promedio_cola_avg']
        m4 = metricas['tiempo_promedio_cola_avg']
        m5 = metricas['utilizacion_servidor_avg']

        leyendas = ['Metrica', 'Media', 'Mediana', 'Desvio Estandar']
        promedio_clientes_cola = [ 'Promedio clientes en cola',  str(round(average(m1),3)), str(round(median(m1),3)), str(round(std(m1),3)) ]
        promedio_clientes_sistema = [ 'Promedio de clientes en sistema', str(round(average(m2),3)), str(round(median(m2),3)), str(round(std(m2),3)) ]
        tiempo_promedio_cola = [ 'Tiempo promedio en cola', str(round(average(m3),3)), str(round(median(m3),3)), str(round(std(m3),3)) ]
        tiempo_promedio_sistema = [ 'Tiempo promedio en cola', str(round(average(m4),3)), str(round(median(m4),3)), str(round(std(m4),3)) ]
        utilizacion_servidor = [ 'Utilizacion del servidor', str(round(average(m5),3)), str(round( median(m5),3)), str(round(std(m5),3)) ]

        reporte = [promedio_clientes_cola, promedio_clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]
        
        #Informa estadísticos en forma tabular
        print(tabulate(reporte, headers=leyendas))

        #Guarda en un archivo la secuencia generada (para visualizar el patrón)
        with open('resultados_metricas.txt', 'a') as file:
            file.write('MU: ' + str(self.parameter_mu) + ' | LAMBDA: ' + str(self.parameter_lambda))
            file.write('\n')
            file.write(tabulate(reporte,headers=leyendas,tablefmt='latex'))
            file.writelines('\n\n')

    
    def reporta_metricas_cola(self,metricas):

        self.reporte_metricas(self,metricas)
        #print('Probabilidad de denegacion de servicio ' + str(metricas['prob_den_servicio']))
        

        
        #print('Probabilidad de n clientes en cola ' + str(prob_n_cola))
        #print('Probabilidad de n clientes en sistema ' + str(metricas['prob_n_sistema']))
       # prob_n_cola = self.calcula_probabilidad_n_cola(n=5)
       # self.grafica_prob(lista=prob_n_cola)
      #  self.grafica_prob(lista=prob_n_sistema)
      #  self.grafica_prob(lista=prob_den_servicio)




    def update_time_avg_stats(self):
        self.time_since_last_event = self.time - self.time_last_event
        self.time_last_event = self.time


        self.qdet.append(self.num_in_q * self.time_since_last_event / self.time)
        self.area_num_in_q += self.num_in_q * self.time_since_last_event
        self.area_server_status += self.server_status * self.time_since_last_event

    def expon(self, mean):
        u = random()
        return -mean * log(u)

    def simmulate(self):

        cant_simulaciones = 10
        metricas_simulacion = []
        historico_cola = []
        self.cantidad_n_clientes_en_cola += 1
        self.cantidad_n_clientes_en_sistema += 1
        

        for i in range(cant_simulaciones):

            historico_cola_simulacion = []
            if i % 10 == 0:
                print('Simulado ' + str(i) + '/' + str(cant_simulaciones))

            seed(datetime.now())
            self.inicializar()
            while(self.nums_custs_delayed < self.num_delays_required):
                self.timing()
                self.update_time_avg_stats()

                #Para calcular la probabilidad de n clientes en cola
                historico_cola_simulacion.append(self.num_in_q)

                if self.next_event_type == 1:
                    self.arrive()
                elif self.next_event_type == 2:
                    self.depart()

            metricas = self.calcula_metricas()
            metricas_simulacion.append(metricas)

            historico_cola.append(historico_cola_simulacion)

        #for m in metricas_simulacion:
        #    print(m) 

        # self.grafica_metricas(metricas_simulacion)
        return self.devuelve_metricas(metricas_simulacion), historico_cola


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
        denegacion_servicio = average(metricas['denegacion_servicio'])
        graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor,denegacion_servicio]

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
 

    def grafica_metricas(self, metricas, mean_interarrival, mean_service, acumulados=False):
        
        par_mu = 1 / mean_interarrival 
        par_lambda = 1 / mean_service


        if (acumulados):
            graficas = self.obtiene_metricas_acumuladas(metricas)
            title = 'Simulación MM1 | Métricas Acumuladas | λ =' + str(par_lambda) + ', μ = ' + str(par_mu)
        else:
            graficas = self.obtiene_metricas_promedio(metricas)
            title = 'Simulación MM1 | λ =' + str(par_lambda) + ', μ = ' + str(par_mu)

        titulos = ['Clientes promedio en cola', 'Clientes promedio en sistema', 'Tiempo promedio en cola', 'Tiempo promedio en sistema', 'Utilizacion del servidor']

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
                y_label = 'Tiempo (s)'
            elif a == 2:
                y_label = 'Utilización (%)'
            
            ax.set_ylabel(y_label)
            ax.set_title(titulos[i])

            cont += 1   

        plt.show()

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

    
    def grafica_mm1k(self, historico_promedios, tamaños_cola):
        par_mu = 1 / mean_interarrival 
        par_lambda = 1 / mean_service


        graficas = self.obtiene_metricas_promedio(metricas)
        title = 'Métricas λ =' + str(par_lambda) + ', μ = ' + str(par_mu)

        titulos = ['Clientes promedio en cola', 'Clientes promedio en sistema', 'Tiempo promedio en cola', 'Tiempo promedio en sistema', 'Utilizacion del servidor', 'Denegación de servicio']

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
                y_label = 'Tiempo (s)'
            elif a == 2:
                y_label = 'Utilización (%)'
            
            ax.set_ylabel(y_label)
            ax.set_title(titulos[i])

            cont += 1   

        plt.show()



    def informa_estadisticos(self, metrica):
        mean = stats.mean(metrica)
        median = stats.median(metrica)
        stdev = stats.stdev(metrica)
        
        print('')
        print('Media ' + str(mean))
        print('Mediana ' + str(median))
        print('Desvio estandar ' + str(stdev))
        print('')

if __name__ == "__main__":

    #PARAMETROS
    num_events = 2
    mean_service = 0.5
    num_delays_required = 1000
    Q_LIMIT = 100000

    print('MM1')

    # tasas_servicio = []
    # tasas_arribos = []
    tamaños_cola = [0,2,5,10,50]
    
    par_mu = 1/mean_service
    tasas_arribos_relativas = [0.25, 0.5, 0.75, 1, 1.25]
    tasas_arribos = [t*par_mu for t in tasas_arribos_relativas]

    corridas = 10
   # metricas_tasas = []

    #Simulaciones mm1
    for t in tasas_arribos:
        mean_interarrival = 1/t
        mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT)
        metricas, historico = mm1.simmulate()
        
        #Métricas promedios
        mm1.grafica_metricas(metricas, mean_interarrival, mean_service)
        mm1.reporte_metricas(metricas)
        
        #Métricas promedios acumulados
        mm1.grafica_metricas(metricas, mean_interarrival, mean_service,True)

        #metricas_tasas.append(metricas)
    

#    mm1.grafica_metricas_conjunto(metricas_tasas)

    # #Simulaciones mm1k
    # for t in tasas_arribos:
    #     mean_interarrival = 1/t

    #     for limite in tamaños_cola:
    #         mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT, cola_maxima=limite)
    #         metricas, historico = mm1.simmulate()
            
    #         #Promedios de las metricas en todas las corridas
    #         promedios = mm1.obtiene_promedio_metricas(metricas)
            
    #         #Métricas promedios
    #         #mm1.grafica_metricas(metricas, mean_interarrival, mean_service)
            
    #         #Métricas promedios acumulados
    #         mm1.grafica_metricas(metricas, mean_interarrival, mean_service,True)