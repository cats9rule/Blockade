import pygame
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN
import colors
import constants
from gameInit import InitGame

WIN = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Blockade")
GAME_INIT = InitGame()

def draw_window():
    WIN.fill(colors.BACKGROUND_DARK)
    GAME_INIT.draw(WIN)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    is_game_init = True
    run = True
    p1_pos = PlayerPositions(3, 3, 7, 3)
    p2_pos = PlayerPositions(3, 10, 7, 10)
    wall1 = WallPosition(2, 3, False)
    wall2 = WallPosition(1, 4, True)
    initial_state = State(p1_pos, p2_pos, [wall1, wall2], (9,9), (9,9), True)

    game = Game(initial_state, (22,28), p1_pos, p2_pos, 9, True, False)
    while run:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if is_game_init:
                    GAME_INIT.handle_mouse_event(pos, event)
            if event.type == pygame.KEYDOWN:
                if is_game_init:
                    if (event.key == pygame.K_RETURN):
                        GAME_INIT.handle_RETURN_event(event)
                    else:
                        GAME_INIT.handle_keyboard_event(event)

        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()
