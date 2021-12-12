import pygame
import colors
import constants
from gameclass import Game
from state import State
from state import PlayerPositions
from state import WallPosition

WIN = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Blockade")
def draw_window(game):
    WIN.fill(colors.BACKGROUND_DARK)
    game.draw(WIN)
    pygame.display.update()


def main():
    clock = pygame.time.Clock() 
    run = True
    p1_pos = PlayerPositions(4, 4, 8, 4)
    p2_pos = PlayerPositions(4, 11, 8, 11)
    initial_state = State(p1_pos, p2_pos, [], True)

    game = Game(initial_state, (22,28), p1_pos, p2_pos, 9, True, False)
    while run:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(game)
    
    pygame.quit()

if __name__ == "__main__":
    main()
