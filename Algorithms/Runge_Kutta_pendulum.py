# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:11:47 2022

@author:Théo
"""

import matplotlib.pyplot as plt
import numpy as np

def rk4(r,x, h):
        """ Runge-Kutta 4 method """
        k1 = h*f(r,x)
        k2 = h*f(r+0.5*k1,x+0.5*h)
        k3 = h*f(r+0.5*k2,x+0.5*h)
        k4 = h*f(r+k3,x+h)
        return (k1 + 2*k2 + 2*k3 + k4)/6

def f(r,x):
    a,b=0.1,1
    x, y = r[0], r[1]
    fx,fy = y,-a*y - b*np.sin(x)
    return np.array([fx, fy], float)

h=0.001
tpoints = np.arange(0, 30, h)
xpoints, ypoints  = [], []
r = np.array([0, 2], float)
for x in tpoints:
        xpoints.append(r[0])
        ypoints.append(r[1])
        r += rk4(r,x, h)
plt.plot(tpoints, xpoints)
plt.plot(tpoints, ypoints)
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Lotka-Volterra Model")
plt.savefig("Lotka_Volterra.png")
plt.show()
plt.plot(xpoints, ypoints)
plt.show()