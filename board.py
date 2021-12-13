import pygame
from state import PlayerPositions
import constants
import colors
import math


class SelectMode:
    SELECT_OFF = 0
    SELECT_INIT_P1F1 = 1    #igrac1 figura1
    SELECT_INIT_P1F2 = 2
    SELECT_INIT_P2F1 = 3
    SELECT_INIT_P2F2 = 4
    SELECT_PLAY_P1F1 = 5
    SELECT_PLAY_P1F2 = 6
    SELECT_PLAY_P2F1 = 7
    SELECT_PLAY_P2F2 = 8
    SELECT_PLAY_WALLB = 9
    SELECT_PLAY_WALLG = 10

class Board:
    def __init__(self, num_rows, num_cols, p1_pos, p2_pos):
        self.columns_count = num_cols
        self.rows_count = num_rows
        self._player1_start_positions = p1_pos
        self._player2_start_positions = p2_pos
        self.positionForTest = (-1, -1)
        self.selection_mode = SelectMode.SELECT_OFF
        self.board_rect = None
        self.board_surface = None

        self._cached_fonts = {}
        self._cached_text = {}
#kad kreiras board-a prosledi konstruktoru broj redova i kolona
#p1 i p2_pos stavljaju se player positions sa svim -1, -1, -1, -1
    def set_start_position(self, player_number, figure_number, x, y):
        if player_number == 1:
            self.player1_start_positions.set_figure_position(figure_number, (x,y))
        elif player_number == 2:
            self.player2_start_positions.set_figure_position(figure_number, (x,y))
        return

    def set_selection_mode(self, mode):
        if mode >= 0 and mode <= 10:
            self.selection_mode = mode;
        return

    def get_p1_f1(self) -> tuple:
        return self._player1_start_positions.get_figure_position(1)
    def get_p1_f2(self) -> tuple:
        return self._player1_start_positions.get_figure_position(2)
    def get_p2_f1(self) -> tuple:
        return self._player2_start_positions.get_figure_position(1)
    def get_p2_f2(self) -> tuple:
        return self._player2_start_positions.get_figure_position(2)

    def draw_board(self, surface_to_draw_in, state, should_scale_to_surface: bool):
        dx = dy = self.cell_size = starting_x = starting_y = 0
        width = surface_to_draw_in.get_bounding_rect().width
        height = surface_to_draw_in.get_bounding_rect().height

        if should_scale_to_surface:
            self.cell_size = min((height - 2 * dy) / self.rows_count, (width - 2 * dx) / self.columns_count)
            dx, dy = height / 22
            starting_x = dx
            starting_y = dy
        else:
            self.cell_size = constants.TABLE_CELL
            dx = dy = 16
            starting_x = width / 2 - self.cell_size * self.columns_count / 2
            starting_y = height / 2 - self.cell_size * self.rows_count / 2
        
        self.board_rect = pygame.Rect(
            starting_x, starting_y, 
            self.columns_count * self.cell_size, self.rows_count * self.cell_size
            )
        self.board_surface = pygame.Surface((self.board_rect.width, self.board_rect.height))
        self.board_surface.fill(colors.BACKGROUND_TABLE)
        pygame.draw.rect(surface_to_draw_in, (255, 255, 255), self.board_rect, 6)

        self.draw_starting_positions(self.board_surface, self.cell_size)
        self.draw_grid(self.board_surface, self.cell_size)
        self.draw_indices(surface_to_draw_in, self.cell_size, starting_x, starting_y, dx, dy)
        if state != 0:
            self.draw_players(self.board_surface, state, self.cell_size)
        self.draw_walls(self.board_surface, state, self.cell_size)
        surface_to_draw_in.blit(self.board_surface, (self.board_rect.x, self.board_rect.y))
        return

    def draw_starting_positions(self, surface, cell_size):
        for i in range(1,3):
            if self._player1_start_positions.is_position_valid(i):
                y = self._player1_start_positions.get_figure_position(i)[0] * cell_size
                x = self._player1_start_positions.get_figure_position(i)[1] * cell_size
                player_rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(surface, colors.PLAYER1_STARTTILE, player_rect)
        
            if self._player2_start_positions.is_position_valid(i):
                y = self._player2_start_positions.get_figure_position(i)[0] * cell_size
                x = self._player2_start_positions.get_figure_position(i)[1] * cell_size
                player_rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(surface, colors.PLAYER2_STARTTILE, player_rect)
        
        if(self.positionForTest != (-1, -1)):
            x = self.positionForTest[1] * cell_size
            y = self.positionForTest[0] * cell_size
            player_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, colors.BUTTON_SUCCESS, player_rect)
        return
        
    def draw_grid(self, surface, cell_size):
        width = cell_size * self.columns_count
        height = cell_size * self.rows_count
        x = y = 0

        for i in range(0, self.columns_count + 1):
            pygame.draw.line(surface, (240, 240, 240), (x, 0), (x, height))
            x += cell_size
        for i in range(0, self.rows_count + 1):
            pygame.draw.line(surface, (240, 240, 240), (0, y), (width, y))
            y += cell_size
        return

    def draw_indices(self, surface, cell_size, starting_x, starting_y, dx, dy):
        pygame.font.init()
        x = starting_x + math.floor(cell_size / 2)
        y = starting_y - dy
        width = starting_x + self.columns_count * cell_size
        height = starting_y + self.rows_count * cell_size
        for i in range(0, self.columns_count):
            text = self._create_text(str(hex(i+1).lstrip("0x").rstrip("L").upper()), ["Consolas"], math.floor(cell_size / 2), colors.TEXT_LIGHT)
            surface.blit(text, (x - math.floor(text.get_width() / 2), y))
            surface.blit(text, (x - math.floor(text.get_width() / 2), height + math.floor(text.get_height())))
            x += cell_size

        x = starting_x - dx
        y = starting_y + math.floor(cell_size / 2)

        for i in range(0, self.rows_count):
            text = self._create_text(str(hex(i+1).lstrip("0x").rstrip("L").upper()), ["Consolas"], math.floor(cell_size / 2), colors.TEXT_LIGHT)
            surface.blit(text, (x - math.floor(text.get_width() / 2), y - math.floor(text.get_height() / 2)))
            surface.blit(text, (width + dx, y - math.floor(text.get_height() / 2)))
            y += cell_size
        
        return

    def draw_players(self, board_surface, state, cell_size):

        width = board_surface.get_bounding_rect().width
        height = board_surface.get_bounding_rect().height
        player1_x1 = state.player1_positions.get_figure_position(1)[1] * cell_size + cell_size / 2
        player1_y1 = state.player1_positions.get_figure_position(1)[0] * cell_size + cell_size / 2
        player1_x2 = state.player1_positions.get_figure_position(2)[1] * cell_size + cell_size / 2
        player1_y2 = state.player1_positions.get_figure_position(2)[0] * cell_size + cell_size / 2

        pygame.draw.circle(board_surface, colors.PLAYER1_FIGURE, (player1_y1, player1_x1), cell_size / 2 - 3)
        pygame.draw.circle(board_surface, colors.PLAYER1_FIGURE, (player1_x2, player1_y2), cell_size / 2 - 3)

        player2_x1 = state.player2_positions.get_figure_position(1)[1] * cell_size + cell_size / 2
        player2_y1 = state.player2_positions.get_figure_position(1)[0] * cell_size + cell_size / 2
        player2_x2 = state.player2_positions.get_figure_position(2)[1] * cell_size + cell_size / 2
        player2_y2 = state.player2_positions.get_figure_position(2)[0] * cell_size + cell_size / 2

        pygame.draw.circle(board_surface, colors.PLAYER2_FIGURE, (player2_x1, player2_y1), cell_size / 2 - 3)
        pygame.draw.circle(board_surface, (0,0,0), (player2_x1, player2_y1), cell_size / 2 - 3, 1)
        pygame.draw.circle(board_surface, colors.PLAYER2_FIGURE, (player2_x2, player2_y2), cell_size / 2 - 3)
        pygame.draw.circle(board_surface, (0,0,0), (player2_x2, player2_y2), cell_size / 2 - 3, 1)

        #window.blit(board_surface, (self.board.board_rect.x, self.board.board_rect.y))
        return
    
    def draw_walls(self, board_surface, state, cell_size):
        for wall in state.wall_positions:
            if wall.isGreen:
                x = wall.x * cell_size + cell_size
                y = wall.y * cell_size
                length = cell_size * 2
                pygame.draw.line(board_surface, colors.WALL_GREEN, (x, y), (x, y + length), 4)
            else:
                x = wall.x * cell_size + cell_size
                y = wall.y * cell_size
                length = cell_size * 2
                pygame.draw.line(board_surface, colors.WALL_BLUE, (x, y), (x + length, y), 4)
        return


    def event_onclick(self, x, y):
        row = column = -1
        if self.board_rect.collidepoint(x, y):
            column = math.floor((x - self.board_rect.x) / self.cell_size)
            row = math.floor((y - self.board_rect.y) / self.cell_size)

            if self.selection_mode != SelectMode.SELECT_OFF:
                self.handle_selection(row, column)

        #self.positionForTest = (row, column)
        return (row, column)

    def handle_selection(self, row, column):
        if self.selection_mode == SelectMode.SELECT_INIT_P1F1:
            self._player1_start_positions.set_figure_position(1, (row, column))
        elif self.selection_mode == SelectMode.SELECT_INIT_P1F2:
            self._player1_start_positions.set_figure_position(2, (row, column))
        elif self.selection_mode == SelectMode.SELECT_INIT_P2F1:
            self._player2_start_positions.set_figure_position(1, (row, column))
        elif self.selection_mode == SelectMode.SELECT_INIT_P2F2:
            self._player2_start_positions.set_figure_position(2, (row, column))

        return

    def _make_font(self, fonts, size):
        available = pygame.font.get_fonts()
        # get_fonts() returns a list of lowercase spaceless font names
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