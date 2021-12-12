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
    p1_pos = PlayerPositions(3, 3, 7, 3)
    p2_pos = PlayerPositions(3, 10, 7, 10)
    initial_state = State(p1_pos, p2_pos, [], True)

    game = Game(initial_state, (11,14), p1_pos, p2_pos, 9, True, False)
    while run:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                print(game.board.event_onclick(pos[0], pos[1]))
        draw_window(game)
    
    pygame.quit()

if __name__ == "__main__":
    main()
