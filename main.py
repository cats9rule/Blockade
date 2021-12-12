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
