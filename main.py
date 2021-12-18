from f1n import get_initial_state
from f1n import is_game_end


def main():

    #TODO: call input functions to set initial parameters: playing_first, board_dim, starting_pos, starting_wall_count

    playing_first = 'X'
    board_dim = (11, 14)
    starting_pos = {
        'X': [(4, 4), (8, 4)],
        'O': [(4, 11), (8, 11)]
    }
    starting_wall_count = 9

    state = get_initial_state(board_dim, starting_wall_count, starting_pos, playing_first)
    move = {
        'player': playing_first,
        'wall': None,
        'figure': None
    }

    while(not is_game_end(state, starting_pos)):
        break
    return