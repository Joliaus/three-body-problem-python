# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import subprocess  
from math import *

 
 
nu = 0.01 # parameters
R = 1.5 # zone de dessin x=-R->R, y=-R->R

opt_section = 1 # 1: en (x,y) condition px+y=0 
                 # 2: en (x,px), condition y=0

#--- recherche precise des points fixe de Lagrange L1,L2,L3
def f_L(x):
    return (1-nu)*(x+nu)/abs((x+nu)**3) + nu*(x+nu-1)/abs((x+nu-1)**3) - x

def Dicho(x1,x2):
    f1,f2 = f_L(x1), f_L(x2) 
    while(x2-x1>1e-10):
       xm = (x1+x2)/2 
       fm=f_L(xm)
       if(fm>=0):
           x1=xm
           f1=fm
       else:
           x2=xm
           f2=fm
    return x2

"""
sortie: Listes TxL, TyL des positions (x,y) des pts de Lagrange
"""
def Calcul_pts_Lagrange():
    global TxL, TyL    
    #-- valeurs approchées pour 0,1,2
    TxL= [1-(nu/3)**(1/3.), 1+(nu/3)**(1/3.), -1-5*nu/13, 0.5-nu, 0.5-nu]
    TyL = [0,0,0, sqrt(3)/2., -sqrt(3)/2.]
    
    #-- valeurs precises trouvées par dichotomie
    x1,x2 = -1e3, -nu-1e-8 # encadrement de départ 
    TxL[2] = Dicho(x1,x2)
    
    x1,x2 = -nu+1e-8, 1-nu-1e-8 # encadrement de départ 
    TxL[0] = Dicho(x1,x2)
    
    x1,x2 = 1-nu+1e-8, 1e3 # encadrement de départ 
    TxL[1] = Dicho(x1,x2)

           

#-------- equations du mouvement pb 3 corps restreint. Variables x, px, y, py
def V(y,t):
  global nu
  x,px,y,py = y[0],y[1],y[2],y[3]   
  R1 = sqrt( (x+nu)**2 + y**2)
  R2 = sqrt( (x+nu-1)**2 + y**2)
  #print('R1=',R1, ' R2=',R2, ' x=',x , ' y=',y, ' nu=',nu)
  dxdt = px + y
  dpxdt = py - (1-nu)*(x+nu)/R1**3 - nu*(x+nu-1)/R2**3
  dydt = py-x
  dpydt = -px - (1-nu)*y/R1**3 - nu*y/R2**3
  return dxdt, dpxdt, dydt, dpydt



 
#--------- fonction pour section de Poincaré
 
def f(y):
    if(opt_section==1):
        return y[1]+y[2]  # condition px + y = 0
    elif(opt_section==2):
        return y[2]  # condition y = 0


#--------------------------------------
"""
entree: y0 : condition initiales
        t : temps initial
        Dt : pas de temps (assez petit)

Utilise la fonction f(y) \in R qui definit la section de Poincare par f(y)=0 et passage de f>0 à f<0
Utilise la fonction dy/dt = V(y) qui definit le champ de vecteur

sortie: y: position suivante qui verifie f(y=0
        t:  tq y =y(t)
        Ly : liste des valeurs intermediaires y(t(i) avec t(i+1) - t(i) = Dt
            contenant la premiere mais pas  la derniere
        
rem: t final > t initial + Dt
        
"""
def Application_de_Poincare(y0,t):
    #----Recherche prochain intervalle ou f change de signe ---------------------
    """
    1ere partie
    entree: y0 : condition initiales
            t : temps initial
            Dt : pas de temps (assez petit)
            
    sortie: Tt: intervalle en temps [t,t+Dt]
           Ty : intervalle en position [y(t), y(t+Dt)]
           tels que f(y(t))>0 et f(y(t+Dt))<0
    """ 
    Ty = [y0] #condition initiales encapsulée dans liste  
    Ly = np.array(y0) # memorise
    
    #-- on passe intervalle Dt
    Tt = [t, t+Dt]
    Ty = odeint(V, y0, Tt)
    y0 = Ty[len(Ty)-1] # coordonnées finales
    
    
    t += Dt
    f_old = f(y0)
    f_new = f_old
   
    while(f_old<0 or f_new >0): 
        f_old = f_new    
        Tt = [t, t+Dt]
        Ly = np.vstack([Ly, y0])
        
        Ty = odeint(V, y0, Tt)
        y0 = Ty[len(Ty)-1] # coordonnées finales
        f_new = f(y0)
        #print ('t=',Tt[1],' y=',y0, ' f=',f_new)
        t +=Dt
        
    
    #-- dichotomie ------
    """     
    2eme partie
    entree: Tt: intervalle en temps [t,t+Dt]
           Ty : intervalle en position [y(t), y(t+Dt)]
               tels que les points y(t) et y(t+Dt) sont de part et d'autre de la Section de Poincaré
    """ 
    
    while((Tt[1]-Tt[0])>1e-10): # precision sur t
        tm = (Tt[0]+Tt[1])/2 #point intermediare
        Ty2 = odeint(V, Ty[0], [Tt[0],tm]) 
        fm = f(Ty2[1]) # valeur intermediaire
        if(fm>0): # on conserve la 2eme moitié
            Tt[0] = tm
            Ty[0] = Ty2[1]
        else: # on conserve la 1ere moitié
            Tt[1] = tm
            Ty[1] = Ty2[1]
        #print('t0=',Tt[0], 't1=', Tt[1], 'fm=',fm)
        
   
    Ly = np.vstack([Ly, Ty[0]]) # rajoute dernier point    
    return Ty[0], Tt[0], Ly  # y,t, Ly
   

#---------  utilisation 1 
"""
    entree: y0 : condition initiales
            t : temps initial
            Dt : pas de temps (assez petit)
Sortie:   Dessin 3D des trajectoires et points d'intersection en rouge

rem: prendre Dt assez petit pour joli dessin (pas obligatoire)
"""   
def Dessin_3D(y0,t,Dt):
    global tmax
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    cpt=0 # compteur
    while(t<tmax):
        y0,t, Ly = Application_de_Poincare(y0,t)
        
        # ... dessin de la trajectoire intermediaire 
        X, Y, Z = Ly[:,0], Ly[:,1], Ly[:,2]
        print('y=',y0, 't=',t)
        ax.plot3D(X,Y,Z, 'blue')
        angle = cpt        
        ax.view_init(30, angle)
        
        #... dessin du point final sur section de poincare
        plt.plot([y0[0]], [y0[1]], [y0[2]],  marker='o', linestyle='none', color='red')
        
        plt.savefig('image_'+str(cpt).zfill(4)+'.png',dpi=70) 
        plt.pause(0.1)    
        cpt +=1

    #plt.show()
 

#--definit l'application  de Poincaré sur R2
"""
entree x,y
sortie x2,y2
"""
def fS(x,y):
    global E
    
    px = -y
    R1 = sqrt( (x+nu)**2 + y**2)
    R2 = sqrt( (x+nu-1)**2 + y**2)    
    Ec = E + 0.5*(x**2+y**2) + (1-nu)/R1 + nu/R2   # (matrice)
    if(Ec>=0):
        py = x + sqrt(2*Ec)
    else:
       print('Erreur: Ec<0 dans Section de Poincaré, zone non accessible.')
       
    y0 = [x,px,y,py] # point de départ sur la section de Poincaré
    t=0 # arbitraire
    
    
    y0,t, Ly = Application_de_Poincare(y0,t)
    
    
    x2,y2 = y0[0], y0[2]
    return x2, y2



#--definit l'application  de Poincaré sur R2
"""
entree x,px
sortie x2,px2
"""
def fS2(x,px):
    global E
    
    y=0
    R1 = sqrt( (x+nu)**2 + y**2)
    R2 = sqrt( (x+nu-1)**2 + y**2)    
    U = - 0.5*(x**2+y**2) - (1-nu)/R1 - nu/R2  
    res = 2*(E-U)-px**2
    if(res>=0):
        py = x + sqrt(res)
    else:
       print('Erreur: res<0 dans Section de Poincaré, zone non accessible.')
       
    y0 = [x,px,y,py] # point de départ sur la section de Poincaré
    t=0 # arbitraire
    
    
    y0,t, Ly = Application_de_Poincare(y0,t)
    
    
    x2,px2 = y0[0], y0[1]
    return x2, px2
    
    
#---- calcule et dessin de la trajectoire
# entree: x,y,tmax (duree)
def dessin_trajectoire(x,y, tmax):
    Lx,Ly = [x],[y] #listes
    for t in range(tmax):
        if(opt_section==1):
            x,y = fS(x,y) # iteration
        elif(opt_section==2):
            x,y = fS2(x,y) # iteration
        Lx.append(x)
        Ly.append(y)
    plt.plot(Lx,Ly, linestyle='none', marker=',', color = Lcol[col]) # marker: ',' 'o', '.'
   # plt.show()
    plt.pause(0.001) # montre le dessin sans bloquer
    return x,y
            
    

#---- si evenement souris (clik)
def on_click(event):
    #print('click')
    global x,y, col, Lcol
    x, y = event.xdata, event.ydata # coord souris en x,y
    #x, y = event.x, event.y # coord souris en pixels
    col = (col+1) % len(Lcol)
    if event.button == 1:
            tmax = 200 # duree (tps discret)
            print('\nAttendez..')
            x,y = dessin_trajectoire(x,y, tmax)
            print('\nVous pouvez cliquer..')
#----- si evenement clavier             
def on_key(event):
    #print('key = ', event.key)
    global x,y
   # print('you pressed', event.key, event.xdata, event.ydata)
    if event.key == ' ': # barre espace
            tmax = 1000 # duree 
            print('\nAttendez..')
            x,y = dessin_trajectoire(x,y, tmax)
            print('\nVous pouvez cliquer..')

#--------------------------
def Dessin_Section_xy():
    global col,Lcol,E, opt_section
    opt_section = 1
    Lcol = ['blue','red', 'green', 'black', 'yellow']
    
    col = 0 # numero de couleur
    
    
    E=-1.8
    Dessin_zone_accessible_xy(E)
    plt.title('Application Poincaré. nu='+ ('%4.3f'%nu)+ ', E='+ ('%4.3f'%E))
    print('\n(cliquer pour condition initiale, et barre espace pour continuer')
        
    #-- dessin des etoiles
    plt.plot([-nu],[0], color = 'yellow', marker = 'o', linestyle = 'none') 
    plt.plot([1-nu],[0], color = 'yellow', marker = 'o', linestyle = 'none') 
    
    #-- dessin des pts fixes de Lagrange
    for i in range(len(TxL)):            
        plt.plot([TxL[i]],[TyL[i]], color = 'red', marker = 'o', linestyle = 'none') 

    plt.axis([-R,R, -R, R]) # selectionne la vue
    
    plt.connect('button_press_event', on_click) # associe la fonction aux evenements  souris
    plt.connect('key_press_event', on_key)  # associe la fonction aux evenements clavier
    
    
    plt.show()
    


#--------------------------
def Dessin_Section_xpx():
    global col,Lcol,E, opt_section
    opt_section = 2
    Lcol = ['blue','red', 'green', 'black', 'yellow']
    
    col = 0 # numero de couleur
    
    
    E=-2
    Dessin_zone_accessible_xpx(E)
    plt.title('Application Poincaré. nu='+ ('%4.3f'%nu)+ ', E='+ ('%4.3f'%E))
    print('\n(cliquer pour condition initiale, et barre espace pour continuer')
        
    plt.axis([-R,R, -R, R]) # selectionne la vue
    
    plt.connect('button_press_event', on_click) # associe la fonction aux evenements  souris
    plt.connect('key_press_event', on_key)  # associe la fonction aux evenements clavier
    
    
    plt.show()
#--------------------------
"""
Entree: x,px,y,py
        tmax : duree
        N : nbre d'images
        opt = 'tournant' si dessin dans ref tournant, ou 'galileen'

Sortie: dessin de la trajectoire sur le plan(x,y), referentiel galiléen
        sur intervalle de temps [0,t] , avec un pas de temps dt        
"""
def Animation_Flot_2D(x,px,y,py,tmax,N,opt):
   
   
    #plt.rc('text', usetex=True)
   # plt.rc('font', family='serif')
    t=0
    dt = tmax/N
    
    global R
    
    for k in range(N):
        
        plt.cla() # efface ecran
        plt.axis([-R,R, -R, R]) # selectionne la vue
        #plt.axis('equal') # pour avoir meme echelle en x,y
        plt.xlabel('x')
        plt.ylabel('y')
        

        
        
        if(opt == 'galileen'):
            text = 'Trajectoire du pb 3 corps dans ref. Galiléen'
        else:
            text = 'Trajectoire du pb 3 corps dans ref. tournant'
        text += '\n nu='+ ('%4.3f'%nu)+ ', t='+ ('%4.2f'%t)
        plt.title(text)  
        
        #-- dessin des etoiles
        x2,y2= -nu,0
        if(opt == 'galileen'):
            x2,y2 =  x2*cos(t) - y2*sin(t), x2*sin(t) + y2*cos(t) # formule de rotation
        plt.plot([x2],[y2], color = 'yellow', marker = 'o', linestyle = 'none') 
        
        
        x2,y2= 1-nu,0
        if(opt == 'galileen'):
            x2,y2 =  x2*cos(t) - y2*sin(t), x2*sin(t) + y2*cos(t) # formule de rotation
        plt.plot([x2],[y2], color = 'yellow', marker = 'o', linestyle = 'none') 
        
        #-- dessin des pts fixes de Lagrange
        for i in range(len(TxL)):            
            xL,yL= TxL[i], TyL[i]
            if(opt == 'galileen'):
                xL,yL =  xL*cos(t) - yL*sin(t), xL*sin(t) + yL*cos(t) # formule de rotation
            plt.plot([xL],[yL], color = 'red', marker = '.', linestyle = 'none') 


        #--dessin du corps 3
        x3,y3= x,y
        if(opt == 'galileen'):
            x3,y3 =  x*cos(t) - y*sin(t), x*sin(t) + y*cos(t) # formule de rotation
        plt.plot(x3,y3, color='blue', linestyle = '-', marker= 'o' )
        
        
        r = max(abs(x),abs(y))
        if(r>R/1.1):
            r=r*1.1
            plt.axis([-r,r, -r, r]) # selectionne la vue
        
    
        Ty = odeint(V, [x,px,y,py], [0,dt])
        x,px,y,py = Ty[1][0], Ty[1][1],Ty[1][2],Ty[1][3]
        
        t = t +dt
        
        plt.savefig('image_' + str(k).zfill(4) + '.png', dpi=50)
        plt.pause(0.01)
        
    subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=10 --loop --optimize=2 --colors=256 --multifile - > animation.gif')
    subprocess.getoutput('rm image_*.png')


def Dessin_zone_accessible_xy(E):
        global R
        xmin,xmax,ymin,ymax = -R,R, -R,R # bornes du domaine
        M = 50 # nombre de points en x et y
         
        x = np.linspace(xmin,xmax,M) # vecteur avec M nombres entre xmin et xmax
        y = np.linspace(ymin,ymax,M)[:,np.newaxis] # vecteur dans la 2eme dimension
        R1 = np.sqrt( (x+nu)**2 + y**2)
        R2 = np.sqrt( (x+nu-1)**2 + y**2)    
        Ec = E + 0.5*(x**2+y**2) + (1-nu)/R1 + nu/R2   # (matrice)
        
        levels = np.linspace(-100,100,3) # defini les lignes de niveaux
        plt.contourf(Ec, levels, extent=(xmin,xmax,ymin,ymax))
        plt.colorbar()
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        
        plt.title('Zone accessible en orange: Ec = E-U(x,y)>0 \n nu='+ ('%4.3f'%nu)+ ', E='+ ('%4.3f'%E))
        
        

        #-- dessin des etoiles
        plt.plot([-nu],[0], color = 'yellow', marker = 'o', linestyle = 'none') 
        plt.plot([1-nu],[0], color = 'yellow', marker = 'o', linestyle = 'none') 
        
        #-- dessin des pts fixes de Lagrange
        for i in range(len(TxL)):            
            plt.plot([TxL[i]],[TyL[i]], color = 'red', marker = '.', linestyle = 'none') 
        

def Animation_zone_accessible_xy():
    Emin, Emax, dE = -2.0, -1.4, 0.01
    k=0    
    for E in np.arange(Emin, Emax, dE):
        k += 1
        plt.clf()
        Dessin_zone_accessible_xy(E)
        plt.savefig('image_' + str(k).zfill(4) + '.png', dpi=50)
        plt.pause(0.03)

    subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=10 --loop --optimize=2 --colors=256 --multifile - > animation.gif')
    subprocess.getoutput('rm image_*.png')


def Dessin_zone_accessible_xpx(E):
        global R
        xmin,xmax,pxmin,pxmax = -R,R, -R,R # bornes du domaine
        M = 80 # nombre de points en x et px
         
        x = np.linspace(xmin,xmax,M) # vecteur avec M nombres entre xmin et xmax
        px = np.linspace(pxmin,pxmax,M)[:,np.newaxis] # vecteur dans la 2eme dimension
        y=0
        R1 = np.sqrt( (x+nu)**2 + y**2)
        R2 = np.sqrt( (x+nu-1)**2 + y**2)    
        U = -0.5*(x**2+y**2) - (1-nu)/R1 - nu/R2
        Z = 2*(E - U) -px**2    # (matrice)
        
        levels = np.linspace(-100,100,3) # defini les lignes de niveaux
        plt.contourf(Z, levels, extent=(xmin,xmax,pxmin,pxmax))
        plt.colorbar()
        plt.xlabel('$x$')
        plt.ylabel('$px$')
        
        plt.title('Zone accessible en orange: 2 (E-U(x,0)) -px**2>0 \n nu='+ ('%4.3f'%nu)+ ', E='+ ('%4.3f'%E))
        
        
   
def Animation_zone_accessible_xpx():
    Emin, Emax, dE = -1.60, -1.55, 0.001
    k=0    
    for E in np.arange(Emin, Emax, dE):
        k += 1
        plt.clf()
        Dessin_zone_accessible_xpx(E)
        plt.savefig('image_' + str(k).zfill(4) + '.png', dpi=50)
        plt.pause(0.03)

    subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=10 --loop --optimize=2 --colors=256 --multifile - > animation.gif')
    subprocess.getoutput('rm image_*.png')


    
#--- Dessin 3D -----------      
"""
t=0 # temps initial
y0 = [0, 1, 1.05] # Conditions initiales
Dt = 0.01  # temps minimal entre deux sections 
tmax = 50
Dessin_3D(y0,t,Dt) 
#subprocess.getoutput('convert -delay 10 -loop 0 image_*.png animation.gif') 
subprocess.getoutput('convert image_*.png GIF:- | gifsicle --delay=30 --loop --optimize=2 --colors=256 --multifile - > animation_Section_Poincare3D.gif')
subprocess.getoutput('rm image_*.png') 
"""



# Partie 1 ############################################
#---- Dessin du flot 2D (x,y)
"""
Calcul_pts_Lagrange()

i=0 # choix point Lagrange i=0->4
x,y= TxL[i], TyL[i]
px,py = -y,x 

x=x+1e-3
px=px+1e-3

x,px,y,py = 0.5, 0, 0, 1

dt = 0.02
tmax = 5
N = int(tmax/dt)
#opt='tournant' # choix du referentel
opt = 'galileen'
Animation_Flot_2D(x,px,y,py,tmax,N, opt)
"""
# Partie 2 #############################################
#-- Dessin de la zone accessible
"""
Calcul_pts_Lagrange()
Animation_zone_accessible_xy()
"""

# Partie 3 ######################################
# ---- Section de Poincaré 2D
"""
Calcul_pts_Lagrange()
Dt=1 # temps minimal entre deux sections
Dessin_Section_xy()
"""


# Partie 4 #############################################
#-- Dessin de la zone accessible en x,px
"""
Animation_zone_accessible_xpx()
"""

# Partie 5 ######################################
# ---- Section de Poincaré 2D en (x,px)
Dt=1 # temps minimal entre deux sections
Dessin_Section_xpx()


