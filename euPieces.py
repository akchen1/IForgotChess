import pygame
import numpy as np
pygame.init()
WIDTH, HEIGHT = pygame.display.get_surface().get_size()

COORD_ID = np.array([['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
            ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
            ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
            ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
            ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
            ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
            ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
            ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']], dtype=str)

class empty:
    def updatep(self, new_tile):
        pass

class pawn(pygame.sprite.Sprite):
    def __init__(self, tile, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pawnB.png').convert()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image.set_colorkey([255,255,255])
        else:
            self.image = pygame.image.load('pawnW.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
           # self.image.set_colorkey([0,0,0])

        self.rect = self.image.get_rect()
        self.tile = tile
        self.first_move = 0
        self.player = player
        
    def set_position(self):
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        self.rect.x = new_tile.x_pos
        self.rect.y = new_tile.y_pos
        self.tile.full = False
        self.tile.piece = empty()
        self.tile = new_tile
        self.tile.full = True
        self.tile.piece = self

    def move(self, key, tile, new_tile, dc):
        self.avaliable_moves = []
        self.current_location_key = key     
        i, j = np.where(COORD_ID == key)    # uses numpy array to find index of key
        #should make 2 functions for white and black i think
        #then handle moveset for each and can call them
        #only really relevant for pawns
        #doesn't handle promotions currently
        
        self.avaliable_moves.append(dc[COORD_ID[i+1,j].item(0)])
        if new_tile in self.avaliable_moves:
            self.updatep(new_tile)


        
        
    def movement(self): #not done
        if self.first_move == 0:
            x, y = self.tile.x_pos - WIDTH/4, self.tile.y_pos
            self.first_move = 1
            return(x, y)
        else:
            x, y = self.tile.x_pos - WIDTH/8, self.tile.y_pos
            return(x, y)