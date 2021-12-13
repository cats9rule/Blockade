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
        self.state = self.initialize_state(starting_positions_p1, starting_positions_p2, initial_wall_count, is_player1_first)
        self.board = Board(
            table_dimensions[0], table_dimensions[1], 
            starting_positions_p1, starting_positions_p2
            )
        self.number_of_walls = initial_wall_count
        self.is_p2_computer = is_player2_computer

        self.new_wall_position = None
        self.figure_moved = -1
        self.new_player_position = None

        self._cached_fonts = {}
        self._cached_text = {}
    
    def start_game(self):
        #TODO: implement starting game
        return
    
    def initialize_state(self, starting_positions_p1, starting_positions_p2, starting_wall_count, is_player1_first):
        return State(starting_positions_p1, starting_positions_p2, [], 
        (starting_wall_count, starting_wall_count), (starting_wall_count, starting_wall_count), is_player1_first)

    def validate_move(self) -> bool:
        if self.figure_moved < 0: 
            return False
        if self.new_wall_position is None: 
            return False
        for wall in state.wall_positions:
            if wall.x == self.new_wall_position.x or wall.y == self.new_wall_position.y:
                return False
        
        positions = self.state.player2_positions
        if self.state.is_player1_move:
            positions = self.state.player1_positions
            if positions.get_figure_position(1) in [self.board.get_p2_f1(), self.board.get_p2_f2()]: return True
            if positions.get_figure_position(2) in [self.board.get_p2_f1(), self.board.get_p2_f2()]: return True
        else:
            if positions.get_figure_position(1) in [self.board.get_p1_f1(), self.board.get_p1_f2()]: return True
            if positions.get_figure_position(2) in [self.board.get_p1_f1(), self.board.get_p1_f2()]: return True

        difference = abs(positions.get_figure_position(self.figure_moved))[0] - self.new_player_position[0] + abs(positions.get_figure_position(self.figure_moved))[1] - self.new_player_position[1]
        if difference < 2:
            return False

        return positions.set_figure_position(self.figure_moved, self.new_player_position)

    def is_game_end() -> bool:
        if self.state.is_p1_on_move:
            # p2 played potential winning move
            pos = self.state.player2_positions.get_figure_position(1)
            if pos in [self.board.get_p1_f1(), self.board.get_p1_f2()]: return True
            pos = self.state.player2_positions.get_figure_position(2)
            if pos in [self.board.get_p1_f1(), self.board.get_p1_f2()]: return True
        else:
            # p1 played potential winning move
            pos = self.state.player1_positions.get_figure_position(1)
            if pos in [self.board.get_p2_f1(), self.board.get_p2_f2()]: return True
            pos = self.state.player1_positions.get_figure_position(2)
            if pos in [self.board.get_p2_f1(), self.board.get_p2_f2()]: return True
        return False

    def generate_next_state():
        positions_p1 = self.state.player1_positions
        positions_p2 = self.state.player2_positions
        p1_walls_left = self.state.p1_walls_left
        p2_walls_left = self.state.p2_walls_left
        walls = self.state.wall_positions

        if self.state.is_p1_on_move:
            # p2 is next
            positions.p1.set_figure_position(self.figure_moved, self.new_player_position)
            if not self.new_wall_position is None:
                walls.append(self.new_wall_position)
                if self.new_wall_position.isGreen:
                    p1_walls_left = (p1_walls_left[0] - 1, p1_walls_left[1])
                else:
                    p1_walls_left = (p1_walls_left[0], p1_walls_left[1] - 1)
        else:
            # p1 is next
            positions.p2.set_figure_position(self.figure_moved, self.new_player_position)
            if not self.new_wall_position is None:
                walls.append(self.new_wall_position)
                if self.new_wall_position.isGreen:
                    p2_walls_left = (p2_walls_left[0] - 1, p2_walls_left[1])
                else:
                    p2_walls_left = (p2_walls_left[0], p2_walls_left[1] - 1)

        self.state = State(positions_p1, positions_p2, walls, p1_walls_left, p2_walls_left, not self.state.is_p1_on_move)
        return

    def handle_events(self, pos):
        #TODO: handle click events on board, or control buttons (wall placement, figure move, finish or reset move)
        return

    def draw(self, window):
        self.board.draw_board(window, self.state, False)
        player1_coord = (0, window.get_height() - 100)
        player2_coord = (0,0)
        self.draw_stats(window, 1, self.state.is_player1_move, player1_coord)
        self.draw_stats(window, 2, not self.state.is_player1_move, player2_coord)
        if self.state.is_player1_move:
            self.draw_controls(window, 1, player1_coord)
        if not self.is_p2_computer and not self.state.is_player1_move: 
                self.draw_controls(window, 2, player2_coord)
        return

    def draw_stats(self, window, player, is_on_move: bool, init_pos: tuple):
        text = self._create_text("Player " + str(player) + ":", 'Consolas', 32, colors.TEXT_LIGHT);
        window.blit(text, (init_pos[0] + 10, init_pos[1] + 4))
        if is_on_move:
            move_text = self._create_text("PLAYING", 'Consolas', 28, colors.BUTTON_SUCCESS);
            window.blit(move_text, (init_pos[0] + text.get_width() + 50, init_pos[1] + 6))
        key = "p" + str(player)
        text = self._create_text("Green walls left: " + str(self.state.walls_left[key][0]), 'Consolas', 28, colors.WALL_GREEN);
        window.blit(text, (init_pos[0] + 18, init_pos[1] + 40))
        text = self._create_text("Blue walls left: " + str(self.state.walls_left[key][1]), 'Consolas', 28, colors.WALL_BLUE);
        window.blit(text, (init_pos[0] + 18, init_pos[1] + 70))
        return;

    def draw_controls(self, window, player, position):
        if self.state.walls_left["p" + str(player)][0] > 0:
            green_rect = pygame.Rect(position[0] + 200, position[1] + 40, 100, 25)
            pygame.draw.rect(window, colors.WALL_GREEN, green_rect)
            text = self._create_text("Place", 'Consolas', 18, colors.TEXT_LIGHT)
            window.blit(text, (green_rect.x + green_rect.width / 2 - text.get_width() / 2, green_rect.y + green_rect.height / 2 - text.get_height() / 2))
        if self.state.walls_left["p" + str(player)][1] > 0:
            blue_rect = pygame.Rect(position[0] + 200, position[1] + 70, 100, 25)
            pygame.draw.rect(window, colors.WALL_BLUE, blue_rect)
            text = self._create_text("Place", 'Consolas', 18, colors.TEXT_LIGHT)
            window.blit(text, (blue_rect.x + blue_rect.width / 2 - text.get_width() / 2, blue_rect.y + blue_rect.height / 2 - text.get_height() / 2))
        
        width = window.get_width()
        x = window.get_width() - 200
        y = position[1] + 10

        reset_move_rect = pygame.Rect(x, y, 100, 30)
        pygame.draw.rect(window, colors.BUTTON_CLICKED_DANGER, reset_move_rect)
        text = self._create_text("Reset move", 'Consolas', 22, colors.TEXT_LIGHT)
        window.blit(text, (reset_move_rect.x + reset_move_rect.width / 2 - text.get_width() / 2, reset_move_rect.y + reset_move_rect.height / 2 - text.get_height() / 2))

        finish_move_rect = pygame.Rect(x, y + 50, 100, 30)
        pygame.draw.rect(window, colors.BUTTON_CLICKED_SUCCESS, finish_move_rect)
        text = self._create_text("Finish move", 'Consolas', 22, colors.TEXT_LIGHT)
        window.blit(text, (finish_move_rect.x + finish_move_rect.width / 2 - text.get_width() / 2, finish_move_rect.y + finish_move_rect.height / 2 - text.get_height() / 2))
        return


    def _make_font(self, fonts, size):
        available = pygame.font.get_fonts()
        choices = map(lambda x:x.lower().replace(' ', ''), fonts)
        for choice in choices:
            if choice in available:
                return pygame.font.SysFont(choice, size)
        return pygame.font.Font(None, size)
    
    def _get_font(self, font_preferences, size):
        key = str(font_preferences) + '|' + str(size)
        font = self._cached_fonts.get(key, None)
        if font == None:
            font = self._make_font(font_preferences, size)
            self._cached_fonts[key] = font
        return font

    def _create_text(self, text, fonts, size, color):
        key = '|'.join(map(str, (fonts, size, color, text)))
        image = self._cached_text.get(key, None)
        if image == None:
            font = self._get_font(fonts, size)
            image = font.render(text, True, color)
            self._cached_text[key] = image
        return image