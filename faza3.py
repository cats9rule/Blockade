from math import sqrt
import faza2
import faza4
import sys
import copy

def computer_move(state: dict, starting_pos: dict, board_dim: tuple, depth: int) -> dict:
    is_x = True if state['current player'] == 'X' else False
    return minmax(state, depth, is_x, board_dim, starting_pos)

def minmax(state: dict, depth: int, is_player_x: bool, board_dim: tuple, starting_pos: dict) -> dict:
    alpha = (state, -sys.maxsize)
    beta = (state, sys.maxsize)
    if is_player_x: return max_value(state, copy.deepcopy(alpha), copy.deepcopy(beta), depth, board_dim, starting_pos)[0]
    else: return min_value(state, copy.deepcopy(alpha), copy.deepcopy(beta), depth, board_dim, starting_pos)[0]
    
def max_value(state: dict, alpha: tuple, beta: tuple, depth: int, board_dim: tuple, starting_pos: dict) -> int:
    if depth == 0: return (state, evaluate(state, starting_pos, board_dim))
    opponent = 'X' if state['current player'] == 'O' else 'O'
    position_backup = copy.deepcopy(state['player positions'][opponent])
    for next_state in faza2.get_next_state_list(state, board_dim, starting_pos):
        alpha = max(alpha, min_value(next_state, copy.deepcopy(alpha), copy.deepcopy(beta), depth-1, board_dim, starting_pos), key = lambda x: x[1])
        if alpha[1] >= beta[1]: return beta
    alpha[0]['player positions'][opponent] = position_backup
    return alpha

def min_value(state: dict, alpha: tuple, beta: tuple, depth: int, board_dim: tuple, starting_pos: dict) -> int:
    if depth == 0: return (state, evaluate(state, starting_pos, board_dim))
    opponent = 'X' if state['current player'] == 'O' else 'O'
    position_backup = copy.deepcopy(state['player positions'][opponent])
    for next_state in faza2.get_next_state_list(state, board_dim, starting_pos):
        beta = min(beta, max_value(next_state, copy.deepcopy(alpha), copy.deepcopy(beta), depth - 1, board_dim, starting_pos), key = lambda x: x[1])
        if beta[1] <= alpha[1]: return alpha
    beta[0]['player positions'][opponent] = position_backup
    return beta
    
def evaluate(state: dict, starting_pos: dict, board_dim: tuple) -> int:
    player = state['current player']
    opponent = 'X' if player == 'O' else 'O'
    mul = 1 if opponent == 'X' else -1
    figure_pos = state['player positions'][opponent]
    opponent_base = starting_pos[player]
    if (figure_pos[0] in starting_pos[player] 
        or figure_pos[1] in starting_pos[player]):
        return (sqrt(board_dim[0] ** 2 + board_dim[1] ** 2) + 1000) * mul
    else:

        wall_h = faza4.wall_heuristics(state, starting_pos, board_dim)

        distance_f1 = 1 / min(sqrt((figure_pos[0][0] - opponent_base[0][0]) ** 2 + (figure_pos[0][1] - opponent_base[0][1]) ** 2),
                          sqrt((figure_pos[0][0] - opponent_base[1][0]) ** 2 + (figure_pos[0][1] - opponent_base[1][1]) ** 2))
        distance_f2 = 1 / min(sqrt((figure_pos[1][0] - opponent_base[0][0]) ** 2 + (figure_pos[1][1] - opponent_base[0][1]) ** 2),
                          sqrt((figure_pos[1][0] - opponent_base[1][0]) ** 2 + (figure_pos[1][1] - opponent_base[1][1]) ** 2))
        return (distance_f1 + distance_f2 + wall_h) * mul
