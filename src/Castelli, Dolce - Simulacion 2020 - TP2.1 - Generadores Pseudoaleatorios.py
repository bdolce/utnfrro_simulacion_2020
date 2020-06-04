import time
from PIL import Image
import matplotlib.pyplot as plt
from random import random
from itertools import repeat
from scipy.stats import chisquare
from math import sqrt
from scipy.stats.distributions import chi2
import numpy as np
from matplotlib.ticker import MaxNLocator
from collections import Counter


############################################ Definiciones ####################################################

class GLC():

    def lcg(self, m, a, c, x):
        """Linear congruential generator. X is the seed (X0)."""
        x = (a * x + c) % m 
        return x

    def get_seed(self, l, debug=False):
            largo = l
            while True:
                string = str(int(time.time()*1000000))
                string = string[-largo:]
                if string[0] != "0":
                    break
            seed = string
            
            if debug:
                print ("\t\tSemilla: " + seed)

            return int(seed)

    def genera_valores(self, cant_simulaciones, total, parametros_glc):
        
        aleatorios = []

        print('Generando Valores GLC')
        
        for parametro in parametros_glc:
            #l representa cada GLC
            #print(parametro[3] + ":")

            secuencia_corridas = []

            for u in range(cant_simulaciones):
                #u cada simulación con semilla diferente
                #print("\tSim: " + str(u + 1))

                #Obtiene parametros para el generador
                #Semilla siempre es el tiempo
                seed = self.get_seed(6)
                x = seed
                a = parametro[0]
                c = parametro[1]
                m = parametro[2]

                secuencia_random = []
                
                #LCG
                for i in range(total):
                    #i es cada número aleatorio de la secuencia
                    x = self.lcg(m,a,c,x)
                    
                    secuencia_random.append(x/m)

                secuencia_corridas.append(secuencia_random)

            aleatorios.append(secuencia_corridas)

        return aleatorios

class medio_del_cuadrado():
    potencias_de_10 = []
    dividir = 0
    largo = 0
    inicio = 0
    fin = 0


    def genera_valores(self, longitudes, cant_simulaciones, total, incluye_semilla):

        aleatorios = []

        print('Generando Valores Medio del cuadrado')

        for longitud in longitudes:
            #print("Longitud : " + str(longitud))
            #l es cada largo de semilla diferente
            self.setear_largo(longitud)
            
            secuencia_corridas = []
            
            for u in range(cant_simulaciones):
                #print("\tSim: " + str(u + 1))
                #u cada simulación con semilla diferente
                secuencia_random = []
                
                seed = self.get_seed(longitud)
                x = seed
                self.llenar_potencias_de_diez()

                #Se usa para calcular las distancias de los ciclos en el grafico
                #de caja y bigotes
                if incluye_semilla:
                    secuencia_random.append(seed/self.dividir)
                
                for i in range(total):
                    #i es cada numero de la secuencia
                    x = self.middle_square(x)
                    secuencia_random.append(x/self.dividir)
                    
                secuencia_corridas.append(secuencia_random)
            
            aleatorios.append(secuencia_corridas)

        return aleatorios

    def get_seed(self, l, debug=False):
        largo = l
        while True:
            string = str(int(time.time()*1000000))
            string = string[-largo:]
            if string[0] != "0":
                break
        seed = string
        
        if debug:
            print ("\t\tSemilla: " + seed)
        
        return int(seed)

    def setear_largo(self, l):
        self.largo = l
        self.inicio = int(2*l*(1/4))
        self.fin = int(2*l*(3/4))

    def llenar_potencias_de_diez(self):
        self.potencias_de_10 = ['0' for i in range(self.largo)]
        self.potencias_de_10.insert(0,'1')
        self.dividir = int("".join(self.potencias_de_10))

    def middle_square(self,seed):
        number = seed
        number = int(str(number * number).zfill(2*self.largo)[self.inicio:self.fin])  # zfill adds padding of zeroes
        return number

class Pruebas():

    def calcular_observadas(self, random_x, casillas):
        print("Calcular observadas:")

        observadas = []

        for parametro in random_x:
            #largo de semilla diferente o cada glc con distintos parametros
            #print("Tipo:" + str(parametro))
            observadas_parametro = []
            observadas_secuencia = []

            for secuencia in parametro:
                #secuencia individual de numeros aleatorios, es cada simulación con semilla diferente
                #print("\tu: " + str(u))
                observadas_secuencia = [0 for x in range(len(casillas)-1)]

                for ran in secuencia:
                    #ran es cada numero aleatorio dentro de la secuencia

                    for i, casilla in enumerate(casillas,start=0):
                        if casilla <= ran < casillas[i+1]:
                            observadas_secuencia[i] += 1
                            break
                
                observadas_parametro.append(observadas_secuencia)
                    
            observadas.append(observadas_parametro)

        return observadas

    def calcular_chi_espera(self, cont_distancias, frec_esp_rangos):

        p_values = []         
        print("Calcular Chi - Prueba de esperas")
        
        for l, distancias_largo_semilla in enumerate(cont_distancias,start=0):
            #print("\ti:" + str(l))
            #l es cada largo de semilla diferente o cada glc

            p_values_parametro = []

            for u, distancias_simulacion in enumerate(distancias_largo_semilla,start=0):
                #print("\t\tu: " + str(u))
                #u cada simulación con semilla diferente
                p_values_parametro.append(chisquare(distancias_simulacion, frec_esp_rangos[l][u]))

            p_values.append(p_values_parametro)

        return p_values 

    def calcular_chi_bondad(self,observadas,esperada):

        p_values = []
        print("Calcular Chi - Prueba de Bondad de ajuste:")

        for observadas_parametro in observadas:
            
            p_values_parametro = []
            
            for observadas_secuencia in observadas_parametro:
                esperadas_secuencia = [esperada for k in range(len(observadas_secuencia))]
                p_values_parametro.append(chisquare(observadas_secuencia, esperadas_secuencia ))

            p_values.append(p_values_parametro)

        return p_values


    ######Esperas###########

    def alinear_casillas_random(self, random_x, casillas):

        print("Alinear casillas y número:")

        rangos_a_random = []

        for largo_semilla in random_x:

            rangos_parametro = []

            for secuencia in largo_semilla:

                rangos_secuencia = []

                for ran in secuencia:
                    
                    for i, casilla in enumerate(casillas,start=0):
                        if casilla <= ran < casillas[i+1]:
                            rangos_secuencia.append(casilla)
                            break
                    
                rangos_parametro.append(rangos_secuencia)

            rangos_a_random.append(rangos_parametro)

        return rangos_a_random

    
    def inicializa_cont_distancias(self, random_x, n):
        
        cont_distancias = []

        for largo_semilla in random_x:
            
            cont_distancias_tipo = []
            for secuencia in largo_semilla:
                
                cont_distancias_secuencia = []
                for num in range(n):
                    cont_distancias_secuencia.append(0)
                
                cont_distancias_tipo.append(cont_distancias_secuencia)
            
            cont_distancias.append(cont_distancias_tipo)
        
        return cont_distancias
            

    def contar_distancias(self, random_x, n, rangos_a_random):

        cont_distancias = self.inicializa_cont_distancias(random_x, n)

        larg = len(rangos_a_random[0][0])
        
        print("Contar casillas:")

        for l, largo_semilla in enumerate(rangos_a_random,start=0):
            #print("i:" + str(l))
            #l es cada largo de semilla diferente o cada glc

            for u, secuencia in enumerate(largo_semilla,start=0):
                #print("\tu: " + str(u))
                #u cada simulación con semilla diferente

                for k in range(larg):
                    #o es la casilla asignada a cada numero de la secuencia:
                    h = k+1
                    while h <= larg-1 and secuencia[k] != secuencia[h]:
                        h += 1
                    
                    if h != larg:
                        espera = h - k
                        if espera > n:
                            espera = n
                        cont_distancias[l][u][espera -1] += 1
                        #cont_distancias[0] -> distancia 1
                        #cont_distancias[1] -> distancia 2
                        #cont_distancias[2] -> distancia 3
                        # ... 
                        #cont_distancias[n-1] -> distancia >= n

        return cont_distancias

    def sumar_distancias(self, cont_distancias):
        
        suma_secuencia = []
        suma_distancias = []
        
        for largo_semilla in cont_distancias:
            for secuencia in largo_semilla:
                suma_secuencia.append(sum(secuencia))

            suma_distancias.append(suma_secuencia)
            
        return suma_distancias 

    def calcular_probabilidades(self, n):

        prob_a_rangos = []

        for i in range(n):
            if i < n-1:
                prob_a_rangos.append(((1-0.01)**(i))*0.01)
            else:
                prob_a_rangos.append((1-0.01)**(i+1))

        return prob_a_rangos


    def calcular_frec_esperadas(self, cont_distancias, n):
        
        suma_frecuencias = self.sumar_distancias(cont_distancias) 
        prob_a_rangos = self.calcular_probabilidades(n)

        frec_esp_rangos = []
        frec_esp_secuencia = []
        frec_esp_tipo = []


        for suma_largo_semilla in suma_frecuencias:

            for suma_secuencia in suma_largo_semilla:
                frec_esp_secuencia = [suma_secuencia * x for x in prob_a_rangos]
                frec_esp_tipo.append(frec_esp_secuencia)

            frec_esp_rangos.append(frec_esp_tipo)

        return frec_esp_rangos

    def clasificar_distancias(self, longitudes, random_x, titulos):
        distancias = []
        largos = [] 

        print('Clasificando distancias')

        for lar, largo_semilla in enumerate(random_x,start=0):

            distancia_patron = []
            largo_patron = []

            print(titulos[lar])

            for s, secuencia in enumerate(largo_semilla,start=1):
                

                larg = len(secuencia)
                if s % 250 == 0:
                    print('\tSimulacion ' + str(s))

                for k in range(larg+1):
                    #o es la casilla asignada a cada numero de la secuencia:
                    if k == larg:
                        break
                    h = k+1
                    while h <= larg-1 and secuencia[h] != secuencia[k]:
                        h += 1
                    if h != larg:
                        distancia = h - k

                        distancia_patron.append(k)
                        largo_patron.append(distancia)
                        break

                if k == larg:
                    #Si k es el largo, no se considerará que existe un ciclo,
                    #por lo que se contará como un ciclo de largo 0
                    distancia_patron.append(k)
                    largo_patron.append(0)

            distancias.append(distancia_patron)
            largos.append(largo_patron)

        return distancias, largos


    def prueba_bondad(self, observadas, esperada, debug=False):
        p_valores = []

        p_valores = self.calcular_chi_bondad(observadas, esperada)
        
        if debug:
            print(p_valores)

        return p_valores 
    
    def prueba_distancias(self, random_x, casillas, debug=False):

        p_valores = []

        rangos_a_random = self.alinear_casillas_random(random_x, casillas)

        n = 200
 
        cont_distancias = self.contar_distancias(random_x, n, rangos_a_random)
        frec_esp_rangos = self.calcular_frec_esperadas(cont_distancias, n)

        p_valores = self.calcular_chi_espera(cont_distancias, frec_esp_rangos)

        if debug:
            print(p_valores)
        
        return p_valores

    def imprime_pvalores(self, p_valores, titulos):
        for i, p_value_parametro in enumerate(p_valores,start=0):
            print('\n' + titulos[i])

            for p_value_secuencia in p_value_parametro:
                print(p_value_secuencia[1])    

class Graficas():
    
    def grafica_observadas(self, observadas, casillas, total, titulos, tipo_rng):

        print("GRAFICA FRECUENCIAS - HISTOGRAMA")


        #l es cada largo de semilla diferente o cada glc
        for l, parametro in enumerate(random_x,start=0):

            fig, axs = plt.subplots(2, 2, constrained_layout=True)
            fig.suptitle('Histograma frecuencias ' + tipo_rng + ' - ' + str(titulos[l]))

            cont = 0
            a = 0
            ax = plt.Subplot 

            #u cada simulación con semilla diferente
            for u, secuencia in enumerate(parametro,start=1):
                if cont < 2:
                    #axs[fila][columna]
                    ax = axs[a][cont]
                else:
                    cont = 0
                    a = 1 
                    ax = axs[a][cont]
            
                ax.hist(secuencia, bins=casillas)
                ax.set_xticks([i/10 for i in range(11)])
                ax.set_title("Simulacion " + str(u))
                ax.set_xlabel("Casilla")
                ax.set_ylabel("Frecuencia Absoluta")

                cont += 1 
            
            win_manager = plt.get_current_fig_manager()
            win_manager.window.state('zoomed')
            #win_manager.full_screen_toggle()

            plt.savefig("Grafica histograma - " + titulos[l] +".png")
            plt.show()



    def grafica_scatter(self,random_x,titulos,tipo_rng):

        print('Grafica Scatter Plot')

        #l es cada largo de semilla diferente o cada glc
        for l, parametro in enumerate(random_x,start=0):

            fig, axs = plt.subplots(2, 2, constrained_layout=True)
            fig.suptitle('Diagrama de dispersión ' + tipo_rng + ' - ' + str(titulos[l]))

            cont = 0
            a = 0
            ax = plt.Subplot 

            #u cada simulación con semilla diferente
            for u, secuencia in enumerate(parametro,start=1):
                #print("u: " + str(u))
                if cont < 2:
                    ax = axs[a][cont]
                else:
                    cont = 0
                    a = 1 
                    ax = axs[a][cont]

                x = secuencia[0:total-1]
                y = secuencia[1:total]
            
                ax.scatter(x,y,marker='o',s=2)
                ax.set_title("Simulacion " + str(u))
                ax.set_xlabel("secuencia[i]")
                ax.set_ylabel("secuencia[i+1]")

                cont += 1 

            win_manager = plt.get_current_fig_manager()
            win_manager.window.state('zoomed')
            #win_manager.full_screen_toggle()

            plt.savefig("Grafica scatter-plot - " + titulos[l] +".png")
            plt.show()

    def grafica_distancias(self, distancias, largos, longitudes):
        for l in range(len(longitudes)):
            fig=plt.figure()
            fig.add_subplot(1,2,1)
            plt.boxplot([distancias[l]],
                patch_artist=True, sym="o",
                capprops=dict(color="green"),
                medianprops=dict(color="orange"),
                whiskerprops=dict(color="yellow"))
            plt.ylabel('Distancia hasta el \ncomienzo del patrón')

            x, y = zip(*sorted(Counter(largos[l]).items()))
            
            fig.add_subplot(1,2,2)
            plt.stem(x, y)#, use_line_collection=True)
            
            fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.ylabel('Largo del patrón')
            fig.suptitle("Diagrama de caja y bigote para simulaciones del \ngenerador ""Parte media del cuadrado"" de longitud de semilla " + str(longitudes[l]))
            
            win_manager = plt.get_current_fig_manager()
            win_manager.window.state('zoomed')
            #win_manager.full_screen_toggle()
            
            plt.savefig("Grafica largo de semilla " + str(longitudes[l]) +".png")
            plt.show()



if __name__ == "__main__":
    
    casillas = [a/100 for a in range(101)]
    total = 10000
    cant_simulaciones = 4
    debug = True

    pruebas = Pruebas()
    graficas = Graficas()


    #GLC

    #Inicializa el glc
    glc = GLC()

    #Parámetros de GLC de C/C++, Java, Visual Basic
    parametros_glc = [[22695477,1,2**32, 'C'],[25214903917,11,2**48-1, 'Java'],[101,1,2**16, 'Arbitrarios']]
    titulos = ['Parametros C', 'Parametros Java', 'Parametros arbitrarios']
    tipo_rng = 'GLC'

    #Genera valores aleatorios usando glc
    random_x = glc.genera_valores(cant_simulaciones=cant_simulaciones, total=total, parametros_glc=parametros_glc)
    
    #Grafica histograma con las frecuencias de los numeros generados
    graficas.grafica_scatter(random_x,titulos,tipo_rng)

    #Calcula observadas y grafica
    observadas = pruebas.calcular_observadas(random_x, casillas)
    esperada = total / len(casillas)

    graficas.grafica_observadas(observadas,casillas, total, titulos, tipo_rng)
    
    #Obtiene pvalores por prueba de bondad de ajuste
    p_valores_bondad = pruebas.prueba_bondad(observadas, esperada, debug=False)    
    pruebas.imprime_pvalores(p_valores_bondad, titulos)

    #Obtiene pvalores por prueba de distancias
    p_valores_distancias = pruebas.prueba_distancias(random_x, casillas, debug=False)
    pruebas.imprime_pvalores(p_valores_distancias, titulos)


    #MIDDLE SQUARE

    #Inicializa el middle_square
    middle_square = medio_del_cuadrado()
    
    #Longitudes del generador
    longitudes = [4,6,8]
    tipo_rng = 'Medio de los cuadrados'
    titulos = ['Longitud 4','Longitud 6','Longitud 8']

    #Genera valores aleatorios usando glc
    random_x = middle_square.genera_valores(longitudes, cant_simulaciones, total, incluye_semilla=False)
    
    #Guarda en un archivo la secuencia generada (para visualizar el patrón)
    with open('Secuencias_middle_square.txt', 'w') as file:

        for l,longitud in enumerate(random_x,start=0):
            file.write('\n' + titulos[l] + '\n')
            
            for s, secuencia in enumerate(longitud,start=1):
                    file.write('\n' + 'Secuencia ' + str(s) + '\n')
                    file.write(str(secuencia))

    #Grafica histograma con las frecuencias de los numeros generados
    graficas.grafica_scatter(random_x, titulos, tipo_rng)

    #Calcula observadas y grafica
    observadas = pruebas.calcular_observadas(random_x, casillas)
    esperada = total / len(casillas)

    graficas.grafica_observadas(observadas,casillas, total, titulos, tipo_rng)

    #Obtiene pvalores por prueba de bondad de ajuste
    p_valores_bondad = pruebas.prueba_bondad(observadas, esperada, debug=False)
    pruebas.imprime_pvalores(p_valores_bondad, titulos)

    #Obtiene pvalores por prueba de distancias
    p_valores_distancias=  pruebas.prueba_distancias(random_x, casillas, debug=False)
    pruebas.imprime_pvalores(p_valores_distancias, titulos)

    #DIAGRAMA CAJA MIDDLE SQUARE
    random_x = middle_square.genera_valores(longitudes, cant_simulaciones=500, total=2000, incluye_semilla=True)
    (distancias, largos) = pruebas.clasificar_distancias(longitudes, random_x, titulos)
    graficas.grafica_distancias(distancias, largos, longitudes)