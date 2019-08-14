import os
import sys
import numpy as np
import yaml
import pickle
import random
import math

from hra.pacman.Factories import GVFListFactory, AggregatorFactory
from hra.HeadCollection import HeadCollection

class HRAManager(object):

    def __init__(self, learning):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        config = os.path.join(dir_path, 'config.yaml')
        with open(config, 'r') as f:
            self.params = yaml.safe_load(f)

        self.rng = np.random.RandomState(self.params['random_seed'])

        self.gvfs = {}

        self.heads = {}

        self.aggregator = AggregatorFactory.create_aggregator(self.params['aggregator'])

        self.learning = eval(learning)

        self.initialized = False;

        self.no_of_episodes = 0

        self.no_of_steps = 0

    def episode_start(self, game_state):

        if self.initialized is False:

            i = 0
            while os.path.exists(os.getcwd() + self.params['folder_location'] + self.params['folder_name'] + str(i)):
                i += 1

            if self.learning is True:

                for head_name in self.params['head_list']:
                    self.heads[head_name] = HeadCollection(head_name, self.params, game_state)
                    gvf_list = GVFListFactory.create_gvf_list(head_name, self.params, game_state)
                    if gvf_list is not None:
                        self.gvfs[head_name] = gvf_list


                self.results_folder = os.getcwd() + self.params['folder_location'] + self.params['folder_name'] + str(i)
                os.mkdir(self.results_folder)

            else:

                self.results_folder = os.getcwd() + self.params['folder_location'] + self.params['folder_name'] + str(i - 1)
                results_state_file = self.results_folder + '/' + self.params['file_name']
                print(results_state_file)
                with open(results_state_file, 'rb') as f:
                    self.gvfs, self.heads = pickle.load(f)

            self.initialized = True

        self.reset()

        self.no_of_episodes += 1

    def episode_end(self, game_state):

        if self.learning is True:
            with open(self.results_folder + '/' + self.params['file_name'], 'wb') as f:
                pickle.dump((self.gvfs, self.heads), f)

    def reset(self):

        self.no_of_steps = 0

        for agent_name in self.heads.keys():
            self.heads[agent_name].reset()

    def done(self, game_state):

        for agent_name in self.heads.keys():
            self.heads[agent_name].done(game_state)

    def learn(self, game_state, action):

        if self.learning is True:

            for agent_name in self.gvfs.keys():
                self.gvfs[agent_name].learn(game_state, action)

    def compute_action(self, agent_location, current_game_state, agent_legal_actions):

        q_aggregate = self.aggregator.get_aggregated_q(self, agent_location, current_game_state, agent_legal_actions)
        action = None
        q_value = None
        while (action not in agent_legal_actions):
            actions = np.where(q_aggregate == q_aggregate.max())[0]  # is biased if using np.argmax(q_aggregate)
            idx = self.rng.choice(actions)
            action = self.params['agent_actions'][idx]
            q_value = q_aggregate[idx]
            q_aggregate[idx] = - sys.maxint - 1

        return q_value, action

    def get_action(self, current_game_state, agent_location, agent_legal_actions):

        q_value, action = self.compute_action(agent_location, current_game_state, agent_legal_actions)
        if self.learning is True:

            self.learn(current_game_state, action)
            self.done(current_game_state)

        else:
            self.done(current_game_state)


        self.no_of_steps += 1

        return q_value, action
