from cyclic import Cyclic
from math import sin, cos, pi
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation as anim
from matplotlib.animation import PillowWriter as pw

################################################################################
# Description:                                                                 #
# Draws out the calculations necessary to find the value of a given number in  #
# a specified cyclic group. Settings are below for users to change.            #
################################################################################


number=467258 # Number to calculate
cyclicBase=7 # Cyclic group to calculate in
base=10 # At the moment, this should be left as 10 -- future use will allow numbers of other base systems
frames_per_digit=40 # Frames to use in the animation for each digit
showLabels=True # Whether to show labels on points around the circle in the animation.
save=False # Whether to save the figure, or show it instead.

# Initial setup
if save==True:
    frames_per_digit=frames_per_digit*2
digits=[int(x) for x in str(number)]
frames=len(digits)*frames_per_digit*2-frames_per_digit
fig, ax = plt.subplots(figsize=(5, 5))

ax.set_xlim([-1.25,1.25])
ax.set_ylim([-1.25,1.25])
ax.axis('off')
style = "Simple, tail_width=0.5, head_width=4, head_length=8"
kw = dict(arrowstyle=style, color="b")

# Converts a cyclic number to a point on the circle
def toPoint(cyclic):
    base=cyclic.base
    n=cyclic.n
    step=2*pi/base
    theta=n*step
    return (sin(theta),cos(theta))

# Draws the main circle
def drawcircle(points=200):
    xs=[]
    ys=[]
    theta=0
    for n in range(points+1):
        xs.append(sin(theta))
        ys.append(cos(theta))
        theta+=2*pi/points
    plt.plot(xs,ys,"k-")

# Draws the main diagram of the cyclic group
def cyclicTable(base,mul=10):
    points=[]
    arrows=[]
    for k in range(base):
        n=Cyclic(base,k)
        m=n*mul
        source=toPoint(n)
        dest=toPoint(m)
        points.append(source)
        arrows.append(patches.FancyArrowPatch(source, dest, **kw))#, connectionstyle="arc3,rad=.5", **kw))
    pltarrows=[]
    for arrow in arrows:
        pltarrows.append(plt.gca().add_patch(arrow))
    pltpoints=plt.plot([point[0] for point in points], [point[1] for point in points], "ko")
    if showLabels:
        labels=[]
        for i in range(len(points)):
            labels.append(ax.annotate(i,(points[i][0]*1.1,points[i][1]*1.1),horizontalalignment='center',verticalalignment="center"))

# Calculates animation following the arrows (multiplying by 10)
def followArrow(source,i):
    i=i%frames_per_digit
    x,y=toPoint(source*base)
    a,b=toPoint(source)
    return plt.plot(
        (1-i/frames_per_digit)*a + i*x/frames_per_digit,
        (1-i/frames_per_digit)*b + i*y/frames_per_digit,
        "ro"
        )[0]

# Calculates animation along the outer arc of the circle
def followArc(source,add,i):
    i=i%frames_per_digit
    sourceTheta=source.n*2*pi/cyclicBase
    theta=sourceTheta+(2*pi/cyclicBase)*add.n*i/frames_per_digit
    return plt.plot(
            sin(theta),
            cos(theta),
            "ro"
            )[0]

#Sets up the initial circle and table
drawcircle()
cyclicTable(cyclicBase,base)
if base==10:
    plt.title(str(number)+" to C"+str(cyclicBase))
else:
    plt.title(str(number)+" (base "+str(base)+") to C"+str(cyclicBase))

point=None
source=None
f=followArc
add=0
labelN=0
label=None

# Functions to update the animation behavior when a new digit appears, or when calculating the next step in a digit calculation
def update1():
    global source, f, add, labelN, label
    if label!=None:
        label.remove()
    if digits==[]:
        f=None
        label=plt.text(-1,-1.2,str(number))
        if point!=None:
            point.remove()
        return
    d=digits.pop(0)
    label=plt.text(-1,-1.2,str(labelN)+" x"+str(base))
    labelN=labelN*10+d
    if source==None:
        source=Cyclic(cyclicBase,d)
    else:
        source=source+add
        add=Cyclic(cyclicBase,d)
    f=followArrow

def update2():
    global f, source, labelN, label
    if label!=None:
        label.remove()
    label=plt.text(-1,-1.2,str(labelN-labelN%10)+" +"+str(labelN%10))
    source=source*base
    f=followArc

def func(i):
    global point
    if point!=None:
        point.remove()
        point=None
    if i>=frames or f==None:
        x,y=toPoint(Cyclic(cyclicBase,number))
        return plt.plot(x,y,'ro')[0]
    if i%frames_per_digit==0:
        if i%(frames_per_digit*2)==0:
            update1()
        else:
            update2()
    if f==followArc:
        point=followArc(source,add,i)
    else:
        point=followArrow(source,i)
    return point

# Runs the simulation
a=anim(fig,func,interval=20,frames=frames,repeat=True)
if save:
    if base==10:
        a.save(str(number)+" to C"+str(cyclicBase)+".gif",dpi=300,writer=pw(fps=25))
    else:
        a.save(str(number)+" (base "+str(base)+") to C"+str(cyclicBase)+".gif",dpi=300,writer=pw(fps=25))
else:
    plt.show()
