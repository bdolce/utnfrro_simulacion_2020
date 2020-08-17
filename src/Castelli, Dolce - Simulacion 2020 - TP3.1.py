from enum import Enum
from random import random
from numpy import log
import matplotlib.pyplot as plt

class Queue_mm1():

    def __init__(self, num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT):
        self.num_events = num_events
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required
        self.Q_LIMIT = Q_LIMIT
        self.parameter_lambda = 1 / self.mean_interarrival
        self.parameter_mu = 1 / self.mean_service

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

    def report(self):
        promedio_clientes_cola = self.area_num_in_q / self.time
        promedio_clientes_sistema = promedio_clientes_cola + self.parameter_lambda / self.parameter_mu
        tiempo_promedio_cola = self.total_of_delays / self.nums_custs_delayed
        tiempo_promedio_sistema = tiempo_promedio_cola + 1 / self.parameter_mu
        utilizacion_servidor = self.area_server_status / self.time
        prob_n_sistema = self.calcula_probabilidad_n_sistema(n=5)
        prob_den_servicio = self.calcula_probabilidad_denegacion_servicio(n=50)


        print('REPORT ')
        #Informa estadísticos
        print('q(n) - Promedio clientes en cola ' + str(promedio_clientes_cola))
        # print('Promedio de clientes en sistema ' + str(promedio_clientes_sistema))
        # print('d(n) - Tiempo promedio en cola ' + str(tiempo_promedio_cola))
        # print('Tiempo promedio en sistema ' + str(tiempo_promedio_sistema))
        # print('u(n) - Utilizacion del servidor ' + str(utilizacion_servidor))
        
        # #print('Probabilidad de n clientes en cola ' + str(prob_n_cola))
        # print('Probabilidad de n clientes en sistema ' + str(prob_n_sistema))
        # print('Probabilidad de denegacion de servicio ' + str(prob_den_servicio))
        
        plt.plot(self.qdet)
        plt.show()
       # prob_n_cola = self.calcula_probabilidad_n_cola(n=5)
       # self.grafica_prob(lista=prob_n_cola)
      #  self.grafica_prob(lista=prob_n_sistema)
      #  self.grafica_prob(lista=prob_den_servicio)

        #Tiempo total de la simulación
        print('Time simulation ended ' + str(self.time))

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
        while(self.nums_custs_delayed < self.num_delays_required):
            self.timing()
            self.update_time_avg_stats()

            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()

        self.report()



if __name__ == "__main__":

    #PARAMETROS
    num_events = 2
    mean_interarrival = 1
    mean_service = 1
    num_delays_required = 1000
    Q_LIMIT = 100000

    print('MM1')

    tasas_servicio = []
    tasas_arribos = []
    tamaños_cola = [0,2,5,10,50]

    mm1 = Queue_mm1(num_events, mean_interarrival, mean_service, num_delays_required, Q_LIMIT)
    mm1.simmulate()
    
