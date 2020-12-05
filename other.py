def getCell(x, y):
        cellWidth  = 1200/15
        cellHeight = 700/15
        row = int((y) / cellHeight)
        col = int((x) / cellWidth)
        return (row, col)

def distance(x, y, x1, y1):
            return ((x-x1)**2 + (y-y1)**2)**0.5

def getCellBounds(row, col):
            cellWidth = 1200 / 15
            cellHeight = 700 / 15
            x0 = col * cellWidth
            x1 = (col+1) * cellWidth
            y0 =  row * cellHeight
            y1 = (row+1) * cellHeight
            return (x0, y0, x1, y1)
