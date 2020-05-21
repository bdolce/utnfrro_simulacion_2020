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

def middle_square(seed):
    number = seed
    number = int(str(number * number).zfill(8)[2:6])  # zfill adds padding of zeroes
    return number / 9999


if __name__ == "__main__":

    #seed = 1
    a = 1103515245
    c = 12345
    m = 2 ** 32
    seed = int(time.time())

    random_x = []

    x = seed
    #x = 99
    total = 262144

    # #LCG
    for i in range(total):
        x = lcg(m,a,c,x)
        random_x.append(x/m)

    #Middle-square
    # for i in range(total):
    #     x = middle_square(x)
    #     random_x.append(x)

    #here we go.. again
    casillas = [a/100 for a in range(101)]
    observadas = [0 for i in range(101)]
    esperadas = [total/100 for i in range(101)]



    #Prueba Chi_cuadrado

    # for n in random_x:
    #     if n == 1:
    #         observadas[100] += 1
    #     else:
    #         for i in range(len(casillas)):
    #             if casillas[i] <= n and n < casillas[i+1]:
    #                 observadas[i] += 1
    #                 break


    # oi_ei = []

    # for i in range(len(observadas)):
    #     oi_ei.append(((observadas[i]-esperadas[i])**2 ) / esperadas[i])

    # chicuadrado = sum(oi_ei)

    # #print(observadas)
    # #p_value = chisquare(observadas,esperadas)

    # p_value = chi2.sf(chicuadrado,99)
    # #print(observadas)
    # #print(esperadas)
    
    # print(chicuadrado)
    # print(p_value)



    #Muestra imagen

    cont = 0
    cont_blancos = 0
    cont_negros = 512*512

    #imagen con resultados RNG
    img = Image.new('RGB', (512,512), "black") #crea imagen en negro
    pixels = img.load()  #crea pixelmap
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if random_x[cont] > 0.5:
                pixels[i,j] = (255,255,255) #set color
                cont_blancos += 1
            cont += 1

   # cont_negros -= cont_blancos
   # print("Blancos: " + str(cont_blancos))
   # print("Negros: " + str(cont_negros))

    img.show()
