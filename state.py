class State:
    def __init__(self, player1_positions, player2_positions, wall_positions: list, p1_walls_left: tuple, p2_walls_left: tuple, is_p1_on_move: bool):
        self.player1_positions = player1_positions
        self.player2_positions = player2_positions
        self.walls_left = {
            "p1": p1_walls_left,
            "p2": p2_walls_left
        }
        self.wall_positions = wall_positions
        self.is_player1_move = is_p1_on_move

class PlayerPositions:
    def __init__(self, x1, y1, x2, y2):
        self._figure1 = (x1, y1)
        self._figure2 = (x2, y2)

    def set_figure_position(self, figure_number: int, new_position: tuple):
        if figure_number == 1:
            if self._figure2 != new_position: 
                self._figure1 = new_position
                return True
        elif figure_number == 2:
            if self._figure1 != new_position: 
                self._figure2 = new_position
                return True
        return False
    
    def get_figure_position(self, figure_number: int) -> tuple:
        if figure_number == 1:
            return self._figure1
        elif figure_number == 2:
            return self._figure2
    
    def is_position_valid(self, figure_to_check) -> bool:
        if figure_to_check == 1:
            return self._figure1[0] > -1 and self._figure1[1] > -1
        elif figure_to_check == 2:
            return self._figure2[0] > -1 and self._figure2[1] > -1

class WallPosition:
    def __init__(self, x: int, y: int, isGreen: bool):
        self.x = x
        self.y = y
        self.isGreen = isGreen