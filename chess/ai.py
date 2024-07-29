import sys
from random import shuffle, randint
import numpy as np
import torch

'''
model = torch.jit.load('nn7EndGame1000_scripted.pt')
model.eval()
'''
mode="all pieces"

if mode=="all pieces":
    model=torch.jit.load('nn7EndGame1000_scripted.pt')
elif mode=="rooks only":
    model=torch.jit.load('nnGMNeil1000_scripted.pt')
model.eval()

def value(board):
    if mode=="all pieces":
        positions=[(board.squares[y][x],x+1,y+1) for x in range(8) for y in range(8) if board.squares[y][x]!=0]
        wKing=[(x,y) for (p,x,y) in positions if p==9]
        bKing=[(x,y) for (p,x,y) in positions if p==-9]
        queen=[(x,y) for (p,x,y) in positions if p==8]
        rooks=[(x,y) for (p,x,y) in positions if p==5]
        bishops=[(x,y) for (p,x,y) in positions if p==3]
        counts=[len(x) for x in [wKing,bKing,queen,rooks,bishops]]
        if (counts[0],counts[1])!=(1,1):
            raise Exception("Incorrect number of kings. Expected 1 white king, 1 black king. Got "+str(counts[0])+" white kings and "+str(counts[1])+" black kings.")
        if counts[2]>1 or counts[3]>2 or counts[4]>2:
            raise Exception("Incorrect number of pieces. Expected 0-1 queens, 0-2 rooks, and 0-2 bishops. Got "+str(count[2])+" queens, "+str(count[3])+" rooks, and "+str(count[4])+" bishops.")
        if counts[2]==0:
            queen.append((0,0))
        while len(rooks)<2:
            rooks.append((0,0))
        while len(bishops)<2:
            bishops.append((0,0))
        array=[wKing[0][0],wKing[0][1],
               bKing[0][0],bKing[0][1],
               queen[0][0],queen[0][1],
               rooks[0][0],rooks[0][1],
               rooks[1][0],rooks[1][1],
               bishops[0][0],bishops[0][1],
               bishops[1][0],bishops[1][1]]
        array=torch.tensor(array).float()
        r=model(array)
    elif mode=="rooks only":
        positions=[(board.squares[y][x],x+1,y+1) for x in range(8) for y in range(8) if board.squares[y][x]!=0]
        wKing=[(x,y) for (p,x,y) in positions if p==9]
        bKing=[(x,y) for (p,x,y) in positions if p==-9]
        rooks=[(x,y) for (p,x,y) in positions if p==5]
        counts=[len(x) for x in [wKing,bKing,rooks]]
        if (counts[0],counts[1])!=(1,1):
            raise Exception("Incorrect number of kings. Expected 1 white king, 1 black king. Got "+str(counts[0])+" white kings and "+str(counts[1])+" black kings.")
        if counts[2]>2:
            raise Exception("Incorrect number of pieces. Expected at most 1 rook. Got "+str(count[2])+" rooks.")
        while len(rooks)<2:
            rooks.append((0,0))
        array=[wKing[0][0],wKing[0][1],
               bKing[0][0],bKing[0][1],
               rooks[0][0],rooks[0][1],
               rooks[1][0],rooks[1][1]]
        array=torch.tensor(array).float()
        r=model(array)
    return r

def minimax(board,depth,maximizing=True,alpha=-sys.maxsize,beta=sys.maxsize,whiteTurn=False):
    if not whiteTurn:
        board.flip()
    boards=board.allMoves()
    if not whiteTurn:
        board.flip()
        [board.flip() for board in boards]
    #if not whiteTurn:
    #    board.flip()
    if depth==0 or len(boards)==0:
        v=value(board)
        return value(board)
    if maximizing:
        v=-sys.maxsize
        for board in boards:
            v=max(v,minimax(board,depth-1,False,alpha,beta,not whiteTurn))
            if v>beta:
                break
            alpha=max(alpha,v)
        return v
    else:
        v=sys.maxsize
        for board in boards:
            v=min(v,minimax(board,depth-1,True,alpha,beta,not whiteTurn))
            if v<alpha:
                break
            beta=min(beta,v)
        return v

def pickMove(board,depth):
    boards=board.allMoves()
    if len(boards)==0:
        return None
    shuffle(boards)
    values=[minimax(b,depth) for b in boards]
    i=values.index(min(values))
    return boards[i]
