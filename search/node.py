
class Node: # Node for A*

    __slots__ = ('state', 'fn', 'gn', 'id', 'path', 'agent_pos', 'enemy_pos',
                 'cycle', 'targets_pos', 'is_weapon_found', 'is_enemy_alive')

    def __init__(self, state, fn, gn, id, path):
        self.state = state
        self.fn = fn
        self.gn = gn
        self.id = id
        self.path = path
        self.agent_pos = state.get_agent_position()
        self.enemy_pos = state.get_enemy_position()
        self.targets_pos = state.get_targets_positions()
        self.cycle = state.get_enemy_cycle()
        self.is_weapon_found = state.has_weapon()
        self.is_enemy_alive = state.is_enemy_alive()

    def __hash__(self):
        return hash((
            self.agent_pos,
            self.enemy_pos,
            self.cycle,
            self.targets_pos,
            self.is_enemy_alive,
            self.is_weapon_found
        ))
    
    def __eq__(self, value):
        return(self.agent_pos == value.agent_pos
               and self.enemy_pos == value.enemy_pos
               and self.targets_pos == value.targets_pos
               and self.cycle == value.cycle
               and self.is_enemy_alive == value.is_enemy_alive
               and self.is_weapon_found == value.is_weapon_found
               )
    
    def __lt__(self, value):
        if self.fn < value.fn:
            return True
        if self.fn == value.fn:
            return self.gn < value.gn
        if self.gn == value.fn:
            return self.id < value.id
        return False
  
    
    def get_node_state(self):
        return self.state
    
    def get_nodes_info(self):   # Used for expantion
        return(self.state,
               self.gn,
               self.path)
    
    def get_node_path(self):
        return self.path
    
    def target_num(self):
        return len(self.targets_pos)
    
    def is_goal(self):
        return self.target_num()==0