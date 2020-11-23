import enemies
import math 
import random
from cmu_112_graphics import *

def board(rows, cols):
    return [[0] * cols for row in range(rows)]

def startend(board):
    startx = random.randrange(len(board))
    rows = len(board)
    cols = len(board)
    for row in range(len(board)):
        for col in range(len(board[0])):
            result = legalmove(board, rows,cols,row,col)
            if result == True:
                return result
    return None
#increment row by 1 and random do columnn up or down by 1

def legalmove(board, rows, cols,startrow,startcol):
    dirs = [(-1, 0), (0, -1), (0, +1), (+1, 0)]
    random.shuffle(dirs)

    
    if startcol == cols-1:
        return True 
    for move in dirs:
        newrow = startrow + move[0]
        newcol = startcol + move[1]
        print(newrow,newcol)
        if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols and board[newrow][newcol] == 0:
            board[newrow][newcol] = 1
            if legalmove(board,rows,cols,newrow,newcol):
                return True 
            else:
                board[newrow][newcol] = 0
            
    return False 

board = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
print(startend(board))
print(board)

