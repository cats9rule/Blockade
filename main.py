
from faza1 import cls, generate_next_state, get_initial_state, is_game_end, show_game, define_initial_parameters
from f2n import get_winner, input_move
import pyfiglet

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

    while(not is_game_end(state, starting_pos)):
        move = input_move(state, board_dim, starting_pos)
        state = generate_next_state(state, move)
        show_game(state, board_dim, starting_pos)

    winner = get_winner(state)
    result = pyfiglet.figlet_format(f"Winner! {winner} won this game!")
    cls()
    print(result)
    return

main()