from hra.GVF import GVF

class GVFList():

    def __init__(self, params, game_state):

        self.params = params
        self.init_game_state = game_state

        self.gvf_map = {}

    def add(self, position):
        if position in self.gvf_map.keys() is False:
            self.gvf_map[position] = GVF(actions=self.params["agent_actions"], init_q=self.params["init_q"],
                         gamma=self.params["gamma"], alpha=self.params["alpha"], learning_method=self.params["learning_method"],
                         rng=self.params["random_seed"])

    def get_gvf(self, position):
        return self.gvf_map[position]

    def done(self, current_game_state):
        pass

    def learn(self, current_game_state, action):
        # Hint: ALL gvf agents learn in parallel at each transition (regardless of player's position)
        pass
