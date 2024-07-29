import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim
import matplotlib.animation as animation
import os.path
import numpy as np
from math import log,sqrt,pi,cos,sin
from random import randint, random, shuffle

############################################################################
# Description:                                                             #
# Generates and simulates a set number of particles, and the gravitational #
# forces between them using real-world physics. Unlike version one, the    #
# grid does not wrap. The simulation also handles collisions, where two    #
# particles may collide to form a larger particle or explode in a shower of#
# smaller particles. Options for users are below. Further options to       #
# customize particle spawning are available as well -- search for "Body    #
# Spawning" section below.                                                 #
# NOTE: this program may require some prior user setup -- see plt.rcParams #
# line below settings.                                                     #
############################################################################



scale=60 # Size of the grid the simulation runs in.
gravConst=0.0001 # Strength of gravity
collisionDist=0.1 # collisions register when objects are within this distance of each other
maxExpParticles=12 # Maximum number of particles created in a single collision
minExpParticles=6 # Minimum number of particles created in a single collision
saveSeconds=20 # How long the animation should be when saved, in seconds
fps=30 # Frames per second of the animation
minExpMass=20 # Particles with mass less than this will never explode
maxParticles=200 # Maximum number of particles allowed in the simulation
distScale=True

# needed for proper animation -- user might need to setup and/or find the appropriate folder on their machine.
plt.rcParams["animation.ffmpeg_path"]='C:\\ffmpeg\\bin\\ffmpeg.exe'

fig,ax=plt.subplots()

"""
Class to store a single point.

Methods:
collsionCheck():
    static method
    checks all combinations of points for collisions, and carries them out with the collide method
step():
    static method
    handles the movement and collisions of all bodies in a single step of the simulation.
__init__(float mass, float xpos, float ypos, float xvel, float yvel, str color, bool immovable):
    initializes a particle with given mass, position (posx, posy), and velocity (velx, vely)
    color indicates the color of the particle in the simulation
    particles with immovable set to true will not ever change their velocity away from their starting velocity.
radius():
    returns the particle's radius, as determined by its mass
dist(Body other):
    returns the distance from one body to another
collideCheck(Body other):
    checks for collision between one body and another, and carries out the collision if a collision takes place.
    low velocity collisions result in bodies combining, while high velocity collisions result in explosions    
combine(Body other):
    combines two bodies together, intended to be used by collideCheck
explode(float F):
    explodes one body into many, where F indicates the force of the collision (and hence the speed of the resulting particles)
draw():
    draws the body to the plot
move():
    moves the particle in accordance with its current velocity
gravForce(Body other):
    accelerates a body in accordance with gravitational attraction from another body
accel(float x, float y):
    accelerates a body with vector (x, y)
"""
class Body:
    allBodies=[]
    exempt=[] #exempt from collisions

    @staticmethod
    def collisions():
        for body in [body for body in Body.allBodies if body not in Body.exempt]:
            for target in[body for body in Body.allBodies if body not in Body.exempt]:
                if body!=target:
                    body.collideCheck(target)

    @staticmethod
    def step():
        Body.collisions()
        for body in Body.allBodies:
            if body in Body.exempt:
                Body.exempt.remove(body)
            for target in body.allBodies:
                if body!=target:
                    body.gravForce(target)
            body.move()
            body.draw()
    
    def __init__(self,mass,xpos,ypos,xvel=0,yvel=0,color="r",immovable=False):
        self.m=mass
        self.x=xpos
        self.y=ypos
        self.xv=xvel
        self.yv=yvel
        self.color=color
        self.immovable=immovable
        Body.allBodies.append(self)
        Body.exempt.append(self)

    def radius(self):
        return sqrt(log(1+self.m))

    def dist(self,other):
        return sqrt((other.x-self.x)**2+(other.y-self.y)**2)
    
    def collideCheck(self,other):
        if self.immovable and other.immovable:
            return False
        d=collisionDist*(self.radius()+other.radius())
        if self.dist(other)<=d:
            F=self.m*sqrt((self.xv-other.xv)**2+(self.yv-other.yv)**2)
            m=max(self.m,other.m)
            new=self.combine(other)
            if F>new.m and new.m>minExpMass and (not (self.immovable or other.immovable)) and len(Body.allBodies)<=maxParticles:
                new.explode(F)
            return True
        return False

    def combine(self,other):
        x=self.x
        y=self.y
        if self.immovable:
            color=self.color
        elif other.immovable:
            color=other.color
        else:
            colors=[b.color for b in [self,other] if b.color!="b"]
            if colors==[]:
                color="b"
            else:
                shuffle(colors)
                color=colors[0]
        if other.m>self.m:
            x=other.x
            y=other.y
        if self in Body.allBodies:
            Body.allBodies.remove(self)
        if other in Body.allBodies:
            Body.allBodies.remove(other)
        if self in Body.exempt:
            Body.exempt.remove(self)
        if other in Body.exempt:
            Body.exempt.remove(other)
        m=self.m+other.m
        if self.immovable:
            xv=self.xv
            yv=self.yv
        elif other.immovable:
            xv=other.xv
            yv=other.yv
        else:
            xv=self.xv*self.m/m+other.xv*other.m/m
            yv=self.yv*self.m/m+other.yv*other.m/m
        return Body(m,x,y,xv,yv,color,(self.immovable or other.immovable))

    def explode(self,F):
        particles=randint(minExpParticles,maxExpParticles)
        minSize=self.m/(4*particles)
        maxSize=self.m/(2*particles)
        for p in range(particles):
            m=minSize+random()*(maxSize-minSize)
            x=self.x
            y=self.y
            while sqrt((x-self.x)**2+(y-self.y)**2)<=collisionDist*(self.radius()+log(1+m)**2)*2:
                x=self.x+random()*collisionDist*(self.radius()+log(1+m)**2)*4
                y=self.y+random()*collisionDist*(self.radius()+log(1+m)**2)*4
            dx=self.x-x
            dy=self.y-y
            Body(m,x,y,self.xv-gravConst*dx*F*(0.5-random()),self.yv-gravConst*dy*F*(0.5-random()),self.color)
            self.m-=m
        
    def draw(self):
        if abs(self.x)<scale or abs(self.y)<scale:
            size=log(self.m+1)
            if distScale:
                sc=((self.x/scale)**2+(self.y/scale)**2)*3
                size=size*(1+sc)
            return plt.plot(self.x,self.y,self.color+".",markersize=size)

    def move(self):
        self.x+=self.xv
        self.y+=self.yv

    def gravForce(self,other):
        if self.immovable:
            return
        xd=other.x-self.x
        yd=other.y-self.y
        d=self.dist(other)
        if d==0:
            d=0.0001
        F=gravConst*other.m/(d**2)
        self.accel(xd*F,yd*F)

    def accel(self,x,y):
        self.xv+=x
        self.yv+=y

colors=["b","g","r","c","m","y"] #colors allowed for bodies

######################################################################
# Body Spawning:                                                     #
# This section can be used by users to define initial body creation. #
# Several predefined options are set out below -- feel free to       #
# uncomment one or more section, or define your own.                 #
######################################################################

'''
rnum=10
t=6
for r in range(rnum):
    r=(1+r)*scale/(2*rnum)
    for th in range(t):
        shuffle(colors)
        th=th*2*pi/t
        x=r*cos(th)
        y=r*sin(th)
        th=th+pi/2
        vx=0.5*cos(th)
        vy=0.5*sin(th)
        Body(30,x,y,vx,vy,colors[0])
    t+=2
'''
'''
for k in range(30):
    th=random()*2*pi
    r=random()*scale/2
    x=r*cos(th)
    y=r*sin(th)
    th=th+pi/2
    v=(1+random())/r
    vx=v*cos(th)
    vy=v*sin(th)
    m=10+random()*50
    shuffle(colors)
    Body(m,x,y,vx,vy,colors[0])
'''   
    
'''
for k in range(80):
    shuffle(colors)
    k+=1
    m=10+random()*90
    r=random()*scale/3
    th=random()*2*pi
    x=r*cos(th)
    y=r*sin(th)
    #x=(random()*2*scale-scale)/3
    #y=(random()*2*scale-scale)/3
    vx=random()*2-1
    vy=random()*2-1
    Body(m,x,y,vx,vy,colors[0])
'''

Body(10000,0,0,0,0,"k",True)
for k in range(120):
    shuffle(colors)
    r=random()*10+40
    seed=random()
    if seed<0.02:
        b=5000
        ran=500
    elif seed<0.2:
        b=100
        ran=50
    elif seed<0.5:
        b=50
        ran=20
    else:
        b=20
        ran=10
    m=b+random()*ran+random()*ran+random()*ran
    th=random()*2*pi
    thv=th+pi/2+random()*pi/4-pi/8
    v=random()*0.5+0.8
    Body(m,r*cos(th),r*sin(th),v*cos(thv),v*sin(thv),colors[0])
    
#########################################################################

# simulates one step of animation
def sketch(i):
    ax.clear()
    ax.set_xlim([-scale,scale])
    ax.set_ylim([-scale,scale])
    Body.step()
    return []

#handles the animation and simulation.
wr=animation.writers["ffmpeg"](fps=fps)
anim=anim(fig,sketch,interval=40,frames=saveSeconds*fps,repeat=True)
i=input("show? ")
if i.lower()=='y':
    plt.show()
else:
    n=0
    while os.path.isfile("fig"+str(n)+".mp4"):
        n+=1
    anim.save('fig'+str(n)+".mp4",dpi=300,writer=wr)
