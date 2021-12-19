import os

def get_initial_state(board_dim: tuple, wall_count: int, initial_positions: dict, playing_first: str) -> dict:
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
    current = 'X' if current == 'O' else 'O'
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

    if isinstance(new_wall, None): 
        placed_walls.add(new_wall)
        walls_left = state['walls left']
        walls_left[player][new_wall[2]] -= 1
    
    return {
        'player positions': player_pos,
        'current player': 'X' if player == 'O' else 'O',
        'placed walls': placed_walls,
        'walls left': walls_left
    }

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
    for key in starting_positions:
        for position in starting_positions[key]:
            table_string = insert_string_at_position(table_string, key, board_dim, position, False)
    return table_string

def insert_figures(table_string: str, player_positions: dict, board_dim: tuple) -> str:
    for key in player_positions:
        for i in range (1,3):
            table_string = insert_string_at_position(table_string, key + str(i), board_dim, player_positions[key][i-1], False)
    return table_string

def insert_walls(table_string: str, walls: list, board_dim: tuple) -> str:
    for wall in walls:
        if wall[2] == 'green':
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
    index = (4 * (board_dim[1] + 2) + 1) * 2* position[0] + position[1] * 4 + (3 if is_wall else 1)
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]

def insert_horiz_wall(table_string: str, string_to_insert: str, board_dim: tuple, position: tuple) -> str:
    index = (4 * (board_dim[1] + 2) + 1) * 2 * position[0] + position[1] * 4 + 1 + 4 * (board_dim[1] + 2) + 1
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]