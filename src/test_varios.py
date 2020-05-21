
import time
from PIL import Image
import matplotlib.pyplot as plt
from random import random
from itertools import repeat
from scipy.stats import chisquare
from math import sqrt
from scipy.stats.distributions import chi2


def lcg(m, a, c, x):
    """Linear congruential generator. X is the seed (X0)."""
    x = (a * x + c) % m 
    return x


if __name__ == "__main__":

    #seed = 1
    a = 1103515245
    c = 12345
    m = 2 ** 32
    seed = int(time.time())

    random_x = []

    x = seed
   # total = 262144
    total = 256*256

    for i in range(total):
        x = lcg(m,a,c,x)
        random_x.append(x/m)


    #here we go.. again
    casillas = [a/100 for a in range(101)]
    observadas = [0 for i in range(101)]
    esperadas = [total/100 for i in range(101)]
    rangos_a_random = []

    n = 200
    cont_distancias = [0 for i in range(n)]

    #arma la secuencia de casillas a las que pertenecen los n aleatorios generados
    for k in random_x:
        if k == 1.0:
                rangos_a_random.append(1.0)
        else:
            for i in range(len(casillas)):
                if casillas[i] <= k and k < casillas[i+1]:
                    rangos_a_random.append(casillas[i])
                    break

    #
    for k in range(len(rangos_a_random)):
        h = k+1
        while h <= len(rangos_a_random)-1 and rangos_a_random[k] != rangos_a_random[h]:
            h += 1
        if h != len(rangos_a_random):
            espera = h - k
            if espera > n:
                espera = n
            cont_distancias[espera -1] += 1
            #cont_distancias[0] -> distancia 1
            #cont_distancias[1] -> distancia 2
            #cont_distancias[2] -> distancia 3
            # ... 
            #cont_distancias[n-1] -> distancia >= n


    print(cont_distancias)
    print(sum(cont_distancias))














# x = 1.00

# class Generator:
    

#     def lcg(self, m, a, c):
#         global x

#         xf = (a * x + c) % m
#         x = xf 

#         return xf/m


# rng = Generator()

# obs = []

# for i in range(10):
#     a = rng.lcg(m=2**32, a=1103515245, c=12345)
#     obs.append(a)

# print(obs)




# def rng(m=2**32, a=1103515245, c=12345):
#     rng.current = (a*rng.current + c) % m
#     return rng.current/m

# # setting the seed
# rng.current = 1
# obs = []

# for i in range(10):
#     obs.append(rng())

# print(obs)
