OPPOSITE = {
'U': 'D',
'D': 'U',
'L': 'R',
'R': 'L'
}

def dls(initial_state):
    targets_dists = targets_grid(initial_state)
    lower_bound = get_mst(targets_dists)
    depth = lower_bound
    solution = None
    while not solution:
        solution = traverse(initial_state, depth)
        depth += 1
        
    return solution
 

def traverse(initial_state, depth_limit):
    search_stack = [] # Node: (state, actions_from_root)
    states_hist = set()
    states_hist.add(initial_state)
    search_stack.append((initial_state, []))

    while search_stack:
        p_state, p_actions = search_stack.pop()
        if p_state.is_goal_state():
            return p_actions
        
        if len(p_actions) < depth_limit:
            expanded = p_state.get_successors()

            if p_actions:
                expanded = sort_children(p_actions[-1], expanded)            
            for c_action, _, c_state in expanded:

                if c_state in states_hist:
                    continue                
                if c_state.has_weapon() or (not c_state.is_collision_state()):
                    states_hist.add(c_state)
                    new_actions = p_actions + [c_action]                                               
                    search_stack.append((c_state, new_actions))

    return None

def sort_children(p_dir, expand):

    def action_priority(action):
        if action == p_dir:
            return 2
        if action == OPPOSITE[p_dir]:
            return 0
        else:
            return 1
        

    if p_dir == None:
        return expand
    
    expand.sort(key=lambda x: action_priority(x[0]))
    return expand
    



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



def targets_grid(state):    # Initialize a Complete graph connecting shards
    targets = list(state.get_targets_positions())
    targets.append(state.get_agent_position())
    grid_size = len(targets)
    grid = [[0] * grid_size for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(i, grid_size):
            dist = manhattan(targets[i], targets[j])
            grid[i][j] = dist
            grid[j][i] = dist
    return grid

   


def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
