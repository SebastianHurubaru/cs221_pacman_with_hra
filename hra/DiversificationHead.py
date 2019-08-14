import numpy as np

from hra.Head import Head

class DiversificationHead(Head):

    def __init__(self, params):

        self.params = params

        self.no_of_steps = 0

    def reset(self):

        Head.reset(self)
        self.no_of_steps = 0

    def update(self, gvf_list, game_state):
        self.game_state = game_state
        self.no_of_steps += 1

    def done(self, current_game_state):

        if self.no_of_steps > self.params['no_of_steps_to_explore']:
            self.deactivate()

    def get_q(self, agent_location):

        if self.is_active() is True:
            q = np.random.uniform(0, 20, len(self.params['agent_actions']))
        else:
            q = 0.

        return q


