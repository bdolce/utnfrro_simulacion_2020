from random import randint
import matplotlib.pyplot as plt 


def fibonacci(n): 
# tomada de 
# https://www.geeksforgeeks.org/python-program-for-program-for-fibonacci-numbers-2/
    a = 0
    b = 1
    if n < 0: 
        print("Incorrect input") 
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        for i in range(2,n): 
            c = a + b 
            a = b 
            b = c 
        return b


class Ruleta():

    cantidad_jugadas = 0
    dinero_disponible = 0
    apuesta_inicial = 0
    plt_index = 1 

    def __init__(self, cantidad_jugadas, dinero_inicial, apuesta_inicial):
        self.cantidad_jugadas = cantidad_jugadas
        self.dinero_inicial = dinero_inicial
        self.apuesta_inicial = apuesta_inicial
        self.inicializa_ruleta()

    def inicializa_ruleta(self):
        self.tiradas = []
        self.numeros_apostados = list(range(0,37,2))
        self.numeros_apostados.remove(0)

        self.dinero_tiempo = []
        self.apuesta_tiempo = []


    def inicializa_ruleta_individual(self):
        self.tiradas_k = []

        self.dinero_disponible = self.dinero_inicial
        self.dinero_tiempo_k = []
        self.dinero_tiempo_k.append(self.dinero_disponible)

        self.apuesta = self.apuesta_inicial
        self.apuesta_tiempo_k = []
        self.apuesta_tiempo.append(self.apuesta)

        #necesaria para estrategia fibonacci
        self.apuesta_fib = 1
        #necesaria para estrategia 1-3-2-6
        self.num_apuesta = 1

    def inicializa_ruleta_conjunto(self):
        self.tiradas_k = []
        #conjuntos
        self.dinero_disponible_conjunto = [self.dinero_inicial for i in range(5)]
        self.dinero_tiempo_conjunto = []
        for d in self.dinero_disponible_conjunto:
            a = []
            a.append(d)
            self.dinero_tiempo_conjunto.append(a)

        self.apuesta_conjunto = [self.apuesta_inicial for i in range(5)]
        self.apuesta_tiempo_conjunto = []
        for d in self.apuesta_conjunto:
            a = []
            a.append(d)
            self.apuesta_tiempo_conjunto.append(a)

        #necesaria para estrategia fibonacci
        self.apuesta_fib = 1
        #necesaria para estrategia 1-3-2-6
        self.num_apuesta = 1

    def apostar(self,estrategia):

        #Registra la apuesta
        self.dinero_disponible -= self.apuesta

        #Tirada de la ruleta
        tiro = randint(0,36)
        self.tiradas_k.append(tiro)

        #estrategia martingala
        if estrategia == "Martingala":
            (self.apuesta, self.dinero_disponible) = self.martingala(tiro, self.apuesta, self.dinero_disponible)

        
        #estrategia martingala inversa
        elif estrategia == "Martingala Inversa":
            (self.apuesta, self.dinero_disponible) = self.martingala_inversa(tiro, self.apuesta, self.dinero_disponible)
        
        # #estrategia dalembert
        elif estrategia == "D'alembert":
            (self.apuesta, self.dinero_disponible) = self.dalembert(tiro, self.apuesta, self.dinero_disponible)
        
        #estrategia fibonacci
        elif estrategia == "Fibonacci":
            (self.apuesta, self.dinero_disponible) = self.fibonacci(tiro, self.apuesta, self.dinero_disponible)

        #estrategia 1-3-2-6
        elif estrategia == "1-3-2-6":
            (self.apuesta, self.dinero_disponible) = self.uno_tres_dos_seis(tiro, self.apuesta, self.dinero_disponible)
        
        #Registra historico de dinero y de apuestas
        self.dinero_tiempo_k.append(self.dinero_disponible)
        self.apuesta_tiempo_k.append(self.apuesta)


    def apostar_conjunto(self):
        #Registra la apuesta
        for i in range(len(self.dinero_disponible_conjunto)):
            if self.apuesta_conjunto[i] <= self.dinero_disponible_conjunto[i]:
                self.dinero_disponible_conjunto[i] -= self.apuesta_conjunto[i]

        #Tirada de la ruleta
        tiro = randint(0,36)
        self.tiradas_k.append(tiro)

        #martingala
        if self.apuesta_conjunto[0] <= self.dinero_disponible_conjunto[0]:
            (self.apuesta_conjunto[0], self.dinero_disponible_conjunto[0]) = self.martingala(tiro, self.apuesta_conjunto[0], self.dinero_disponible_conjunto[0])

        #martingala inversa
        if self.apuesta_conjunto[1] <= self.dinero_disponible_conjunto[1]:
            (self.apuesta_conjunto[1], self.dinero_disponible_conjunto[1]) = self.martingala_inversa(tiro, self.apuesta_conjunto[1], self.dinero_disponible_conjunto[1])

        #Dalembert
        if self.apuesta_conjunto[2] <= self.dinero_disponible_conjunto[2]:
            (self.apuesta_conjunto[2], self.dinero_disponible_conjunto[2]) = self.dalembert(tiro, self.apuesta_conjunto[2], self.dinero_disponible_conjunto[2])

        #Fibonacci
        if self.apuesta_conjunto[3] <= self.dinero_disponible_conjunto[3]:
            (self.apuesta_conjunto[3], self.dinero_disponible_conjunto[3]) = self.fibonacci(tiro, self.apuesta_conjunto[3], self.dinero_disponible_conjunto[3])

        #1-3-2-6
        if self.apuesta_conjunto[4] <= self.dinero_disponible_conjunto[4]:
            (self.apuesta_conjunto[4], self.dinero_disponible_conjunto[4]) = self.uno_tres_dos_seis(tiro, self.apuesta_conjunto[4], self.dinero_disponible_conjunto[4])


        #Registra historico de dinero y de apuestas
        for i in range(len(self.dinero_disponible_conjunto)):
            if self.apuesta_conjunto[i] <= self.dinero_disponible_conjunto[i]:
                self.dinero_tiempo_conjunto[i].append(self.dinero_disponible_conjunto[i])
        
        for i in range(len(self.apuesta_conjunto)):
            if self.apuesta_conjunto[i] <= self.dinero_disponible_conjunto[i]:
                self.apuesta_tiempo_conjunto[i].append(self.apuesta_conjunto[i])
            
        

    def martingala(self, tiro, apuesta, dinero_disponible):
        if tiro in self.numeros_apostados:
            dinero_disponible += apuesta * 2
            apuesta = self.apuesta_inicial
        else:
            apuesta = apuesta * 2 
        
        return (apuesta, dinero_disponible)

    def martingala_inversa(self, tiro, apuesta, dinero_disponible):
        if tiro in self.numeros_apostados:
            dinero_disponible += apuesta * 2
            apuesta = apuesta * 2 
        else:
            apuesta = self.apuesta_inicial

        return (apuesta, dinero_disponible)

    def dalembert(self, tiro, apuesta, dinero_disponible):
        if tiro in self.numeros_apostados:
            dinero_disponible += apuesta * 2 
            if apuesta > 1:
                apuesta -= 1 
        else:
            apuesta += 1

        return (apuesta, dinero_disponible)

    def fibonacci(self, tiro, apuesta, dinero_disponible):
        if tiro in self.numeros_apostados:
            dinero_disponible += apuesta * 2
            if self.apuesta_fib > 2:
                self.apuesta_fib -= 2
                apuesta = fibonacci(self.apuesta_fib) * self.apuesta_inicial
        else:
            self.apuesta_fib += 1
            apuesta = fibonacci(self.apuesta_fib) * self.apuesta_inicial

        return (apuesta, dinero_disponible)

    def uno_tres_dos_seis(self, tiro, apuesta, dinero_disponible):
        if tiro in self.numeros_apostados:
            dinero_disponible += apuesta * 2

            if self.num_apuesta < 5:
                self.num_apuesta += 1 
            else:
                self.num_apuesta = 1
        else:
            self.num_apuesta = 1

        #Hacer la proxima apuesta
        if self.num_apuesta == 1:
            apuesta = self.apuesta_inicial
        elif self.num_apuesta == 2:
            apuesta = self.apuesta_inicial * 3
        elif self.num_apuesta == 3:
            apuesta = self.apuesta_inicial * 2
        elif self.num_apuesta == 4:
            apuesta = self.apuesta_inicial * 6

        return (apuesta, dinero_disponible)


    def agrega_grafica(self, estrategia):

        subplt = plt.subplot(3,2,self.plt_index)

        for i in self.dinero_tiempo:
            subplt.hlines(0,0,len(i),linestyles="dashed", lw=0.8)
            subplt.plot(i)

            if len(i) < self.cantidad_jugadas:
                subplt.annotate("",xy=(len(i), i[len(i)-1]), xytext=(-1,-0.5), textcoords='offset points', arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
            
        subplt.set_xlabel("Numero de tiradas")
        subplt.set_ylabel("Dinero")
        subplt.set_title(estrategia)

        self.plt_index += 1



    def graficar_conjunto(self,estrategias):

        ax1 = plt.subplot(2,1,1)
        ax2 = plt.subplot(2,1,2)


        c = 0
        for i in self.dinero_tiempo_conjunto:
            ax1.plot(i, label=estrategias[c])
            ax1.legend(loc="upper right")
            ax1.set_title("Evolución de dinero en el tiempo")
            ax1.set_xlabel("Numero de tiradas")
            ax1.set_ylabel("Dinero")
            
            if len(i) < self.cantidad_jugadas:
                ax1.annotate("",xy=(len(i), i[len(i)-1]), xytext=(-1,-0.5), textcoords='offset points', arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
 
            c+=1

        c=0
        for i in self.apuesta_tiempo_conjunto:
            ax2.plot(i, label=estrategias[c])
            ax2.legend(loc="upper right")
            ax2.set_title("Evolución de apuestas en el tiempo")
            ax2.set_xlabel("Numero de tiradas")
            ax2.set_ylabel("Apuesta")
            c += 1

        plt.tight_layout(pad=0.5)
        plt.savefig("Graficas_conjunto (" + str(cant_simulaciones) + " simulaciones).png")
        plt.show()

    def simula_apuestas_individual(self, estrategia, dinero_infinito):

        #Setea valores iniciales
        self.inicializa_ruleta_individual()
        
        if dinero_infinito:
            #Dinero infinito
            while len(self.tiradas_k) <= self.cantidad_jugadas:
                self.apostar(estrategia)
        else:
            #Dinero acotado
            while len(self.tiradas_k) <= self.cantidad_jugadas and self.apuesta <= self.dinero_disponible:
                self.apostar(estrategia)
        
        #Añade corrida actual 
        self.dinero_tiempo.append(self.dinero_tiempo_k)
        self.apuesta_tiempo.append(self.apuesta_tiempo_k)
        self.tiradas.append(self.tiradas_k)


    def simula_apuestas_conjunto(self):

        #Setea valores iniciales
        self.inicializa_ruleta_conjunto()
        
        #Dinero infinito
        while len(self.tiradas_k) <= self.cantidad_jugadas:
            self.apostar_conjunto()
        

if __name__ == "__main__":

    ruleta = Ruleta(cantidad_jugadas=50000, dinero_inicial=50000, apuesta_inicial=10)
    
    # Cantidad de corridas a realizar
    cant_simulaciones = 5

    # ¿Simular con dinero infinito?
    #dinero_infinito = True
    dinero_infinito = False

    estrategias = ["Martingala", "Martingala Inversa", "D'alembert", "Fibonacci", "1-3-2-6"]

    for e in estrategias:
        ruleta.inicializa_ruleta()
        
        for k in range(cant_simulaciones):
            ruleta.simula_apuestas_individual(e, dinero_infinito)
        
        #Grafica
        ruleta.agrega_grafica(e)
    

    #Grafica de estategias individuales
    plt.tight_layout(0.5)
    plt.savefig("Graficas_individuales (" + str(cant_simulaciones) + " simulaciones).png")
    plt.show()
    

    # Simulacion de estrategias en conjunto 

    # Simula que se 5 personas están jugando la misma ruleta al mismo tiempo
    # Cada una utiliza una estrategia diferente 
    ruleta.simula_apuestas_conjunto()
    ruleta.graficar_conjunto(estrategias)
