from hra.pacman.Factories import HeadFactory

class HeadCollection:

    def __init__(self, name, params, game_state):

        self.name = name
        self.game_state = game_state
        self.params = params
        self.gvf_list = None

        self.head_map = {}

        HeadFactory.add_heads(self.head_map, self.name, self.params, self.game_state)


    def clear(self):

        self.head_map.clear()

    def reset(self):

        for head_identifier in self.head_map.keys():
            self.head_map[head_identifier].reset()

    def done(self, current_game_state):
        for head_identifier in self.head_map.keys():
            self.head_map[head_identifier].done(current_game_state)

    def get_q(self, agent_location, game_state, gvf_list):

        q = []

        self.gvf_list = gvf_list
        self.game_state = game_state
        self.update_heads()

        for head_identifier in self.head_map.keys():
            q.append(self.head_map[head_identifier].get_q(agent_location))

        return q

    def update_heads(self):

        for head_identifier in self.head_map.keys():
            self.head_map[head_identifier].update(self.gvf_list, self.game_state)