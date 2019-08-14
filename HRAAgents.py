from game import Agent, Directions
import util
from hra.HRAManager import HRAManager

class HRAAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.
    """

    def __init__(self, learn='False'):

        self.gvf_manager = HRAManager(learn)
        self.previous_game_state = None

    def registerInitialState(self, gameState):

        self.gvf_manager.episode_start(gameState)

    def final(self, gameState):

        self.gvf_manager.episode_end(gameState)

    def getQValueAndAction(self, currentGameState):

        pacman_location = currentGameState.getPacmanPosition()
        pacmanIndex = 0
        agent_legal_actions = currentGameState.getLegalActions(pacmanIndex)

        q_value, action = self.gvf_manager.get_action(currentGameState, pacman_location, agent_legal_actions)

        self.previous_game_state = currentGameState

        return q_value, action

    def getAction(self, currentGameState):

        q_value, action = self.getQValueAndAction(currentGameState)
        return action

