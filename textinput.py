import pygame
import colors

pygame.init()

FONT = pygame.font.Font(None, 20)

class TextInput(object):
    def __init__(self, rect, text=''):
        self.rect = pygame.Rect(rect)
        self.color = colors.MESSAGE_BASIC #colors.MESSAGE_SUCCESS kad se promeni active
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = colors.MESSAGE_SUCCESS if self.active else colors.MESSAGE_BASIC
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = colors.MESSAGE_SUCCESS if self.active else colors.MESSAGE_BASIC
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif (event.key == pygame.K_0 
                        or event.key == pygame.K_1 
                        or event.key == pygame.K_2
                        or event.key == pygame.K_3
                        or event.key == pygame.K_4
                        or event.key == pygame.K_5
                        or event.key == pygame.K_6
                        or event.key == pygame.K_7
                        or event.key == pygame.K_8
                        or event.key == pygame.K_9):
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw_input_box(self, surface):
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
