
from faza1 import generate_next_state, is_figure_movement_valid, is_walls_overlap, validate_move
from faza1 import cls
import copy

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

def get_next_state(state: dict, move: dict) -> dict:
    return generate_next_state(state, move)

def get_next_state_list(state: dict, board_dim: tuple, starting_pos: dict) -> list:
    states = []
    possible_figure_moves = []
    player = state['current player']
    for i in range(0, 2):
        possible_figure_moves += get_figure_moves(
            i, state['player positions'][player][i], player, state['player positions'], starting_pos, state['placed walls'], board_dim
            )
    potential_walls = get_wall_placements(state, board_dim)
    
    for figure_move in possible_figure_moves:
        if len(potential_walls) == 0:
            states.append(get_next_state(state, {'player': copy.copy(player), 'wall': None, 'figure': copy.deepcopy(figure_move)}))
        else: 
            for wall in potential_walls:
                potential_move = {
                    'player': copy.copy(player),
                    'wall': copy.deepcopy(wall),
                    'figure': copy.deepcopy(figure_move)
                }
                if validate_move(state, potential_move, board_dim, starting_pos):
                    states.append(get_next_state(state, potential_move))
        
    return states
    


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


def get_figure_moves(figure_index: int, old_pos: tuple, player: str, player_positions:dict, starting_pos:dict, placed_walls:list, board_dim:tuple) -> list:  
    move_list = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (0, 1), (1, 0), (0, -1)]
    figure_moves = []
    for move in move_list:
        new_move = (old_pos[0] + move[0], old_pos[0] + move[0], figure_index)
        if is_figure_movement_valid(new_move, figure_index, old_pos, player, player_positions, starting_pos, placed_walls, None, board_dim):
            figure_moves.append(new_move)
    return figure_moves
    
def get_wall_placements(state: dict, board_dim: tuple) -> list:
    wall_placements = list()
    
    for i in range(1, board_dim[0]):
        for j in range(1, board_dim[1]):
            new_wall_g = None
            new_wall_b = None
            
            if state['walls left'][state['current player']][0] > 0:
                new_wall_g = (i, j, 'g')
            if state['walls left'][state['current player']][1] > 0:
                new_wall_b = (i, j, 'b')
                
            for wall in state['placed walls']:
                if not isinstance(new_wall_g, type(None)) and not is_walls_overlap(wall, new_wall_g):
                    wall_placements.append(new_wall_g)
                if not isinstance(new_wall_b, type(None)) and not is_walls_overlap(wall, new_wall_b):
                    wall_placements.append(new_wall_g)
                    
    return wall_placements