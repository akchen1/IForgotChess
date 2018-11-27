import pygame
import euChange as EUP
pygame.init()

white = (232, 235, 239)
black = (125, 135, 150)
height = 635
width = 635
offset = 35
all_sprites_list = pygame.sprite.Group()

display = pygame.display.set_mode((height, width))

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
    pos_dict = {}
    counter = 1
    initialx = offset
    initialy = 0
    for x in label:
        for term in x:
            if counter%2 != 0:
                pos_dict[term] = tile(white, initialx, initialy)
                pos_dict[term].draw_tile()
                initialx += (width-offset)/8
                counter += 1
            else:
                pos_dict[term] = tile(black, initialx, initialy)
                pos_dict[term].draw_tile()
                initialx += (width-offset)/8
                counter += 1
            
        initialy += (height-offset)/8
        initialx = offset
        counter = counter -1
    return (pos_dict)

pos_dict = make_board()
p1 = EUP.pawn(pos_dict['G1'], width, height, offset)
pygame.display.flip()
pygame.display.update()

all_sprites_list.add(p1)

while True:
    move = input('move where: ')
    all_sprites_list.update()
    all_sprites_list.draw(display)
    pygame.display.flip()
    pygame.display.update()
    if move != '':
        pygame.quit()