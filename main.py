import faza1
import faza2
import f3n
import pyfiglet
import copy

def main():
    #init_params = faza1.define_initial_parameters()

    playing_first = 'O' #init_params["playing_first"]
    board_dim = (11,14) #init_params["board_dim"]
    starting_pos = {
        'X': [(4, 4) , (8, 4)],
        'O': [(4, 11) , (8, 11)]
    } #init_params["starting_pos"]
    starting_wall_count = 9 #init_params["starting_wall_count"]


    state = faza1.get_initial_state(starting_wall_count, starting_pos, playing_first)
    move = {
        'player': playing_first,
        'wall': None,
        'figure': None
    }
    faza1.show_game(state, board_dim, starting_pos)

    while(not faza1.is_game_end(state, starting_pos)):
        if state['current player'] == 'X':
            move = faza2.input_move(state, board_dim, starting_pos)
            state = faza1.generate_next_state(state, move)
            faza1.show_game(state, board_dim, starting_pos)
            state = f3n.computer_move(state, starting_pos, board_dim, 1)
            faza1.show_game(state, board_dim, starting_pos)
        else:
            state = f3n.computer_move(state, starting_pos, board_dim, 1)
            faza1.show_game(state, board_dim, starting_pos)
            move = faza2.input_move(state, board_dim, starting_pos)
            state = faza1.generate_next_state(state, move)
            faza1.show_game(state, board_dim, starting_pos)
        

    winner = faza2.get_winner(state)
    result = pyfiglet.figlet_format(f"Winner! {winner} won this game!")
    faza1.cls()
    print(result)
    
    print(faza2.is_path_available(state, starting_pos, board_dim)) 
    
    return

main()
