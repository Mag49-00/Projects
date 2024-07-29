from board import Board
import pygame
import numpy as np
from math import floor
from ai import pickMove

p1="human" #white player -- "human" or "botx", x=0: use random moves. x>0: use smartMove method with depth=x
p2="human" #black player -- "human" or "botx" as above
graphicSwap=1

lastMove=None #used for debugging purposes.

def getDepth(x):
    if x==1:
        if p1[:3]=="bot":
            if p1[-1]!="t":
                return int(p1[-1])
    else:
        if p2[:3]=="bot":
            if p2[-1]!="t":
                return int(p2[-1])
    return None

class Graphic:
    pieces={
        1:"pawn",
        2:'knight',
        3:'bishop',
        5:'rook',
        8:'queen',
        9:'king'
        }
    for piece in pieces.keys():
        pieces[piece]=[
            pygame.image.load(pieces[piece]+"-black.png"),
            pygame.image.load(pieces[piece]+"-white.png")
            ]
    sq=[pygame.image.load("sq-black.png"),pygame.image.load("sq-white.png")]
    highlightGraphic=pygame.image.load("sq-highlight.png")
    captureGraphic=pygame.image.load("sq-takable.png")
    threatGraphic=pygame.image.load("sq-threat.png")
    promotionGraphic=pygame.Surface((60*5,60*2))
    promotionGraphic.fill((140,140,200))
    def __init__(self,board):
        self.board=board
        self.moving=None
        self.highlighted={}
        self.capturable={}
        self.promoting=False
        self.promotingKeys=[]
        self.swap=1 #displays black as white and white as black if this is -1.

    def display(self,screen,location,first=True):
        x,y=location
        for i in range(8):
            for j in range(8):
                a=x+60*i
                b=y+60*j
                screen.blit(Graphic.sq[(i+j)%2==0],(a,b))
                p=self.board.getSqr((i,j))*self.swap
                if p!=0:
                    k=1
                    if p not in Graphic.pieces.keys():
                        p=-p
                        k=0
                    graphic=Graphic.pieces[p][k]
                    screen.blit(graphic,(a,b))
                if (i,j) in self.highlighted.keys():
                    screen.blit(Graphic.highlightGraphic,(a,b))
                elif (i,j) in self.capturable.keys():
                    screen.blit(Graphic.captureGraphic,(a,b))
        if self.promoting:
            y+=60*3
            x+=60*2-30
            screen.blit(self.promotionGraphic,(x,y))
            x+=30
            y+=30
            for p in range(len(self.promotingKeys)):
                if self.swap==1:
                    screen.blit(Graphic.pieces[self.promotingKeys[p]][1],(x,y))
                else:
                    screen.blit(Graphic.pieces[self.promotingKeys[p]][0],(x,y))
                x+=60

    def reset(self):
        self.moving=None
        self.highlighted={}
        self.capturable={}
        self.promoting=False
        self.promotingKeys=[]

    def botMove(self,x):
        global lastMove
        lastMove=board.board.copy() #used for debugging
        if x==None:
            move=self.board.randomMove()
        else:
            move=pickMove(board.board,x)#Chain(self.board,x).minimax()
        if move==None:
            if self.board.isValid():
                print("Stalemate!")
            else:
                print("You win!")
            return False
        else:
            self.board=move
        return True

    #process a click
    def click(self,pos):
        if p1[:3]==p2[:3] and p1[:3]=="bot":
            m1=getDepth(1)
            m2=getDepth(2)
            if p1=="bot":
                if self.botMove(m1):
                    self.board.flip()
                    self.botMove(m2)
                    self.board.flip()
            return
        x0,y0=pos
        x=floor(x0/60)
        y=floor(y0/60)
        if self.promoting:
            #pawn promotions
            x0-=120
            y0-=210
            x0=floor(x0/60)
            y0=floor(y0/60)
            if y0==0 and x0 in range(len(self.promotingKeys)):
                self.board=self.promoting[self.promotingKeys[x0]]
                self.reset()
                self.board.flip()
                if "bot" in [p1[:3],p2[:3]]:
                    if p1=="human":
                        self.botMove(getDepth(2))
                    else:
                        self.botMove(getDepth(1))
                    self.board.flip()
        elif self.moving==None:
            self.moving=(x,y)
            piece=self.board.getSqr(self.moving)
            if piece<=0:
                self.reset()
            else:
                moves=self.board.movesFrom((x,y))
                for move in moves:
                    array=np.array(self.board.squares-move.squares)
                    b,a=np.where(array<0)
                    s=np.sum(array)
                    if 1 in array[1,:]:
                        #this should be a promotion move
                        a=int(a)
                        b=int(b)
                        p=move.squares[b][a]
                        if (a,b) in self.highlighted.keys():
                            self.highlighted[(a,b)][p]=move
                        else:
                            self.highlighted[(a,b)]={p:move}
                    elif s==-1 and len(a)>1:
                        #this move is an en passant
                        d,c=np.where(array>0)
                        d-=1
                        if c+1 in a:
                            self.capturable[(int(c+1),int(d))]=move
                        else:
                            self.capturable[(int(c-1),int(d))]=move
                    elif len(a)>1:
                        #castle
                        if array[7][6]!=0:
                            #right castle
                            if (6,7) not in self.highlighted.keys():
                                self.highlighted[(6,7)]=move
                        elif array[7][2]!=0:
                            #left castle
                            if (2,7) not in self.highlighted.keys():
                                self.highlighted[(2,7)]=move
                    else:
                        #any other move goes here
                        a=int(a)
                        b=int(b)
                        if ((a,b) not in self.highlighted.keys()) and s==0:
                            self.highlighted[(a,b)]=move
                        elif ((a,b) not in self.capturable.keys()) and s<0:
                            self.capturable[(a,b)]=move
        else:
            #move the selected piece
            piece=self.board.getSqr(self.moving)
            if (x,y) in list(self.highlighted.keys())+list(self.capturable.keys()):
                if (x,y) in self.highlighted.keys():
                    if type(self.highlighted[(x,y)])==dict:
                        self.promoting=self.highlighted[(x,y)]
                        self.promotingKeys=list(self.promoting.keys())
                    else:
                        self.board=self.highlighted[(x,y)]
                else:
                    self.board=self.capturable[(x,y)]
                if not self.promoting:
                    self.board.flip()
                if (not self.promoting) and "bot" in [p1[:3],p2[:3]]:
                    move=self.board.randomMove()
                    if p1=="human":
                        self.botMove(getDepth(2))
                    else:
                        self.botMove(getDepth(1))
                    self.board.flip()
                    if self.board.allMoves()==[]:
                        print("You lose!")
                if not (self.promoting) and "bot" not in [p1[:3],p2[:3]]:
                    if self.swap==1:
                        self.swap=-1
                    else:
                        self.swap=1
            if not self.promoting:
                self.reset()
                

pygame.init()
X=8*60
Y=8*60
bgColor=(100,100,180)

screen=pygame.display.set_mode((X,Y),pygame.RESIZABLE)
pygame.display.set_caption("Chess AI")
screen.fill(bgColor)

blitLoc=(X/2-4*60,Y/2-4*60)
board=Graphic(Board())

pygame.display.flip()
status = True
first=True

if p1[:3]=="bot" and p2=="human":
    board.botMove(getDepth(1))
    board.swap=-1
    board.board.flip()

while (status):
    for event in pygame.event.get():
        #handles what happens if the window's x is pressed.
        if event.type == pygame.QUIT:
            status = False

        #handles window resizing.
        elif event.type==pygame.VIDEORESIZE:
            X=event.w
            Y=event.h
            #Ensure minimum size...
            if X<=60*8:
                X=60*8
            if Y<=60*8:
                Y=60*8
            screen=pygame.display.set_mode((X,Y),pygame.RESIZABLE) 
            blitLoc=(X/2-4*60,Y/2-4*60) #update blitLoc

        #process clicks.
        elif event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            board.click((pos[0]-blitLoc[0],pos[1]-blitLoc[1]))

    #update the graphics.
    screen.fill(bgColor)
    board.display(screen,blitLoc,first)
    pygame.display.flip()
    first=False
    pygame.time.wait(60)

pygame.quit()
