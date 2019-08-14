import numpy as np

class GVF:

    def __init__(self, actions, init_q, gamma, alpha, learning_method, rng):

        self.actions = actions
        self.init_q = init_q
        self.q = dict()
        self.gamma = gamma
        self.alpha = alpha
        self.start_alpha = alpha
        self.learning_method = learning_method
        self.rng = np.random.RandomState(rng)

    def _get_q(self, s, a):
        sa = tuple(list(s) + [a])
        if sa in self.q:
            return self.q[sa]
        else:
            self._set_init_q(s)
            return self.init_q

    def get_q(self, s, a=None):
        if a is not None:
            return self._get_q(s, a)
        else:
            return np.asarray([self._get_q(s, a) for a in self.actions], dtype=np.float32)

    def _set_q(self, s, a, q):
        sa = tuple(list(s) + [a])
        if sa not in self.q:
            self._set_init_q(s)
        self.q[sa] = np.float32(q)

    def _set_init_q(self, s):
        s = list(s)
        for a in self.actions:
            self.q[tuple(s + [a])] = np.float32(self.init_q)

    def get_max_action(self, s, stochastic=True):
        values = self.get_q(s)
        if stochastic:
            actions = np.where(values == values.max())[0]
            return self.rng.choice(actions)
        else:
            return np.argmax(values)

    def learn(self, s, a, r, s2, term):

        if term:
            q2 = 0.
        elif self.learning_method == 'max':
            q2 = np.max(self.get_q(s2))
        elif self.learning_method == 'mean':
            q2 = np.mean(self.get_q(s2))
        else:
            raise ValueError('Learning method is not known.')
        delta = r + self.gamma * q2 - self._get_q(s, a)
        self._set_q(s, a, self._get_q(s, a) + self.alpha * delta)



