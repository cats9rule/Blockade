
from f1n import is_game_end
from faza1 import validate_move
from faza1 import cls

def input_move(state: dict, board_dim: tuple, starting_pos: dict) -> dict:
    """Requests input for wall (if needed) and moving figure. Validates the move. 
    Returns move in form of dict."""
    loop = True
    player = state['current player']
    can_place_wall_g = True if (state['walls left'][player][0] > 0) else False
    can_place__wall_b = True if (state['walls left'][player][1] > 0) else False

    while loop:

        figure = input_figure()
        wall_pos = None
        if can_place_wall_g or can_place__wall_b:
            wall_pos = input_wall(can_place_wall_g, can_place__wall_b)

        move = {
            'player': player,
            'wall': wall_pos,
            'figure': figure
        }

        loop = not validate_move(state, move, board_dim, starting_pos)
        if loop:
            print("> You must enter a valid move.")

    return move    

def get_winner(state: dict) -> str:
    """Returns winner of the game. Does not validate if game has truly ended."""
    return 'X' if state['current player'] == 'O' else 'O'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def input_wall(can_green: bool, can_blue: bool) -> tuple:
    color = ''
    row = 0
    col = 0

    while (row < 1 and col < 1):
        if (can_green and can_blue and color == ''):
            color = input("> What wall are you placing? (g/b) ")
            if color != 'g' and color != 'b':
                print("> Please choose either green or blue.")
                color = ''
                continue

        elif can_green and color == '':
            color = 'g'
            print("> You can only place a green wall now.")

        elif can_blue and color == '':
            color = 'b'
            print("> You can only place a blue wall now.")
        
        row = int(input("> Choose wall row: "))
        col = int(input("> Choose wall column: "))

    return (row, col, color)

        
def input_figure() -> tuple:
    figure_index = -1
    row = 0
    col = 0

    while figure_index < 0:
        figure_index = int(input("> What figure are you moving? (1/2) "))
        if figure_index < 1 or figure_index > 2:
            print("> You must specify a valid index.")
            figure_index = -1
            continue
        
        row = int(input("> What row? "))
        col = int(input("> What column? "))

    return (row, col, figure_index - 1)
