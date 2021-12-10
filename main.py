import pygame
import colors

#TODO: move code to game class
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blockade")
FPS = 60
def draw_window():
    WIN.fill(colors.BACKGROUND)
    pygame.display.update()


def main():
    clock = pygame.time.Clock() 
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()
