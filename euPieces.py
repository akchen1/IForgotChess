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


class pawn(pygame.sprite.Sprite):
    ''' pawn class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.player = player    # colour (black/white)
        self.key = key  # tile key (eg "A1") piece is on
        if self.player == "BLACK":  # load black image
            self.image = pygame.image.load('pieces/pawnB.png').convert_alpha()
        else:   # load white image
            self.image = pygame.image.load('pieces/pawnW.png').convert_alpha()
        # scale image to match tile size
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

        self.rect = self.image.get_rect()   # collision box
        self.tile = tile    # tile data
        self.available_moves = []   # list of availabe moves
        self.first_move = True
        self.set_position()  # set initial position

    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True   # set tile to full
        self.tile.piece = self  # set tile piece class to self

    def updatep(self, new_tile):
        ''' updatep updates the piece. This involves their movement, killing,
        and promotion. '''
        if new_tile.full:   # check tile is occupied
            new_tile.piece.kill()   # if tile is occupied kill it
        # if player clicked on same tile do nothing
        if self.rect.x == new_tile.x_pos and self.rect.y == new_tile.y_pos:
            return(False, False, False)
        else:
            # set position to new tile position
            self.rect.x = new_tile.x_pos
            self.rect.y = new_tile.y_pos
            # set current tile to empty
            self.tile.full = False
            self.tile.piece = empty()
            # set current tile as new tile and set new tile to full
            self.tile = new_tile
            self.tile.full = True
            # check if piece qualifies for promotion
            promoted, new_piece = self.promotion()
            if promoted:
                self.kill()  # kill the current piece
                # create new piece
                command = '{}(self.tile, self.player, self.key)'
                command = command.format(new_piece)
                self.tile.piece = eval(command)
                # return piece moved (True), piece is promoted (True),
                # identifier to piece
                return(True, True, self.tile.piece)
            else:   # not promoted
                self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        # uses numpy array to find 2D-index of key
        i, j = np.where(COORD_ID == key)

        for k in range(1, 3):    # killing moves
            p = 1
            if player == "WHITE":
                p = p * (-1)    # move up
            try:
                # possible tile
                trial_tile = dc[COORD_ID[i + p, j + (-1)**k].item(0)]
                if trial_tile.piece.player == enemy:    # if tile is occupied by enemy
                    self.available_moves.append(trial_tile)  # append to list
            except:
                continue
        # first move test
        if self.first_move:
            for k in range(1, 3):
                p = k
                if player == "WHITE":
                    p = -k  # move up
                try:
                    # possible tile for it to move
                    trial_tile = dc[COORD_ID[i + p, j].item(0)]
                    if trial_tile.full != True:         # only works for pawn since checks if space above full
                        self.available_moves.append(trial_tile)
                    else:
                        break
                except:
                    continue
        else:   # not first move
            p = 1
            if player == "WHITE":
                p = p * (-1)
            try:
                trial_tile = dc[COORD_ID[i + p, j].item(0)]
                if trial_tile.full != True:         # only works for pawn since checks if space above full
                    self.available_moves.append(trial_tile)
            except:
                pass

    def move(self, new_tile):
        ''' move function checks if tile selected is in available moves
        then calles updatep function '''
        if new_tile in self.available_moves:
            changed, promoted, new_piece = self.updatep(new_tile)
            self.first_move = False  # no longer pawns first move
            return (changed, promoted, new_piece)
        else:
            return (False, False, None)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves:
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)  # draw image
            pygame.display.update()  # update screen

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, player will be asked if they want to promote and to what
        class. Invalid input will cause function to recurse '''

        allowed_promotions = ['queen', 'rook', 'bishop', 'knight']

        if self.player == "WHITE" and self.rect.y == 0:  # white promotion
            promote = input("Promote pawn? (y/n): ").lower()    # player input
            if promote == 'y':  # yes to promotion
                while promote == 'y':
                    new_class = input(
                        "select class (queen, rook, bishop, knight): ").lower()
                    if new_class in allowed_promotions:  # check if player input is allowed
                        return(True, new_class)
                    else:
                        print("Invalid class")
                        return self.promotion()
            elif promote == 'n':    # no to promotion
                return(False, None)
            else:   # invalid player input
                print("Invalid answer")
                return self.promotion()

        elif self.player == "BLACK" and self.rect.y == 563:  # black promotion
            promote = input("Promote pawn? (y/n): ").lower()    # player input
            if promote == 'y':  # yes to promotion
                while promote == 'y':
                    new_class = input(
                        "select class (queen, rook, bishop, knight): ").lower()
                    if new_class in allowed_promotions:  # check if player input is valid
                        return(True, new_class)
                    else:   # invalid player input
                        print("Invalid class")
                        return self.promotion()
            elif promote == 'n':    # no to promotion
                return(False, None)
            else:   # invalid player input
                print("Invalid answer")
                return self.promotion()

        return(False, None)  # piece does not qualify for promotion


class bishop(pygame.sprite.Sprite):
    ''' bishop class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":  # load bishop images
            self.image = pygame.image.load(
                'pieces/bishopblack.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/bishopwhite.png').convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

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
        ''' updates piece. This involves killing and movement.
        Same as updatep in class pawn without the promotion aspect'''
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        # uses numpy array to find 2D-index of key
        i, j = np.where(COORD_ID == key)

        # move set for down right. allowed tiles depend on location on board
        if j[0] >= i[0]:
            for k in range(1, 8 - j[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j + k].item(0)]
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
            for k in range(1, 8 - i[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j + k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player:
                        break
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue
        # move set for up-right diagonal. allowed tiles depend on location on
        # board
        if 7 - j[0] <= i[0]:
            for k in range(1, 8 - j[0]):
                try:
                    trial_tile = dc[COORD_ID[i - k, j + k].item(0)]
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
            for k in range(1, i[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j + k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player:
                        break
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue
        # move set for up-left diagonal. allowed tiles depend on location
        if i[0] >= j[0]:
            for k in range(1, j[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j - k].item(0)]
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
            for k in range(1, i[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j - k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                        break
                    elif trial_tile.piece.player == player:
                        break
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue
        # move set for down-left. allowed tiles depend on location
        if 7 - j[0] >= i[0] + 1:
            for k in range(1, j[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i + k, j - k].item(0)]
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
            for k in range(1, 8 - i[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j - k].item(0)]
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
            return (False, False, None)

    def highlight(self, key, tile, dc):
        ''' highlights possible moves player can choose from, using
        moveset '''
        self.key = key
        if tile.piece.player == "BLACK":
            self.moveset("BLACK", "WHITE", key, dc)
        else:
            self.moveset("WHITE", "BLACK", key, dc)
        for i in self.available_moves:
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()


class rook(pygame.sprite.Sprite):
    ''' rook class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/rookblack.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/rookwhite.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

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
        ''' updates piece. This involves killing and movement.
        Same as updatep in class pawn without the promotion aspect'''
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)

        # right
        for k in range(1, 8 - j[0]):
            try:
                trial_tile = dc[COORD_ID[i, j + k].item(0)]
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
        for k in range(1, j[0] + 1):
            try:
                trial_tile = dc[COORD_ID[i, j - k].item(0)]
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
        for k in range(1, i[0] + 1):
            try:
                trial_tile = dc[COORD_ID[i - k, j].item(0)]
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
        for k in range(1, 8 - i[0]):
            try:
                trial_tile = dc[COORD_ID[i + k, j].item(0)]
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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()


class queen(pygame.sprite.Sprite):
    ''' queen class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/queenblack.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/queenwhite.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

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
        ''' updates piece. This involves killing and movement.
        Same as updatep in class pawn without the promotion aspect'''
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        # uses numpy array to find 2D-index of key
        i, j = np.where(COORD_ID == key)

        if j[0] >= i[0]:  # down right
            for k in range(1, 8 - j[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j + k].item(0)]
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
            for k in range(1, 8 - i[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j + k].item(0)]
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
        if 7 - j[0] <= i[0]:
            for k in range(1, 8 - j[0]):
                try:
                    trial_tile = dc[COORD_ID[i - k, j + k].item(0)]
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
            for k in range(1, i[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j + k].item(0)]
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
            for k in range(1, j[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j - k].item(0)]
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
            for k in range(1, i[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i - k, j - k].item(0)]
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
        if 7 - j[0] >= i[0] + 1:
            for k in range(1, j[0] + 1):
                try:
                    trial_tile = dc[COORD_ID[i + k, j - k].item(0)]
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
        else:
            for k in range(1, 8 - i[0]):
                try:
                    trial_tile = dc[COORD_ID[i + k, j - k].item(0)]
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
        # right
        for k in range(1, 8 - j[0]):
            try:
                trial_tile = dc[COORD_ID[i, j + k].item(0)]
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
        for k in range(1, j[0] + 1):
            try:
                trial_tile = dc[COORD_ID[i, j - k].item(0)]
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
        for k in range(1, i[0] + 1):
            try:
                trial_tile = dc[COORD_ID[i - k, j].item(0)]
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
        for k in range(1, 8 - i[0]):
            try:
                trial_tile = dc[COORD_ID[i + k, j].item(0)]
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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()


class knight(pygame.sprite.Sprite):
    ''' knight class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.player = player
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/knightblack.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/knightwhite.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

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
        ''' updates piece. This involves killing and movement.
        Same as updatep in class pawn without the promotion aspect'''
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)

        for k in range(0, 2):
            if (i - 2 > -1 and j + 1 - 2 * k > -1):
                try:
                    trial_tile = dc[COORD_ID[i - 2, j + 1 - 2 * k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                    elif trial_tile.piece.player == player:
                        pass
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue

        for k in range(0, 2):
            if (i + 2 > -1 and j + 1 - 2 * k > -1):
                try:
                    trial_tile = dc[COORD_ID[i + 2, j + 1 - 2 * k].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                    elif trial_tile.piece.player == player:
                        pass
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue

        for k in range(0, 2):
            if (i + 1 - 2 * k > -1 and j - 2 > -1):
                try:
                    trial_tile = dc[COORD_ID[i + 1 - 2 * k, j - 2].item(0)]
                    if trial_tile.piece.player == enemy:
                        self.available_moves.append(trial_tile)
                    elif trial_tile.piece.player == player:
                        pass
                    else:
                        self.available_moves.append(trial_tile)
                except:
                    continue

        for k in range(0, 2):
            if (i + 1 - 2 * k > -1 and j + 2 > -1):
                try:
                    trial_tile = dc[COORD_ID[i + 1 - 2 * k, j + 2].item(0)]
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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()


class king(pygame.sprite.Sprite):
    ''' knight class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.key = key
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/kingblack.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/kingwhite.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.set_position()
        pass

    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self
        pass

    def updatep(self, new_tile):
        ''' updates piece. This involves killing and movement.
        Same as updatep in class pawn without the promotion aspect'''
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)
        for k in range(-1, 2):
            for w in range(0, 3):
                try:
                    trial_tile = dc[COORD_ID[i - 1 + w, j + k].item(0)]
                    if (i - 1 + w > -1 and j + k > -1):
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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()


class checker(pygame.sprite.Sprite):
    ''' checker class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.key = key
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/blackchecker.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/whitechecker.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.kill_set = {}
        self.set_position()

    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self

    def updatep(self, new_tile):
        ''' updates piece. This involves killing and movement and promotion '''
        if new_tile in self.kill_set:
            self.rect.x = new_tile.x_pos
            self.rect.y = new_tile.y_pos
            self.kill_set[new_tile].piece.kill()
            self.kill_set[new_tile].full = False
            self.kill_set[new_tile].piece = empty()
            self.tile.full = False
            self.tile.piece = empty()
            self.tile = new_tile
            self.tile.full = True
            self.tile.piece = self
            promoted, new_piece = self.promotion()
            if promoted:
                self.kill()
                command = '{}(self.tile, self.player, self.key)'
                command = command.format(new_piece)
                self.tile.piece = eval(command)
                #self.tile.piece = queen(self.tile, "WHITE")
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)
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
            promoted, new_piece = self.promotion()
            if promoted:
                self.kill()
                command = '{}(self.tile, self.player, self.key)'
                command = command.format(new_piece)
                self.tile.piece = eval(command)
                #self.tile.piece = queen(self.tile, "WHITE")
                return(True, True, self.tile.piece)
            else:
                self.tile.piece = self
            return(True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. Adititionally, if the checker is able to jump over a piece
        the move will be appended into kill set '''
        self.available_moves = []
        p = 1
        i, j = np.where(COORD_ID == key)
        if player == "WHITE":
            p = -1

        try:
            if (i + p) >= 0 and (j + 1) >= 0:
                trial_tile = dc[COORD_ID[i + p, j + 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i + p * 2) >= 0 and (j + 2) >= 0 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i + p * 2, j + 2].item(0)].full != True):
                self.available_moves.append(
                    dc[COORD_ID[i + p * 2, j + 2].item(0)])
                self.kill_set[
                    dc[COORD_ID[i + p * 2, j + 2].item(0)]] = trial_tile
        except:
            None

        try:
            if (i + p) >= 0 and (j - 1) >= 0:
                trial_tile = dc[COORD_ID[i + p, j - 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i + p * 2) >= 0 and (j - 2) >= 0 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i + p * 2, j - 2].item(0)].full != True):
                self.available_moves.append(
                    dc[COORD_ID[i + p * 2, j - 2].item(0)])
                self.kill_set[
                    dc[COORD_ID[i + p * 2, j - 2].item(0)]] = trial_tile
        except:
            None

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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()

    def promotion(self):
        ''' checks if the piece is a specified location on the board.
        if it is, piece will promote '''

        if self.player == "WHITE" and self.rect.y == 0:
            return(True, "kingchecker")
        elif self.player == "BLACK" and self.rect.y == 563:
            return(True, "kingchecker")
        else:
            return(False, False)


class kingchecker(pygame.sprite.Sprite):
    ''' king checker class as a pygame sprite '''

    def __init__(self, tile, player, key):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.key = key
        if self.player == "BLACK":
            self.image = pygame.image.load(
                'pieces/blackcheckerking.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                'pieces/whitecheckerking.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (int(WIDTH / 8), int(HEIGHT / 8)))

        self.rect = self.image.get_rect()
        self.tile = tile
        self.available_moves = []
        self.kill_set = {}
        self.set_position()

    def set_position(self):
        ''' sets original position for piece when game starts '''
        (self.rect.left, self.rect.top) = (self.tile.x_pos, self.tile.y_pos)
        self.tile.full = True
        self.tile.piece = self

    def updatep(self, new_tile):
        ''' updates piece. This involves killing and movement and promotion '''
        if new_tile in self.kill_set:
            self.rect.x = new_tile.x_pos
            self.rect.y = new_tile.y_pos
            self.kill_set[new_tile].piece.kill()
            self.kill_set[new_tile].full = False
            self.kill_set[new_tile].piece = empty()
            self.tile.full = False
            self.tile.piece = empty()
            self.tile = new_tile
            self.tile.full = True
            self.tile.piece = self
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
            return (True, False, False)

    def moveset(self, player, enemy, key, dc):
        ''' finds possible moves for piece and appends it to a list. Finds a possible
        tile it can move to and if it satisfies all the conditions it will be added
        to the moveset. Adititionally, if the checker is able to jump over a piece
        the move will be appended into kill set '''
        self.available_moves = []
        i, j = np.where(COORD_ID == key)
        try:  # downright
            if (i + 1) > -1 and (j + 1) > -1:
                trial_tile = dc[COORD_ID[i + 1, j + 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i + 2) > -1 and (j + 2) > -1 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i + 2, j + 2].item(0)].full != True):
                self.available_moves.append(dc[COORD_ID[i + 2, j + 2].item(0)])
                self.kill_set[dc[COORD_ID[i + 2, j + 2].item(0)]] = trial_tile
        except:
            None

        try:  # downleft
            if (i + 1) > -1 and (j - 1) > -1:
                trial_tile = dc[COORD_ID[i + 1, j - 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i + 2) > -1 and (j - 2) > -1 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i + 2, j - 2].item(0)].full != True):
                self.available_moves.append(dc[COORD_ID[i + 2, j - 2].item(0)])
                self.kill_set[dc[COORD_ID[i + 2, j - 2].item(0)]] = trial_tile
        except:
            None

        try:  # upright
            if (i - 1) > -1 and (j + 1) > -1:
                trial_tile = dc[COORD_ID[i - 1, j + 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i - 2) > -1 and (j + 2) > -1 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i - 2, j + 2].item(0)].full != True):
                self.available_moves.append(dc[COORD_ID[i - 2, j + 2].item(0)])
                self.kill_set[dc[COORD_ID[i - 2, j + 2].item(0)]] = trial_tile
        except:
            None

        try:  # upleft
            if (i - 1) > -1 and (j - 1) > -1:
                trial_tile = dc[COORD_ID[i - 1, j - 1].item(0)]
            if not trial_tile.full:
                self.available_moves.append(trial_tile)
            elif (i - 2) > -1 and (j - 2) > -1 and trial_tile.piece.player == enemy and (
                    dc[COORD_ID[i - 2, j - 2].item(0)].full != True):
                self.available_moves.append(dc[COORD_ID[i - 2, j - 2].item(0)])
                self.kill_set[dc[COORD_ID[i - 2, j - 2].item(0)]] = trial_tile
        except:
            None

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
            p = pygame.Surface((WIDTH / 8, HEIGHT / 8))  # size
            p.set_alpha(100)    # transparency
            p.fill((153, 204, 255))  # colour
            display.blit(p, i.rect)
            pygame.display.update()
