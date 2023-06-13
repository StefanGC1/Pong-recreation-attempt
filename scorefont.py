import pygame

pygame.font.init()


class Score():  # Score text class
    def __init__(self, score, pos):
        super().__init__()
        self.font = pygame.font.SysFont('freesansbold.ttf', 35)  # Font creation
        self.color = pygame.color.Color("white")
        self.fontRender = self.font.render(f'{score}', False, self.color)  # Font rendering
        self.fontRect = self.fontRender.get_rect()  # Creating a rect surface
        self.fontRect.center = pos

    def update(self, score, display):  # Update method
        self.fontRender = self.font.render(f'{score}', False, self.color)
        display.blit(self.fontRender, self.fontRect)
