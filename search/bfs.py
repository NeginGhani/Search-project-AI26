            
from collections import deque

def bfs(initial_state):

    queue = deque()
    queue.append((initial_state, None, None))  
    # (state, action, parent_node)

    visited_states = {initial_state}
    goal_node = None

    while queue:
        state, action, parent = queue.popleft()

        if state.is_goal_state():
            goal_node = (state, action, parent)
            break

        for action, _, child_state in state.get_successors():

            if child_state not in visited_states:
                if child_state.has_weapon() or not child_state.is_collision_state():
                    visited_states.add(child_state)
                    queue.append((child_state, action, (state, action, parent)))

    return reconstruct_path(goal_node)


def reconstruct_path(node):
    actions = []

    while node is not None:
        _, action, parent = node
        if action is not None:
            actions.append(action)
        node = parent

    return actions[::-1]

