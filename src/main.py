'''
  Donkey Kong made by Léo, Alexandre, Amine and Jonathan.
  Font made by: Yuji Adachi; Copyright (C)1997-2003 Yuji Adachi.
'''

import pygame

from monkey import Monkey
from mario import Mario
from pillar import Pillar
from pauline import Pauline
from ladder import Ladder
from barrel import Barrel

SCREEN_SIZE = (800, 800)
CLEAR_COLOR = (0, 0, 0)
FPS = 60

# Initialisation

pygame.init()
pygame.display.set_caption('Donkey Kong')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)
running = True
delta_time = 0

# Instantiates objects

pillars = [
    Pillar(100, 20, Pillar.LEFT_TO_RIGHT, window, 7, True),
    Pillar(200, 16, Pillar.LEFT_TO_RIGHT, window),
    Pillar(300, 17, Pillar.RIGHT_TO_LEFT, window),
    Pillar(400, 16, Pillar.LEFT_TO_RIGHT, window),
    Pillar(500, 16, Pillar.RIGHT_TO_LEFT, window),
    Pillar(600, 17, Pillar.LEFT_TO_RIGHT, window, 6)
]

ladders = [
    Ladder(80, 120, 250, True, window),
    Ladder(80, 300, 450, False, window),
    Ladder(170, 200, 600, False, window),
    Ladder(280, 200, 400, False, window),
    Ladder(375, 300, 450, True, window),
    Ladder(385, 500, 700, False, window),
    Ladder(500, 300, 450, True, window),
    Ladder(500, 550, 750, False, window)
]

barrels = [Barrel(window, ladders) for _ in range(4)]

mario = Mario(window, ladders, barrels, pillars)
monkey = Monkey(window)
pauline = Pauline(window)

# Music et sounds

background_sound = pygame.mixer.Sound('./art/background-music.mp3')
background_sound.set_volume(0.1)
background_sound.play(-1)

# Static environment

oil_fire = pygame.image.load('./art/oil-fire.png')
oil = pygame.image.load('./art/oil.png')
barrel_stack = pygame.image.load('./art/barrel-stack.png')

# +--------+--------+--------+--------+--------+--------+--------+

def check_collisions():
    ''' 
    None -> None
    This function checks for collisions between elements
    and takes action when necessary.
    '''
    # Colision between Mario and Pauline
    if mario.rect.colliderect(pauline.rect):
        mario.score += 1000
        mario.reset_position()

    # Colision between Mario and a barrel
    if mario.rect.collidelist(barrels) >= 0:
        mario.reset_position()
        mario.loose_life()
        if mario.life <= 0:
            mario.game_over()

# Main loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(CLEAR_COLOR)

    for echelle in ladders:
        echelle.draw()

    for pilier in pillars:
        pilier.draw()

    for tonneau in barrels:
        tonneau.draw()
        tonneau.roll(delta_time)
        if tonneau.rect.x > window.get_width() or tonneau.rect.x < 0:
            tonneau.reset()

    window.blit(oil_fire, (5, 625))
    window.blit(oil, (50, 665))
    window.blit(barrel_stack, (10, 113))

    check_collisions()

    monkey.draw(delta_time)
    pauline.draw(delta_time)

    mario.draw()
    mario.update_inputs(delta_time)

    pygame.display.update()

    delta_time = clock.tick(FPS) / 1000

pygame.quit()
