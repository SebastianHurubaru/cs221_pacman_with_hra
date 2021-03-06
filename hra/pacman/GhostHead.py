from hra.Head import Head

class GhostHead(Head):

    def __init__(self, params, index):

        Head.__init__(self, params, None)
        self.index = index

        self.environment_reward = params['ghost_env_reward']

    def update(self, gvf_list, game_state):

        self.location = game_state.getGhostPosition(self.index)
        self.gvf = gvf_list.gvf_map[(int(self.location[0]), int(self.location[1]))]


        ghost_state = game_state.getGhostState(self.index)
        if ghost_state.scaredTimer > 0:
            self.deactivate()
        else:
            self.activate()