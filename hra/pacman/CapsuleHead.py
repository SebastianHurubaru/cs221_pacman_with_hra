from hra.Head import Head

class CapsuleHead(Head):

    def __init__(self, params, location):

        Head.__init__(self, params, location)

        self.environment_reward = params['capsule_env_reward']



