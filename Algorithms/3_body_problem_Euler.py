import math
import numpy as np
import matplotlib.pyplot as plt

µL = 0.012277471
µT = 1 - µL

def three_body_problem(t, y):
    y1, y2, y3, y4 = y
    
    a = y1 + µL
    b = y1 - µT
    y2_2 = y2 * y2
    r1 = math.sqrt(a * a + y2_2)
    r2 = math.sqrt(b * b + y2_2)
    inv_r1_3 = 1 / (r1 * r1 * r1)
    inv_r2_3 = 1 / (r2 * r2 * r2)
    
    return np.array([
        y3,
        y4,
        y1 + 2*y4 - µT*a*inv_r1_3 - µL*b*inv_r2_3,
        y2 - 2*y3 - µT*y2*inv_r1_3 - µL*y2*inv_r2_3
        ])

def Euler(f, t0, y0, h, tmax):
    t = t0
    y = y0
    liste = [y]
    while t < tmax:
        y = y + h*f(t,y)
        t += h
        liste.append(y)
    return liste

y0 = np.array([0.994, 0, 0, -2.0015851063790825224053786224])

liste = Euler(three_body_problem, 0, y0, 1e-6, 17.0652165601579625588917206249)
x = [x[0] for x in liste]
y = [x[1] for x in liste]

plt.plot(x, y)
plt.title("Trajectoire du satellite avec la méthode d'Euler dans le plan (y1,y2)") #fixe le titre du graph
plt.xlabel('y1') #fixe le nom de la courbe en x
plt.ylabel('y2') #fixe le nom de la courbe en y
plt.grid() #configure les lignes de grilles
plt.show() #affiche le graph