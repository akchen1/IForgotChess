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
    ''' gold class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/gold-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/gold-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))

        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
      
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
    
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
 
        for k in range(-1,2):
            if player == "WHITE":
                r = range(0,2)
                b = 1
            else:
                r = range(1,3)
                b = -1
            for w in r:
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w) >= 0 and (j+k) >= 0:
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue
            try:
                trial_tile = dc[COORD_ID[i+b,j].item(0)]
                if (i+b) >= 0:
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
                
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()
   
class silver(pygame.sprite.Sprite):
    ''' silver class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/silver-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/silver-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_silver(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key

        for k in range(-1,2):
            if player == "BLACK":
                b = 1
            else:
                b = -1
            try:
                trial_tile = dc[COORD_ID[i+b,j+k].item(0)]
                if i+b > -1 and j+k > -1:
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
            try:
                b = b*(-1)
                for x in [-1, 1]:
                    trial_tile = dc[COORD_ID[i+b,j+x].item(0)]
                    if i+b > -1 and j+x > -1:
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
            except: 
                continue
                
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_silver(pygame.sprite.Sprite):
    ''' promoted silver class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_silver-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)        
        else:
            self.image = pygame.image.load('pieces/P_silver-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
        for k in range(-1,2):
            if player == "WHITE":
                r = range(0,2)
                b = 1
            else:
                r = range(1,3)
                b = -1
            for w in r:
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w > -1 and j+k > -1):
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue
            try:
                trial_tile = dc[COORD_ID[i+b,j].item(0)]
                if (i-1+w > -1 and j+k > -1):
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
                
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

class knight(pygame.sprite.Sprite):
    ''' knight class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/knight-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)  
        else:
            self.image = pygame.image.load('pieces/knight-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 

    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_knight(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)
        if player == "WHITE":
            x = 1
        else:
            x = -1 
        for k in range(0,2):
            if (i-2*x > -1 and j+1-2*k > -1):
                try:
                    trial_tile = dc[COORD_ID[i-2*x,j+1-2*k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_knight(pygame.sprite.Sprite):
    ''' promoted knight class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_knight-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/P_knight-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
        for k in range(-1,2):
            if player == "WHITE":
                r = range(0,2)
                b = 1
            else:
                r = range(1,3)
                b = -1
            for w in r:
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w > -1 and j+k > -1):
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue
            try:
                trial_tile = dc[COORD_ID[i+b,j].item(0)]
                if (i-1+w > -1 and j+k > -1):
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
        
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()


class lance(pygame.sprite.Sprite):
    ''' lance class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/lance-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/lance-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_lance(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)
        if player == "WHITE":
           for k in range(1,i[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,8-i[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue 
                
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_lance(pygame.sprite.Sprite):
    ''' Promoted lance class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_lance-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/P_lance-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
        
        for k in range(-1,2):
            if player == "WHITE":
                r = range(0,2)
                b = 1
            else:
                r = range(1,3)
                b = -1
            for w in r:
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w > -1 and j+k > -1):
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue
            try:
                trial_tile = dc[COORD_ID[i+b,j].item(0)]
                if (i-1+w > -1 and j+k > -1):
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
        
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

class bishop(pygame.sprite.Sprite):
    ''' bishop class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/bishop-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/bishop-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
       
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_bishop(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)
        
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key

        if j[0] >= i[0]: # down right
            for k in range(1,8-j[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,8-i[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # up-right diagonal
        if 7-j[0] <= i[0]:
            for k in range(1,8-j[0]):
                try:
                    trial_tile = dc[COORD_ID[i-k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,i[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # up-left diagonal
        if i[0] >= j[0]:
            for k in range(1,j[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,i[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # down-left
        if 7-j[0] >= i[0] + 1:
            for k in range(1,j[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i+k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,8-i[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue

    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_bishop(pygame.sprite.Sprite):
    ''' Promoted bishop class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_bishop-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/P_bishop-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)
        
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key

        if j[0] >= i[0]: # down right
            for k in range(1,8-j[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,8-i[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # up-right diagonal
        if 7-j[0] <= i[0]:
            for k in range(1,8-j[0]):
                try:
                    trial_tile = dc[COORD_ID[i-k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,i[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # up-left diagonal
        if i[0] >= j[0]:
            for k in range(1,j[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        else:
            for k in range(1,i[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i-k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        # down-left
        if 7-j[0] >= i[0] + 1:
            for k in range(1,j[0]+1):
                try:
                    trial_tile = dc[COORD_ID[i+k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue

        else:
            for k in range(1,8-i[0]):
                try:
                    trial_tile = dc[COORD_ID[i+k,j-k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player: 
                        break
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue
        
        for k in [-1,1]:
            try:
                trial_tile = dc[COORD_ID[i+k,j].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    
                elif trial_tile.piece.player == player: 
                    pass
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
            try:
                trial_tile = dc[COORD_ID[i,j+k].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    
                elif trial_tile.piece.player == player: 
                    pass
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
            
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

class rook(pygame.sprite.Sprite):
    ''' rook class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/rook-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/rook-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
    
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
    
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_rook(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)
       
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)

        # right
        for k in range(1,8-j[0]):
            try:
                trial_tile = dc[COORD_ID[i,j+k].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # left
        for k in range(1,j[0]+1):
            try:
                trial_tile = dc[COORD_ID[i,j-k].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # up
        for k in range(1,i[0]+1):
            try:
                trial_tile = dc[COORD_ID[i-k,j].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # down
        for k in range(1,8-i[0]):
            try:
                trial_tile = dc[COORD_ID[i+k,j].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue

    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_rook(pygame.sprite.Sprite):
    ''' Promoted rook class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_rook-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/P_rook-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
    
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
    
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return (True, False,False)
       
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)

        # right
        for k in range(1,8-j[0]):
            try:
                trial_tile = dc[COORD_ID[i,j+k].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # left
        for k in range(1,j[0]+1):
            try:
                trial_tile = dc[COORD_ID[i,j-k].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # up
        for k in range(1,i[0]+1):
            try:
                trial_tile = dc[COORD_ID[i-k,j].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        # down
        for k in range(1,8-i[0]):
            try:
                trial_tile = dc[COORD_ID[i+k,j].item(0)]
                if trial_tile.piece.player == enemy:
                    self.available_moves.append(trial_tile)
                    break
                elif trial_tile.piece.player == player: 
                    break
                else: 
                    self.available_moves.append(trial_tile)
            except: 
                continue
        pass
        
        for k in [-1,1]:
            for w in [-1,1]:
                try:
                    trial_tile = dc[COORD_ID[i+w,j+k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
                except: 
                    continue

    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

class pawn(pygame.sprite.Sprite):
    ''' pawn class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/pawn-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
            
        else:
            self.image = pygame.image.load('pieces/pawn-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
    
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
    
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
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
            promote = self.promotion()
            if promote:
                self.kill()
                self.tile.piece = P_pawn(self.tile, self.player, self.key)
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)
       
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)
        if player == "WHITE":
            x = 1
        else:
            x = -1 
        try:
            trial_tile = dc[COORD_ID[i-1*x,j].item(0)]
            if trial_tile.piece.player == enemy:
                self.available_moves.append(trial_tile)
            elif trial_tile.piece.player == player: 
                pass
            else: 
                self.available_moves.append(trial_tile)
        except: 
            pass
        
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''
        if self.player == "WHITE" and self.rect.y <= 80:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()
        elif self.player == "BLACK" and self.rect.y >= 483:
            promote = input("promote?(y/n) ").lower()
            if promote == "y":
                return(True)
            elif promote == "n":
                return(False)
            else:
                print("Invalid answer")
                return self.promotion()

class P_pawn(pygame.sprite.Sprite):
    ''' Promoted pawn class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/P_pawn-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/P_pawn-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing. '''
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
            self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)    # uses numpy array to find 2D-index of key
        for k in range(-1,2):
            if player == "WHITE":
                r = range(0,2)
                b = 1
            else:
                r = range(1,3)
                b = -1
            for w in r:
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w > -1 and j+k > -1):
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue
            try:
                trial_tile = dc[COORD_ID[i+b,j].item(0)]
                if (i-1+w > -1 and j+k > -1):
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile) 
                    elif trial_tile.piece.player == player: 
                        pass
                    else: 
                        self.available_moves.append(trial_tile)
            except: 
                continue
                
    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()

class king(pygame.sprite.Sprite):
    ''' king class as a pygame sprite '''
    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.key = key
        if self.player == "BLACK":
            self.image = pygame.image.load('pieces/king-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
            self.image = pygame.transform.flip(self.image, 0, 1)
        else:
            self.image = pygame.image.load('pieces/king-jpn.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(WIDTH/8),int(HEIGHT/8)))
        
        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        
    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self 
        
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
            self.tile.piece = self
            return (True, False,False)
        
    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key) 
        for k in range(-1,2):
            for w in range(0, 3):
                try:
                    trial_tile = dc[COORD_ID[i-1+w,j+k].item(0)]
                    if (i-1+w > -1 and j+k > -1):
                        if trial_tile.piece.player == enemy:
                            self.available_moves.append(trial_tile) 
                        elif trial_tile.piece.player == player: 
                            pass
                        else: 
                            self.available_moves.append(trial_tile)
                except: 
                    continue

    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            return (changed, promoted, new_piece)
        else:
            return (False, False, False)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves: 
            p = pygame.Surface((WIDTH/8,HEIGHT/8))  # size
            p.set_alpha(100)    # transparency 
            p.fill((153, 204, 255)) # colour
            display.blit(p,i.rect)
            pygame.display.update()