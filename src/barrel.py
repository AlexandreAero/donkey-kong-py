import pygame
import random

class Barrel:
    START_X = 150.0
    START_Y = 178.0
    SPEED_MIN = 150.0
    SPEED_MAX = 220.0
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1

    def __init__(self, window, ladders):
        ''' 
        pygame.Surface, [Ladder] -> None
        Instantiates a barrel in the game.
        '''
        self.sprites = []
        self.sprites.append(pygame.image.load('./art/tonneau.png'))
        self.sprites.append(pygame.image.load('./art/tonneau-rot.png'))
        self.current_sprite_index = 0

        self.sprite = self.sprites[self.current_sprite_index]
        self.rect = self.sprite.get_rect()

        self.rect.x = Barrel.START_X
        self.rect.y = Barrel.START_Y
        self.speed = random.randrange(Barrel.SPEED_MIN, Barrel.SPEED_MAX)
        self.direction = Barrel.LEFT_TO_RIGHT

        self.window = window
        self.ladders = ladders

    def roll(self, delta_time):
        ''' 
        float -> None
        Moves the barrel until it no longer collides with a pillar or ladder.
        '''
        match self.direction:
            case Barrel.LEFT_TO_RIGHT:
                self.rect.x += self.speed * delta_time
            case Barrel.RIGHT_TO_LEFT:
                self.rect.x -= self.speed * delta_time
            case _:
                pass

        # Check for colision with a ladder
        col_index = self.rect.collidelist(self.ladders)

        if col_index >= 0 and not self.ladders[col_index].broken:
            self.current_sprite_index = 1
            self.rect.y += self.speed * delta_time
            self.rect.x = self.ladders[col_index].rect.x
            self.direction = self.get_random_direction()
        else:
            self.current_sprite_index = 0

    def reset(self):
        '''
        None -> None
        Puts the barrel at the start.
        '''
        self.rect.x = Barrel.START_X
        self.rect.y = Barrel.START_Y
        self.direction = Barrel.LEFT_TO_RIGHT
        self.speed = random.randrange(Barrel.SPEED_MIN, Barrel.SPEED_MAX)

    def get_random_direction(self):
        ''' 
        None -> int
        Returns a random direction.
        '''
        return random.randint(Barrel.LEFT_TO_RIGHT,
                              Barrel.RIGHT_TO_LEFT)

    def draw(self):
        ''' 
        None -> None
        Draws the barrel on the screen.
        '''
        self.sprite = self.sprites[self.current_sprite_index]
        self.window.blit(self.sprite, self.rect)
