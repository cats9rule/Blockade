from os import X_OK
from faza1 import get_initial_state
from faza1 import is_game_end
from faza1 import show_game
from faza1 import define_initial_parameters


def main():
    init_params = define_initial_parameters()

    playing_first = init_params["playing_first"]
    board_dim = init_params["board_dim"]
    starting_pos = init_params["starting_pos"]
    starting_wall_count = init_params["starting_wall_count"]

    state = get_initial_state(starting_wall_count, starting_pos, playing_first)
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