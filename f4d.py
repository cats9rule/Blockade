from asyncio.proactor_events import constants
from tracemalloc import start
import faza3

# promena u evaluate(state, starting_pos, board_dim) iz faza3.py

def wall_heuristics(state: dict, starting_pos: dict, board_dim: tuple) -> int:
    player = state['current player']
    opponent = 'X' if player == 'O' else 'O'
    figure_pos = state['player positions'][opponent]
    opponent_base = starting_pos[player]
    wall_h = 0

    for figure in figure_pos:
        for base in opponent_base:
            if figure[0] < base[0] and figure[1] < base[1]:
                constraints_list_1wall = [{(figure[0], figure[1], 'b')}, {(figure[0] + 1, figure[1], 'b')}, 
                                        {(figure[0], figure[1], 'g')}, {(figure[0], figure[1] + 1, 'g')}]
                constraints_list_2walls = [{(figure[0] - 1, figure[1], 'g'), (figure[0], figure[1] - 1, 'b')}, 
                                        {(figure[0] + 1, figure[1], 'g'), (figure[0], figure[1] + 1, 'b')}, 
                                        {(figure[0] - 1, figure[1], 'g'), (figure[0] + 1, figure[1], 'g')}, 
                                        {(figure[0], figure[1] - 1, 'b'), (figure[0], figure[1] + 1, 'b')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)

            if figure[0] < base[0] and figure[1] == base[1]:
                constraints_list_1wall = [{(figure[0], figure[1], 'b')}, {(figure[0] - 1, figure[1], 'b')}, 
                                        {(figure[0] - 1, figure[1] + 1, 'b')}, {(figure[0], figure[1] + 1, 'b')}]
                constraints_list_2walls = [{(figure[0] - 1, figure[1], 'g'), (figure[0], figure[1] - 1, 'b')}, 
                                        {(figure[0] + 1, figure[1], 'g'), (figure[0], figure[1] + 1, 'b')}, 
                                        {(figure[0], figure[1] - 1, 'b'), (figure[0], figure[1] + 1, 'b')}, 
                                        {(figure[0], figure[1] - 2, 'b'), (figure[0], figure[1], 'b')},
                                        {(figure[0], figure[1], 'b'), (figure[0] - 1, figure[1] - 1, 'g')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)

            if figure[0] < base[0] and figure[1] > base[1]:
                constraints_list_1wall = [{(figure[0], figure[1] + 1, 'b')}, {(figure[0] - 1, figure[1] + 1, 'b')}, 
                                        {(figure[0], figure[1] + 1, 'g')}, {(figure[0], figure[1] + 2, 'g')}]
                constraints_list_2walls = [{(figure[0] - 1, figure[1] - 1, 'g'), (figure[0], figure[1], 'b')}, 
                                        {(figure[0] + 1, figure[1] - 1, 'g'), (figure[0], figure[1] + 2, 'b')}, 
                                        {(figure[0] - 1, figure[1] - 1, 'g'), (figure[0] + 1, figure[1] - 1, 'g')}, 
                                        {(figure[0], figure[1], 'b'), (figure[0], figure[1] - 2, 'b')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)
            if figure[0] == base[0] and figure[1] < base[1]:
                constraints_list_1wall = [{(figure[0], figure[1] - 1, 'g')}, {(figure[0] - 1, figure[1] - 1, 'g')}, 
                                        {(figure[0], figure[1], 'g')}, {(figure[0], figure[1] - 1, 'g')}]
                constraints_list_2walls = [{(figure[0] - 1, figure[1], 'g'), (figure[0], figure[1] - 1, 'b')}, 
                                        {(figure[0], figure[1], 'g'), (figure[0] - 1, figure[1] - 1, 'b')}, 
                                        {(figure[0] - 1, figure[1], 'g'), (figure[0] + 1, figure[1], 'g')}, 
                                        {(figure[0], figure[1], 'g'), (figure[0] - 2, figure[1], 'g')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)
            if figure[0] == base[0] and figure[1] > base[1]:
                constraints_list_1wall = [{(figure[0] - 1, figure[1] - 1, 'g')}, {(figure[0] - 1, figure[1] - 2, 'g')}, 
                                        {(figure[0], figure[1] - 1, 'g')}, {(figure[0], figure[1] - 2, 'g')}]
                constraints_list_2walls = [{(figure[0] - 1, figure[1] - 1, 'g'), (figure[0], figure[1], 'b')}, 
                                        {(figure[0], figure[1] - 1, 'g'), (figure[0] - 1, figure[1], 'b')}, 
                                        {(figure[0], figure[1] - 1, 'g'), (figure[0] - 2, figure[1] - 1, 'g')}, 
                                        {(figure[0] - 1, figure[1] - 1, 'g'), (figure[0] + 1, figure[1] - 1, 'g')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)
            if figure[0] > base[0] and figure[1] < base[1]:
                constraints_list_1wall = [{(figure[0] - 1, figure[1], 'g')}, {(figure[0] - 1, figure[1] + 1, 'g')}, 
                                        {(figure[0] - 1, figure[1], 'b')}, {(figure[0] - 2, figure[1], 'b')}]
                constraints_list_2walls = [{(figure[0], figure[1], 'g'), (figure[0] - 2, figure[1], 'g')}, 
                                        {(figure[0] - 1, figure[1] - 1, 'b'), (figure[0] - 1, figure[1] + 1, 'b')}, 
                                        {(figure[0], figure[1], 'g'), (figure[0] - 1, figure[1] - 1, 'b')}, 
                                        {(figure[0] - 2, figure[1], 'g'), (figure[0] - 1, figure[1] + 1, 'b')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)
            if figure[0] > base[0] and figure[1] == base[1]:
                constraints_list_1wall = [{(figure[0] - 1, figure[1] - 1, 'b')}, {(figure[0] - 2, figure[1] - 1, 'b')}, 
                                        {(figure[0] - 1, figure[1], 'b')}, {(figure[0] - 2, figure[1], 'b')}]
                constraints_list_2walls = [{(figure[0], figure[1] - 1, 'g'), (figure[0] - 1, figure[1], 'b')}, 
                                        {(figure[0], figure[1], 'g'), (figure[0] - 1, figure[1] - 1, 'b')}, 
                                        {(figure[0] - 1, figure[1], 'b'), (figure[0] - 1, figure[1] - 2, 'b')}, 
                                        {(figure[0] - 1, figure[1] - 1, 'g'), (figure[0] - 1, figure[1] + 1, 'b')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)
            if figure[0] > base[0] and figure[1] > base[1]:
                constraints_list_1wall = [{(figure[0] - 1, figure[1] - 1, 'g')}, {(figure[0] - 1, figure[1] - 2, 'g')}, 
                                        {(figure[0] - 1, figure[1] - 1, 'b')}, {(figure[0] - 2, figure[1] - 1, 'b')}]
                constraints_list_2walls = [{(figure[0], figure[1] - 1, 'g'), (figure[0] - 1, figure[1], 'b')}, 
                                        {(figure[0] - 2, figure[1] - 1, 'g'), (figure[0] - 1, figure[1] - 2, 'b')}, 
                                        {(figure[0], figure[1] - 1, 'g'), (figure[0] - 2, figure[1] - 1, 'g')}, 
                                        {(figure[0] - 1, figure[1], 'g'), (figure[0] - 1, figure[1] - 2, 'b')}]
                wall_h += calculate_h(constraints_list_1wall, constraints_list_2walls, state)

    return wall_h

def calculate_h(constraints_list_1, constraints_list_2, state):
    wall_h = 0
    for element in constraints_list_1:
        if element.issubset(state['placed walls']):
            wall_h -= 3
    for element in constraints_list_2:
        if element.issubset(state['placed walls']):
            wall_h -= 8
    return wall_h
