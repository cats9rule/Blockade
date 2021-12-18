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
    green_seg = '\u01c1'
    blue_seg = '='

    show_player_stats(2, state['walls left']['O'], True if state['current player'] == 'O' else False)
    print("\n" + "#" * board_dim[1]*4 + "########\n")

    #TODO: implement drawing the board
    output = generate_table_string(board_dim)
    print(output)

    print("#" * board_dim[1]*4 + "########\n")
    show_player_stats(1, state['walls left']['X'], True if state['current player'] == 'X' else False)
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def cls() -> None:
    """Clears console, taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console."""
    os.system('cls' if os.name=='nt' else 'clear')

def show_player_stats(player_index: int, walls_left: tuple, is_current: bool) -> None:
    """Draws player info based on parameters."""
    output = f'PLAYER {player_index}'
    output += '                  ( current move )\n' if is_current else '\n'
    output += f'    Green walls left: {walls_left[0]}\n    Blue walls left:  {walls_left[1]}'
    print(output)
    return

def generate_table_string(board_dim: tuple) -> str:
    string = ''
    for i in range(0, board_dim[0] + 2):
        if i != 0 and i != board_dim[0] + 1:
            string += f'{hex(i).lstrip("0x").rstrip("L").upper()}{" " if i < 15 else ""} \u01c1'
        for j in range(1, board_dim[1] + 1):
            if i == 0 or i == board_dim[0] + 1:
                string += f'{" " * 5 if j == 1 else ""}' + f'{hex(j).lstrip("0x").rstrip("L").upper()}{" " if j < 15 else ""}  '
            else:
                char = "\u01c1" if j == (board_dim[1]) else "|"
                string += f'   {char}'
        if i != board_dim[0] + 1:
            string += f'{"" if i == 0 else " "}' + f' {hex(i).lstrip("0x").rstrip("L").upper()}' + '\n'
            string += '   ' + ("  = " if (i == board_dim[0] or i == 0) else "  - ") * board_dim[1] + '\n'
    return string + '\n'