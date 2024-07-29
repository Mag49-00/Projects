import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim
import matplotlib.animation as animation
import os.path
from math import sqrt,log
from random import random


############################################################################
# Description:                                                             #
# Generates and simulates a set number of particles, and the gravitational #
# forces between them using real-world physics. The simulation uses north/ #
# south and east/west grid wrapping, so particles that leave the simulation#
# area to the north appear at the south (and vice versa), and similar for  #
# east/west. The simulation also handles collisions, where two particles   #
# may collide to form a larger particle. Options for users are below.      #
# NOTE: this program may require some prior user setup -- see plt.rcParams #
# line below settings.                                                     #
############################################################################

gridSize=10 # Size of the grid the simulation runs in.
gravStr=0.00001 # Strength of gravity
collideDist=0.05 # collisions register when objects are within this distance of each other
nPoints=20 # Number of points to spawn
speedLimit=None #limits the initial speed of points -- if set to None, initial points will begin with no velocity

# needed for proper animation -- user might need to setup and/or find the appropriate folder on their machine.
plt.rcParams["animation.ffmpeg_path"]='C:\\ffmpeg\\bin\\ffmpeg.exe'

"""
Class to store a single point.

Methods:
collsionCheck():
    static method
    checks all combinations of points for collisions, and carries them out with the collide method
__init__(float mass, float posx, float posy, float velx, float vely):
    initializes a particle with given mass, position (posx, posy), and velocity (velx, vely)
accel(x,y):
    increases the particles velocity by the vector (x, y)
step():
    simulates one step of motion for the particle
    calls method correct after finished
correct():
    handles grid wrapping -- particles that move out the right side of the grid appear on the left, and similar for the top/bottom
xDist1(Point other):
    returns the raw Euclidean x-distance from a particle to a given other particle
    does not take into account grid wrapping
xDist2(Point other):
    returns the x-distance from a particle to a given other particle, wrapping around the left/right
yDist1(Point other):
    returns the raw Euclidean y-distance from a particle to a given other particle
    does not take into account grid wrapping
yDist2(Point other):
    returns the y-distance from a particle to a given other particle, wrapping around the top/bottom
dist(Point other):
    returns the true distance of a particle to a given other particle; takes into account grid wrapping
collide(Point other):
    initiates a collision between one particle and another, joining them together into a larger particle of equivalent mass to both initial particles.
approach(Point other):
    simulates gravitational force, accelerating the particle towards the other using real-world gravitational formula
    
"""
class Point:
    allPoints=[]
    
    @staticmethod
    def collisionCheck():
        collisions=[]
        for point1 in Point.allPoints:
            for point2 in Point.allPoints:
                if point1!=point2 and point1.dist(point2)<collideDist:
                    if (point1,point2) not in collisions and (point2,point1) not in collisions:
                        collisions.append((point1,point2))
        for p1,p2 in collisions:
            p1.collide(p2)
            
    def __init__(self,mass,posx,posy,velx=0,vely=0):
        self.m=mass
        self.x=posx
        self.y=posy
        self.velx=velx
        self.vely=vely
        self.correct()
        Point.allPoints.append(self)

    def accel(self,x,y):
        self.velx+=x
        self.vely+=y

    def step(self):
        speed=sqrt(self.velx**2+self.vely**2)
        if speed==0:
            self.correct()
            return
        if speedLimit:
            self.x+=self.velx*speedLimit/(speed+speedLimit) 
            self.y+=self.vely*speedLimit/(speed+speedLimit)
        else:
            self.x+=self.velx
            self.y+=self.vely      
        self.correct()

    def correct(self):
        self.x=((self.x+gridSize)%(gridSize*2))-gridSize
        self.y=((self.y+gridSize)%(gridSize*2))-gridSize

    def xDist1(self,other):
        return other.x-self.x

    def xDist2(self,other):
        d=self.xDist1(other)
        ret=2*gridSize-abs(d)
        if d>=0:
            return -ret
        return ret

    def yDist1(self,other):
        return other.y-self.y

    def yDist2(self,other):
        d=self.yDist1(other)
        ret=2*gridSize-abs(d)
        if d>=0:
            return -ret
        return ret

    def dist(self,other):
        dx1=self.xDist1(other)
        dx2=self.xDist2(other)
        dy1=self.yDist1(other)
        dy2=self.yDist2(other)
        ret=[]
        for x in [dx1,dx2]:
            for y in [dy1,dy2]:
                ret.append(x**2+y**2)
        return sqrt(min(ret))

    def collide(self,other):
        x=self.x
        y=self.y
        if self.m<other.m:
            x=other.x
            y=other.y
        newPoint=Point(self.m+other.m,x,y,0,0)
        if self in Point.allPoints:
            Point.allPoints.remove(self)
        if other in Point.allPoints:
            Point.allPoints.remove(other)

    def approach(self,other):
        a1=self.xDist1(other)
        a2=self.xDist2(other)
        b1=self.yDist1(other)
        b2=self.yDist2(other)
        for x in [a1,a2]:
            for y in [b1,b2]:
                d=x**2+y**2
                if d==0:
                    d=0.00000000000001
                a=gravStr*other.m/d
                self.accel(x*a/d,y*a/d)

fig,ax=plt.subplots()

#creates points
def populate():
    for k in range(nPoints):
        x=random()*gridSize*2-gridSize
        y=random()*gridSize*2-gridSize
        if speedLimit:
            vx=random()*speedLimit-speedLimit/2
            vy=random()*speedLimit-speedLimit/2
        else:
            vx=0
            vy=0
        m=1+random()*100
        Point(m,x,y,vx,vy)
    
#simulates one step of the animation
def step(i):
    Point.collisionCheck()
    if len(Point.allPoints)<nPoints/2:
        populate()
    ax.clear()
    ax.set_xlim([-gridSize,gridSize])
    ax.set_ylim([-gridSize,gridSize])
    plots=[]
    for point1 in Point.allPoints:
        for point2 in Point.allPoints:
            if point1!=point2:
                point1.approach(point2)
        point1.step()
        plots.append(plt.plot(point1.x,point1.y,"r.",markersize=log(2*point1.m)))
    return plots

#carries out animation, and either saves or shows the graphic
populate()

wr=animation.writers["ffmpeg"]()
a=anim(fig,step,interval=40,frames=300,repeat=True)

if input("show? ")=="y":
    plt.show()
else:
    n=0
    while os.path.isfile("fig"+str(n)+".mp4"):
        n+=1
    fname="fig"+str(n)+".mp4"
    a.save(fname,writer=wr,dpi=300)
