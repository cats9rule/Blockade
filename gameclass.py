from state import *

class Game:
    def __init__(
        self, initial_state: State, table_dimensions: tuple, 
        starting_positions_p1: PlayerPositions, starting_positions_p2: PlayerPositions, 
        initial_wall_count: int, is_player1_first: bool, is_player2_computer: bool
    ):
        self.state = initial_state
        self.table_dimensions = table_dimensions
        self.player1_start = starting_positions_p1
        self.player2_start = starting_positions_p2
        self.number_of_walls = initial_wall_count
        self.is_p1_move = is_player1_first
        self.is_p2_computer = is_player2_computer
    
    def start_game(self):
        #TODO: implement starting game
        return

    def draw(self, window):
        #TODO: implement drawing in window
        return

    def draw_board(self, window):
        #TODO: implement drawing table based on self.table_dimensions and starting positions
        return

    def draw_players(self, window):
        #TODO: implement drawing players as circles on their positions
        return

    def draw_walls(self, window):
        #TODO: implement drawing placed walls
        return

    def draw_stats(self, window, player, is_on_move: bool):
        #TODO: implement drawing status text for player
        return;

    def draw_controls(self, window, player):
        #TODO: draw buttons for walls and finishing move
        return