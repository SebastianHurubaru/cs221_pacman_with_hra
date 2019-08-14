from hra.GVFList import GVFList
from hra.GVF import GVF


class GVFGhostList(GVFList):

    def __init__(self, params, game_state):

        GVFList.__init__(self, params, game_state)

        self.pseudo_reward = self.params['gvf_ghost_pseudo_reward']
        self.pseudo_negative_reward = self.params['gvf_pseudo_negative_reward']

        for x in range(game_state.data.layout.width):
            for y in range(game_state.data.layout.height):
                if game_state.hasWall(x, y) is False:
                    self.gvf_map[(x, y)] = GVF(actions=self.params["agent_actions"], init_q=self.params["init_q"],
                                               gamma=self.params["gamma"], alpha=self.params["alpha"],
                                               learning_method=self.params["learning_method"],
                                               rng=self.params["random_seed"])

    def learn(self, current_game_state, action):

        pacman_index = 0
        pacman_location = current_game_state.getPacmanPosition()
        next_state = current_game_state.generateSuccessor(pacman_index, action)
        next_pacman_location = next_state.getPacmanPosition()

        for ghost_gvf_location in self.gvf_map.keys():

            if ghost_gvf_location != next_pacman_location:

                self.gvf_map[ghost_gvf_location].learn(pacman_location, action, self.pseudo_negative_reward,
                                                  next_pacman_location, False)

            else:
                self.gvf_map[ghost_gvf_location].learn(pacman_location, action, self.pseudo_reward, next_pacman_location,
                                                  True)
