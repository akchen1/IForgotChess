import pygame

pygame.init()

white = (232, 235, 239)
black = (125, 135, 150)
co = (100, 100, 100) # random background color for now
height = 1444
width = 1444

display = pygame.display.set_mode((height, width))
display.fill(co)

class tile:
    def __init__(self, colour, x_pos, y_pos):
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw_tile(self):
        pygame.draw.rect(display, self.colour, [self.x_pos, self.y_pos, width/8, height/8]) # (x,y,xsize,ysize)
def make_board():    
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
    initalx=0
    initaly=0
    for x in label:
        for term in x:
            if counter%2 != 0:
                dc[term] = tile(white, initalx, initaly)
                dc[term].draw_tile()
                initalx+=width/8
                counter += 1
            else:
                dc[term] = tile(black, initalx, initaly)
                dc[term].draw_tile()
                initalx+=width/8
                counter += 1
            
        initaly+=height/8
        initalx=0
        counter = counter -1
    return(dc)

class pawn:
    def __init__(self, tile):
        self.x = tile.x_pos
        self.y = tile.y_pos
        self.tile = tile
        self.image = pygame.image.load('pawn.png')
        self.image = pygame.transform.scale(self.image, (100,125))
        display.blit(self.image,(self.x + 35, self.y + 20))
    def move(self, n_tile):
        self.tile.draw_tile()
        self.tile = n_tile
        display.blit(self.image,(n_tile.x_pos + 35, n_tile.y_pos + 20))
        
        
dc = make_board()
p1 = pawn(dc['G1'])
pygame.display.flip()
pygame.display.update()


while True:
    move = input('move where: ')
    p1.move(dc[move])
    pygame.display.flip()
    pygame.display.update()    



