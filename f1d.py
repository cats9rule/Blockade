import os
from f1n import cls


def define_initial_parameters():
    ret_val = dict()

    starting_player = playing_first()
    board_size = board_dimensions()
    starting_pos = positions(board_size)
    starting_wall_count = wall_count()

    ret_val = {
        "playing_first": starting_player,
        "board_dim": board_size,
        "starting_pos": starting_pos,
        "starting_wall_count": starting_wall_count
    }

    return ret_val


def playing_first():
    loop = True

    while loop:
        cls()
        pf = input("Which player will be playing first? (X or O)")
        if pf == "x":
            pf = "X"
        elif pf == "o":
            pf = "O"

        are_you_sure = input("Are you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False

    return pf


def board_dimensions():
    loop = True

    while loop:
        cls()
        print("Define the dimensions of the gameboard. \nIf dimensions are off-limit, we will automatically limit them.")
        board_rows_str = input("Number of rows (11-22): ")
        board_columns_str = input("Number of columns (14-28): ")

        board_rows = int(board_rows_str)
        board_columns = int(board_columns_str)
        
        if board_rows > 22:
            board_rows = 22
        elif board_rows < 11:
            board_rows = 11
        if board_columns > 28:
            board_columns = 28
        elif board_columns < 14:
            board_columns = 14

        board_dim = (board_rows, board_columns)

        are_you_sure = input("Are you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False

    return board_dim


def positions(board: tuple):

    loop = True
    cls()
    while loop:
        starting_positions = {
            'X': [(-1, -1), (-1, -1)],
            'O': [(-1, -1), (-1, -1)]
        }
        print("Time to choose starting positions. \nDon't forget, 2 figures can't have same starting positions!\n\n")
        x1 = pos("X", "1", board, starting_positions)
        x2 = pos("X", "2", board, starting_positions)
        o1 = pos("O", "1", board, starting_positions)
        o2 = pos("O", "2", board, starting_positions)

        starting_positions = {
            'X': [x1, x2],
            'O': [o1, o2]
        }

        x1_str = str(x1[0]) + ' - ' + str(x1[1])
        x2_str = str(x2[0]) + ' - ' + str(x2[1])
        o1_str = str(o1[0]) + ' - ' + str(o1[1])
        o2_str = str(o2[0]) + ' - ' + str(o2[1])
        print("\n\nStarting positions are: " + "\nX1: " + x1_str + "\nX2: " + x2_str + "\nO1: " + o1_str + "\nO2: " + o2_str)

        are_you_sure = input("\nAre you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False

    return starting_positions
        


def pos(player: str, figure: str, board: tuple, starting_positions: dict):
    loop = True
    while loop:
        print("Choose " + player + figure + " starting row: ")
        row_string = input()
        row = int(row_string)
        print("Choose " + player + figure + " starting column: ")
        column_string = input()
        column = int(column_string)

        if(row < 0 or row > board[0] or column < 0 or column > board[1]):
            print("Out of bounds!")
            continue
        pos = (row, column)
        if(pos in starting_positions["X"] or pos in starting_positions["O"]):
            print("Told ya two figures can't have same starting positions...")
            continue
        
        are_you_sure = input("Are you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False

    return pos


def wall_count():
    loop = True
    cls()
    while loop:
        print("How many available walls will players have? (9-18): ")
        walls_string = input()
        walls = int(walls_string)

        if walls < 9 or walls > 18:
            print("Whoops, invalid ammount of walls. Try again")
            continue
        
        are_you_sure = input("Are you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False
    
    return walls