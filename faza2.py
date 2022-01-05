
import faza1
import copy
import math

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

        loop = not faza1.validate_move(state, move, board_dim, starting_pos)
        if loop:
            print("> You must enter a valid move.")

    return move    

def get_winner(state: dict) -> str:
    """Returns winner of the game. Does not validate if game has truly ended."""
    return 'X' if state['current player'] == 'O' else 'O'

def get_next_state(state: dict, move: dict) -> dict:
    return faza1.generate_next_state(state, move)

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
                if faza1.validate_move(state, potential_move, board_dim, starting_pos):
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
        new_move = (old_pos[0] + move[0], old_pos[1] + move[1], figure_index)
        if faza1.is_figure_movement_valid(new_move, figure_index, old_pos, player, player_positions, starting_pos, placed_walls, None, board_dim):
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
                if faza1.is_wall_placement_valid(state['placed walls'], new_wall_g, board_dim):
                    wall_placements.append(new_wall_g)
            if state['walls left'][state['current player']][1] > 0:
                new_wall_b = (i, j, 'b')
                if faza1.is_wall_placement_valid(state['placed walls'], new_wall_b, board_dim):
                    wall_placements.append(new_wall_b)
                    
    return wall_placements

####################################
def h(currentPosition, endPosition):
    x = currentPosition[0] - endPosition[0]
    y = currentPosition[1] - endPosition[1]
    return math.sqrt( x**2 + y**2 )

def a_star(start, end, figure_index, player, player_positions, starting_pos, placed_walls, board_dim):
    start = (start[0], start[1], 0)
    found_end = False
    open_set = set()
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    open_set.add(tuple(start, ))

    while len(open_set) > 0 and not found_end:
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h(next_node, end) < g[node] + h(node, end):
                node = next_node
        
        if node[0] == end[0] and node[1] == end[1]:
            found_end = True
            break

        for destination in get_figure_moves(figure_index, node, player, player_positions, starting_pos, placed_walls, board_dim):
            if destination not in open_set and destination not in closed_set:
                open_set.add(destination)
                prev_nodes[destination] = node
                g[destination] = g[node] + 1
            else:
                if g[destination] > g[node] + 1:
                    g[destination] = g[node] + 1
                    prev_nodes[destination] = node
                    if destination in closed_set:
                        closed_set.remove(destination)
                        open_set.add(destination)
        open_set.remove(node)
        closed_set.add(node)
    
    return found_end


def is_path_available(state, starting_pos, board_dim):
    path_available = True
    for player in state['player positions']:
        if player == 'X':
            opponent = 'O'
        elif player == 'O':
            opponent = 'X'

        for figure_pos in state['player positions'][player]:
            figure_index = state['player positions'][player].index(figure_pos)
            for end in starting_pos[opponent]:
                p_a = a_star(figure_pos, end, figure_index, player, state['player positions'], starting_pos, state['placed walls'], board_dim)
                path_available = path_available and p_a
    return path_available