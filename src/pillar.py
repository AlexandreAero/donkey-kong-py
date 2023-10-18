import pygame

class Pillar:
    RIGHT_TO_LEFT = 0
    LEFT_TO_RIGHT = 1

    def __init__(self,
                 height,
                 section_count,
                 direction,
                 window,
                 y_offset_apply_index=0,
                 bottom_pillar=False):
        ''' 
        int, int, int, int, pygame.Surface, (int), (bool) -> None
        Instantiates a pillar in the game.
        y_offset_apply_index: allows you to control the index of sections
        the vertical offset is applied.
        '''
        self.sprite = pygame.image.load('./art/pillier.png')
        self.rect = self.sprite.get_rect()

        if direction == Pillar.LEFT_TO_RIGHT:
            # We put the pillar at the right of the screen
            self.rect.x = 0
        elif direction == Pillar.RIGHT_TO_LEFT:
            # We put the pillar at the left of the screen
            self.rect.x = window.get_width()

        # Height relative to the floor
        self.rect.y = window.get_height() - height

        self.window = window
        self.section_count = section_count

        self.direction = direction
        self.y_offset_apply_index = y_offset_apply_index

        self.y_offset_factor = 0.05
        self.x_offset_factor = 1
                     
        # If the pillar is the first pillar with the lowest 
        # height, then, as in the official game, the shift on the
        # vertical axis is upwards, not downwards.
        if bottom_pillar:
            self.y_offset_factor = -self.y_offset_factor
                     
        self.x_offset = self.rect.width * self.x_offset_factor
        self.y_offset = self.rect.height * self.y_offset_factor

        self.sections = []

    def calculate_section_rect(self, section_index):
        ''' 
        int -> pygame.Rect
        Calculates the position of the specified section.
        '''
        section_rect = self.rect.copy()

        if section_index >= self.y_offset_apply_index:
            section_rect.y += (section_index -
                               self.y_offset_apply_index) * self.y_offset
        else:
            section_rect.y -= self.y_offset * self.y_offset_apply_index

        match self.direction:
            case Pillar.RIGHT_TO_LEFT:
                section_rect.x -= section_index * self.x_offset
            case Pillar.LEFT_TO_RIGHT:
                section_rect.x += section_index * self.x_offset
            case _:
                pass
        
        return section_rect

    def draw(self):
        '''
        None -> None
        Draws the pillar on the screen.
        '''
        for i in range(self.section_count):
            section_rect = self.calculate_section_rect(i)
            if section_rect not in self.sections:
                self.sections.append(section_rect)
            self.window.blit(self.sprite, section_rect)
