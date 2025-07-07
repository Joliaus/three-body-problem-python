# -*- coding: utf-8 -*-

#Les méthodes : Euler/runge kutta d'ordre 4/Bogaki/et représentation des courbes pour déterminer la meilleur
import numpy as np
import matplotlib.pyplot as plt

h=0.05
length=1
def euler():   
    #définition des variables 
    f = lambda t, s: s*t 
    #h = 0.1 # Définition du pas
    t = np.arange(0, length + h, h) #grille numérique (tableau)
    s0 = 1 # Condition initiales
    
    #Méthode d'Euler
    s = np.zeros(len(t))
    s[0] = s0
    
    for i in range(0, len(t) - 1): #i prend des valeurs entre O et la longueur - 1
        s[i + 1] = s[i] + h*f(t[i], s[i]) #
    return s,t
"""
    plt.style.use('seaborn-poster')#défini le style du graphique
    plt.figure(figsize = (12, 8))#créer un objet figure pour lui attribuer des caractéristiques.
    plt.plot(t, s, label='Courbe approximative') #label permet de nommer
    plt.plot(t, (t*t)/2, 'g', label='Courbe exacte') #tracer le graph
    plt.title("Résolution d'une équation différentielle avec la méthode d'Euler") #fixe le titre du graph
    plt.xlabel('t') #fixe le nom de la courbe en x
    plt.ylabel('f(t)') #fixe le nom de la courbe en x
    plt.grid() #configure les lignes de grilles
    plt.legend(loc='lower right') #placer une légende sur les axes.
    plt.show() #afficher le graph
"""

import matplotlib.pyplot as plt
import numpy as np
def f(x,y):
    return y*x
#bogacki-shampine
def runge(x0, y0, h, f, maxi, X, Y):
    #Compter le nombre d'itérations en utilisant la taille du pas ou la hauteur de pas h
    y=y0
    while x0+h<maxi:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * f(x0, y)
        k2 = h * f(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * f(x0 + 0.5 * h, y + 0.5 * k2)
        k4 = h * f(x0 + h, y + k3)
        
        #Attribue la prochaine valeur de y
        y = y + (k1 + 2 * k2 + 2 * k3 + k4)/6
        Y.append(y)
        
        #Attribue la prochaine valeur de x
        x0 = x0 + h
        X.append(x0)
    return X,Y

def bogaki(x0, y0, h, f, maxi, X, Y):
    y=y0
    while x0+h<maxi:
        "Application des formules de Runge Kutta pour trouver la prochaine valeur de y"
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

X,Y= runge(0,length,h,f,1,X,Y)
Yr=[np.exp(x*x/2) for x in X]
Y4,X4=euler()
X1,Y1 = bogaki(0,length,h,f,1,X2,Y2)

plt.style.use('seaborn-poster')#défini le style du graphique

plt.figure(figsize = (12, 8))#créer un objet figure pour lui attribuer des caractéristiques.
plt.title("Résolution d'une équation différentielle avec la méthode d'Euler, de runge et bogacki") #fixe le titre du graph

plt.xlabel('t') #fixe le nom de la courbe en x
plt.ylabel('f(t)') #fixe le nom de la courbe en x
plt.grid() #configure les lignes de grilles
plt.plot(X,Y1,color='black',linewidth=5,linestyle="dotted",label="Bogaki")
plt.plot(X,Y,color='r',linewidth=1,label='Runge')
plt.plot(X4,Y4,color='green',linewidth=5,label='euler')
plt.plot(X,Yr,color='b',linewidth=2,linestyle="dashdot",label='Réel')

plt.legend(loc='lower right') #placer une légende sur les axes.
plt.show()

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

#La fonction plot est créée pour tracer le graphique 
def plot():
    fig = Figure(figsize = (12, 8),dpi = 100)
   	# list of squares
    X=[0]
    Y=[1]
    X2=[0]
    Y2=[1]
    Y3=[0]

    X,Y= runge(0,length,h,f,1,X,Y)
    Yr=[np.exp(x*x/2) for x in X]
    Y4,X4=euler()
    X1,Y1 = bogaki(0,length,h,f,1,X2,Y2)

    plot1 = fig.add_subplot(111)


    plot1.plot(X,Y,color='r',linewidth=1,label='Runge')
    plot1.plot(X1,Y1,color='black',linewidth=5,linestyle="dotted",label="Bogaki")
    plot1.plot(X4,Y4,color='green',linewidth=5,label='euler')
    plot1.plot(X,Yr,color='b',linewidth=2,linestyle="dashdot",label='Réel')
    fig.legend(loc ='upper center')

	# création du canevas Tkinter contenant la figure Matplotlib
    canvas = FigureCanvasTkAgg(fig,
							master = window)
    canvas.draw()

	# placer le canevas dans la fenêtre Tkinter
    canvas.get_tk_widget().pack()

	#création de la barre d'outils Matplotlib
    toolbar = NavigationToolbar2Tk(canvas,
								window)
    toolbar.update()

	# placer la barre d'outils dans la fenêtre Tkinter
    canvas.get_tk_widget().pack()

#La fenêtre principale Tkinter
window = Tk()

#définition du titre
window.title('Plotting in Tkinter')

#dimensions de la fenêtre principale
window.geometry("500x500")

#boutton qui affiche le tracé
plot_button = Button(master = window,
					command = plot,
					height = 2,
					width = 10,
					text = "Plot")

# placer le boutton dans la fenêtre principale
plot_button.pack()

#lancer l'execution
window.mainloop()
