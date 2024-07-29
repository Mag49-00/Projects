from math import floor
from random import shuffle
import numpy as np
from random import randint

'''
Todo:
-check for inobvious stalemates (e.g. king vs king and knight)
-check for bugs
-optimize speed
'''

class Board:
    def __init__(self,array=None,moved=None):
        if array.__class__.__name__=='NoneType':
            array=np.array([[-5,-2,-3,-8,-9,-3,-2,-5],
                            [-1,-1,-1,-1,-1,-1,-1,-1],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 1, 1, 1, 1, 1, 1, 1, 1], 
                            [ 5, 2, 3, 8, 9, 3, 2, 5]],dtype=np.int8)
            '''[[ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0,-9, 0, 0],
                            [ 0, 0, 5, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 9, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0], 
                            [ 0, 0, 0, 0, 0, 0, 5, 0]],dtype=np.int8)'''
            '''normal starting board state: [[-5,-2,-3,-8,-9,-3,-2,-5],
                            [-1,-1,-1,-1,-1,-1,-1,-1],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0, 0, 0],
                            [ 1, 1, 1, 1, 1, 1, 1, 1], 
                            [ 5, 2, 3, 8, 9, 3, 2, 5]],dtype=np.int8)'''
        #self.populate()
        self.squares=array
        self.whiteKingPos=(4,7)
        self.blackKingPos=(4,0)
        self.enPassant=(-1,-1)
        self.updateKingPos()
        if moved==None:
            moved=[False,False,False,False,False,False]
            #First index: white king moved?
            #Second index: black king moved?
            #Third index: white E rook moved?
            #Fourth index: white W rook moved?
            #Fifth index: black E rook moved?
            #Sixth index: black W rook moved?
            if self.whiteKingPos!=(4,7):
                moved[0]=True
            if self.blackKingPos!=(4,0):
                moved[1]=True
        self.moved=moved

    '''def populate(self):
        array=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0]],dtype=np.int8)
        x=randint(0,7)
        y=randint(0,7)
        array[x][y]=9
        a=x
        b=y
        while (a in [x-1,x+1,x]) and (b in [y-1,y+1,y]):
            a=randint(0,7)
            b=randint(0,7)
        array[a][b]=-9
        pieces={'rook':0,'bishop':0,'queen':0}
        while sum([pieces[x] for x in pieces.keys()])==0:
            pieces['rook']=randint(0,2)
            pieces['bishop']=randint(0,2)
            pieces['queen']=randint(0,1)
        for k in range(pieces['rook']):
            while array[a][b]!=0:
                a=randint(0,7)
                b=randint(0,7)
            array[a][b]=5
        for k in range(pieces['bishop']):
            while array[a][b]!=0:
                a=randint(0,7)
                b=randint(0,7)
            array[a][b]=3
        for k in range(pieces['queen']):
            while array[a][b]!=0:
                a=randint(0,7)
                b=randint(0,7)
            array[a][b]=8
        self.squares=array'''
            
    def copy(self):
        b=Board(np.copy(self.squares),list(self.moved))
        b.whiteKingPos=self.whiteKingPos
        b.blackKingPos=self.blackKingPos
        #self.enPassant should be cleared on copy.
        return b

    def __str__(self):
        ret=[]
        for line in self.squares:
            line=",".join([str(x) if x<0 else " "+str(x) for x in line])
            ret.append(line)
        return "\n".join(ret)

    def __repr__(self):
        return str(self)

    def flip(self):
        self.squares=-self.squares
        for i in range(4):
            self.squares[[i,7-i],:]=self.squares[[7-i,i],:]
        self.moved=[self.moved[1],self.moved[0],self.moved[4],self.moved[5],self.moved[2],self.moved[3]]
        x,y=self.whiteKingPos
        a,b=self.blackKingPos
        y=7-y
        self.blackKingPos=(x,y)
        b=7-b
        self.whiteKingPos=(a,b)
        if self.enPassant!=(-1,-1):
            self.enPassant=(self.enPassant[0],7-self.enPassant[1])
        return self

    def __getitem__(self,key):
        return self.squares[:,key]

    def getSqr(self,index):
        return self[index[0]][index[1]]

    #returns the line from one board edge to another going through the given index, pointing in the given direction
    #also returns the index in the returned line that corresponds to the value of the square at the given index in the board as a whole.
    #direction may be:
    #   "v": vertical line
    #   "h": horizontal line
    #   "dd": downward diagonal (from the perspective of white at the bottom of the board)
    #   "du": upward diagonal (from the same perspective)
    def line(self,index,direction):
        x,y=index
        if direction=="v":
            ret=self.squares[:,x]
            i=y
        elif direction=="h":
            ret=self.squares[y,:]
            i=x
        elif direction=="dd":
            m=min(x,y)
            a=x-m
            b=y-m
            ret=[self.getSqr((a+i,b+i)) for i in range(8) if max(a+i,b+i)<8]
            i=m
        elif direction=="ud":
            m=min(x,7-y)
            a=x-m
            b=y+m
            ret=[self.getSqr((a+i,b-i)) for i in range(8) if a+i<8 and b-i>-1]
            i=m
        return (np.array(ret),i)

    #returns a list of all indices that are one knight-move away from the given index.
    #Note: unlike the line method above, this *does not* return square values, instead indices.
    def knightMoves(self,index):
        x,y=index
        ret=[
            (x+2,y+1),
            (x+2,y-1),
            (x-2,y+1),
            (x-2,y-1),
            (x+1,y+2),
            (x-1,y+2),
            (x+1,y-2),
            (x-1,y-2)
            ]
        return [i for i in ret if (i[0] in range(8) and i[1] in range(8))]

    def move(self,start,end):
        a,b=start
        x,y=end
        piece=self.getSqr(start)
        if piece in [9,5]:
            if piece==9:
                self.moved[0]=True
                self.whiteKingPos=end
            else:
                if start==(0,7):
                    self.moved[2]=True
                elif start==(7,7):
                    self.moved[3]=True
        self[a][b]=0
        self[x][y]=piece

    def isValid(self):
        #given a line and index as an input (i.e. the output of self.line function),
        #returns false if an attack can be made at the king from that line, true otherwise
        #pieces should be a list of which pieces in the line should be considered for potential attacks
        def lineAtk(line,index,pieces):
            pline=line[index+1:]
            mline=np.flip(line[:index])
            def subLine(line):
                while True:
                    if line.size==0:
                        return True
                    elif line[0]!=0:
                        if line[0] in pieces:
                            return False
                        return True
                    else:
                        line=line[1:]
            return subLine(mline) and subLine(pline)
        x,y=self.whiteKingPos
        #Check for checks from knights
        if -2 in [self.getSqr(i) for i in self.knightMoves(self.whiteKingPos)]:
            return False
        #Check for checks from pawns
        if (y-1) in range(8):
            if x+1 in range(8):
                if self.getSqr((x+1,y-1))==-1:
                    return False
            if x-1 in range(8):
                if self.getSqr((x-1,y-1))==-1:
                    return False
        #Check for checks from straight-line attacks
        v,vi=self.line(self.whiteKingPos,"v")
        if not lineAtk(v,vi,[-5,-8]):
            return False
        h,hi=self.line(self.whiteKingPos,"h")
        if not lineAtk(h,hi,[-5,-8]):
            return False
        #Check for checks from diagonal-line attacks
        d,di=self.line(self.whiteKingPos,"dd")
        if not lineAtk(d,di,[-3,-8]):
            return False
        u,ui=self.line(self.whiteKingPos,"ud")
        if not lineAtk(u,ui,[-3,-8]):
            return False
        #Check for adjacency to opposing king
        a,b=self.blackKingPos
        if a in (x-1,x,x+1) and b in (y-1,y,y+1):
            return False
        return True

    #makes sure the listed king positions are accurate.
    def updateKingPos(self):
        for i in range(8):
            for j in range(8):
                v=self.getSqr((i,j))
                if v==9:
                    self.whiteKingPos=(i,j)
                elif v==-9:
                    self.blackKingPos=(i,j)

    def moveAndCopy(self,start,end):
        b=self.copy()
        b.move(start,end)
        return b

    #returns a list of all possible moves the piece at the given index can make, as board states (i.e. board objects).
    def movesFrom(self,index):
        #given a line and index as an input (i.e. the output of self.line function),
        #returns the number of indices the piece can move in both directions as an ordered pair: (-x,y) which indicates the piece
        #can move up to x units down the list and y units up the list (both x and y should be nonnegative)
        def moves(line,index):
            pline=line[index+1:]
            mline=np.flip(line[:index])
            def subLine(line):
                i=0
                cont=True
                while cont:
                    if line.size==0:
                        cont=False
                    elif line[0]!=0:
                        cont=False
                    else:
                        line=line[1:]
                        i+=1
                if line.size>0:
                    if line[0]<0:
                        i+=1
                return i
            return (-subLine(mline),subLine(pline))
            
        piece=self.getSqr(index)
        x,y=index
        ret=[]
        if piece<=0:
            return ret
        if piece==2:
            #knight moves
            moves=[i for i in self.knightMoves(index) if self.getSqr(i)<=0]
            ret+=[self.moveAndCopy(index,move) for move in moves]
        if piece in [5,8]:
            #straight line moves...
            v,vi=self.line(index,"v")
            h,hi=self.line(index,"h")
            a,b=moves(v,vi)
            c,d=moves(h,hi)
            ret+=[self.moveAndCopy(index,(x,y+i+1)) for i in range(b)]
            ret+=[self.moveAndCopy(index,(x,y-i-1)) for i in range(-a)]
            ret+=[self.moveAndCopy(index,(x+i+1,y)) for i in range(d)]
            ret+=[self.moveAndCopy(index,(x-i-1,y)) for i in range(-c)]
        if piece in [3,8]:
            #diagonal moves...
            d,di=self.line(index,"dd")
            u,ui=self.line(index,"ud")
            a,b=moves(d,di)
            c,d=moves(u,ui)
            ret+=[self.moveAndCopy(index,(x+i+1,y+i+1)) for i in range(b)]
            ret+=[self.moveAndCopy(index,(x-i-1,y-i-1)) for i in range(-a)]
            ret+=[self.moveAndCopy(index,(x+i+1,y-i-1)) for i in range(d)]
            ret+=[self.moveAndCopy(index,(x-i-1,y+i+1)) for i in range(-c)]
        if piece==1:
            moves=[]
            #standard pawn moves...
            if self.getSqr((x,y-1))==0:
                if y-1==0:
                    for k in [2,3,5,8]:
                        b=self.moveAndCopy(index,(x,0))
                        b.squares[0][x]=k
                        ret.append(b)
                else:
                    moves.append((x,y-1))
                if y==6 and self.getSqr((x,y-2))==0:
                    b=self.moveAndCopy(index,(x,y-2))
                    b.enPassant=(x,y-1)
                    ret.append(b)
            #taking and en passant pawn moves...
            if x+1<8:
                if self.getSqr((x+1,y-1))<0 or (x+1,y-1)==self.enPassant:
                    board=self.moveAndCopy(index,(x+1,y-1))
                    if self.enPassant==(x+1,y-1):
                        board.squares[y][x+1]=0
                    if y-1==0:
                        for k in [2,3,5,8]:
                            b=board.copy()
                            b.squares[0][x+1]=k
                            ret.append(b)
                    else:
                        ret.append(board)
            if x-1>-1:
                if self.getSqr((x-1,y-1))<0 or (x-1,y-1)==self.enPassant:
                    board=self.moveAndCopy(index,(x-1,y-1))
                    if self.enPassant==(x-1,y-1):
                        board.squares[y][x-1]=0
                    if y-1==0:
                        for k in [2,3,5,8]:
                            b=board.copy()
                            b.squares[0][x-1]=k
                            ret.append(b)
                    else:
                        ret.append(board)
            ret+=[self.moveAndCopy(index,move) for move in moves]
        if piece==9:
            #king moves
            moves=[
                (x+1,y-1),(x+1,y),(x+1,y+1),
                (x,y-1),(x,y+1),
                (x-1,y-1),(x-1,y),(x-1,y+1)
                ]
            moves=[move for move in moves if (move[0] in range(8) and move[1] in range(8))]
            moves=[i for i in moves if self.getSqr(i)<=0]
            ret+=[self.moveAndCopy(index,move) for move in moves]
            #Check for possible castling
            if (not self.moved[0]) and (not self.moved[2]) and self.isValid():
                castle=True
                for i in range(3):
                    if self.getSqr((i+1,7))!=0:
                        castle=False
                        break
                if castle:
                    board=self.moveAndCopy(index,(3,7))
                    if board.isValid():
                        board.move((3,7),(2,7))
                        board.move((0,7),(3,7))
                        ret.append(board)
            if (not self.moved[0]) and (not self.moved[3]) and self.isValid():
                castle=True
                for i in range(2):
                    if self.getSqr((7-i-1,7))!=0:
                        castle=False
                        break
                if castle:
                    board=self.moveAndCopy(index,(5,7))
                    if board.isValid():
                        board.move((5,7),(6,7))
                        board.move((7,7),(5,7))
                        ret.append(board)
            for board in ret:
                board.updateKingPos()
        return [board for board in ret if board.isValid()]

    #returns a list of all possible moves
    def allMoves(self):
        moves=[self.movesFrom((i,j)) for i in range(8) for j in range(8)]
        moves=[x for move in moves for x in move]
        '''
        for i in range(8):
            for j in range(8):
                moves+=self.movesFrom((i,j))'''
        return moves

    '''
    Old method--safe to delete
    #returns a list of all possible moves the enemy could make
    def enemyMoves(self):
        self.flip()
        ret=self.allMoves()
        self.flip()
        for board in ret:
            board.flip()
        return ret
    '''

    #returns the raw sum of point values of the pieces
    def score(self):
        return self.squares.sum()

    '''
    Old method--safe to delete
    #if currently in checkmate, returns -100000000000 if whitTurn and 100000000000 if not whitTurn
    #(based on who's turn it is, determined by whiteTurn)
    #if no one is in checkmate, returns the same as score.
    def modScore(self,whiteTurn=True):
        if whiteTurn and not self.isValid():
            return -100000000000
        elif not whiteTurn:
            self.flip()
            v=self.isValid()
            self.flip()
            if not v:
                return 100000000000
        return self.score()'''
    
    #makes a random move
    def randomMove(self):
        moves=self.allMoves()
        if len(moves)==0:
            return None
        shuffle(moves)
        return moves[0]

    #returns a vector to be fed into the neural net
    def toVector(self):
        return np.array(list(self.squares.flatten())+self.moved+[self.score(),self.isValid()])

def randomGame():
    B=Board()
    while True:
        input(B)
        moves=B.allMoves()
        if len(moves)==0:
            break
        else:
            shuffle(moves)
            B=moves[0]
            B.flip()
            moves=B.allMoves()
            if len(moves)==0:
                break
            else:
                shuffle(moves)
                B=moves[0]
                B.flip()
        print()
