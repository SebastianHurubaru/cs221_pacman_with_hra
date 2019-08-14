from hra.Aggregator import Aggregator

from sklearn.preprocessing import MinMaxScaler, StandardScaler

import numpy as np

class PosNormNegAggregator(Aggregator):

    def get_aggregated_q(self, manager, agent_location, current_game_state, agent_legal_actions):

        # sum all q's
        q_pos = []
        q_neg = []
        q_aggregate = []

        for head_name in manager.heads.keys():
            if manager.learning is True or head_name not in manager.params['learn_only_head_list']:
                if head_name == 'ghost':
                    q_neg += manager.heads[head_name].get_q(agent_location, current_game_state, manager.gvfs.get(head_name, None))
                else:
                    q_pos += manager.heads[head_name].get_q(agent_location, current_game_state, manager.gvfs.get(head_name, None))

        # normalize the positive Qs
        q_pos = np.sum(q_pos, axis=0)
        # q_pos_norm = MinMaxScaler().fit_transform(q_pos.reshape(-1, 1)).reshape(-1, )
        # if np.all(np.isnan(q_pos_norm)):
        #     q_pos_norm = q_pos_norm
        q_pos_norm = StandardScaler().fit_transform(q_pos.reshape(-1, 1)).reshape(-1, )

        # weigh the negative Qs
        q_neg = np.sum(q_neg, axis=0)
        q_neg_weighted = np.multiply(q_neg, manager.params['q_neg_weight_vec'])

        # add the negative weighted Qs
        q_aggregate = q_pos_norm + q_neg_weighted

        return q_aggregate