import pygame
import math
import random
import numpy as np

pygame.init()
pygame.mixer.init()     # Initiate the pygame module

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
HEIGHT = 644
WIDTH = 644
display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
# Declare global variables of color color and determines the game window size

import jpnPieces as JPN
import euPieces as EUP
# These import modules are not in the header since they require a display to be 
# made in pygame so that they can get the display size


COORD_ID = np.array([['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                     ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                     ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                     ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                     ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                     ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                     ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                     ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']])
# 2D Coordinate array that shows the position of each tile of the chess board

random_pawn = [EUP.pawn, JPN.pawn, EUP.pawn, EUP.pawn, JPN.pawn, JPN.gold]
random_exclusive = [EUP.bishop, EUP.knight, EUP.rook, JPN.silver, JPN.silver,
                    JPN.lance, EUP.queen]
random_king = [EUP.king, JPN.king]


class tile:
    def __init__(self, colour, x_pos, y_pos):
        self.full = False
        self.piece = empty()
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, WIDTH/8, HEIGHT/8)

    def draw_tile(self):
        pygame.draw.rect(display, self.colour, self.rect)  # (x,y,xsize,ysize)


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
        initalx = 0
        initaly = 0
        for x in self.label:
            for term in x:
                if counter % 2 != 0:
                    self.dc[term] = tile(WHITE, initalx, initaly)
                    initalx += WIDTH/8
                    counter += 1
                else:
                    self.dc[term] = tile(BLACK, initalx, initaly)
                    initalx += WIDTH/8
                    counter += 1

            initaly += HEIGHT/8
            initalx = 0
            counter = counter - 1

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


def checkmate(player, enemy, king):
    for x in all_sprites:
        if x.player == player and type(x) != type(king):
            if x != new_tile.piece:
                x.moveset(player, enemy, x.key, dc)
            else:
                x.moveset(player, enemy, new_key, dc)
            for y in x.available_moves:
                if int(y.x_pos) == king.rect.x and int(y.y_pos) == king.rect.y:
                    print("CHECK")
    if not king.alive():
        print("YOU LOSE")
        return(False)
    return(True)

def make_pieces():

    p = [None]*8
    i = 1
    for x in p:  # black pawns
        key = "B{}"
        key = key.format(i)
        x = random.choice(random_pawn)(board.dc[key], "BLACK", key)
        all_sprites.add(x)
        key = "A{}"
        key = key.format(i)
        if key == "A5":
            k1 = JPN.king(board.dc["A5"], "BLACK", "A5")
            all_sprites.add(k1)
            i += 1
            continue
        x = random.choice(random_exclusive)(board.dc[key], "BLACK", key)
        all_sprites.add(x)
        i += 1

    i = 1
    p = [None]*8
    for x in p:  # white pawns
        key = "G{}"
        key = key.format(i)
        x = random.choice(random_pawn)(board.dc[key], "WHITE", key)
        all_sprites.add(x)
        key = "H{}"
        key = key.format(i)
        if key == "H5":
            K2 = JPN.king(board.dc["H5"], "WHITE", "H5")
            all_sprites.add(K2)
            i += 1
            continue
        x = random.choice(random_exclusive)(board.dc[key], "WHITE", key)
        all_sprites.add(x)
        i += 1
    pass


tile_flag = 1
fps = 30
clock = pygame.time.Clock()
board = board()  # initialize board
dc = board.gimme_dictionary_lmao()
all_sprites = pygame.sprite.Group()

make_pieces()

# # r1 = JPN.rook(board.dc["A1"], "BLACK", "A1")
# r2 = JPN.rook(board.dc["A8"], "BLACK", "A8")
# # R1 = JPN.rook(board.dc["H1"], "WHITE", "H1")
R2 = JPN.rook(board.dc["D4"], "BLACK", "D4")

# k1 = JPN.king(board.dc["A5"], "BLACK", "A5")
# K2 = JPN.king(board.dc["H5"], "WHITE", "H5")

# b1 = JPN.bishop(board.dc["A3"], "BLACK", "A3")
# # b2 = JPN.bishop(board.dc["A6"], "BLACK", "A6")
B1 = JPN.bishop(board.dc["D3"], "BLACK", "D3")
all_sprites.add(B1,R2)
# # B2 = JPN.bishop(board.dc["H6"], "WHITE", "H6")

# # q1 = EUP.queen(board.dc["A4"], "BLACK", "A4")
# # Q1 = EUP.queen(board.dc["H4"], "WHITE", "H4")

# kn1 = JPN.knight(board.dc["A2"], "BLACK", "A2")
# # kn2 = JPN.knight(board.dc["A7"], "BLACK", "A7")
# Kn1 = JPN.knight(board.dc["H2"], "WHITE", "H2")
# # Kn2 = JPN.knight(board.dc["H7"], "WHITE", "H7")

# s1 = JPN.silver(board.dc["F1"], "BLACK", "F1")
# s2 = JPN.silver(board.dc["F2"], "WHITE", "F2")
# g1 = JPN.pawn(board.dc["E4"], "BLACK", "E3")
# g2 = JPN.pawn(board.dc["E5"], "WHITE", "E5")

# l1 = JPN.lance(board.dc["F3"], "BLACK", "F3")
# l2 = JPN.lance(board.dc["F4"], "WHITE", "F4")


# all_sprites.add(p1, p2, p3, p4, p5, p6, p7, p8, P1, P2, P3, P4, P5, P6, P7, P8)
#all_sprites.add(r1, r2, R1, R2, k1, K2, q1, Q1, b1, b2, B1, B2, kn1, kn2, Kn1, Kn2)
#all_sprites.add(g1, g2, s1, s2, l1, l2, kn1, Kn1, B1, b1, k1, K2, r2, R2)

running = True
white_turn = True

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
        if event.type == pygame.MOUSEBUTTONDOWN:  # click on piece
            mouse_pos = pygame.mouse.get_pos()  # get piece location
            found, key, tile = find_tile(
                board, mouse_pos, tile_flag)  # find corresponding tile
            if found and tile.piece.player == "WHITE" and white_turn:
                tile.piece.highlight(key, tile, dc)
                wait_button()   # wait for input for new location
                new_mouse_pos = pygame.mouse.get_pos()
                found, new_key, new_tile = find_tile(
                    board, new_mouse_pos, not tile_flag)
                if found:
                    changed, promotion, new_promo = tile.piece.move(new_tile)
                    if changed:
                        try:
                            running = checkmate("WHITE", "BLACK", k1)
                        except:
                            pass
                        white_turn = False
                        if promotion:
                            all_sprites.add(new_promo)

            elif found and tile.piece.player == "BLACK" and not white_turn:
                tile.piece.highlight(key, tile, dc)
                wait_button()   # wait for input for new location
                new_mouse_pos = pygame.mouse.get_pos()
                found, new_key, new_tile = find_tile(
                    board, new_mouse_pos, not tile_flag)
                if found:
                    changed, promotion, new_promo = tile.piece.move(new_tile)

                    if changed:
                        try:
                            running = checkmate("BLACK", "WHITE", K2)
                        except:
                            pass
                        white_turn = True
                        if promotion:
                            all_sprites.add(new_promo)


pygame.quit()
