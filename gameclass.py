from state import *
from board import Board
import colors
import constants
import pygame

class Game:
    def __init__(
        self, initial_state: State, table_dimensions: tuple, 
        starting_positions_p1: PlayerPositions, starting_positions_p2: PlayerPositions, 
        initial_wall_count: int, is_player1_first: bool, is_player2_computer: bool
    ):
        self.state = initial_state
        self.board = Board(
            table_dimensions[0], table_dimensions[1], 
            starting_positions_p1, starting_positions_p2
            )
        self.number_of_walls = initial_wall_count
        self.is_p2_computer = is_player2_computer
    
    def start_game(self):
        #TODO: implement starting game
        return

    def draw(self, window):
        self.board.draw_board(window, False)
        self.draw_stats(window, 1, self.state.is_player1_move)
        self.draw_stats(window, 2, not self.state.is_player1_move)
        self.draw_controls(window, 1)
        if not self.is_p2_computer:
            self.draw_controls(window, 2)
        return

    # def draw_board(self, window):
    #     starting_point_x = constants.WINDOW_WIDTH / 2 - self.table_dimensions[0] * constants.TABLE_CELL / 2
    #     starting_point_y = constants.WINDOW_HEIGHT / 2 - self.table_dimensions[1] * constants.TABLE_CELL  / 2
    #     board_rect = pygame.Rect(starting_point_x, starting_point_y, self.table_dimensions[0] * constants.TABLE_CELL, self.table_dimensions[1] * constants.TABLE_CELL)
    #     board_surface = pygame.Surface((board_rect.width, board_rect.height))
    #     board_surface.fill(colors.BACKGROUND_TABLE)
    #     pygame.draw.rect(window, (255, 255, 255), board_rect, 6)
    #     self._draw_starting_positions(board_surface)
    #     self._draw_lines(board_surface)
    #     self.draw_players(board_surface)
    #     self.draw_walls(board_surface)
    #     window.blit(board_surface, (board_rect.x, board_rect.y))

    #     return

    # def _draw_lines(self, board_surface):
    #     width = board_surface.get_bounding_rect().width
    #     height = board_surface.get_bounding_rect().height
    #     increment_y = width / self.table_dimensions[0]
    #     increment_x = height / self.table_dimensions[1]
    #     x = 0
    #     y = 0
    #     for inc in range(0, self.table_dimensions[0] + 1):
    #         pygame.draw.line(board_surface, (255,255,255), (x, 0), (x, height), 1)
    #         x += increment_x
        
    #     for inc in range(0, self.table_dimensions[1] + 1):
    #         pygame.draw.line(board_surface, (255,255,255), (0, y), (width, y), 1)
    #         y += increment_y

    #     return

    # def _draw_starting_positions(self, board_surface):
    #     width = board_surface.get_bounding_rect().width
    #     height = board_surface.get_bounding_rect().height
    #     player1_x1 = (self.player1_start.get_figure_position(1)[0] - 1) * constants.TABLE_CELL
    #     player1_y1 = (self.player1_start.get_figure_position(1)[1] - 1) * constants.TABLE_CELL
    #     player1_x2 = (self.player1_start.get_figure_position(2)[0] - 1) * constants.TABLE_CELL
    #     player1_y2 = (self.player1_start.get_figure_position(2)[1] - 1) * constants.TABLE_CELL

    #     player_rect = pygame.Rect(player1_x1, player1_y1, constants.TABLE_CELL, constants.TABLE_CELL)
    #     pygame.draw.rect(board_surface, colors.PLAYER1_STARTTILE, player_rect)
    #     player_rect.x = player1_x2
    #     player_rect.y = player1_y2
    #     pygame.draw.rect(board_surface, colors.PLAYER1_STARTTILE, player_rect)

    #     player2_x1 = (self.player2_start.get_figure_position(1)[0] - 1) * constants.TABLE_CELL
    #     player2_y1 = (self.player2_start.get_figure_position(1)[1] - 1) * constants.TABLE_CELL
    #     player2_x2 = (self.player2_start.get_figure_position(2)[0] - 1) * constants.TABLE_CELL
    #     player2_y2 = (self.player2_start.get_figure_position(2)[1] - 1) * constants.TABLE_CELL

    #     player_rect = pygame.Rect(player2_x1, player2_y1, constants.TABLE_CELL, constants.TABLE_CELL)
    #     pygame.draw.rect(board_surface, colors.PLAYER2_STARTTILE, player_rect)
    #     player_rect.x = player2_x2
    #     player_rect.y = player2_y2
    #     pygame.draw.rect(board_surface, colors.PLAYER2_STARTTILE, player_rect)

    #     return
        
    def draw_players(self, board_surface):

        width = board_surface.get_bounding_rect().width
        height = board_surface.get_bounding_rect().height
        player1_x1 = (self.state.player1_positions.get_figure_position(1)[0] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player1_y1 = (self.state.player1_positions.get_figure_position(1)[1] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player1_x2 = (self.state.player1_positions.get_figure_position(2)[0] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player1_y2 = (self.state.player1_positions.get_figure_position(2)[1] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2

        pygame.draw.circle(board_surface, colors.PLAYER1_FIGURE, (player1_x1, player1_y1), constants.TABLE_CELL / 2 - 3)
        pygame.draw.circle(board_surface, colors.PLAYER1_FIGURE, (player1_x2, player1_y2), constants.TABLE_CELL / 2 - 3)

        player2_x1 = (self.state.player2_positions.get_figure_position(1)[0] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player2_y1 = (self.state.player2_positions.get_figure_position(1)[1] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player2_x2 = (self.state.player2_positions.get_figure_position(2)[0] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2
        player2_y2 = (self.state.player2_positions.get_figure_position(2)[1] - 1) * constants.TABLE_CELL + constants.TABLE_CELL / 2

        pygame.draw.circle(board_surface, colors.PLAYER2_FIGURE, (player2_x1, player2_y1), constants.TABLE_CELL / 2 - 3)
        pygame.draw.circle(board_surface, (0,0,0), (player2_x1, player2_y1), constants.TABLE_CELL / 2 - 3, 1)
        pygame.draw.circle(board_surface, colors.PLAYER2_FIGURE, (player2_x2, player2_y2), constants.TABLE_CELL / 2 - 3)
        pygame.draw.circle(board_surface, (0,0,0), (player2_x2, player2_y2), constants.TABLE_CELL / 2 - 3, 1)

        return

    def draw_walls(self, board_surface):
        #TODO: implement drawing placed walls
        return

    def draw_stats(self, window, player, is_on_move: bool):
        #TODO: implement drawing status text for player
        return;

    def draw_controls(self, window, player):
        #TODO: draw buttons for walls and finishing move
        return