from hra.GVFList import GVFList
from hra.GVF import GVF


class GVFFoodList(GVFList):

    def __init__(self, params, game_state):

        GVFList.__init__(self, params, game_state)

        self.pseudo_reward = self.params['gvf_food_pseudo_reward']
        self.pseudo_negative_reward = self.params['gvf_pseudo_negative_reward']

        for x in range(game_state.data.food.width):
            for y in range(game_state.data.food.height):
                if game_state.hasFood(x, y):
                    self.gvf_map[(x, y)] = GVF(actions=self.params["agent_actions"], init_q=self.params["init_q"],
                                 gamma=self.params["gamma"], alpha=self.params["alpha"], learning_method=self.params["learning_method"],
                                 rng=self.params["random_seed"])


    def learn(self, current_game_state, action):

        pacman_index = 0
        pacman_location = current_game_state.getPacmanPosition()
        next_state = current_game_state.generateSuccessor(pacman_index, action)
        next_pacman_location = next_state.getPacmanPosition()

        for food_location in self.gvf_map.keys():

            if food_location != next_pacman_location:
                self.gvf_map[food_location].learn(pacman_location, action, self.pseudo_negative_reward, next_pacman_location, False)

            else:
                self.gvf_map[food_location].learn(pacman_location, action, self.pseudo_reward, next_pacman_location, True)


    def set_location(self, location):
        pass