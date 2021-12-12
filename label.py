import pygame

class Label(object):
    def __init__(self, text, size, color):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', size, True)
        self.text = self.font.render(text, True, color)
        self.size = self.font.size(text) #(w, h)

    def draw_label(self, window, pos):
        window.blit(self.text, pos)