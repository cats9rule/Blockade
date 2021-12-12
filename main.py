import pygame
import colors
import constants
import gameInit

WIN = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Blockade")
GAME_INIT = gameInit.InitGame()

def draw_window():
    WIN.fill(colors.BACKGROUND_DARK)
    GAME_INIT.draw(WIN)
    pygame.display.update()

# def draw_label(text, size, pos):
#     lab = label.Label(text, size, colors.TEXT_LIGHT)
#     WIN.blit(lab.text, pos)

def main():
    clock = pygame.time.Clock() 
    run = True
    while run:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()
