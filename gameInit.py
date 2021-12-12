#ne znam kako da nazovem fajl
import constants
import state
import label
import colors
import pygame
import buttonstyles
from pygame_button import Button, button

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
        self.p1_start_position_1 = state.PlayerPositions(-1, -1, -1, -1)
        self.p1_start_position_2 = state.PlayerPositions(-1, -1, -1, -1)
        self.p2_start_position_1 = state.PlayerPositions(-1, -1, -1, -1)
        self.p2_start_position_2 = state.PlayerPositions(-1, -1, -1, -1)
        self.btn_next = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_prev = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)
        self.btn_start = Button((0, 0, 0, 0), colors.BUTTON_BASIC, self.do_nothing)

    def do_nothing(self):
        return
    def draw(self, surface):
        btn_rect = pygame.Rect(0, 0, 70, 30)
        if(self.current_step == 0):
            self.draw_screen_0(surface)
            self.btn_next = self.draw_next_button(surface, btn_rect)
        elif(self.current_step == 1):
            self.draw_screen_1(surface)
            self.btn_prev = self.draw_previous_button(surface, btn_rect)
            self.btn_next = self.draw_next_button(surface, btn_rect)
        elif(self.current_step == 2):
            self.draw_screen_2(surface)
            self.btn_prev = self.draw_previous_button(surface, btn_rect)
            self.btn_next = self.draw_next_button(surface, btn_rect)
        elif(self.current_step == 3):
            self.btn_prev = self.draw_previous_button(surface, btn_rect)
            self.btn_next = self.draw_next_button(surface, btn_rect)
            if(self.is_p1_first):
                self.draw_screen_3(surface)
            else:
                self.draw_screen_4(surface)
        elif(self.current_step == 4):
            self.btn_prev = self.draw_previous_button(surface, btn_rect)
            self.btn_start = self.draw_start_button(surface, btn_rect)
            if(self.is_p1_first):
                self.draw_screen_4(surface)
            else:
                self.draw_screen_3(surface)

    def draw_button(self, surface, rect, color, func, pos, txt, buttonstyle):
        btn = Button(
            rect,
            color,
            func,
            text = txt,
            **buttonstyle)
        btn.rect.center = (pos[0], pos[1])
        btn.update(surface)
        return btn

    def draw_next_button(self, surface, rect: pygame.Rect):
        position = (constants.WINDOW_WIDTH - rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        btn = self.draw_button(surface, 
                                rect, 
                                colors.BUTTON_SUCCESS, 
                                self.next_screen, 
                                position, 
                                "Next", 
                                buttonstyles.NEXT_BUTTON)
        return btn

    def draw_start_button(self, surface, rect: pygame.Rect):
        position = (constants.WINDOW_WIDTH - rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        self.draw_button(surface, 
                        rect, 
                        colors.BUTTON_SUCCESS, 
                        self.start_game, 
                        position, 
                        "Start", 
                        buttonstyles.NEXT_BUTTON)

    def draw_previous_button(self, surface, rect: pygame.Rect):
        position = (rect.width * 2, constants.WINDOW_HEIGHT - rect.height * 2)
        self.draw_button(surface,
                        rect,
                        colors.BUTTON_WARNING,
                        self.next_screen,
                        position,
                        "Previous",
                        buttonstyles.PREV_BUTTON)

    
    def start_game(self):
        return

    #draw_screen
    def draw_screen_0(self, surface):
        btn_rect = pygame.Rect(0, 0, 100, 50)
        lab = label.Label("Choose an opponent:", 24, colors.TEXT_LIGHT)
        btn1 = Button(
                btn_rect, 
                colors.PLAYER_HUMAN, 
                self.player2_is_player, 
                text="Human", 
                **buttonstyles.CHOICE_BUTTON)
        # btn2 = Button(
        #         (0, 0, 100, 50), 
        #         colors.PLAYER_COMPUTER, 
        #         self.player2_is_computer, 
        #         text="Computer", 
        #         **buttonstyles.CHOICE_BUTTON)
        btn2 = self.draw_button(
            surface, 
            btn_rect, 
            colors.PLAYER_COMPUTER, 
            self.player2_is_computer, 
            (constants.WINDOW_WIDTH / 2 + btn_rect.width * 2, 150),
            "Computer",
            buttonstyles.CHOICE_BUTTON)

        lab.draw_label(surface, (constants.WINDOW_WIDTH / 2 - lab.size[0] / 2, 50))
        btn1.rect.center = (constants.WINDOW_WIDTH / 2 - btn1.rect.width * 2, 150)
        btn1.update(surface)
        # btn2.rect.center = (constants.WINDOW_WIDTH / 2 + btn2.rect.width * 2, 150)
        # btn2.update(surface)

        btn1.check_event

        pygame.display.update()

    def draw_screen_1(self, surface):
        lab = label.Label("Choose who plays first:", 24, colors.TEXT_LIGHT)
        btn_rect = pygame.Rect(0, 0, 100, 50)
        btn1 = self.draw_button(
            surface,
            btn_rect,
            colors.BUTTON_BASIC,
            self.player1_plays_first,
            (constants.WINDOW_WIDTH / 2 - btn_rect.width * 2, 150),
            "Player1",
            buttonstyles.CHOICE_BUTTON
        )
        btn2 = self.draw_button(
            surface,
            btn_rect,
            colors.BUTTON_BASIC,
            self.player2_plays_first,
            (constants.WINDOW_WIDTH / 2 + btn_rect.width * 2, 150),
            "Player2/Computer",
            buttonstyles.CHOICE_BUTTON
        )

        lab.draw_label(surface, (constants.WINDOW_WIDTH / 2 - lab.size[0] / 2, 50))

            
    #handlers    
    def player2_is_player(self):
        self.is_p2_computer = False
        pygame.display.update()
    def player2_is_computer(self):
        self.is_p2_computer = True
        pygame.display.update()

    def next_screen(self):
        if self.current_step < 4:
            self.current_step += 1
        pygame.display.update()
    def prev_screen(self):
        if self.current_step > 0:
            self.current_step -= 1
        pygame.display.update()

    def player1_plays_first(self):
        self.is_p1_first = True
        pygame.display.update()
    def player2_plays_first(self):
        self.is_p1_first = False
        pygame.display.update()
