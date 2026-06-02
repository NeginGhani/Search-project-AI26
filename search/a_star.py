import heapq
import itertools
from .node import Node
from env.constants import SNOW_PASSING_COST, ENEMY_KILL_REWARD

def a_star(initial_state):
    frontier = []   # Priority queue -> (fn, gn, id, state, path_from_root)
    visited = set() # Keeps visited states
    id_counter = itertools.count()
    global dist_grid    # Cash distances between all targets
    global target_index # Stores all targets as a list for consitency
    
    targets, dist_grid = targets_grid(initial_state)
    target_index = {pos: i for i, pos in enumerate(targets)}

    hn = heuristic(initial_state)
    # (state, fn, gn, id, path)
    initial_node = Node(initial_state, hn, 0, next(id_counter), [])
    heapq.heappush(frontier, initial_node)
    
    while frontier:
        p_node = heapq.heappop(frontier)    # P: Parent
        if p_node.is_goal():
            return p_node.get_node_path()
        
        if p_node in visited:
            continue

        visited.add(p_node)
        # if a sub-problem was solved:
        if p_node.target_num() < initial_node.target_num():
            frontier = []
            visited = set()
            initial_node = p_node   

        p_state, p_gn, p_path = p_node.get_nodes_info()
        expand = p_state.get_successors()

        for c_state in expand:   # C: Child
            c_act, c_cost, c_state = c_state
            if c_state.has_weapon() or (not c_state.is_collision_state()):

                c_hn = heuristic(c_state)
                c_gn = p_gn + c_cost                    
                c_fn =  c_gn + c_hn
                c_path = p_path + [c_act]
                c_node = Node(c_state, c_fn, c_gn, next(id_counter), c_path)

                heapq.heappush(frontier, c_node)        
    return None



def heuristic(state):
    agent_pos = state.get_agent_position()
    targets = list(state.get_targets_positions())
    # MST on targets + agent
    nodes = targets + [agent_pos]
    graph = build_graph(nodes)
    direct_cost = SNOW_PASSING_COST * get_mst(graph)
    weapon_cost = float('inf')
    kill_cost = float('inf')
    # MST on weapon
    if not state.has_weapon() and state.get_weapon_position():
        weapon = state.get_weapon_position()
        weapon_nodes = targets + [weapon]
        weapon_graph = build_graph(weapon_nodes)
        weapon_cost = SNOW_PASSING_COST * (
            manhattan(agent_pos, weapon) + get_mst(weapon_graph)
        )

        # __Penalize approaching enemy without weapon__
        if state.is_enemy_alive():
            enemy_dist = manhattan(agent_pos, state.get_enemy_position())
            close_enemy_cost = max(0, (2-enemy_dist)*8*SNOW_PASSING_COST)    # Danger radius: 1
            weapon_cost += close_enemy_cost
            direct_cost += close_enemy_cost
                    
    # __Reward killing enemy if it is close__
    elif state.has_weapon() and state.is_enemy_alive():
        enemy = state.get_enemy_position()
        enemy_dist = manhattan(enemy, agent_pos)
        next_enemy = state.get_enemy_next_position()
        enemy_next_dist = manhattan(next_enemy, agent_pos)
        if enemy_dist < 2 and enemy_dist < enemy_next_dist:
            kill_cost = direct_cost + (SNOW_PASSING_COST * enemy_next_dist) - ENEMY_KILL_REWARD

    hn = min(direct_cost, weapon_cost, kill_cost)
    return hn


def build_graph(nodes):     # Builds a Complete graph connecting objects
    n = len(nodes)
    graph = [[0]*n for _ in range(n)]
    for x in range(n):
        for y in range (x+1, n):
            d = get_dists(nodes[x], nodes[y])
            graph[x][y] = d
            graph[y][x] = d
    return graph
    


def get_mst(adj_matrix):    # Prim's MST
    n = len(adj_matrix)
    vis = [False] * n
    vis[0] = True
    edges_used = 0
    total = 0
    while edges_used < n-1:
        best_cost = float('inf')
        best_node = -1
        for u in range(n):
            if not vis[u]:
                continue
            for v in range(n):
                if vis[v]:
                    continue
                if adj_matrix[u][v] < best_cost:
                    best_cost = adj_matrix[u][v]
                    best_node = v
        vis[best_node] = True
        total += best_cost
        edges_used += 1
    return total



def targets_grid(state):    # Initialize a Complete graph connecting targets for cashing
    targets = list(state.get_targets_positions())
    grid_size = len(targets)
    grid = [[0] * grid_size for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(i, grid_size):
            dist = manhattan(targets[i], targets[j])
            grid[i][j] = dist
            grid[j][i] = dist
    return targets, grid



def get_dists(p1, p2):  # Uses cashed distances
    if p1 in target_index and p2 in target_index:
        return dist_grid[target_index[p1]][target_index[p2]]
    else:
        return manhattan(p1, p2)
    


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
