import matplotlib.pyplot as plt
from math import sqrt, sin, cos, pi,tan, atan, e
from matplotlib.animation import FuncAnimation as anim
from matplotlib.animation import PillowWriter as pw
import os.path
import numpy as np

#############################################################################
# Description:                                                              #
# Given a set of two time dependent  polar differential equations, displays #
# an animation of the nullclines of that system of differential equations   #
# over time, as well as user-defined points which will move in accordance   #
# with the differential equations. Users may edit the settings below as     #
# well as the dxt and dyt functions to set their own system of ODEs. Upon   #
# running, the program  will initially ask the user whether to display or   #
# save the figure.                                                          #
#############################################################################

#Settings, to be changed by user.
yncol='blue' # Color of the y nullclines
xncol='red' # Color of the x nullclines
pointcol="k." # Color of the points to be plotted
meshsize=0.02 # Interval between points that are plotted
gridsize=(5,5) # Determines the maximal values of x and y, respectively
timerange=(0,10) # Time values will be within this interval
timesteps=500 # Number of timesteps
periods=5 # 
spd=0.001 # Speed of the animation -- best set to a small value (much less than 1)
dispnulls=True # Display method for nullclines. True for cartesian nullclines, "polar" for polar nullclines, False for no nullclines
limitmag=True  # Whether to limit the magnitudes of points -- points will be forced back into viewing range if they go outside of it, with this setting on.

# Settings for points, which may be altered by the user
points=[] # List of points to plot, as (x,y) coordinates
spawnpoints=[] # List of points to plot, as (x,y) coordinates. These points will periodically respawn new dots, unlike the previous list!
spawninter=25 # Time interval between spawning new dots in the previous list.

# Advanced users may use this section to automate populating the points and spawnpoints lists. Delete this section to enter your own points manually.
#------------------------------
for k in range(1,16):
    points.append((0,k/4))
    points.append((0,-k/4))
#------------------------------
    
# Set up values based on the settings above for the points to be plotted
# Users should not edit this section.
#--------------------------
xrange=np.arange(-gridsize[0],gridsize[0],meshsize)
yrange=np.arange(-gridsize[1],gridsize[1],meshsize)
x,y=np.meshgrid(xrange,yrange)

#--------------------------

# Define equations here:
# dxt represents the x-variable's differential equation
# dyt represents the y-variable's differential equation
# Both take in a time value (float) and output a float (value of the appropriate derivative at that point)
# Both are intended to use the x and y values above, where an (x,y) pair is the position of a point on the plane.
# Users may enter their own function here (just edit the "return" line)
# NOTE: Unlike other versions of this program, this version is meant to be used with polar variables, in the following way:
#   "r" may be used for magnitude (squared)
#   "c" may be used for cosine(theta) and "s" may be used for sine(theta)
# Users should only edit the return line.
def dxt(t):
    r=x**2+y**2 # Calculates the magnitude of the point, squared
    c=x/r # Use this for cosine values
    s=y/r # Use this for sine values
    return -y*r

def dyt(t):
    r=x**2+y**2 # Calculates the magnitude of the point, squared
    c=x/r # Use this for cosine values
    s=y/r # Use this for sine values
    return x*r

# Redefined versions of dxt and dyt that take in x and y explicitly
# This needs to be identical to dxt and dyt to work properly
# Note: these methods are used to plot points; the above are used to plot nullclines.
# Users should only edit the return line.
def dx(t,x,y):
    if x==y:
        if y==0:
            return 0
    r=x**2+y**2 #sub for r
    c=x/r #sub for cosine
    s=y/r #sub for sine
    return -y*r

def dy(t,x,y):
    if x==y:
        if y==0:
            return 0
    r=x**2+y**2 #sub for r
    c=x/r #sub for cosine
    s=y/r #sub for sine
    return x*r

#---------------------------------------------
# Used to plot polar nullclines
def drt(t):
    return dxt(t)**2+dyt(t)**2

def dtht(t):
    return np.arctan(dyt(t)/dxt(t))


#Finish setting up the plots.
fig,ax=plt.subplots()

plt.xlim(-gridsize[0],gridsize[0])
plt.ylim(-gridsize[1],gridsize[1])
tmin,tmax=timerange

# This function handles the animation: given a time value, computes the frame at that time.
def animate(t):
    global points
    if t%spawninter==0:
        points+=spawnpoints
    plots=[]
    t=tmin+t*(tmax-tmin)/timesteps
    #t=10*sin(2*pi*(t*periods/(timerange[1]-timerange[0])))
    ax.clear()
    
    #plot nullclines
    if dispnulls:
        plots.append(plt.contour(x,y,dxt(t),[0],colors=[xncol]))
        plots.append(plt.contour(x,y,dyt(t),[0],colors=[yncol]))
    if dispnulls=='polar': #currently not working
        plots.append(plt.contour(x,y,drt(t),[0],colors=[xncol]))
        plots.append(plt.contour(x,y,dtht(t),[0],colors=[yncol]))

    #plot points
    newpoints=[]
    for point in points:
        a,b=point
        plots.append(plt.plot(a,b,pointcol))
        Dx=dx(t,a,b)*spd
        Dy=dy(t,a,b)*spd
        a=a+Dx
        b=b+Dy
        if limitmag:
            mag=sqrt(a**2+b**2)
            if mag>4.99:
                a=4.99*a/mag
                b=4.99*b/mag
        newpoints.append((a,b))
    points=newpoints
    
    plt.xlim(-gridsize[0],gridsize[0])
    plt.ylim(-gridsize[1],gridsize[1])
    return plots

# Calls the animate function and prompts the user to save or display the animation.
animation=anim(fig,animate,interval=40,frames=timesteps,repeat=True)
if input("show? ")=="y":
    plt.show()
else:
    n=0
    while os.path.isfile("fig"+str(n)+".gif"):
        n+=1
    animation.save('fig'+str(n)+".gif",dpi=300,writer=pw(fps=25))
