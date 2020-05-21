from random import randint
import matplotlib.pyplot as plt 
import numpy as np

cant_tiros = 0
cant_simulaciones = 0

# Input 
print("Elija un numero de la ruleta (0-36)")
num_elegido = input()
print("Ingrese la cantidad de tiros que desea simular")
cant_tiros = input()
print("Ingrese la cantidad de simulaciones que desea realizar")
cant_simulaciones = input()

num_elegido = int(num_elegido)
cant_tiros = int(cant_tiros)
cant_simulaciones = int(cant_simulaciones)


# Valores esperados (a priori se conoce que son equiprobables)
frecuencia_esperada = 1/37
promedio_esperado = np.average(range(37))
desvio_esperado = np.std(range(37))
varianza_esperada = np.var(range(37))

# Inicializa las listas generales de los valores a buscar. Consistirán de sublistas con los valores obtenidos en cada simulación
frecuencias_relativas = []
promedios = []
desvios = []
varianzas = []

for k in range(cant_simulaciones):  
    frec_absol = 0
    frec_rel = 0

    #Listas de la corrida actual
    tiradas = []
    frec_relativas_k = []
    promedios_k = []
    desvios_k = []
    varianzas_k = []

    #Simulacion (corrida)
    for i in range(1, cant_tiros + 1):
        
        #randint() devuelve un entero aleatorio comprendido entre los dos valores (incluidos los mismos)
        tiro = randint(0,36)
        tiradas.append(tiro)

        #Calcula frecuencia    
        if (tiro == num_elegido):
            frec_absol += 1
        frec_rel = frec_absol / i

        #Añade a las listas de la simulación actual
        frec_relativas_k.append(frec_rel)
        promedios_k.append(np.average(tiradas))
        desvios_k.append(np.std(tiradas))
        varianzas_k.append(np.var(tiradas))
    
    #Añade las listas de la simulación anterior a las matrices generales
    frecuencias_relativas.append(frec_relativas_k)
    promedios.append(promedios_k)
    desvios.append(desvios_k)
    varianzas.append(varianzas_k)



# Grafica datos
# Usa subplots() para poder redimensionar automaticamente el padding entre cada subplot mediante constrained_layout=True 
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, constrained_layout=True)

# Frecuencia
for i in frecuencias_relativas:
    ax1.plot(i)   

ax1.hlines(frecuencia_esperada,0, cant_tiros, linestyles="dashed", lw=1)
ax1.set_xlabel("Numero de tiradas")
ax1.set_ylabel("Frecuencia Relativa")
ax1.set_title("Frecuencia Relativa")


# Promedio
for i in promedios:
    ax2.plot(i)

ax2.hlines(promedio_esperado,0, cant_tiros, linestyles="dashed", lw=1)
ax2.set_xlabel("Numero de tiradas")
ax2.set_ylabel("Promedio")
ax2.set_title("Promedio")

# Desvio
for i in desvios:
    ax3.plot(i)

ax3.hlines(desvio_esperado ,0, cant_tiros, linestyles="dashed", lw=1)
ax3.set_xlabel("Numero de tiradas")
ax3.set_ylabel("Desvio estándar")
ax3.set_title("Desvio estándar")

# Varianza
for i in varianzas:
    ax4.plot(i)

ax4.hlines(varianza_esperada,0, cant_tiros, linestyles="dashed", lw=1)
ax4.set_xlabel("Numero de tiradas")
ax4.set_ylabel("Varianza")
ax4.set_title("Varianza")

# Grafica la figura con todas las graficas en cada subplot y la guarda en un archivo
plt.savefig("Grafica (" + str(cant_simulaciones) + " simulaciones).png")
plt.show()
