import matplotlib.pyplot as plt
from math import sqrt, sin, cos, pi,tan
from matplotlib.animation import FuncAnimation as anim
from matplotlib.animation import PillowWriter as pw
import os.path

######################################################################################
# Description:                                                                       #
# Displays an animation depicting the evolution of the slope field of a set of time- #
# dependent differential equations. The differential equations are determined by the #
# "dxt" and "dyt" functions (free for the user to edit), and settings below can be   #
# used to change the appearance of the animation.                                    #
######################################################################################

# The function to use for the differential equation governing the x-axis variable
# Takes in the x and y coordinates of a point as well as the current time t, all as floats
# Outputs a single float corresponding to the derivative of the x variable at that point in space/time.
# Enter in any x,y,t dependent equation to set that as the x partial derivative equation.
def dxt(x,y,t):
    # Edit the line below only with an appropriate equation for the x partial derivative.
    return t*x**2+y**2-10*cos(t*y)

# The function to use for the differential equation governing the y-axis variable
# Has the same inputs/outputs as dxt, but now will be used for the y partial derivative.
def dyt(x,y,t):
    # Edit the line below only with an appropriate equation for the x partial derivative.
    return x+tan(t*y)

# Editable settings:
col='b' # Color to use for the lines in the graph. See below for a reference of possible colors.
meshsize=1 # Interval between (the center of) any two lines.
gridsize=(4,4) # (x,y) size of the plot
timerange=(0,10) # Time values will be sampled from this interval
timesteps=10 # Number of time intervals to use.
# Do not edit anything beyond this point.

'''
reference for colors in matplotlib:
b=blue
g=green
r=red
c=cyan
m=magenta
y=yellow
k=black
w=white

plot types:
-=solid line
--=dashed line
:=dotted line
.=point marker
,=pixel marker
o=circle marker
v=triangle down marker
^=triangle up marker
<=triangle left marker
>=triangle right marker
1=tri down marker
2=tri up marker
3=tri left marker
4=tri right marker
s=square marker
p=pentagon marker
*=star marker
h=hexagon1 marker
H=hexagon2 marker
+=plus marker
x=x marker
D=diamond marker
d=thin diamond marker
|=vline marker
_=hline marker

syntax:
color first, then plot type, no spaces, as a str
'''

# Set up the appropriate settings in matplotlib based on the settings above.
fig,ax=plt.subplots()

xrange=meshsize*gridsize[0]
yrange=meshsize*gridsize[1]
nxs=int(gridsize[0]*2/meshsize)
nys=int(gridsize[1]*2/meshsize)
tmin,tmax=timerange

plt.xlim(-gridsize[0],gridsize[0])
plt.ylim(-gridsize[1],gridsize[1])

# Given a time value, returns all artists required for the given frame of animation.
def animate(t):
    ax.clear()
    t=tmin+t*(tmax-tmin)/timesteps
    t=5*sin(t)
    plots=[]
    for x in range(nxs):
        x=meshsize*x-gridsize[0]
        for y in range(nys):
            y=meshsize*y-gridsize[0]
            dx=dxt(x,y,t)
            dy=dyt(x,y,t)
            if dx==0:
                if dy==0:
                    plots.append(ax.plot(x,y,col+"."))
                else:
                    yvals=[y-meshsize/6,y+meshsize/6]
                    xvals=[x,x]
                    plots.append(ax.plot(xvals,yvals,col+"-"))
            else:
                m=dy/dx
                epsilon=meshsize/(6*sqrt(1+m**2))
                delta=m*epsilon
                xvals=[x-epsilon,x+epsilon]
                yvals=[y-delta,y+delta]
                plots.append(ax.plot(xvals,yvals,col+"-"))
    return plots

# Display and save the animation
animation=anim(fig,animate,interval=40,frames=timesteps,repeat=True)
plt.show()
n=0
while os.path.isfile("fig"+str(n)+".gif"):
    n+=1
animation.save('fig'+str(n)+".gif",dpi=300,writer=pw(fps=25))
