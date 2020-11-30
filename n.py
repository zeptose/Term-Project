import enemies
import math 
import random
from cmu_112_graphics import *



def createmap(board, path):
    startrow = random.randrange(len(board))
    startcol = 0
    endrow = random.randrange(len(board))
    endcol = len(board) -1
    rows = len(board)
    cols = len(board)
    board[startrow][startcol] = 1
    result = legalmove(board, rows,cols,startrow, startcol, endrow, endcol, path)
    if result == True:
        return board, path
    else:
        return None
#increment row by 1 and random do columnn up or down by 1

def legalmove(board, rows, cols,startrow,startcol, endrow, endcol, path):
    if (startrow, startcol) not in path:
        path.append((startrow, startcol))
    dirs = [(0, 0), (1, 0)]
    random.shuffle(dirs)

    if startcol == endcol:
        return True 

    for move in dirs:
        newcol = startcol + 1
        board[startrow][newcol] = 1
        if (startrow, newcol) not in path:
            path.append((startrow, newcol))
        if newcol == endcol:
            return True 
        newrow = startrow + move[0]
        if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols and board[newrow][newcol] == 0:
            if newrow == startrow:
                newcol += 1
                board[newrow][newcol] = 1
                if (newrow, newcol) not in path:
                    path.append((newrow, newcol))
                if legalmove(board,rows,cols,newrow,newcol,endrow, endcol, path):
                    return True 
                else:
                    board[newrow][newcol] = 0
            else:
                board[newrow][newcol] = 1
                if legalmove(board,rows,cols,newrow,newcol,endrow, endcol, path):
                    return True 
                else:
                    board[newrow][newcol] = 0
        if newrow == len(board) - 1:
            newrow = 0
            newcol += 1
            for row in range(len(board)-1, -1, -1):
                board[row][newcol] = 1
                if (row, newcol) not in path:
                    path.append((row, newcol))
            if legalmove(board,rows,cols,newrow,newcol,endrow, endcol, path):
                return True 
            else:
                board[newrow][newcol] = 0
    return False


