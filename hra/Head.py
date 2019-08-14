from hra.GVF import GVF

class Head:

    def __init__(self, params, location):

        self.params = params
        self.location = location
        self.game_state = None
        self.gvf = None

        self.active = True

        self.environment_reward = 0.


    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def reset(self):
        self.activate()

    def set_gvf(self, gvf):
        self.gvf = gvf

    def set_location(self, location):
        self.location = location

    def get_q(self, agent_location):
        if self.is_active() is True:
            return self.gvf.get_q(agent_location) * self.environment_reward
        else:
            return 0.

    def done(self, current_game_state):

        pacman_location = current_game_state.getPacmanPosition()

        if self.location == pacman_location:
            self.deactivate()

    def update(self, gvf_list, game_state):
        self.gvf = gvf_list.gvf_map[self.location]
        self.game_state = game_state