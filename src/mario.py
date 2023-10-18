import pygame

class Mario:
    START_X = 120.0
    START_Y = 660.0
    MAX_HEALTH = 3
    SPEED = 150.0
    TEXT_COLOR = (220, 70, 100)

    JUMP_HEIGHT = 9.0
    GRAVITY = 200.0

    def __init__(self, window, ladders, barrels, pillars):
        '''
        pygame.display, [Ladder], [Barrel], [Pillar] -> None
        '''
        self.mario_sprites = []
        self.mario_sprites.append(pygame.image.load('./art/mario-left.png'))
        self.mario_sprites.append(pygame.image.load('./art/mario-right.png'))
        self.mario_sprites.append(pygame.image.load('./art/mario-climb.png'))
        self.mario_sprites.append(pygame.image.load('./art/mario-dead.png'))
        self.current_mario_sprite_index = 0

        self.hammer_sprites = []
        self.hammer_sprites.append(pygame.image.load('./art/hammer.png'))
        self.hammer_sprites.append(
            pygame.image.load('./art/hammer-rot-right.png'))
        self.hammer_sprites.append(
            pygame.image.load('./art/hammer-rot-left.png'))
        self.current_hammer_sprite_index = 0

        self.sprite = self.mario_sprites[self.current_mario_sprite_index]
        self.rect = self.sprite.get_rect()

        self.score = 0
        self.y_speed = 1
        self.speed = Mario.SPEED
        self.life = Mario.MAX_HEALTH
        self.rect.x = Mario.START_X
        self.rect.y = Mario.START_Y

        self.window = window
        self.ladders = ladders
        self.barrels = barrels
        self.pillars = pillars

        self.grounded = True
        self.climbing = False
        self.jumping = False

        self.sounds = {
            'walk': pygame.mixer.Sound('./art/walking-sound.mp3'),
            'jump': pygame.mixer.Sound('./art/jumping-sound.mp3'),
            'dead': pygame.mixer.Sound('./art/dying-sound.mp3'),
            'game-over': pygame.mixer.Sound('./art/game-over-sound.mp3'),
            'win': pygame.mixer.Sound('./art/win-sound.mp3'),
            'hammer-use': pygame.mixer.Sound('./art/hammer-use-sound.mp3')
        }

        # We grab the channels of every different sounds
        self.channels = [self.sounds[key].play() for key in self.sounds]

        self.font = pygame.font.Font('./art/arcade_font.TTF', 16)

    def reset_position(self):
        ''' 
        None -> None
        Resets the player position.
        '''
        self.current_mario_sprite_index = 1
        self.rect.x = Mario.START_X
        self.rect.y = Mario.START_Y
        self.sounds['win'].play()

    def loose_life(self):
        ''' 
        None -> None
        Removes a life from the player.
        '''
        if self.life > 0:
            self.life -= 1
            self.current_mario_sprite_index = 3
            self.sounds["dead"].play()

    def draw_text(self, text, color, pos):
        ''' 
        str, tuple, tuple -> None
        Draws text on the screen with a color and position.
        '''
        if not pygame.font.get_init():
            pygame.font.init()

        text_surface = self.font.render(text, False, color)
        self.window.blit(text_surface, pos)

    def update_gui(self):
        '''
        None -> None
        Updates the graphic interface linked to mario data.
        data.
        '''
        self.draw_text(f'Life: {self.life}', Mario.TEXT_COLOR, (620, 50))
        self.draw_text(f'Score {self.score}', Mario.TEXT_COLOR, (620, 80))

    def game_over(self):
        '''
        None -> None
        Draws a text with the game over on the screen.
        '''
        text = f'Game over! Your score is: {self.score} points.'
        self.draw_text(text, (255, 255, 255), (150, 400))
        self.sounds['game-over'].play()
        pygame.display.flip()
        pygame.time.wait(2000)

        self.score = 0
        self.life = Mario.MAX_HEALTH

    def jump(self):
        ''' 
        None -> None
        Makes a jump.
        '''
        if self.grounded:
            self.y_speed = -Mario.JUMP_HEIGHT
            self.grounded = False
            self.sounds['jump'].play()
            self.jumping = True
            print(' fu ')

        self.rect.y += self.y_speed
        self.y_speed += Mario.GRAVITY

        if self.rect.y >= Mario.START_Y:
            self.rect.y = Mario.START_Y
            self.y_speed = 0.0
            self.grounded = True
            self.jumping = False

    def climb_ladder(self, delta_time):
        ''' 
        float -> None
        Instruction that allows the player to climb a ladder.
        '''
        col_index = self.rect.collidelist(self.ladders)
        self.climbing = (col_index >= 0
                         and not self.ladders[col_index].broken)

        if self.climbing:
            self.rect.x = self.ladders[col_index].rect.x
            self.rect.y -= self.speed * delta_time
            self.current_mario_sprite_index = 2

    def climb_down_ladder(self, delta_time):
        ''' 
        float -> None
        Instruction that allows the player to climb down a ladder.
        '''
        col_index = self.rect.collidelist(self.ladders)
        self.climbing = (col_index >= 0
                         and not self.ladders[col_index].broken)

        if self.climbing:
            self.rect.x = self.ladders[col_index].rect.x
            self.rect.y += self.speed * delta_time
            self.current_mario_sprite_index = 2

    def move_right(self, delta_time):
        ''' 
        float -> None
        Moves the player to the right.
        '''
        if not self.channels[0].get_busy():
            self.sounds['walk'].play()

        if not self.climbing:
            self.rect.x += self.speed * delta_time
            self.current_mario_sprite_index = 1

    def move_left(self, delta_time):
        ''' 
        float -> None
        Moves the player to the left.
        '''
        if not self.channels[0].get_busy():
            self.sounds['walk'].play()

        if not self.climbing:
            self.rect.x -= self.speed * delta_time
            self.current_mario_sprite_index = 0

    def attack_barrel(self):
        ''' 
        None -> None
        Allows to attack the barrels with a hammer.
        '''
        # You can't attack if you're climbing a ladder
        # a ladder or jumping
        if self.jumping or self.climbing:
            return

        if self.current_mario_sprite_index == 0:
            hammer_pos = (self.rect.x - 27, self.rect.y + 20)
            self.current_hammer_sprite_index = 2
        elif self.current_mario_sprite_index == 1:
            hammer_pos = (self.rect.x + 29, self.rect.y + 20)
            self.current_hammer_sprite_index = 1
        else:
            hammer_pos = (-100, -100)

        hammer_rect = self.hammer_sprites[
            self.current_hammer_sprite_index].get_rect()
        hammer_rect.x, hammer_rect.y = hammer_pos

        col_index = hammer_rect.collidelist(self.barrels)

        # We have a colision with a barrel
        if col_index >= 0:
            self.sounds['hammer-use'].play()
            self.barrels[col_index].reset()
            self.score += 300
            self.draw_text('300', Mario.TEXT_COLOR, self.rect)

        self.window.blit(self.hammer_sprites[self.current_hammer_sprite_index],
                         hammer_pos)

    def update_inputs(self, delta_time):
        ''' 
        float -> None
        Enables you to perform an action if required based on keys.
        '''
        keys = pygame.key.get_pressed()

        if not self.climbing and not self.grounded:
            self.rect.y += Mario.GRAVITY * delta_time

        if keys[pygame.K_UP]:
            self.climb_ladder(delta_time)
        elif keys[pygame.K_DOWN]:
            self.climb_down_ladder(delta_time)

        if keys[pygame.K_RIGHT]:
            self.move_right(delta_time)
        if keys[pygame.K_LEFT]:
            self.move_left(delta_time)
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_b]:
            self.attack_barrel()

        if not self.climbing:
            found_ground = False

            for pilier in self.pillars:
                for section_rect in pilier.sections:
                    if self.rect.colliderect(section_rect):
                        self.rect.y = section_rect.y - (section_rect.height *
                                                        2)
                        found_ground = True
                        break
                if found_ground:
                    self.grounded = True

        win_size = self.window.get_size()
        self.rect.clamp_ip((0, 0, *win_size))

    def draw(self):
        ''' 
        None -> None
        Draws the player on the screen.
        '''
        self.update_gui()
        self.sprite = self.mario_sprites[self.current_mario_sprite_index]
        self.window.blit(self.sprite, self.rect)
