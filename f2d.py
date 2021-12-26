import math
from f2n import get_figure_moves


def h(currentPosition, endPosition):
    x = currentPosition[0] - endPosition[0]
    y = currentPosition[1] - endPosition[1]
    return math.sqrt( x**2 + y**2 )

def a_star(start, end, figure_index, player, player_positions, starting_pos, placed_walls, board_dim):
    found_end = False
    open_set = set()
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    open_set.add(tuple(start, ))

    while len(open_set) > 0 and not found_end:
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + h(next_node, end) < g[node] + h(node, end):
                node = next_node
        
        if node == end:
            found_end = True
            break

        for destination in get_figure_moves(figure_index, node, player, player_positions, starting_pos, placed_walls, board_dim):
            if destination not in open_set and destination not in closed_set:
                open_set.add(destination)
                prev_nodes[destination] = node
                g[destination] = g[node] + 1
            else:
                if g[destination] > g[node] + 1:
                    g[destination] = g[node] + 1
                    prev_nodes[destination] = node
                    if destination in closed_set:
                        closed_set.remove(destination)
                        open_set.add(destination)
        open_set.remove(node)
        closed_set.add(node)
    
    return found_end


def is_path_available(state, starting_pos, board_dim):
    path_available = True
    for player in state['player positions']:
        if player == 'X':
            opponent = 'O'
        elif player == 'O':
            opponent = 'X'

        for figure_pos in state['player positions'][player]:
            figure_index = state['player positions'][player].index(figure_pos)
            for end in starting_pos[opponent]:
                p_a = a_star(figure_pos, end, figure_index, player, state['player positions'], starting_pos, state['placed walls'], board_dim)
                path_available = path_available and p_a
    return path_available