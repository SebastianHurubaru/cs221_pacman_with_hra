from hra.pacman.FoodHead import FoodHead
from hra.pacman.CapsuleHead import CapsuleHead
from hra.pacman.GhostHead import GhostHead
from hra.pacman.ScaredGhostHead import ScaredGhostHead
from hra.DiversificationHead import DiversificationHead

from hra.pacman.GVFFoodList import GVFFoodList
from hra.pacman.GVFCapsuleList import GVFCapsuleList
from hra.pacman.GVFGhostList import GVFGhostList
from hra.pacman.GVFScaredGhostList import GVFScaredGhostList

from hra.LinearAggregator import LinearAggregator
from hra.PosNormNegAggregator import PosNormNegAggregator


class GVFListFactory(object):

    object_dict = {
        "food": GVFFoodList,
        "capsule": GVFCapsuleList,
        "ghost": GVFGhostList,
        "scared_ghost": GVFScaredGhostList
    }

    @staticmethod
    def create_gvf_list(name, params, game_state):

        gvf_list_object = GVFListFactory.object_dict.get(name)

        if gvf_list_object is not None:
            return gvf_list_object(params, game_state)
        else:
            return None

class HeadFactory(object):

    object_dict = {
        "food": FoodHead,
        "capsule": CapsuleHead,
        "ghost": GhostHead,
        "scared_ghost": ScaredGhostHead,
        "diversification": DiversificationHead
    }

    @staticmethod
    def create_head(name, params, location):

        head_object = HeadFactory.object_dict.get(name)

        return head_object(params, location)

    @staticmethod
    def add_heads(heads, name, params, game_state):

        head_object = HeadFactory.object_dict.get(name)
        if name == 'food':
            for x in range(game_state.data.food.width):
                for y in range(game_state.data.food.height):
                    if game_state.hasFood(x, y) is True:
                        heads[(x, y)] = head_object(params, (x, y))

        elif name == 'capsule':
            for capsule in game_state.getCapsules():
                heads[capsule] = head_object(params, capsule)

        elif name == 'ghost' or name == 'scared_ghost':
            for idx in range(1, game_state.getNumAgents()):
                heads[name + '_' + str(idx)] = head_object(params, idx)

        elif name == 'exploration':
            head_object = HeadFactory.object_dict.get("diversification")
            heads['diversification'] = head_object(params)


class AggregatorFactory(object):

    object_dict = {
        "linear": LinearAggregator,
        "posnormneg": PosNormNegAggregator
    }

    @staticmethod
    def create_aggregator(name):

        aggregator_object = AggregatorFactory.object_dict.get(name)

        if aggregator_object is not None:
            return aggregator_object()
        else:
            return None