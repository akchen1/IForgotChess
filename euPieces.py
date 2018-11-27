import pygame
pygame.init()

class pawn:
    def __init__(self, tile):
        display = pygame.display.get_surface()
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
