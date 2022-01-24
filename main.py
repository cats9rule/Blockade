import faza1
import faza2
import faza3
import pyfiglet
import cProfile

def main():
    # init_params = faza1.define_initial_parameters()

    # playing_first = init_params["playing_first"]
    # board_dim = init_params["board_dim"]
    # starting_pos = init_params["starting_pos"]
    # starting_wall_count = init_params["starting_wall_count"]

    playing_first = "X"
    board_dim = (11, 14)
    starting_pos = {
            'X': [(4, 4), (8, 4)],
            'O': [(4, 11), (8, 11)]
    }
    starting_wall_count = 0

    state = faza1.get_initial_state(starting_wall_count, starting_pos, playing_first)
    move = {
        'player': playing_first,
        'wall': 0,
        'figure': None
    }

    faza1.show_game(state, board_dim, starting_pos)

    while(not faza1.is_game_end(state, starting_pos)):
        if state['current player'] == 'X':
            move = faza2.input_move(state, board_dim, starting_pos)
            state = faza1.generate_next_state(state, move)
            faza1.show_game(state, board_dim, starting_pos)  
        else:
            state = faza3.computer_move(state, starting_pos, board_dim, 3)
            faza1.show_game(state, board_dim, starting_pos)     

    winner = faza2.get_winner(state)
    result = pyfiglet.figlet_format(f"Winner! {winner} won this game!")
    faza1.cls()
    print(result)
    
    return

main()

#cProfile.run("main()")