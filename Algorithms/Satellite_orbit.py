# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:32:53 2022

@author: johan
"""

from tkinter import *
from math import hypot,sqrt,floor,cos,sin,pi,atan,exp,log


# Ce code simule la mise en orbite d'un satellite.

# Paramètres
#
# L'altitude doit être comprise entre 0 et 360
# La vitesse donnée doit être de l'odre de 15 (unité arbitraire)
# L'angle (exprimé en degrés) peut prendre toutes les valeurs entre 0 et 360
# On peut obtenir les différentes trajectoires d'un satellite (ellipse, parabole ou hyperbole)
# exemple : 105/105/14 ellipse
#           210/45/9   ellipse
#           350/18/12  hyperbole
# Quand à la parabole, c'est plus difficile à obtenir, je vous laisse essayer!

# Fonctionnement
#
# La constante K joue le rôle du produit G(constante de gravité universelle) * M (masse terrestre)
# La trajectoire du satellite est déterminée de façon numérique par résolution de l'équation mécanique:
#     masse_satellite * accélération = force_gravitationnelle_exercée_par_la_terre_sur_le_satellite

def preparer():
    # initialise les paramètres et dessine la terre
    global flag,x,y,dx,dy,D,satellite
    P.config(state=DISABLED)
    T.config(state=ACTIVE)
    can.delete(ALL)

    altitude=int(E_altitude.get())
    angle_degre=int(E_angle.get())
    angle=angle_degre*2*pi/360
    force=int(E_force.get())
    
    x,y=L/2-D/2-altitude,L/2
    dx,dy=force*cos(angle)/20,-force*sin(angle)/20

    Terre=can.create_oval(L/2-D/2,L/2+D/2,L/2+D/2,L/2-D/2,fill='blue')
    satellite=can.create_oval(x-d/2,y+d/2,x+d/2,y-d/2,fill='grey')

def lancer():
    #lance le satellite
    global flag
    flag=1
    orbite()

def orbite():
    #fonction auxilliaire de la fonction lancer
    global x,y,dx,dy,orb
    if flag==1:
        T.config(state=DISABLED)
        #nouvelle position
        x,y=x+dx,y+dy
        r=hypot(x-L/2,L/2-y)
        v=hypot(dx,dy)
        #angle repérant la position du satellite par rapport à l'horizontale
        if x-L/2>0:
            theta=atan((-y+L/2)/(x-L/2))
        else:
            theta=atan((-y+L/2)/(x-L/2))+pi
        dx,dy=dx-K*cos(theta)/(r*r),dy+K*sin(theta)/(r*r)
        can.coords(satellite,x-d/2,y+d/2,x+d/2,y-d/2)
        if x<0 or x>L or y<0 or y>L or r<D/2:
            stop()
        #suivi de la trajectoire du satellite
        can.create_oval(x,y+1,x+1,y,outline='yellow')
    orb=fen.after(8,orbite)

def stop():
    #arrête le satellite et efface l'écran
    "" 
    global flag,orb
    flag=0
    fen.after_cancel(orb)
    P.config(state=ACTIVE)
    can.delete(ALL) # effacement du contenu de la fenêtre 
    E_angle.delete(0,angle)
    E_force.delete(0,force)
    texte=can.create_text(L/2,L/3,text='MERCI\n\nvous pouvez continuer en modifiant les paramètres\n\nou, tout simplement, arrêter !!!',fill="white")



fen=Tk()
fen.title('Mise en orbite!')

L=800 #côté du canvas
D=80  #diamètre de la terre
d=8   #diamètre du satellite
flag=0
angle,force=0,0
K=50  #joue le rôle du produit G*M

can=Canvas(fen,bg='dark blue',height=L,width=L)
can.grid(row=1,column=0,rowspan=2) 
can2=Canvas(fen,bg='brown',highlightbackground='brown') 
can2.grid(row=1,column=1,sticky=N)



S=Button(can2,text='Stop !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",command=stop) 
S.pack(padx=5,pady=5,side=BOTTOM,anchor=SW)

T=Button(can2,text='Lancer !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",command=lancer) 
T.pack(padx=5,pady=5,side=BOTTOM,anchor=SW)

P=Button(can2,text='Préparer !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",command=preparer) 
P.pack(padx=5,pady=5,side=BOTTOM,anchor=SW)

E_force=Entry(can2) 
E_force.pack(padx=8,pady=5,side=BOTTOM) 
Label(can2,text="Choisir la vitesse initiale à donner",fg='white',bg='brown').pack(side=BOTTOM) 

E_angle=Entry(can2) 
E_angle.pack(padx=8,pady=5,side=BOTTOM) 
Label(can2,text="Choisir l'angle à donner",fg='white',bg='brown').pack(side=BOTTOM)

E_altitude=Entry(can2) 
E_altitude.pack(padx=8,pady=5,side=BOTTOM) 
Label(can2,text="Choisir l'altitude de départ",fg='white',bg='brown').pack(side=BOTTOM)

fen.mainloop()
fen.destroy()