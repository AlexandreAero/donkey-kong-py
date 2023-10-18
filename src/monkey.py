import pygame

class Monkey:
    START_X = 70.0
    START_Y = 102.0

    def __init__(self, window):
        ''' 
        pygame.Surface -> None
        Instantiates the monkey in the game.
        '''
        self.sprites = []
        self.sprites.append(pygame.image.load('./art/singe-left.png'))
        self.sprites.append(pygame.image.load('./art/singe.png'))
        self.sprites.append(pygame.image.load('./art/singe-right.png'))
        self.current_sprite_index = 0

        self.sprite = self.sprites[self.current_sprite_index]
        self.rect = self.sprite.get_rect()

        self.rect.x = Monkey.START_X
        self.rect.y = Monkey.START_Y

        self.sprite_timer = 0

        self.window = window

    def draw(self, delta_time):
        ''' 
        float -> None
        Draws the monkey on the screen.
        '''
        self.sprite_timer += delta_time
        if self.sprite_timer >= 0.8:
            self.current_sprite_index += 1
            if self.current_sprite_index >= len(self.sprites):
                self.current_sprite_index = 0
            self.sprite_timer = 0

        self.sprite = self.sprites[self.current_sprite_index]
        self.window.blit(self.sprite, self.rect)
