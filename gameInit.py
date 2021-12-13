#ne znam kako da nazovem fajl
from types import NoneType
from typing import Text
from pygame.display import update
from pygame.mouse import set_visible
import constants
import state
import label
import colors
import pygame
import buttonstyles
import board
from board import Board
from textinput import TextInput
from pygame_button import Button

class InitGame(object):
    def __init__(self):
        pygame.init() #more da se inicijalizuje tamo gde se koristi
        self.current_step = 0 #vrednosti 0-4
        self.is_p2_computer = False
        self.is_p1_first = True
        self.row_count = -1
        self.column_count = -1
        self.wall_count = -1
        #oba igraca imaju po dve figurice
        self.p1_start_positions = state.PlayerPositions(-1, -1, -1, -1)
        self.p2_start_positions = state.PlayerPositions(-1, -1, -1, -1)
        # self.buttons = dict()
        self.btn1 = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn2 = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_next = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_prev = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_start = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.text_input1 = None
        self.text_input2 = None
        self.text_input3 = None

    def do_nothing(self):
        return
    def draw(self, surface):
        btn_rect = pygame.Rect(0, 0, 70, 30)
        if(self.current_step == 0):
            self.draw_screen_0(surface)

        elif(self.current_step == 1):
            self.draw_screen_1(surface)

        elif(self.current_step == 2):
            self.draw_screen_2(surface)

        elif(self.current_step == 3):
            self.draw_screen_3(surface)

        elif(self.current_step == 4):
            self.draw_screen_4(surface)

        self.draw_navigation_buttons(surface, btn_rect)

    def create_button(self, surface, rect, color, func, pos, txt, buttonstyle):
        btn = Button(
            rect,
            color,
            func,
            text = txt,
            **buttonstyle)
        btn.rect.center = pos
        btn.update(surface)
        return btn

    def create_next_button(self, surface, rect: pygame.Rect):
        position = (constants.WINDOW_WIDTH - rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        btn = self.create_button(surface, 
                                rect, 
                                colors.BUTTON_SUCCESS, 
                                self.next_screen, 
                                position, 
                                "Next", 
                                buttonstyles.NEXT_BUTTON)
        btn.update(surface)
        return btn

    def create_start_button(self, surface, rect: pygame.Rect):
        position = (constants.WINDOW_WIDTH - rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        btn = self.create_button(surface, 
                        rect, 
                        colors.BUTTON_SUCCESS, 
                        self.start_game, 
                        position, 
                        "Start", 
                        buttonstyles.NEXT_BUTTON)
        btn.update(surface)
        return btn

    def create_previous_button(self, surface, rect: pygame.Rect):
        position = (rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        btn = self.create_button(surface,
                        rect,
                        colors.BUTTON_WARNING,
                        self.prev_screen,
                        position,
                        "Previous",
                        buttonstyles.PREV_BUTTON)
        btn.update(surface)
        return btn

    def draw_navigation_buttons(self, surface, btn_rect):
        if self.current_step < 4:
            self.btn_next = self.create_next_button(surface, btn_rect)

        if self.current_step > 0:
            self.btn_prev = self.create_previous_button(surface, btn_rect)

        if self.current_step == 4:
            self.btn_start = self.create_start_button(surface, btn_rect)

    
    def start_game(self):
        return

    #draw_screen
    def draw_screen_0(self, surface):
        self.btn_prev = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_start = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        btn_rect = pygame.Rect(0, 0, 120, 60)
        btn1_text = "Human"
        btn2_text = "Computer"
        lab = label.Label("Choose an opponent:", 48, colors.TEXT_LIGHT)
        lab1 = label.Label("Computer" if self.is_p2_computer else "Player", 48, colors.TEXT_LIGHT)
        self.btn1 = self.create_button(
            surface,
            btn_rect, 
            colors.PLAYER_HUMAN, 
            self.player2_is_player,
            (constants.WINDOW_WIDTH / 2 - btn_rect.width, 200), 
            btn1_text, 
            buttonstyles.CHOICE_BUTTON)
        self.btn2 = self.create_button(
            surface, 
            btn_rect, 
            colors.PLAYER_COMPUTER, 
            self.player2_is_computer, 
            (constants.WINDOW_WIDTH / 2 + btn_rect.width, 200),
            btn2_text,
            buttonstyles.CHOICE_BUTTON)

        lab.draw_label(surface, (constants.WINDOW_WIDTH / 2 - lab.size[0] / 2, 30))
        lab1.draw_label(surface, ((constants.WINDOW_WIDTH / 2 - lab1.size[0] / 2, 70)))
        self.btn1.update(surface)
        self.btn2.update(surface)



    def draw_screen_1(self, surface):
        self.btn_start = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        lab = label.Label("Choose who plays first:", 48, colors.TEXT_LIGHT)
        btn_rect = pygame.Rect(0, 0, 120, 60)
        btn1_text = "Player1"
        btn2_text = "Player2" if not self.is_p2_computer else "Computer"
        self.btn1 = self.create_button(
            surface,
            btn_rect,
            colors.BUTTON_BASIC,
            self.player1_plays_first,
            (constants.WINDOW_WIDTH / 2 - btn_rect.width, 200),
            btn1_text,
            buttonstyles.CHOICE_BUTTON
        )
        self.btn2 = self.create_button(
            surface,
            btn_rect,
            colors.BUTTON_BASIC,
            self.player2_plays_first,
            (constants.WINDOW_WIDTH / 2 + btn_rect.width, 200),
            btn2_text,
            buttonstyles.CHOICE_BUTTON
        )
        
        lab1 = label.Label(btn1_text if self.is_p1_first else btn2_text, 48, colors.TEXT_LIGHT)
        self.btn1.update(surface)
        self.btn2.update(surface)
        lab.draw_label(surface, (constants.WINDOW_WIDTH / 2 - lab.size[0] / 2, 30))
        lab1.draw_label(surface, ((constants.WINDOW_WIDTH / 2 - lab1.size[0] / 2, 70)))

    def draw_screen_2(self, surface):
        self.btn_start = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn1 = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn2 = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        input_rect = pygame.Rect(0, 0, 145, 19)

        lab1 = label.Label("Table size: ", 48, colors.TEXT_LIGHT)
        lab2 = label.Label("Rows: ", 24, colors.TEXT_LIGHT)
        lab3 = label.Label("Columns: ", 24, colors.TEXT_LIGHT)
        lab4 = label.Label("(max 22)", 18, colors.TEXT_LIGHT)
        lab5 = label.Label("(max 28)", 18, colors.TEXT_LIGHT)
        lab6 = label.Label("How many walls?", 36, colors.TEXT_LIGHT)
        lab7 = label.Label("(9-18)", 18, colors.TEXT_LIGHT)

        if self.text_input1 is None:
            self.text_input1 = TextInput(input_rect)
        self.text_input1.move((130, 98))
        self.text_input1.draw_input_box(surface)
        # lab_8 = label.Label(self.text_input1.text, 36, colors.TEXT_LIGHT)
        # lab_8.draw_label(surface, (500, 400))

        input_rect.width = 125
        if self.text_input2 is None:
            self.text_input2 = TextInput(input_rect)
        self.text_input2.move((155, 128))
        self.text_input2.draw_input_box(surface)

        input_rect.width = 200
        if self.text_input3 is None:
            self.text_input3 = TextInput(input_rect)
        self.text_input3.move((65, 308))
        self.text_input3.draw_input_box(surface)

        lab1.draw_label(surface, (60, 40))
        lab2.draw_label(surface, (65, 100))
        lab3.draw_label(surface, (65, 130))
        lab4.draw_label(surface, (300, 100))
        lab5.draw_label(surface, (300, 130))
        lab6.draw_label(surface, (65, 250))
        lab7.draw_label(surface, (300, 310))

    def draw_screen_3(self, surface):
        lab = label.Label("Choose Player1 starting positions: ", 48, colors.TEXT_LIGHT)

        #position_init_board = Board()

    



    def handle_mouse_event(self, pos, event):
        if self.btn_next.rect.collidepoint(pos[0], pos[1]):
            self.btn_next.function()
        if self.btn_prev.rect.collidepoint(pos[0], pos[1]):
            self.btn_prev.function()
        if self.btn_start.rect.collidepoint(pos[0], pos[1]):
            self.btn_start.function()
        if self.btn1.rect.collidepoint(pos[0], pos[1]):
            self.btn1.function()
        if self.btn2.rect.collidepoint(pos[0], pos[1]):
            self.btn2.function()
        if not self.text_input1 is None:
            self.text_input1.event_handle(event)
        if not self.text_input2 is None:
            self.text_input2.event_handle(event)
        if not self.text_input3 is None:    
            self.text_input3.event_handle(event)    

    def handle_keyboard_event(self, event):
        if (self.text_input1.active):
            self.text_input1.event_handle(event)
        if (self.text_input2.active):
            self.text_input2.event_handle(event)
        if (self.text_input3.active):
            self.text_input3.event_handle(event)

    #handlers    
    def player2_is_player(self):
        self.is_p2_computer = False
    def player2_is_computer(self):
        self.is_p2_computer = True

    def next_screen(self):
        if self.current_step < 4:
            self.current_step += 1
    def prev_screen(self):
        if self.current_step > 0:
            self.current_step -= 1

    def player1_plays_first(self):
        self.is_p1_first = True
    def player2_plays_first(self):
        self.is_p1_first = False
