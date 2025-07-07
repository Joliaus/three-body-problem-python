import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.axes_grid1
import matplotlib.widgets

class Player(FuncAnimation):
    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, mini=0, maxi=100, pos=(0.125, 0.92), **kwargs):
        self.i = 0
        self.min=mini
        self.max=maxi
        self.runs = True
        self.forwards = True
        self.fig = fig
        self.func = func
        self.setup(pos)
        FuncAnimation.__init__(self,self.fig, self.func, frames=self.play(), 
                                           init_func=init_func, fargs=fargs,
                                           save_count=save_count, **kwargs )    

    def play(self):
        while self.runs:
            self.i = self.i+self.forwards-(not self.forwards)
            if self.i > self.min and self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i

    def start(self):
        self.runs=True
        self.event_source.start()

    def stop(self, event=None):
        self.runs = False
        self.event_source.stop()

    def forward(self, event=None):
        self.forwards = True
        self.start()
    def backward(self, event=None):
        self.forwards = False
        self.start()
    def oneforward(self, event=None):
        self.forwards = True
        self.onestep()
    def onebackward(self, event=None):
        self.forwards = False
        self.onestep()

    def onestep(self):
        if self.i > self.min and self.i < self.max:
            self.i = self.i+self.forwards-(not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i+=1
        elif self.i == self.max and not self.forwards:
            self.i-=1
        self.func(self.i)
        self.fig.canvas.draw_idle()

    def setup(self, pos):
        playerax = self.fig.add_axes([pos[0],pos[1], 0.22, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)
        bax = divider.append_axes("right", size="80%", pad=0.05)
        sax = divider.append_axes("right", size="80%", pad=0.05)
        fax = divider.append_axes("right", size="80%", pad=0.05)
        ofax = divider.append_axes("right", size="100%", pad=0.05)
        self.button_oneback = matplotlib.widgets.Button(playerax, label=u'$u29CF$')
        self.button_back = matplotlib.widgets.Button(bax, label=u'$u25C0$')
        self.button_stop = matplotlib.widgets.Button(sax, label=u'$u25A0$')
        self.button_forward = matplotlib.widgets.Button(fax, label=u'$u25B6$')
        self.button_oneforward = matplotlib.widgets.Button(ofax, label=u'$u29D0$')
        self.button_oneback.on_clicked(self.onebackward)
        self.button_back.on_clicked(self.backward)
        self.button_stop.on_clicked(self.stop)
        self.button_forward.on_clicked(self.forward)
        self.button_oneforward.on_clicked(self.oneforward)

### using this class is as easy as using FuncAnimation:            

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
        h2 = h/2
        v1 = f(t, y)
        v2 = f(t + h2, y + h2*v1)
        v3 = f(t + h2, y + h2*v2)
        v4 = f(t + h, y + h*v3)
        y = y + (h2/3)*(v1 + 2*v2 + 2*v3 + v4)
        t += h
        liste.append(y)
    return liste

y0 = np.array([0.994, 0, 0, -2.0015851063790825224053786224])

liste = Bogacki_Shampine(three_body_problem, 0, y0, 0.001, 17.0652165601579625588917206249)
x = [x[0] for x in liste]
y = [x[1] for x in liste]

fig, ax = plt.subplots()

ax.plot(x,y)
point, = ax.plot([],[], marker="o", color="crimson", ms=15)

def update(i):
    point.set_data(x[i],y[i])

ani = Player(fig, update, maxi=len(y)-1)

plt.show()