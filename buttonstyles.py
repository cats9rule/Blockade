import colors
import pygame as pg

CHOICE_BUTTON = { #dugme koje sluzi za neki izbor (npr. player ili computer)
    "font_color": colors.TEXT_DARK,
    "clicked_font_color": colors.TEXT_LIGHT,
    "clicked_color": colors.BUTTON_CLICKED_BASIC,
    "hover_color": colors.BUTTON_HOVER_BASIC,
}

PREV_BUTTON = { #dugme koje sluzi za povratak nazad
    "font_color": colors.TEXT_DARK,
    "clicked_font_color": colors.TEXT_LIGHT,
    "clicked_color": colors.BUTTON_CLICKED_WARNING,
    "hover_color": colors.BUTTON_HOVER_WARNING,
}

NEXT_BUTTON = {
    "font_color": colors.TEXT_DARK,
    "clicked_font_color": colors.TEXT_LIGHT,
    "clicked_color": colors.BUTTON_CLICKED_BASIC,
    "hover_color": colors.BUTTON_HOVER_BASIC,
}

START_BUTTON = {
    "font_color": colors.TEXT_DARK,
    "clicked_font_color": colors.TEXT_LIGHT,
    "clicked_color": colors.BUTTON_CLICKED_SUCCESS,
    "hover_color": colors.BUTTON_HOVER_SUCCESS,
}