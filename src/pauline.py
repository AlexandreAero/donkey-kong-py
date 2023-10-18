import pygame

class Pauline:
    START_X = 220.0
    START_Y = 132.0

    def __init__(self, window):
        ''' 
        pygame.Surface -> None
        Instantiates Pauline in the game.
        '''
        self.sprites = []
        self.sprites.append(pygame.image.load('./art/pauline.png'))
        self.sprites.append(pygame.image.load('./art/pauline-help.png'))
        self.current_sprite_index = 0

        self.sprite = self.sprites[self.current_sprite_index]
        self.rect = self.sprite.get_rect()

        self.rect.x = Pauline.START_X
        self.rect.y = Pauline.START_Y

        self.sprite_timer = 0

        self.window = window

    def draw(self, delta_time):
        ''' 
        float -> None
        Draws Pauline on the screen.
        '''
        self.sprite_timer += delta_time
        if self.sprite_timer >= 10:
            self.current_sprite_index += 1
            if self.current_sprite_index >= len(self.sprites):
                self.current_sprite_index = 0
            self.sprite = self.sprites[self.current_sprite_index]
            self.sprite_timer = 0

        self.window.blit(self.sprite, self.rect)
