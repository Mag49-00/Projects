import matplotlib.pyplot as plt
from math import sqrt, sin, cos, pi,tan
from matplotlib.animation import FuncAnimation as anim
from matplotlib.animation import PillowWriter as pw
import os.path
import numpy as np

############################################################################
# Description:                                                             #
# Given a set of two time dependent differential equations, displays an    #
# animation of the nullclines of that system of differential equations     #
# over time. Users may edit the settings below as well as the dxt and      #
# dyt functions to set their own system of ODEs. Upon running, the program #
# will initially ask the user whether to display or save the figure.       #
############################################################################

#Settings
yncol='blue' # Color for the x nullcline
xncol='red' # Color for the y nullcline
meshsize=0.02 # Interval between points that are plotted
gridsize=(4,4) # Determines the maximal values of x and y, respectively
timerange=(0,10) # Time values will be within this interval
timesteps=50 #Number of timesteps

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
def dxt(t):
    return x**2+y**2-10*np.cos(t*y)

def dyt(t):
    return x**2+t*y**2/5-np.cos(t*y/5)

#Finish setting up the plots.
fig,ax=plt.subplots()

plt.xlim(-gridsize[0],gridsize[0])
plt.ylim(-gridsize[1],gridsize[1])
tmin,tmax=timerange

# This function handles the animation: given a time value, computes the frame at that time.
def animate(t):
    t=tmin+t*(tmax-tmin)/timesteps
    t=5*sin(2*pi*t/10)
    ax.clear()
    plt.contour(x,y,dxt(t),[0],colors=[xncol])
    plt.contour(x,y,dyt(t),[0],colors=[yncol])
    plt.xlim(-gridsize[0],gridsize[0])
    plt.ylim(-gridsize[1],gridsize[1])

# Calls the animate function and prompts the user to save or display the animation.
animation=anim(fig,animate,interval=40,frames=timesteps,repeat=True)
n=0
while os.path.isfile("fig"+str(n)+".gif"):
    n+=1
while True:
    t=input("save? ")
    if t=='y':
        animation.save('fig'+str(n)+".gif",dpi=300,writer=pw(fps=25))
        break
    elif t=='n':
        plt.show()
        break
