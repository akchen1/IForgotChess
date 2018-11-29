import pygame
import math
import numpy as np

pygame.init()
pygame.mixer.init()

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
HEIGHT = 644
WIDTH = 644

display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
import euPieces as EUP

COORD_ID = np.array([['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
            ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
            ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
            ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
            ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
            ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']])

class tile:
    def __init__(self, colour, x_pos, y_pos):
        self.full = False
        self.piece = empty()
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, WIDTH/8, HEIGHT/8)
        
    def draw_tile(self):
        pygame.draw.rect(display, self.colour, self.rect) # (x,y,xsize,ysize)


class empty:
    def __init__(self):
        self.full = False
        self.player = None
    def updatep(self, new_tile):
        pass
    def move(self, a, b, c, d):
        pass
        
class board:
    def __init__(self):
        self.dc = {}
        self.label = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                      ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                      ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                      ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                      ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                      ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                      ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                      ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']]
        self.make_board()
    def gimme_dictionary_lmao(self):
        return self.dc
    
    def make_board(self):
        counter = 1
        initalx=0
        initaly=0
        for x in self.label:
            for term in x:
                if counter%2 != 0:
                    self.dc[term] = tile(WHITE, initalx, initaly)
                    initalx+=WIDTH/8
                    counter += 1
                else:
                    self.dc[term] = tile(BLACK, initalx, initaly)
                    initalx+=WIDTH/8
                    counter += 1
            
            initaly+=HEIGHT/8
            initalx=0
            counter = counter -1

    def draw_board(self):
        for _, tile in self.dc.items():
            tile.draw_tile()
                
def wait_button():
    pygame.event.clear()
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return(True)
            
def find_tile(board, mouse_pos, tile_flag):
    ''' find tile will find the corresponding tile to mouse_pos, if it's the first
    iteration, the tile_flag will be on so that if an empty space is clicked, it will
    stop the loop and allow player to try again '''
    for key, tile in board.dc.items():
        if mouse_pos[1] > tile.y_pos and mouse_pos[1] < (tile.y_pos + HEIGHT/8):
            if mouse_pos[0] > tile.x_pos and mouse_pos[0] < (tile.x_pos + WIDTH/8):
                if tile.piece.player == None and tile_flag: 
                    return(False, None, None)
                return(True, key, tile)
    return(False, None, None)

tile_flag = 1 
fps = 30
clock = pygame.time.Clock()
board = board() # initialize board
dc = board.gimme_dictionary_lmao()
all_sprites = pygame.sprite.Group()

p1 = EUP.pawn(board.dc["B1"], "BLACK")
p2 = EUP.pawn(board.dc["B2"], "BLACK")
p3 = EUP.pawn(board.dc["B3"], "BLACK")
p4 = EUP.pawn(board.dc["B4"], "BLACK")
p5 = EUP.pawn(board.dc["B5"], "BLACK")
p6 = EUP.pawn(board.dc["B6"], "BLACK")
p7 = EUP.pawn(board.dc["B7"], "BLACK")
p8 = EUP.pawn(board.dc["B8"], "BLACK")
P1 = EUP.pawn(board.dc["G1"], "WHITE")
P2 = EUP.pawn(board.dc["G2"], "WHITE")
P3 = EUP.pawn(board.dc["G3"], "WHITE")
P4 = EUP.pawn(board.dc["G4"], "WHITE")
P5 = EUP.pawn(board.dc["G5"], "WHITE")
P6 = EUP.pawn(board.dc["G6"], "WHITE")
P7 = EUP.pawn(board.dc["G7"], "WHITE")
P8 = EUP.pawn(board.dc["G8"], "WHITE")

r1 = EUP.rook(board.dc["A1"], "BLACK")
r2 = EUP.rook(board.dc["A8"], "BLACK")
R1 = EUP.rook(board.dc["H1"], "WHITE")
R2 = EUP.rook(board.dc["H8"], "WHITE")

k1 = EUP.king(board.dc["A5"], "BLACK")
K2 = EUP.king(board.dc["H5"], "WHITE")

b1 = EUP.bishop(board.dc["A3"], "BLACK")
b2 = EUP.bishop(board.dc["A6"], "BLACK")
B1 = EUP.bishop(board.dc["H3"], "WHITE")
B2 = EUP.bishop(board.dc["H6"], "WHITE")

q1 = EUP.queen(board.dc["A4"], "BLACK")
Q1 = EUP.queen(board.dc["H4"], "WHITE")

kn1 = EUP.knight(board.dc["A2"], "BLACK")
kn2 = EUP.knight(board.dc["A7"], "BLACK")
Kn1 = EUP.knight(board.dc["H2"], "WHITE")
Kn2 = EUP.knight(board.dc["H7"], "WHITE")
all_sprites.add(p1, p2, p3, p4, p5, p6, p7, p8, P1, P2, P3, P4, P5, P6, P7, P8)
all_sprites.add(r1, r2, R1, R2, k1, K2, q1, Q1, b1, b2, B1, B2, kn1, kn2, Kn1, Kn2)
running = True
white_turn = True
print(board.dc["A1"].x_pos)
while running:
    clock.tick(fps)
    board.draw_board()
    all_sprites.update()
    all_sprites.draw(display)
    pygame.display.update() 
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.MOUSEBUTTONDOWN: # click on piece

            mouse_pos = pygame.mouse.get_pos() # get piece location
            found, key, tile = find_tile(board, mouse_pos, tile_flag)  # find corresponding tile
            if found and tile.piece.player == "WHITE" and white_turn:
                tile.piece.highlight(key, tile, dc)
                wait_button()   # wait for input for new location
                new_mouse_pos = pygame.mouse.get_pos()
                found, new_key, new_tile = find_tile(board, new_mouse_pos, not tile_flag)
                if found: 
                    changed, promotion, new_promo = tile.piece.move(new_tile)
                    if changed:
                        white_turn = False
                        if promotion:
                            all_sprites.add(new_promo)
 
            elif found and tile.piece.player == "BLACK" and not white_turn:
                tile.piece.highlight(key, tile, dc)
                wait_button()   # wait for input for new location
                new_mouse_pos = pygame.mouse.get_pos()
                found, new_key, new_tile = find_tile(board, new_mouse_pos, not tile_flag)
                if found:
                    changed, promotion, new_promo = tile.piece.move(new_tile)
                    if changed:
                        white_turn = True
                        if promotion:
                            all_sprites.add(new_promo)
                           
                             
pygame.quit()


