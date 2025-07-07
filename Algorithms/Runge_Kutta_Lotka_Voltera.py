import matplotlib.pyplot as plt
import numpy as np
def f(y, x): #définition de la fonction à deux variables pour la simulation de la population
        x, y = r[0], r[1]
        fxd = x*(1 - y) #comportement sur x
        fyd = y*(x-1) #comportement sur y 
        return np.array([fxd, fyd], float)

def rk4(y, x, h): #méthode runge kutta RK4 sans itération 
        """ Runge-Kutta 4 method """
        k1 = h*f(y, x)
        k2 = h*f(y+0.5*k1, x+0.5*h)
        k3 = h*f(y+0.5*k2, x+0.5*h)
        k4 = h*f(y+k3, x+h)
        return (k1 + 2*k2 + 2*k3 + k4)/6

h=0.001 #pas
tpoints = np.arange(0, 30, h) #échelle dans le temps
xpoints, ypoints  = [], [] 
r = np.array([2, 2], float)
for i in tpoints:
        xpoints.append(r[0])
        ypoints.append(r[1])
        r += rk4(r, i, h)
plt.plot(tpoints, xpoints)
plt.plot(tpoints, ypoints)

plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Lotka-Volterra Model")
plt.savefig("Lotka_Volterra.png")
plt.show()
plt.plot(xpoints, ypoints)
plt.show()