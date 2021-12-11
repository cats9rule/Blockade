import pygame
import colors
import constants

WIN = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Blockade")
def draw_window():
    WIN.fill(colors.BACKGROUND_DARK)
    pygame.display.update()


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
