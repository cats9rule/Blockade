class State:
    def __init__(self, player1_positions: PlayerPositions, player2_positions: PlayerPositions, wall_positions: list[WallPosition], is_player1_on_move: bool):
        self.player1_positions = player1_positions
        self.player2_positions = player2_positions
        self.wall_positions = wall_positions
        self.is_player1_playing = is_player1_on_move

class PlayerPositions:
    def __init__(self, x1, y1, x2, y2):
        self._figure1 = (x1, y1)
        self._figure2 = (x2, y2)

    def set_figure_position(self, figure_number: int, new_position: tuple):
        if figure_number == 1:
            self._figure1 = new_position
        elif figure_number == 2:
            self._figure2 = new_position
    
    def get_figure_position(self, figure_number: int) -> tuple:
        if figure_number == 1:
            return self._figure1
        elif figure_number == 2:
            return self._figure2

class WallPosition:
    def __init__(self, x: int, y: int, isGreen: bool):
        self.x = x
        self.y = y
        self.isGreen = isGreen

