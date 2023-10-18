import pygame
import random

class Ladder:
    def __init__(self, height, x_min, x_max, broken, window):
        ''' 
        int, int, int, bool, pygame.Surface -> None
        The vertical position of the ladder is defined by its height, which is
        a height from the ground.
        The horizontal position is a randomly generated integer located
        between x_min and x_max.
        '''
        if broken:
            self.sprite = pygame.image.load('./art/echelle_broken.png')
        else:
            self.sprite = pygame.image.load('./art/echelle.png')

        self.rect = self.sprite.get_rect()

        self.rect.x = random.randint(x_min, x_max)
        self.rect.y = window.get_height() - height - self.rect.height

        self.window = window
        self.broken = broken

    def draw(self):
        ''' 
        None -> None
        Draws the ladder on the screen.
        '''
        self.window.blit(self.sprite, self.rect)
