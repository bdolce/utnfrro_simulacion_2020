import matplotlib.pyplot as plt
from matplotlib import ticker as tick
from math import log, exp, trunc, ceil, floor, factorial, sqrt
from scipy.stats import chisquare, norm, expon, anderson, normaltest
from scipy.special import comb
import numpy as np
import time

class GLC():
    m = 2**32
    a = 22695477
    c = 1
    x = 0
    seed = 0
    def lcg(self):
        """Linear congruential generator. X is the seed (X0)."""
        self.x = (self.a * self.x + self.c) % self.m 
        return (self.x / self.m)

    def get_seed(self):
        while True:
            string = str(int(time.time()*1000000))
            string = string[-8:]
            if string[0] != "0":
                break
        self.seed = int(string)

class Funciones():

    gen = GLC()

    def uniforme(self, a,b):
        r = self.gen.lcg()
        x = a + (b-a)*r
        return x

    def gamma(self, k, a):
        tr = 1.0
        for i in range(k):
            r = self.gen.lcg()
            tr = tr * r
        x = -log(tr) / a
        return x
        
    def exponencial(self, a):
        ex = 1/a
        r = self.gen.lcg()
        x = -ex * log(r)
        return x

    def normal(self, mu, std, K):
        suma = 0
        for i in range(K):
            r = self.gen.lcg()
            suma = suma + r
        x = std * (suma - K/2) / sqrt(K/12) + mu
        return x

    def binomial(self, N, p):
        x = 0
        for i in range(N):
            r = self.gen.lcg()
            if ((r-p) <= 0):
                x = x + 1
        return x

    def pascal(self,k,q):
        tr = 1.0
        qr = log(q)
        for i in range(k):
            r = self.gen.lcg()
            tr = tr * r
        x = log(tr)/qr
        return x

    def hipergeometrica(self, N, p, m):
        x = 0.0
        
        for i in range(m):
            r = self.gen.lcg()
            if (r-p)<= 0:
                s = 1.0
                x += 1.0
            else:
                s = 0.0
            p = (N * p - s) / (N - 1.0)
            N -= 1.0

        return x

    def poisson(self, l):
        x = 0.0
        b = exp(-l)
        t = 1.0
        while True:
            r = self.gen.lcg()
            t = t * r
            if (t - b)<= 0:
                break
            else:
                x += 1.0
        return x

    def empirica(self, n,casillas):
        r = self.gen.lcg()
        for i in range(1,len(casillas)):
            if casillas[i-1] < r <= casillas[i]:
                return n[i-1][0]


class Pruebas():
    def test(self,distri,random_x, casillas, **params):
        #obs = self.calcular_observadas(random_x, casillas)
        plt.clf()
        
        if distri == "Normal":
            p_valor = normaltest(random_x)[1]
            print("Distribución " + distri +": P-valor = " + str(p_valor))
        elif distri == "Exponencial":
            self.test_expon(exponenciales=random_x)
        elif distri == "Empirica":
            #El parámetro casillas es la lista Muestra, no la lista Casillas"
            #Casillas[0] son las clases
            #Casillas[1] son las probabilidades
            clases = [x[0] for x in casillas]
            clases.append(clases[-1]+0.1)
            probabilidades = [x[1] for x in casillas]

            obs = list(plt.hist(random_x, clases)[0])
            esp = self.calcular_frecs(distri,random_x,probabilidades)

            p_valor = chisquare(obs, esp)[1]
            print("Distribución " + distri +": P-valor = " + str(p_valor))

        else:
            cas = [c for c in casillas]
            cas.append(cas[-1]+0.1)
            obs = list(plt.hist(random_x, cas)[0])

            if distri == "Uniforme":
                esp = self.calcular_frecs(distri,random_x,casillas)
            elif distri == "Binomial":
                esp = self.calcular_frecs(distri,random_x,casillas, p=params["p"], N=params["N"])
            elif distri == "Poisson":
                esp = self.calcular_frecs(distri,random_x,casillas, lamb=params["lamb"])

            p_valor = chisquare(obs, esp)[1]
            print("Distribución " + distri +": P-valor = " + str(p_valor))

    def calcular_observadas(self, random_x, casillas):
        #Por ahora no se usa
        observadas = [0 for x in range(len(casillas)-1)]            
        for num in random_x:
            for i in range(len(casillas)):
                if casillas[i] <= num < casillas[i+1]:
                    observadas[i] += 1
                    break
        return observadas

    def calcular_frecs(self,distri, random_x, casillas, **params):

        if distri == "Uniforme":
            acum = (casillas[1]-casillas[0])/(casillas[-1] - casillas[0]) * len(random_x)
            frec_esp = [acum for x in casillas]
        elif distri == "Exponencial":
            prob_a_rangos = self.calcular_probabilidades(distri,random_x, casillas, lamb = params["lamb"])
            frec_esp = [len(random_x) * x for x in prob_a_rangos]
        elif distri == "Binomial":
            p = params["p"]
            q = 1 - p
            N = params["N"]
            frec_esp = [len(random_x) * comb(N,x) * (p**x) * (q**(N-x)) for x in casillas]
        elif distri == "Poisson":
            lamb = params["lamb"]
            frec_esp = [len(random_x) * exp(-lamb)*(lamb**x)/factorial(x) for x in casillas]
        elif distri == "Empirica":
            frec_esp = [len(random_x) * x for x in casillas]
        return frec_esp

    def calcular_probabilidades(self,distri,random_x, casillas, **params):
        prob_a_rangos = []
        if distri == "Normal":
            mu = params["media"]
            desv = params["desv"]
            for i in range(len(casillas)-1):
                r = abs(norm.cdf(casillas[i+1],mu,desv) - norm.cdf(casillas[i],mu,desv))
                prob_a_rangos.append(r)
        elif distri == "Exponencial":
            lamb = params["lamb"]
            for i in range(len(casillas)-1):
                prob_a_rangos.append(-exp(-lamb*casillas[i+1])+exp(-lamb*casillas[i]))
        return prob_a_rangos


    def test_expon(self, exponenciales):
        statistic, critical, significance = anderson(exponenciales, "expon")
        print("Statistic:" + str(statistic))
        print("Critical:" + str(critical[2]))
        if (statistic > critical[2]):
            print("No pasa test Anderson-Darling (5% nivel de significación)")
        else:
            print("Pasa test Anderson-Darling (5% nivel de significación)")



def mod_eje_y(lista):
    return np.zeros_like(lista) + 1. / len(lista)


class Distribuciones():

    funciones = Funciones()

    def genera_uniforme(self, a,b,n):
        self.funciones.gen.get_seed()

        uniformes = []
        for i in range(n):
            uniformes.append(self.funciones.uniforme(a,b))

        return uniformes

    def genera_gamma(self, k, alpha, n):
        self.funciones.gen.get_seed()

        gammas = []
        for i in range(n):
            gammas.append(self.funciones.gamma(k, alpha))

        return gammas

    def genera_exponencial(self, lamb, n):
        self.funciones.gen.get_seed()
        
        exponenciales = []
        for i in range(n):
            exponenciales.append(self.funciones.exponencial(lamb))

        return exponenciales
        
    def genera_normal(self,media,desv,K,n):
        self.funciones.gen.get_seed()
        
        normales = []
        for i in range(n):
            normales.append(self.funciones.normal(media, desv, K))

        return normales
        

    def genera_binomial(self,N,p,n):
        self.funciones.gen.get_seed()
        
        binomiales = []
        for i in range(n):
            binomiales.append(self.funciones.binomial(N,p))

        return binomiales

    def genera_hipergeometricas(self, N, p, m, n):
        self.funciones.gen.get_seed()

        hipergeometricas = []
        for i in range(n):
            x = self.funciones.hipergeometrica(N,p,m)
            hipergeometricas.append(x)

        return hipergeometricas

    def genera_poisson(self, lamb, n):
        self.funciones.gen.get_seed()
        
        poissons = []
        for i in range(n):
            poissons.append(self.funciones.poisson(lamb))

        return poissons

    def genera_empirica(self, n):
        self.funciones.gen.get_seed()
        
        #muestras = self.pedir_muestra()
        muestras = [(0,0.15),(1,0.2),(2,0.1),(3,0.05),(4,0.1),(5,0.15),(6,0.25)]
        casillas = self.crear_casillas_empirica(muestras)

        empiricas = []

        for l in range(n):
            empiricas.append(self.funciones.empirica(muestras,casillas))

        return empiricas, muestras

    def genera_pascal(self, k, p, n):
        self.funciones.gen.get_seed()
        q = 1 - p

        pascales = []
        for i in range(n):
            pascales.append(self.funciones.pascal(k,q))
        
        return pascales

    def grafica_distribucion(self, distribucion, random_x, **params):
        
        plt.clf()

        discretas = ["Pascal", "Binomial", "Hipergeometrica", "Poisson", "Empirica"]
        discrete = False

        if distribucion in discretas:
            discrete = True 

        if distribucion == "Geometrica":
            bins = np.arange(0, 750, 10) - 0.5
            # pyplot.xticks(np.arange(0, 750, 50))
        else:
           bins = np.arange(0,max(random_x) + 1.5) - 0.5

        if discrete:
            plt.hist(random_x, bins, weights=mod_eje_y(random_x), rwidth = 0.1)
            plt.xticks(bins + 0.5)
        else:
            plt.hist(random_x, bins=1000, weights=mod_eje_y(random_x))
            plt.xticks(bins + 0.5)
           

        plt.show()


    def crear_casillas_normal(self, lista, mu, sigma):
        a = min(lista)
        b = mu - 4 * sigma
        c = (b - a)/10
        casillas = list(np.arange(a,b,c))

        a = casillas.pop(-1)
        b = mu + 4 * sigma
        c = (b - a)/100
        casillas = casillas + list(np.arange(a,b,c))

        a = casillas.pop(-1)
        b = max(lista)   
        c = (b - a)/10
        casillas = casillas + list(np.arange(a,b,c))

        return list(casillas)

    def crear_casillas(self, lista):
        a = int(floor(min(lista)))
        b = int(ceil(max(lista)))
        c = (b - a)/10000 
        casillas = np.arange(a,b,c)
        return list(casillas)
    
    def crear_casillas_empirica(self,n):
        casillas=[]
        casillas.append(-0.1)
        pos = 0
        for i in n:
            pos +=  i[1]
            casillas.append(pos)
        return casillas

    def pedir_muestra(self):
        n = []
        print("Ingrese por linea valor - probabilidad, fin para terminar")
        while True:
            valor = input().replace(" ","")
            if valor == "fin":
                break
            else:
                pos = valor.find("-")
                n.append((float(valor[:pos]),float(valor[pos+1:])))
        return n  


if __name__ == "__main__":

    distribuciones = Distribuciones()
    pruebas = Pruebas()

    # UNIFORME ##
    uniformes = distribuciones.genera_uniforme(a=1,b=2,n=10000)
    casillas_uniformes = distribuciones.crear_casillas(uniformes)
    distribuciones.grafica_distribucion(distribucion="Uniforme", random_x=uniformes, a=1, b=2)
    pruebas.test("Uniforme",uniformes,casillas_uniformes)
    
    ## EXPONENCIAL ##
    exponenciales = distribuciones.genera_exponencial(lamb=1.3,n=10000)
    casillas_exponenciales = distribuciones.crear_casillas(exponenciales)
    distribuciones.grafica_distribucion(distribucion="Exponencial", random_x=exponenciales, lamb=1.3)
    pruebas.test("Exponencial", exponenciales, casillas_exponenciales,lamb=1.3)

    # ## GAMMA ##
    gammas = distribuciones.genera_gamma(k=5,alpha=0.5,n=10000)
    casillas_gamma = distribuciones.crear_casillas(gammas)
    distribuciones.grafica_distribucion(distribucion="Gamma", random_x=gammas, k=5, alpha=0.5)

    ## NORMAL ##
    normales = distribuciones.genera_normal(media=2, desv=0.75, K=102, n=10000)
    casillas_normales = distribuciones.crear_casillas_normal(normales, mu=2, sigma=0.75)
    distribuciones.grafica_distribucion(distribucion="Normal", random_x=normales, media=2, desv=0.75)
    pruebas.test("Normal",normales, casillas_normales,media=2, desv=0.75)

    # ## PASCAL ##
    pascales = distribuciones.genera_pascal(k=2,p=0.2, n=10000)
    casillas_pascales = distribuciones.crear_casillas(pascales)
    distribuciones.grafica_distribucion("Pascal", pascales)
    
    # BINOMIAL ##
    binomiales = distribuciones.genera_binomial(N=30, p=0.45, n=10000)
    casillas_binomiales = [0,1,2]
    distribuciones.grafica_distribucion("Binomial", random_x=binomiales)
    pruebas.test("Binomial",binomiales, casillas_binomiales, p = 0.45, N=30)

    # ## HIPERGEOMETRICA ##
    hipergeometricas = distribuciones.genera_hipergeometricas(N=130, p=0.2, m=30, n=10000)
    distribuciones.grafica_distribucion("Hipergeometrica", hipergeometricas)

    # POISSON ##
    poissons = distribuciones.genera_poisson(lamb=5, n=10000)
    casillas_poisson = range(int(max(poissons))+2)
    distribuciones.grafica_distribucion("Poisson", poissons, lamb=5)
    pruebas.test("Poisson", poissons, casillas_poisson, lamb=5)

    ## EMPIRICA ##
    empiricas, muestras = distribuciones.genera_empirica(n=10000)
    distribuciones.grafica_distribucion("Empirica", empiricas)
    pruebas.test("Empirica", empiricas, muestras)