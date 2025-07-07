# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:44:00 2022

@author: Théo
"""
import matplotlib.pyplot as plt
import numpy as np
def f(x,y):
    return y
#bogacki-shampine
def runge(x0, y0, h, f, maxi, X, Y):
    # Count number of iterations using step size or
    # step height h
    # Iterate for number of iterations
    y=y0
    while x0<maxi:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * f(x0, y)
        k2 = h * f(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(x0 + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(x0 + h, y + k3)
        # Update next value of y
        y = y + (k1 + 2 * k2 + 2 * k3 + k4)/6
        Y.append(y)
        # Update next value of x
        x0 = x0 + h
        X.append(x0)
    return X,Y
def bogaki(x0, y0, h, f, maxi, X, Y):
    y=y0
    while x0<maxi:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * f(x0, y)
        k2 = h * f(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(x0 + 0.75 * h, y + 0.75 * k2)
        y1 = y + (2*k1 + 3 * k2 + 4 * k3)/9
        k4 = h*f(x0 + h, y1)
        z=y+(7/24)*k1 + (1/4)*k2 + (1/3)*k3 + (1/8)*k4
        Y.append(z)
        y=y1
        x0 = x0 + h
        X.append(x0)
    return X,Y

X=[0]
Y=[1]
X2=[0]
Y2=[1]
Y3=[0]
X,Y= runge(0,1,0.01,f,10,X,Y)
"""
plt.plot(X,Y)
plt.show()
"""
X1,Y1 = bogaki(0,1,0.01,f,10,X2,Y2)
for t in range(len(Y)-1):
    Y3.append(Y[t]-Y1[t]) #calcul de l'erreur
plt.plot(X,Y3,color='green')
plt.show()

    