from os import X_OK
from f1n import get_initial_state
from f1n import is_game_end
from f1n import show_game
from f1d import define_initial_parameters, playing_first


def main():

    #TODO: call input functions to set initial parameters: playing_first, board_dim, starting_pos, starting_wall_count

    init_params = define_initial_parameters()

    # playing_first = 'X'
    # board_dim = (11, 14)
    # starting_pos = {
    #     'X': [(4, 4), (8, 4)],
    #     'O': [(4, 11), (8, 11)]
    # }
    # starting_wall_count = 9

    playing_first = init_params["playing_first"]
    board_dim = init_params["board_dim"]
    starting_pos = init_params["starting_pos"]
    starting_wall_count = init_params["starting_wall_count"]

    state = get_initial_state(board_dim, starting_wall_count, starting_pos, playing_first)
    move = {
        'player': playing_first,
        'wall': None,
        'figure': None
    }

    show_game(state, board_dim, starting_pos)

    # while(not is_game_end(state, starting_pos)):
    #     break
    return

main()