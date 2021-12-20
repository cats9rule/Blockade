import os

# NOTE TO SELF: GREEN WALL IS VERTICAL!!!

def get_initial_state(wall_count: int, initial_positions: dict, playing_first: str) -> dict:
    """Returns state with initialized player positions, first player, walls left initialized to initial wall count, and empty placed walls list."""
    return {
        'player positions': initial_positions,
        'current player': playing_first,
        'placed walls': [],
        'walls left': {
            'X': [wall_count, wall_count],
            'O': [wall_count, wall_count]
        }
    }
    
def is_game_end(state: dict, starting_pos: dict) -> bool:
    """Checks if game is end after played move, based on current state and starting positions."""
    # because move is already played, current player is the opponent of previous state
    opponent = state['current player']
    current = 'X' if opponent == 'O' else 'O'
    if state['player positions'][current][0] in starting_pos[opponent]: 
        return True
    if state['player positions'][current][1] in starting_pos[opponent]:
        return True
    return False

def generate_next_state(state: dict, move: dict) -> dict:
    """Returns next state based on current state and played move, does not check validity of the move."""
    player = move['player']
    figure_index = move['figure'][2]
    figure_pos = (move['figure'][0], move['figure'][1])
    player_pos = state['player positions']
    player_pos[player][figure_index] = figure_pos
    new_wall = move['wall']
    placed_walls = state['placed walls']

    if not isinstance(new_wall, type(None)): 
        placed_walls.append(new_wall)
        walls_left = state['walls left']
        walls_left[player][0 if new_wall[2] == 'g' else 1] -= 1
    
    return {
        'player positions': player_pos,
        'current player': 'X' if player == 'O' else 'O',
        'placed walls': placed_walls,
        'walls left': walls_left
    }

def validate_move(state: dict, move: dict, board_dim: tuple, starting_pos: dict) -> bool:
    """Checks if move is valid according to game rules. Returns bool."""
    player = move['player'] # X or O
    opponent = 'X' if player == 'O' else 'O'
    new_wall = move['wall']
    figure_index = move['figure'][2]
    figure_pos = (move['figure'][0], move['figure'][1])

    if any([figure_pos[0] < 1, figure_pos[0] > board_dim[0], figure_pos[1] < 1, figure_pos[1] > board_dim[1]]): return False
    if not isinstance(new_wall, type(None)) and any([new_wall[0] < 1, new_wall[0] > board_dim[0] - 1, new_wall[1] < 1, new_wall[1] > board_dim[1] - 1]): return False

    for p in state['player positions']:
        for position in state['player positions'][p]:
            if figure_pos[0] == position[0] and figure_pos[1] == position[1] and figure_pos not in starting_pos[opponent]: return False

    if not check_figure_movement(state, figure_pos, figure_index, starting_pos, player, opponent, new_wall):
        return False
    
    return True

def show_game(state: dict, board_dim: tuple, starting_pos: dict) -> None:
    """Clears console, then draws board with information about current state of game"""
    cls()
    p2stats = show_player_stats(2, state['walls left']['O'], True if state['current player'] == 'O' else False)
    output = insert_walls(
        insert_figures(insert_starting_positions(generate_table_string(board_dim), starting_pos, board_dim), 
            state['player positions'], board_dim
            ), 
        state['placed walls'], board_dim
        )
    p1stats = show_player_stats(1, state['walls left']['X'], True if state['current player'] == 'X' else False)
    print(p2stats + "\n" + "#" * board_dim[1]*4 + "########\n\n" + output + "\n\n" + "#" * board_dim[1]*4 + "########\n\n" + p1stats)
    return


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def cls() -> None:
    """Clears console, taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console."""
    os.system('cls' if os.name=='nt' else 'clear')

def show_player_stats(player_index: int, walls_left: tuple, is_current: bool) -> str:
    """Draws player info based on parameters."""
    output = f'PLAYER {player_index}'
    output += '                  ( current move )\n' if is_current else '\n'
    output += f'    Green walls left: {walls_left[0]}\n    Blue walls left:  {walls_left[1]}'
    return output + '\n'

def generate_table_string(board_dim: tuple) -> str:
    """Makes a string representing the table without walls, figures or starting positions."""
    string = ''
    for row in range(0, board_dim[0] + 2):
        for col in range(0, board_dim[1] + 2):
            if row == 0 or row == board_dim[0] + 1:
                if col == 0 or col == board_dim[1] + 1:
                    string += '    '
                else:
                    string += f' {hex(col).lstrip("0x").rstrip("L").upper()} {" " if col <= 15 else ""}'
            else:
                if col == 0:
                    string += f'{hex(row).lstrip("0x").rstrip("L").upper()} {" " if row <= 15 else ""}' + '\u01c1'
                elif col == board_dim[1] + 1:
                    string += f'  {hex(row).lstrip("0x").rstrip("L").upper()}{" " if row <= 15 else ""}'
                else:
                    char = "\u01c1" if col == (board_dim[1]) else "|"
                    string += f'   {char}'
        if row != board_dim[0] + 1:
            string += '\n    ' + f' {"-" if (row != 0 and row != board_dim[0]) else "="}  ' * board_dim[1] + '    \n'
    return string

def insert_starting_positions(table_string: str, starting_positions: dict, board_dim: tuple) -> str:
    """Inserts starting positions into string table where they belong. 
    Returns string with inserted positions."""
    for key in starting_positions:
        for position in starting_positions[key]:
            table_string = insert_string_at_position(table_string, key, board_dim, position, False)
    return table_string

def insert_figures(table_string: str, player_positions: dict, board_dim: tuple) -> str:
    """Inserts player figures into string table on their positions. 
    Returns string with inserted figures."""
    for key in player_positions:
        for i in range (1,3):
            table_string = insert_string_at_position(table_string, key + str(i), board_dim, player_positions[key][i-1], False)
    return table_string

def insert_walls(table_string: str, walls: list, board_dim: tuple) -> str:
    """Inserts walls into string table where they belong. 
    Returns string with inserted walls."""
    for wall in walls:
        if wall[2] == 'g':
            table_string = insert_string_at_position(
                insert_string_at_position(table_string, "\u01c1", board_dim, (wall[0], wall[1]), True),
                "\u01c1", board_dim, (wall[0] + 1, wall[1]), True
            )
        else:
            table_string = insert_horiz_wall(
                insert_horiz_wall(table_string, "=", board_dim, (wall[0], wall[1])),
                "=", board_dim, (wall[0], wall[1] + 1)
            )
    return table_string

def insert_string_at_position(table_string: str, string_to_insert: str, board_dim: tuple, position: tuple, is_wall: bool) -> str:
    """Inserts string_to_insert into table_string on position.
    Can be used for inserting a vertical wall.
    Returns table string."""
    index = (4 * (board_dim[1] + 2) + 1) * 2* position[0] + position[1] * 4 + (3 if is_wall else 1)
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]

def insert_horiz_wall(table_string: str, string_to_insert: str, board_dim: tuple, position: tuple) -> str:
    """Inserts horizontal wall onto given position. Returns table string."""
    index = (4 * (board_dim[1] + 2) + 1) * 2 * position[0] + position[1] * 4 + 1 + 4 * (board_dim[1] + 2) + 1
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]

def check_figure_movement(state: dict, figure_pos: tuple, figure_index: int, starting_pos: dict, player: str, opponent: str, new_wall: tuple) -> bool:
    old_pos = state['player positions'][player][figure_index]
    d_row = abs(old_pos[0] - figure_pos[0])
    d_col = abs(old_pos[1] - figure_pos[1])
    direction = get_movement_direction(figure_pos, old_pos)
    other_figure = starting_pos[opponent][(figure_index + 1) % 2]
    checklist = []

    if d_row + d_col == 1:
        for position in starting_pos[opponent]:
            checklist.append(not (position[0] == figure_pos[0] and position[1] == figure_pos[1]))
        if any(checklist): return False
        checklist = get_blocking_figure_checklist(direction, starting_pos[opponent], figure_pos, other_figure)
        if any(checklist): return False
    if d_row + d_col > 2: return False 
    return check_walls(state, direction, old_pos, new_wall)
    
def check_walls(state:dict, direction: str, old_pos: tuple, new_wall: tuple) -> bool:
    #NOTE: direction: u (up), d (down), l (left), r (right), ul (up left), ur (up right), dl (down left), dr (down right)
    for wall in state['placed walls']:
        if not isinstance(new_wall, type(None)):
            if wall[0] == new_wall[0] and wall[1] == new_wall[1]: return False
        if direction == 'l':
            if wall[2] == 'g' and (wall[1] == old_pos[1] - 1 or wall[1] == old_pos[1] - 2) and (wall[0] == old_pos[0] or wall[0] == old_pos[0] - 1):
                return False
        if direction == 'r':
            if wall[2] == 'g' and (wall[1] == old_pos[1] or wall[1] == old_pos[1] + 1) and (wall[0] == old_pos[0] or wall[0] == old_pos[0] - 1):
                return False
        if direction == 'd':
            if wall[2] == 'b' and (wall[1] == old_pos[1] or wall[1] == old_pos[1] - 1) and (wall[0] == old_pos[0] or wall[0] == old_pos[0] + 1):
                return False
        if direction == 'u':
            if wall[2] == 'b' and (wall[1] == old_pos[1] or wall[1] == old_pos[1] - 1) and (wall[0] == old_pos[0] - 1 or wall[0] == old_pos[0] - 2):
                return False
            
        if direction == 'ul':
            if wall[1] == old_pos[1] - 1 and wall[0] == old_pos[0] - 1:
                return False
        if direction == 'ur':
            if wall[1] == old_pos[1] and wall[0] == old_pos[0] - 1:
                return False
        if direction == 'dl':
            if wall[1] == old_pos[1] - 1 and wall[0] == old_pos[0]:
                return False
        if direction == 'dr':
            if wall[1] == old_pos[1] and wall[0] == old_pos[0]:
                return False
    return True
        

def get_movement_direction(figure_pos: tuple, old_pos: tuple) -> str:
    direction = ""
    if old_pos[0] > figure_pos[0]: direction += "u"
    elif old_pos[0] < figure_pos[0]: direction += "d"
    if old_pos[1] > figure_pos[1]: direction += "l"
    elif old_pos[1] < figure_pos[1]: direction += "r"
    return direction

def get_blocking_figure_checklist(direction: str, opponent_start_pos: list, figure_pos: tuple, other_figure:tuple) -> list:
    checklist = list()
    for position in opponent_start_pos:
        checklist.append(not (direction == 'l' and position[0] == figure_pos[0] and position[1] == (figure_pos[1] - 1)))
        checklist.append(not (direction == 'r' and position[0] == figure_pos[0] and position[1] == (figure_pos[1] + 1)))
        checklist.append(not (direction == 'u' and position[0] == (figure_pos[0] - 1) and position[1] == figure_pos[1]))
        checklist.append(not (direction == 'd' and position[0] == (figure_pos[0] + 1) and position[1] == figure_pos[1]))
    checklist.append(not (direction == 'l' and other_figure[0] == figure_pos[0] and other_figure[1] == (figure_pos[1] - 1)))
    checklist.append(not (direction == 'r' and other_figure[0] == figure_pos[0] and other_figure[1] == (figure_pos[1] + 1)))
    checklist.append(not (direction == 'u' and other_figure[0] == (figure_pos[0] - 1) and other_figure[1] == figure_pos[1]))
    checklist.append(not (direction == 'd' and other_figure[0] == (figure_pos[0] + 1) and other_figure[1] == figure_pos[1]))
    return checklist
