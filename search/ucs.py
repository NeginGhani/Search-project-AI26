# Dijkstra Algorithm

import heapq
import itertools

def ucs(initial_state):

    counter = itertools.count()
    frontier = []
    best_cost = {initial_state: 0}
    All_Nodes = {}
    root_id = next(counter)
    All_Nodes[root_id] = (0, None, initial_state, -1)

    heapq.heappush(frontier, (0, root_id, initial_state))
    min_goal_id = -1

    while frontier:

        cost, pn_id, pn_state = heapq.heappop(frontier)

        if cost > best_cost.get(pn_state, float('inf')):
            continue
        if pn_state.is_goal_state():
            min_goal_id = pn_id
            break
            
        for action, edge_cost, c_state in pn_state.get_successors():
            if c_state.has_weapon() or not c_state.is_collision_state():

                new_cost = cost + edge_cost
                if new_cost < best_cost.get(c_state, float('inf')):
                    best_cost[c_state] = new_cost
                    c_id = next(counter)
                    All_Nodes[c_id] = (new_cost, action, c_state, pn_id)

                    heapq.heappush(frontier, (new_cost, c_id, c_state))

    return reconstruct_path(All_Nodes, min_goal_id)


def reconstruct_path(states_history, goal_id):
    actions_list = []
    state_id = goal_id
    while states_history[state_id][3] != -1:
        action = states_history[state_id][1]
        actions_list.append(action)
        state_id = states_history[state_id][3]

    actions_list.reverse()
    return actions_list
    

