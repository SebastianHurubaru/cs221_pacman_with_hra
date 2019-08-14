from hra.Aggregator import Aggregator

import numpy as np

class LinearAggregator(Aggregator):

    def get_aggregated_q(self, manager, agent_location, current_game_state, agent_legal_actions):

        # sum all q's
        q = []

        for head_name in manager.heads.keys():
            if manager.learning is True or head_name not in manager.params['learn_only_head_list']:
                q += manager.heads[head_name].get_q(agent_location, current_game_state, manager.gvfs.get(head_name, None))

        q_aggregate = np.sum(q, axis=0)

        return q_aggregate