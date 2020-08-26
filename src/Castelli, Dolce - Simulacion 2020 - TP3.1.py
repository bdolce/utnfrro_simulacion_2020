from enum import Enum
from random import random,seed
from numpy import log, average
import matplotlib.pyplot as plt
import statistics as stats
from datetime import datetime

class Queue_mm1():

    def __init__(self, num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT):
        self.num_events = num_events
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required
        self.Q_LIMIT = Q_LIMIT
        self.parameter_lambda = 1 / self.mean_interarrival
        self.parameter_mu = 1 / self.mean_service

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

            # if (self.num_in_q > self.Q_LIMIT):
            #     print('OVERFLOW')
            #     exit()
        
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
       # prob_n_cola = self.calcula_probabilidad_n_cola(n=5)
       # prob_n_sistema = self.calcula_probabilidad_n_sistema(n=5)
       # prob_den_servicio = self.calcula_probabilidad_denegacion_servicio(n=50)

        metricas['promedio_clientes_cola'] = promedio_clientes_cola
        metricas['promedio_clientes_sistema'] = promedio_clientes_sistema
        metricas['tiempo_promedio_cola'] = tiempo_promedio_cola
        metricas['tiempo_promedio_sistema'] = tiempo_promedio_sistema
        metricas['utilizacion_servidor'] = utilizacion_servidor

        return metricas

    # def reporte_metricas(self,metricas):
    #     print('REPORT ')
    #     #Informa estadísticos
    #     print('q(n) - Promedio clientes en cola ' + str(metricas['promedio_clientes_cola']))
    #     print('Promedio de clientes en sistema ' + str(metricas['promedio_clientes_sistema']))
    #     print('d(n) - Tiempo promedio en cola ' + str(metricas['tiempo_promedio_cola']))
    #     print('Tiempo promedio en sistema ' + str(metricas['tiempo_promedio_sistema']))
    #     print('u(n) - Utilizacion del servidor ' + str(metricas['utilizacion_servidor']))
        
    #     #print('Probabilidad de n clientes en cola ' + str(prob_n_cola))
    #     #print('Probabilidad de n clientes en sistema ' + str(metricas['prob_n_sistema']))
    #     #print('Probabilidad de denegacion de servicio ' + str(metricas['prob_den_servicio']))
        
    #     plt.plot(self.qdet)
    #     plt.show()
    #    # prob_n_cola = self.calcula_probabilidad_n_cola(n=5)
    #    # self.grafica_prob(lista=prob_n_cola)
    #   #  self.grafica_prob(lista=prob_n_sistema)
    #   #  self.grafica_prob(lista=prob_den_servicio)

    #     #Tiempo total de la simulación
    #     print('Time simulation ended ' + str(self.time))


    # def report(self):

    #     print('REPORT ')
    #     #Informa estadísticos
    #     print('q(n) - Promedio clientes en cola ' + str(promedio_clientes_cola))
    #     print('Promedio de clientes en sistema ' + str(promedio_clientes_sistema))
    #     print('d(n) - Tiempo promedio en cola ' + str(tiempo_promedio_cola))
    #     print('Tiempo promedio en sistema ' + str(tiempo_promedio_sistema))
    #     print('u(n) - Utilizacion del servidor ' + str(utilizacion_servidor))
        
    #     #print('Probabilidad de n clientes en cola ' + str(prob_n_cola))
    #     print('Probabilidad de n clientes en sistema ' + str(prob_n_sistema))
    #     print('Probabilidad de denegacion de servicio ' + str(prob_den_servicio))
        
    #     #self.grafica_prob(lista=prob_n_cola)
    #     #self.grafica_prob(lista=prob_n_sistema)
    #     #self.grafica_prob(lista=prob_den_servicio)

    #     #Tiempo total de la simulación
    #     print('Time simulation ended ' + str(self.time))

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
        

        for i in range(cant_simulaciones):

            historico_cola_simulacion = []
            if i % 100 == 0:
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

    def grafica_metricas_conjunto(self, metricas_simulacion):
        
        clientes_cola = []
        clientes_sistema = []
        tiempo_promedio_cola = []
        tiempo_promedio_sistema = []
        utilizacion_servidor = []
        
        for m in metricas_simulacion:
            clientes_cola.append(m['clientes_cola_avg'])
            clientes_sistema.append(m['clientes_sistema_avg'])
            tiempo_promedio_cola.append(m['tiempo_promedio_cola_avg'])
            tiempo_promedio_sistema.append(m['tiempo_promedio_sistema_avg'])
            utilizacion_servidor.append(m['utilizacion_servidor_avg'])


        
        tasas_arribos = [0.25, 0.5, 0.75, 1, 1.25]
        fig=plt.figure(constrained_layout=True)

        fig.add_subplot(3,2,1)
        plt.plot(clientes_cola)
        plt.title("Clientes promedio en cola")
        # plt.show()
        # print('Clientes en cola ' + str(clientes_cola))
        # self.informa_estadisticos(clientes_cola)

        fig.add_subplot(3,2,2)
        plt.plot(clientes_sistema)
        plt.title("Clientes promedio en sistema")
        # plt.show()
        # # print('Clientes en sistema ' )#+ str(clientes_sistema))
        # # self.informa_estadisticos(clientes_sistema)

        fig.add_subplot(3,2,3)
        plt.plot(tiempo_promedio_cola)
        plt.title("Tiempo promedio en cola")
        # plt.show()
        # # print('Tiempo promedio en cola ' )#+ str(tiempo_promedio_cola))
        # # self.informa_estadisticos(tiempo_promedio_cola)

        fig.add_subplot(3,2,4)
        plt.plot(tiempo_promedio_sistema)
        plt.title("Tiempo promedio en sistema")
        # plt.show()
        # # print('Tiempo promdio en sistema ' )# + str(tiempo_promedio_sistema))
        # # self.informa_estadisticos(tiempo_promedio_sistema)

        fig.add_subplot(3,2,5)
        plt.plot(utilizacion_servidor)
        plt.title("Utilizacion del servidor")
        # plt.show()
        # # print('Utilizacion del servidor ' )#+ str(utilizacion_servidor))
        # # self.informa_estadisticos(utilizacion_servidor)

        plt.show()
 

    def grafica_metricas(self, metricas, mean_interarrival, mean_service):
        
        par_mu = 1 / mean_interarrival 
        par_lambda = 1 / mean_service

        clientes_cola = []
        clientes_sistema = []
        tiempo_promedio_cola = []
        tiempo_promedio_sistema = []
        utilizacion_servidor = []
        
        clientes_cola = metricas['clientes_cola_avg']
        clientes_sistema = metricas['clientes_sistema_avg']
        tiempo_promedio_cola = metricas['tiempo_promedio_cola_avg']
        tiempo_promedio_sistema = metricas['tiempo_promedio_sistema_avg']
        utilizacion_servidor = metricas['utilizacion_servidor_avg']

        graficas = [clientes_cola, clientes_sistema, tiempo_promedio_cola, tiempo_promedio_sistema, utilizacion_servidor]
        titulos = ['Clientes promedio en cola', 'Clientes promedio en sistema', 'Tiempo promedio en cola', 'Tiempo promedio en sistema', 'Utilizacion del servidor']

        fig, axs = plt.subplots(3, 2, constrained_layout=True)
        fig.suptitle('Métricas λ =' + str(par_lambda) + ', μ = ' + str(par_mu))

        cont = 0
        a = 0
        ax = plt.Subplot 

        for i, grafica in enumerate(graficas,start=0):
            
            if cont == 2:
                cont = 0
                a += 1

            ax = axs[a][cont]
           # ax.set_xticks([i for i in range(len(grafica))])
            ax.plot(grafica)
            ax.hlines(average(grafica), 0, len(grafica), colors='r', linestyles="dashed", lw=1)
            # ax.set_xlabel("Casilla")
            # ax.set_ylabel("Frecuencia Absoluta")
            ax.set_title(titulos[i])

            cont += 1   

            # fig.add_subplot(3,2,1)
            # plt.plot(clientes_cola)
            # plt.title("Clientes promedio en cola")
            # # plt.show()
            # # print('Clientes en cola ' + str(clientes_cola))
            # # self.informa_estadisticos(clientes_cola)

            # fig.add_subplot(3,2,2)
            # plt.plot(clientes_sistema)
            # plt.title("Clientes promedio en sistema")
            # # plt.show()
            # # # print('Clientes en sistema ' )#+ str(clientes_sistema))
            # # # self.informa_estadisticos(clientes_sistema)

            # fig.add_subplot(3,2,3)
            # plt.plot(tiempo_promedio_cola)
            # plt.title("Tiempo promedio en cola")
            # # plt.show()
            # # # print('Tiempo promedio en cola ' )#+ str(tiempo_promedio_cola))
            # # # self.informa_estadisticos(tiempo_promedio_cola)

            # fig.add_subplot(3,2,4)
            # plt.plot(tiempo_promedio_sistema)
            # plt.title("Tiempo promedio en sistema")
            # # plt.show()
            # # # print('Tiempo promdio en sistema ' )# + str(tiempo_promedio_sistema))
            # # # self.informa_estadisticos(tiempo_promedio_sistema)

            # fig.add_subplot(3,2,5)
            # plt.plot(utilizacion_servidor)
            # plt.title("Utilizacion del servidor")
            # # plt.show()
            # # # print('Utilizacion del servidor ' )#+ str(utilizacion_servidor))
            # # # self.informa_estadisticos(utilizacion_servidor)

        plt.show()

    def devuelve_metricas(self, metricas_simulacion):
        
        clientes_cola = []
        clientes_sistema = []
        tiempo_promedio_cola = []
        tiempo_promedio_sistema = []
        utilizacion_servidor = []
        metricas_salida = []
        
        for m in metricas_simulacion:
            clientes_cola.append(m['promedio_clientes_cola'])
            clientes_sistema.append(m['promedio_clientes_sistema'])
            tiempo_promedio_cola.append(m['tiempo_promedio_cola'])
            tiempo_promedio_sistema.append(m['tiempo_promedio_sistema'])
            utilizacion_servidor.append(m['utilizacion_servidor'])

        # clientes_cola_avg = stats.mean(clientes_cola)
        # clientes_sistema_avg = stats.mean(clientes_sistema)
        # tiempo_promedio_cola_avg = stats.mean(tiempo_promedio_cola)
        # tiempo_promedio_sistema_avg = stats.mean(tiempo_promedio_sistema)
        # utilizacion_servidor_avg = stats.mean(utilizacion_servidor)


        clientes_cola_avg = clientes_cola
        clientes_sistema_avg = clientes_sistema
        tiempo_promedio_cola_avg = tiempo_promedio_cola
        tiempo_promedio_sistema_avg = tiempo_promedio_sistema
        utilizacion_servidor_avg = utilizacion_servidor

        metricas = {}
        metricas['clientes_cola_avg'] = clientes_cola_avg
        metricas['clientes_sistema_avg'] = clientes_sistema_avg 
        metricas['tiempo_promedio_cola_avg'] = tiempo_promedio_cola_avg 
        metricas['tiempo_promedio_sistema_avg'] = tiempo_promedio_sistema_avg 
        metricas['utilizacion_servidor_avg'] = utilizacion_servidor_avg 

        return metricas



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
    # tamaños_cola = [0,2,5,10,50]
    
    par_mu = 1/mean_service
    par_lambdas = [0.25, 0.5, 0.75, 1, 1.25]
    par_lambdas = [t*par_mu for t in par_lambdas]

    print(par_lambdas)
    corridas = 10

    metricas_tasas = []

    for t in par_lambdas:
        mean_interarrival = 1/t
        mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT)
        metricas, historico = mm1.simmulate()
        mm1.grafica_metricas(metricas, mean_interarrival, mean_service)
        metricas_tasas.append(metricas)

        # for i in historico:
        #     print(i)
        #     plt.hist(i)
        # #     plt.show()
        # plt.hist(historico[0])
        # plt.show()

    mm1.grafica_metricas_conjunto(metricas_tasas)
        # print(metricas)