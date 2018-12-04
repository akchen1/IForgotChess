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

random_pawn = [EUP.pawn, JPN.pawn, EUP.pawn, EUP.pawn, JPN.pawn, JPN.gold,EUP.checker, JPN.silver]
random_exclusive = [EUP.bishop, EUP.knight, EUP.rook, JPN.knight, JPN.bishop,
                    JPN.lance, EUP.queen, JPN.gold, JPN.rook]
random_king = [EUP.king, JPN.king]


class tile:
    ''' tile class stores information such as its colour, position and whether the tile is empty.
    draw_tile draws a tile onto the display'''
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
    ''' stores tiles into a board class where the tile label ('A1') is stored
    as a key to a dictionary with its subsequent tile class as the value of the key'''
    def __init__(self):
        self.dc = {}    # dictionary to store tiles
        self.label = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                      ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                      ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                      ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                      ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                      ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                      ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                      ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']]
        self.make_board()

    def give_dictionary(self):
        ''' returns created dictionary'''
        return self.dc

    def make_board(self):
        ''' make_board() creates a white tile for odd indexes and a black tile for
        even indexes.'''
        counter = 1 # used to determine even or odd
        initalx = 0 # intial x (left) coordinate for first tile
        initaly = 0 # intial y (top) coordinate for first tile
        for x in self.label:    # for each row
            for term in x:  # for each column in row
                if counter % 2 != 0:    # if odd create white tile
                    self.dc[term] = tile(WHITE, initalx, initaly)   # make tile
                    initalx += WIDTH/8  # increase left coordinate by width of tile
                    counter += 1    # increase counter by 1
                else:   # if even create black tile
                    self.dc[term] = tile(BLACK, initalx, initaly)   # make tile
                    initalx += WIDTH/8  # increase left coordinate by width of tile
                    counter += 1    # increase counter by 1

            initaly += HEIGHT/8 # new row, move down by height of tile
            initalx = 0 # reset x postion to beginning of row
            counter = counter - 1   # change counter to alternate between black/white

    def draw_board(self):
        ''' uses draw_tile() function to draw tiles (stored in dictionayr) onto the board'''
        for _, tile in self.dc.items():
            tile.draw_tile()

def wait_button():
    ''' wait_button() clears past events and waits for user to press
    mouse button again. If button is pressed, wait_button() will end
    and game loop will continue '''
    pygame.event.clear()    # clear all events
    while True:
        pygame.time.delay(100)  # wait for user
        for event in pygame.event.get():    
            if event.type == pygame.MOUSEBUTTONDOWN:    # if mouse button is pressed
                return(True)    # return true

def find_tile(board, mouse_pos, tile_flag):
    ''' find tile will find the corresponding tile to mouse_pos, if it's the first
    iteration, the tile_flag will be on so that if an empty space is clicked, it will
    stop the loop and allow player to try again '''
    for key, tile in board.dc.items():  # iterate through tiles
        # if y position corresponds to a tile
        if mouse_pos[1] > tile.y_pos and mouse_pos[1] < (tile.y_pos + HEIGHT/8):
            # if x position corresponds to a tile
            if mouse_pos[0] > tile.x_pos and mouse_pos[0] < (tile.x_pos + WIDTH/8):
                # if tile is empty
                if tile.piece.player == None and tile_flag:
                    return(False, None, None)
                # if tile found return key and tile
                return(True, key, tile)
    # if no tile is found
    return(False, None, None)

def checkmate(player, enemy, king):
    ''' checkmate() iterates through all sprites in sprite group corresponding to
    players pieces except for players king and calles the moveset function 
    corresponding to each pieces class. It then checks if any of the possible
    moves corresponds to the enemy's kings position. If true, "check" will
    be outputed. Additinally, checkmate() checks if the the enemy king is alive.
    if dead, game loop will end. '''
    for x in all_sprites:   # loop through all sprites (pieces)
        if x.player == player:  # if piece found is same as player piece
            if x != new_tile.piece: # if piece hasn't moved
                x.moveset(player, enemy, x.key, dc) # find moveset using old coordinates
            else:   # if piece moved
                x.moveset(player, enemy, new_key, dc)   # find moveset using new coordinates
            for y in x.available_moves: # loop through all available moves
                # if any of the available moves for a piece is on a king
                if int(y.x_pos) == king.rect.x and int(y.y_pos) == king.rect.y:
                    print("CHECK")  # print check

    if not king.alive():    # if king is killed
        print(enemy,"LOSES")   # print you lose
        return(False)   # return running is false (breaks game loop)
    return(True)    # else return true (king is alive)

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
            k1 = EUP.king(board.dc["A5"], "BLACK", "A5")
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
            K2 = EUP.king(board.dc["H5"], "WHITE", "H5")
            all_sprites.add(K2)
            i += 1
            continue
        x = random.choice(random_exclusive)(board.dc[key], "WHITE", key)
        all_sprites.add(x)
        i += 1
    return(k1,K2)


tile_flag = 1
fps = 30
clock = pygame.time.Clock()
board = board()  # initialize board
dc = board.give_dictionary()
all_sprites = pygame.sprite.Group()
k1,K2 = make_pieces()

running = True  # run game
white_turn = True   # white goes first

if __name__ == "__main__":
    while running:
        clock.tick(fps) # set constant fps
        board.draw_board()  # draw board
        all_sprites.update()    # update sprite
        all_sprites.draw(display)   # draw sprite
        pygame.display.update() # update display
        pygame.display.flip()   # update display

        for event in pygame.event.get():    # if close button is hit, close window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # if player clicked on something
                mouse_pos = pygame.mouse.get_pos()  # get the location of the mouse
                found, key, tile = find_tile(
                    board, mouse_pos, tile_flag)  # see if player clicked on a tile and if there is a piece on it

                # if a tile and piece is found, check the player is 'white' and if it's white turn
                if found and tile.piece.player == "WHITE" and white_turn:
                    tile.piece.highlight(key, tile, dc) # highlight the available moves corresponding to the piece
                    wait_button()   # wait for input for new location to move to
                    new_mouse_pos = pygame.mouse.get_pos()  # obtain location of new location
                    found, new_key, new_tile = find_tile(
                        board, new_mouse_pos, not tile_flag)    # if new location is tile, found will be true
                    if found:   # if tile is found
                        # move piece to new location and check if it can be promoted
                        changed, promotion, new_promo = tile.piece.move(new_tile)
                        if changed: # if the move is successful
                            try:    # see if enemy king is in check
                                running = checkmate("WHITE", "BLACK", k1)
                            except:
                                pass
                            white_turn = False  # switch to black turn
                            if promotion:   # if piece qualifies for promotion
                                all_sprites.add(new_promo)  # add new promoted piece to sprite group

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
    pass
