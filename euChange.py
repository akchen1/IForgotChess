import pygame
pygame.init()

class pawn(pygame.sprite.Sprite):
    def __init__(self, tile, width, height, offset):
        self.x = tile.x_pos
        self.y = tile.y_pos
        pygame.sprite.Sprite.__init__(self)
        display = pygame.display.get_surface
        self.image = pygame.image.load('pawn.png')
        self.image = pygame.transform.scale(self.image, (round(width/8), round(height/8)))
        self.rect = self.image.get_rect()
    def move(self, n_tile):
        self.tile.draw_tile()
        self.tile = n_tile
        display.blit(self.image,(n_tile.x_pos + 35, n_tile.y_pos + 20))