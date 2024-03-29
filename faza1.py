import os
import copy
from faza2 import is_path_available


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
        # elif board_rows < 11:
        #     board_rows = 11
        if board_columns > 28:
            board_columns = 28
        # elif board_columns < 14:
        #     board_columns = 14

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
        print("\n\nStarting positions are: " + "\nX1: " + x1_str +
              "\nX2: " + x2_str + "\nO1: " + o1_str + "\nO2: " + o2_str)

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

        if walls < 0 or walls > 18:
            print("Whoops, invalid ammount of walls. Try again")
            continue

        are_you_sure = input("Are you sure? (y/n): ")
        if are_you_sure == "y":
            loop = False

    return walls

# NOTE TO SELF: GREEN WALL IS VERTICAL!!!


def get_initial_state(wall_count: int, initial_positions: dict, playing_first: str) -> dict:
    """Returns state with initialized player positions, first player, walls left initialized to initial wall count, and empty placed walls list."""
    return {
        'player positions': copy.deepcopy(initial_positions),
        'current player': copy.copy(playing_first),
        'placed walls': set(),
        'walls left': {
            'X': [copy.copy(wall_count), copy.copy(wall_count)],
            'O': [copy.copy(wall_count), copy.copy(wall_count)]
        }
    }


def is_game_end(state: dict, starting_pos: dict) -> bool:
    """Checks if game is end after played move, based on current state and starting positions."""
    # because move is already played, current player is the opponent of previous state
    opponent = state['current player']
    current = 'X' if opponent == 'O' else 'O'
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
    player_pos = copy.deepcopy(state['player positions'])
    player_pos[player][figure_index] = figure_pos
    new_wall = move['wall']
    placed_walls = copy.deepcopy(state['placed walls'])
    walls_left = copy.deepcopy(state['walls left'])

    if new_wall != 0:
        placed_walls.add(new_wall)
        walls_left[player][0 if new_wall[2] == 'g' else 1] -= 1

    return {
        'player positions': player_pos,
        'current player': 'X' if player == 'O' else 'O',
        'placed walls': placed_walls,
        'walls left': walls_left
    }


def validate_move(state: dict, move: dict, board_dim: tuple, starting_pos: dict) -> bool:
    """Checks if move is valid according to game rules. Returns bool."""
    player = move['player']  # X or O
    #opponent = 'X' if player == 'O' else 'O'
    new_wall = move['wall']
    figure_index = move['figure'][2]
    figure_pos = (move['figure'][0], move['figure'][1])

    if new_wall != 0:
        if not is_wall_placement_valid(state['placed walls'], new_wall, board_dim):
            return False

    player_positions = state['player positions']
    old_pos = player_positions[player][figure_index]
    placed_walls = state['placed walls']
    if not is_figure_movement_valid(figure_pos, figure_index, old_pos, player, player_positions, starting_pos, placed_walls, new_wall, board_dim):
        return False
    new_state = generate_next_state(state, move)
    if not is_game_end(new_state, starting_pos)and not is_path_available(new_state, starting_pos, board_dim):
        return False
        
    return True


def show_game(state: dict, board_dim: tuple, starting_pos: dict) -> None:
    """Clears console, then draws board with information about current state of game"""
    cls()
    p2stats = show_player_stats(
        2, state['walls left']['O'], True if state['current player'] == 'O' else False)
    output = insert_walls(
        insert_figures(insert_starting_positions(generate_table_string(board_dim), starting_pos, board_dim),
            state['player positions'], board_dim
            ),
        state['placed walls'], board_dim
        )
    p1stats = show_player_stats(
        1, state['walls left']['X'], True if state['current player'] == 'X' else False)
    print(p2stats + "\n" + "#" * board_dim[1]*4 + "########\n\n" +
          output + "\n\n" + "#" * board_dim[1]*4 + "########\n\n" + p1stats)
    return


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def cls() -> None:
    """Clears console, taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_player_stats(player_index: int, walls_left: tuple, is_current: bool) -> str:
    """Draws player info based on parameters."""
    output = f'PLAYER {player_index}'
    output += '                  ( current move )\n' if is_current else '\n'
    output += f'    Green walls left: {walls_left[0]}\n    Blue walls left:  {walls_left[1]}'
    return output + '\n'

def generate_table_string(board_dim: tuple) -> str:
    """Makes a string representing the table without walls, figures or starting positions."""
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
            string += '\n    ' + \
                f' {"-" if (row != 0 and row != board_dim[0]) else "="}  ' * \
                            board_dim[1] + '    \n'
    return string

def insert_starting_positions(table_string: str, starting_positions: dict, board_dim: tuple) -> str:
    """Inserts starting positions into string table where they belong.
    Returns string with inserted positions."""
    for key in starting_positions:
        for position in starting_positions[key]:
            table_string = insert_string_at_position(
                table_string, key, board_dim, position, False)
    return table_string

def insert_figures(table_string: str, player_positions: dict, board_dim: tuple) -> str:
    """Inserts player figures into string table on their positions.
    Returns string with inserted figures."""
    for key in player_positions:
        for i in range(1, 3):
            table_string = insert_string_at_position(
                table_string, key + str(i), board_dim, player_positions[key][i-1], False)
    return table_string

def insert_walls(table_string: str, walls: list, board_dim: tuple) -> str:
    """Inserts walls into string table where they belong.
    Returns string with inserted walls."""
    for wall in walls:
        if wall[2] == 'g':
            table_string = insert_string_at_position(
                insert_string_at_position(
                    table_string, "\u01c1", board_dim, (wall[0], wall[1]), True),
                "\u01c1", board_dim, (wall[0] + 1, wall[1]), True
            )
        else:
            table_string = insert_horiz_wall(
                insert_horiz_wall(table_string, "=",
                                  board_dim, (wall[0], wall[1])),
                "=", board_dim, (wall[0], wall[1] + 1)
            )
    return table_string

def insert_string_at_position(table_string: str, string_to_insert: str, board_dim: tuple, position: tuple, is_wall: bool) -> str:
    """Inserts string_to_insert into table_string on position.
    Can be used for inserting a vertical wall.
    Returns table string."""
    index = (4 * (board_dim[1] + 2) + 1) * 2 * \
             position[0] + position[1] * 4 + (3 if is_wall else 1)
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]

def insert_horiz_wall(table_string: str, string_to_insert: str, board_dim: tuple, position: tuple) -> str:
    """Inserts horizontal wall onto given position. Returns table string."""
    index = (4 * (board_dim[1] + 2) + 1) * 2 * position[0] + \
             position[1] * 4 + 1 + 4 * (board_dim[1] + 2) + 1
    return table_string[:index] + string_to_insert + table_string[index + len(string_to_insert):]


def is_figure_movement_valid(figure_pos: tuple, figure_index: int, old_pos: tuple, player: str, player_positions: dict, starting_pos: dict, placed_walls: set, new_wall: tuple, board_dim: tuple) -> bool:
    """Returns True if moving the given figure does not violate game rules. If any rule is violated, returns False."""
    d_row = abs(old_pos[0] - figure_pos[0])
    d_col = abs(old_pos[1] - figure_pos[1])
    if d_row + d_col > 2: return False
    
    if figure_pos[0] == old_pos[0] and figure_pos[1] == old_pos[1]: return False
    if is_figure_out_of_bounds(figure_pos, board_dim):
        return False

    opponent = 'X' if player == 'O' else 'O'
    other_figure = player_positions[player][(figure_index + 1) % 2]
    
    if figure_pos[0] == other_figure[0] and figure_pos[1] == other_figure[1]: return False
    for position in player_positions[opponent]:
        if figure_pos[0] == position[0] and figure_pos[1] == position[1] and (figure_pos[0], figure_pos[1]) not in starting_pos[opponent]: return False    
    
    direction = get_movement_direction(figure_pos, old_pos)
    if (d_row + d_col == 1):
        if ( not (starting_pos[opponent][0][0] == figure_pos[0] and starting_pos[opponent][0][1] == figure_pos[1])
            and not (starting_pos[opponent][1][0] == figure_pos[0] and starting_pos[opponent][1][1] == figure_pos[1])):
            if not is_figure_blocking_valid(
                direction, player_positions[opponent], figure_pos, other_figure, placed_walls):
                return False
         
    if new_wall != 0:
        walls_with_new_wall = copy.deepcopy(placed_walls)
        walls_with_new_wall.add(new_wall)
        if is_hitting_any_wall(walls_with_new_wall, old_pos, direction):
            return False
    elif is_hitting_any_wall(placed_walls, old_pos, direction):
        return False
    
    return True

def is_wall_placement_valid(placed_walls: set, new_wall: tuple, board_dim:tuple) -> bool:
    """Checks if wall placement is valid. Returns True if valid."""
    is_wall_out_of_bounds(new_wall, board_dim)
    for wall in placed_walls:
        if new_wall != 0:
            if is_walls_overlap(wall, new_wall):
                return False
    return True

def is_hitting_any_wall(placed_walls, old_pos, direction):
    """Returns True if figure trying to move in direction from old_pos is hitting a wall."""
    # NOTE: direction: u (up), d (down), l (left), r (right), ul (up left), ur (up right), dl (down left), dr (down right)
    constraints_list = list()
    if direction == 'r':
        constraints_list = [{(old_pos[0] - 1, old_pos[1], 'g')}, {(old_pos[0] - 1, old_pos[1] + 1, 'g')}, 
                            {(old_pos[0], old_pos[1], 'g')}, {(old_pos[0], old_pos[1] + 1, 'g')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'l':
        constraints_list = [{(old_pos[0] - 1, old_pos[1] - 1, 'g')}, {(old_pos[0] - 1, old_pos[1] - 2, 'g')}, 
                            {(old_pos[0], old_pos[1] - 1, 'g')}, {(old_pos[0], old_pos[1] - 2, 'g')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'd':
        constraints_list = [{(old_pos[0], old_pos[1] - 1, 'b')}, {(old_pos[0] + 1, old_pos[1] - 1, 'b')}, 
                            {(old_pos[0], old_pos[1], 'b')}, {(old_pos[0] + 1, old_pos[1], 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'u':
        constraints_list = [{(old_pos[0] - 1, old_pos[1] - 1, 'b')}, {(old_pos[0] - 2, old_pos[1] - 1, 'b')}, 
                            {(old_pos[0] - 1, old_pos[1], 'b')}, {(old_pos[0] - 2, old_pos[1], 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True

    elif direction == 'dr':
        constraints_list = [{(old_pos[0], old_pos[1], 'g')}, {(old_pos[0], old_pos[1], 'b')},
                            {(old_pos[0] - 1, old_pos[1], 'g'), (old_pos[0], old_pos[1] - 1, 'b')}, 
                            {(old_pos[0] + 1, old_pos[1], 'g'), (old_pos[0], old_pos[1] + 1, 'b')}, 
                            {(old_pos[0] - 1, old_pos[1], 'g'), (old_pos[0] + 1, old_pos[1], 'g')}, 
                            {(old_pos[0], old_pos[1] - 1, 'b'), (old_pos[0], old_pos[1] + 1, 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'dl':
        constraints_list = [{(old_pos[0], old_pos[1] - 1, 'g')}, {(old_pos[0], old_pos[1] - 1, 'b')},
                            {(old_pos[0] - 1, old_pos[1] - 1, 'g'), (old_pos[0], old_pos[1], 'b')}, 
                            {(old_pos[0] + 1, old_pos[1] - 1, 'g'), (old_pos[0], old_pos[1] - 2, 'b')}, 
                            {(old_pos[0] - 1, old_pos[1] - 1, 'g'), (old_pos[0] + 1, old_pos[1] - 1, 'g')}, 
                            {(old_pos[0], old_pos[1], 'b'), (old_pos[0], old_pos[1] - 2, 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'ur':
        constraints_list = [{(old_pos[0] - 1, old_pos[1], 'g')}, {(old_pos[0] - 1, old_pos[1], 'b')},
                            {(old_pos[0], old_pos[1], 'g'), (old_pos[0] - 1, old_pos[1] - 1, 'b')}, 
                            {(old_pos[0] - 2, old_pos[1], 'g'), (old_pos[0] - 1, old_pos[1] + 1, 'b')}, 
                            {(old_pos[0], old_pos[1], 'g'), (old_pos[0] - 2, old_pos[1], 'g')}, 
                            {(old_pos[0] - 1, old_pos[1] - 1, 'b'), (old_pos[0] - 1, old_pos[1] + 1, 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True
    elif direction == 'ul':
        constraints_list = [{(old_pos[0] - 1, old_pos[1] - 1, 'g')}, {(old_pos[0] - 1, old_pos[1] - 1, 'b')},
                            {(old_pos[0], old_pos[1] - 1, 'g'), (old_pos[0] - 1, old_pos[1], 'b')}, 
                            {(old_pos[0] - 2, old_pos[1] - 1, 'g'), (old_pos[0] - 1, old_pos[1] - 2, 'b')}, 
                            {(old_pos[0], old_pos[1] - 1, 'g'), (old_pos[0] - 2, old_pos[1] - 1, 'g')}, 
                            {(old_pos[0] - 1, old_pos[1], 'b'), (old_pos[0] - 1, old_pos[1] - 2, 'b')}]
        for element in constraints_list:
            if element.issubset(placed_walls): return True

    return False

def is_walls_overlap(wall: tuple, new_wall: tuple) -> bool:
    """Returns True if new wall overlaps wall."""
    if wall[0] == new_wall[0] and wall[1] == new_wall[1]: return True
    
    if new_wall[2] == 'g' and wall[2] == 'g':
        if new_wall[1] == wall[1] and abs(new_wall[0] - wall[0]) == 1:
            return True
    elif new_wall[2] == 'b' and wall[2] == 'b':
        if new_wall[0] == wall[0] and abs(new_wall[1] - wall[1]) == 1:
            return True
    return False
        
def is_wall_out_of_bounds(new_wall: tuple, board_dim: tuple) -> bool:
    if any([new_wall[0] < 1, new_wall[0] > board_dim[0] - 1, new_wall[1] < 1, new_wall[1] > board_dim[1] - 1]):
        return True
    else: return False

def is_figure_out_of_bounds(figure_pos: tuple, board_dim: tuple) -> bool:
    if any([figure_pos[0] < 1, figure_pos[0] > board_dim[0], figure_pos[1] < 1, figure_pos[1] > board_dim[1]]):
        return True
    else: return False
      
def get_movement_direction(figure_pos: tuple, old_pos: tuple) -> str:
    """Returns str representing movement direction.     \n 
    u - up                         \n      
    d - down                       \n      
    l - left                       \n      
    r - right                      \n       
    ul - upper left diagonal       \n
    ur - upper right diagonal      \n
    dl - down left diagonal        \n
    dr - down right diagonal 
    """
    direction = ""
    if old_pos[0] > figure_pos[0]: direction += "u"
    elif old_pos[0] < figure_pos[0]: direction += "d"
    if old_pos[1] > figure_pos[1]: direction += "l"
    elif old_pos[1] < figure_pos[1]: direction += "r"
    return direction

def is_figure_blocking_valid(direction: str, opponent_positions: list, figure_pos: tuple, other_figure:tuple, placed_walls: list) -> list:
    """Returns True if figure movement (horizontal or vertical) was blocked by some other figure so that it can be moved only by one position instead of two.
    If no figure is blocking it or the blocking figure is on opponent starting position, or a wall is blocking it, returns False."""
    other_figures = [other_figure, opponent_positions[0], opponent_positions[1]]
    for position in other_figures:
        if direction == 'l':
            if (position[0] == figure_pos[0] and position[1] == (figure_pos[1] - 1) 
                    and (figure_pos[0], figure_pos[1] - 1, 'g') not in placed_walls
                    and (figure_pos[0] - 1, figure_pos[1] - 1, 'g') not in placed_walls): 
                return True
        elif direction == 'r':
            if (position[0] == figure_pos[0] and position[1] == (figure_pos[1] + 1) 
                    and (figure_pos[0], figure_pos[1] + 1, 'g') not in placed_walls
                    and (figure_pos[0] - 1, figure_pos[1] + 1, 'g') not in placed_walls):
                return True
        elif direction == 'u':
            if (position[0] == (figure_pos[0] - 1) and position[1] == figure_pos[1] 
                    and (figure_pos[0] - 1, figure_pos[1] - 1, 'b') not in placed_walls 
                    and (figure_pos[0] - 1, figure_pos[1], 'b') not in placed_walls):
                return True
        elif direction == 'd':
            if (position[0] == (figure_pos[0] + 1) and position[1] == figure_pos[1]
                    and (figure_pos[0], figure_pos[1] - 1, 'b') not in placed_walls
                    and (figure_pos[0], figure_pos[1], 'b') not in placed_walls):
                return True
    return False
