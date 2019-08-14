from hra.GVFList import GVFList
from hra.GVF import GVF


class GVFCapsuleList(GVFList):

    def __init__(self, params, game_state):

        GVFList.__init__(self, params, game_state)

        for capsule in game_state.getCapsules():
            self.gvf_map[capsule] = GVF(actions=self.params["agent_actions"], init_q=self.params["init_q"],
                         gamma=self.params["gamma"], alpha=self.params["alpha"], learning_method=self.params["learning_method"],
                         rng=self.params["random_seed"])

        self.pseudo_reward = self.params['gvf_capsule_pseudo_reward']
        self.pseudo_negative_reward = self.params['gvf_pseudo_negative_reward']

    def done(self, current_game_state):

        pacman_location = current_game_state.getPacmanPosition()

        for gvf_idx, gvf_goal in enumerate(self.init_game_state.getCapsules()):

            if gvf_goal == pacman_location:
                self.gvf_map[gvf_idx].deactivate()

    def learn(self, current_game_state, action):

        pacman_index = 0
        pacman_location = current_game_state.getPacmanPosition()
        next_state = current_game_state.generateSuccessor(pacman_index, action)
        next_pacman_location = next_state.getPacmanPosition()

        for capsule_location in self.gvf_map.keys():

            if capsule_location != next_pacman_location:
                self.gvf_map[capsule_location].learn(pacman_location, action, self.pseudo_negative_reward, next_pacman_location, False)

            else:
                self.gvf_map[capsule_location].learn(pacman_location, action, self.pseudo_reward, next_pacman_location, True)


    def set_location(self, location):
        pass