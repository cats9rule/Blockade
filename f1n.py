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

def show_game(state: dict, board_dim: tuple):
    """Clears console, then draws board with information about current state of game"""
    
    return