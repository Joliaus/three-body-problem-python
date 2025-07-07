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

def Bogacki_Shampine(f, t0, y0, h, tmax):
    t = t0
    y = y0
    liste = [y]
    while t < tmax:
        F1 = f(t, y)
        F2 = f(t + h/2, y + h/2*F1)
        F3 = f(t + 3*h/4, y + 3*h/4*F2)
        y = y + h*(2*F1/9 + F2/3 + 4*F3/9)
        t += h
        liste.append(y)
    return liste

y0 = np.array([0.994, 0, 0, -2.0015851063790825224053786224])

liste = Bogacki_Shampine(three_body_problem, 0, y0, 1e-4, 17.0652165601579625588917206249)
x = [x[0] for x in liste]
y = [x[1] for x in liste]

plt.plot(x, y)
plt.title("Trajectoire du satellite avec la méthode de Bogacki-Shampine dans le plan (y1,y2)") #fixe le titre du graph
plt.xlabel('y1') #fixe le nom de la courbe en x
plt.ylabel('y2') #fixe le nom de la courbe en y
plt.grid() #configure les lignes de grilles
plt.show() #affiche le graph