import pygame
import euPieces as EUP

pygame.init()

white = (232, 235, 239)
black = (125, 135, 150)
co = (100, 100, 100) # random background color for now
height = 1444
width = 1444
offset = 0

display = pygame.display.set_mode((height, width))
display.fill(co)

class tile:
    def __init__(self, colour, x_pos, y_pos):
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw_tile(self):
        pygame.draw.rect(display, self.colour, [self.x_pos, self.y_pos, 
                        (width-offset)/8, (height-offset)/8]) # (x,y,xsize,ysize)

def make_board():    
    label = [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1'],
             ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
             ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
             ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
             ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
             ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
             ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
             ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8']]
    dc = {}
    counter = 1
    initalx = 0
    initaly = 0
    for x in label:
        for term in x:
            if counter%2 != 0:
                dc[term] = tile(white, initalx, initaly)
                dc[term].draw_tile()
                initalx += (width-offset)/8
                counter += 1
            else:
                dc[term] = tile(black, initalx, initaly)
                dc[term].draw_tile()
                initalx += (width-offset)/8
                counter += 1
            
        initaly += (height-offset)/8
        initalx = 0
        counter = counter -1
    return(dc)

dc = make_board()
p1 = EUP.pawn(dc['G1'], display)
pygame.display.flip()
pygame.display.update()

while True:
    move = input('move where: ')
    p1.move(dc[move], display)
    pygame.display.flip()
    pygame.display.update()    



