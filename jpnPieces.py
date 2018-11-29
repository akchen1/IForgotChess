import pygame
import numpy as np
pygame.init()
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
display = pygame.display.get_surface()

COORD_ID = np.array([['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
                     ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'],
                     ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'],
                     ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'],
                     ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8'],
                     ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8'],
                     ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'],
                     ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']], dtype=str)
# COORD_ID is just a special numpy array that makes working in 2D easier

class empty:
    def __init__(self):
        self.full = False
        self.player = None
    def updatep(self, new_tile):
        pass
    def move(self, a, b, c, d):
        pass
        
class gold(pygame.sprite.Sprite):
    def __init__(self, tile, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/gold.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)

          #  self.image.set_colorkey([255,255,255])
            
        else:
            self.image = pygame.image.load('pieces/gold.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
         #   self.image = pygame.transform.flip(self.image, 0, 1)
           # self.image.set_colorkey([0,0,0])
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.first_move = True
        self.player = player
        self.set_position()
        pass
        
    def set_position(self):
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        pass
        
    def updatep(self, new_tile):
        
        if new_tile.full:
            new_tile.piece.kill()
        if self.rect.x == new_tile.x_pos and self.rect.y == new_tile.y_pos:
            return(False, False, False)
        else:
            self.rect.x = new_tile.x_pos
            self.rect.y = new_tile.y_pos
            self.tile.full = False
            self.tile.piece = empty()
            self.tile = new_tile
            self.tile.full = True
            promoted, new_piece = self.promotion()
            if promoted:
                self.kill()
                command = '{}(self.tile, self.player)'
                command = command.format(new_piece)
                self.tile.piece = eval(command)
                #self.tile.piece = queen(self.tile, "WHITE")
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)
        pass

    def moveset(self, player, enemy, key, dc):
        """ reciprocal of white movement """
        """ moves down """
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
        # kill testing
        for k in range(1,3):
            p = 1
            if player == "WHITE":
                p = p * (-1)
            try:
                trial_tile = dc[COORD_ID[i+p,j+(-1)**k].item(0)]  
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
            except:
                continue
        # first move test
        if self.first_move:
            for k in range(1,3):
                p = k
                if player == "WHITE":
                    p = -k
                trial_tile = dc[COORD_ID[i+p,j].item(0)]    # possible tile for it to move
                if trial_tile.full != True:         # only works for pawn since checks if space above full
                    self.available_moves.append(trial_tile)
                else:
                    break
        else:
            p = 1
            if player == "WHITE":
                p = p*(-1)
            trial_tile = dc[COORD_ID[i+p,j].item(0)]   
            if trial_tile.full != True:         # only works for pawn since checks if space above full
                    self.available_moves.append(trial_tile)
        pass

    def move(self, new_tile):
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            self.first_move = False 
            
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)
        pass

    def highlight(self, key, tile, dc):
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            #p = pygame.draw.rect(display, (230, 90, 40, 50), i.rect)
            pygame.display.update()
        pass
    def promotion(self):
        if self.player == "WHITE" and self.rect.y == 0:
            new_class = input("select class: ")
            return(True, new_class)
        elif self.player == "BLACK" and self.rect.y == 563:
            new_class = input("select class: ")
            return(True, new_class)
        else:
            return(False,False)
    pass