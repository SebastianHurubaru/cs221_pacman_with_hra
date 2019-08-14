from hra.Head import Head

class FoodHead(Head):

    def __init__(self, params, location):

        Head.__init__(self, params, location)

        self.environment_reward = params['food_env_reward']
