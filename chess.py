import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
co = (100, 100, 100) # random background color for now
height = 1444
width = 1444

display = pygame.display.set_mode((height, width))
display.fill(co)

class tile:
    def __init__(self, colour, x_position, y_position):
        self.colour = colour
        self.x_position = x_position
        self.y_position = y_position

def draw_tile(colour, x, y, disp):
    pygame.draw.rect(disp, colour, [x, y, width/9, height/9]) # (x,y,xsize,ysize)
    
label = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
         ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
         ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
         ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
         ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
         ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
         ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
         ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']]
dc ={}

counter = 1
initalx=20
initaly=20
for x in label:
    for term in x:
        if counter%2 != 0:
            dc[term] = tile(white, initalx, initaly)
            draw_tile(dc[term].colour, dc[term].x_position, dc[term].y_position, display)
            initalx+=width/9
            counter += 1
        else:
            dc[term] = tile(black, initalx, initaly)
            draw_tile(dc[term].colour, dc[term].x_position, dc[term].y_position, display)
            initalx+=width/9
            counter += 1
        
    initaly+=height/9
    initalx=20
    counter = counter -1


pygame.display.update()
