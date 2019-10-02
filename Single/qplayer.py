import random
import numpy as np
from Single import gridworld
import action_cst


class QPlayer:
    name = 'Q Learning player'
    Q = {}  # dictionary of vector
    lr = 0.05

    discount = 0.9
    epsilon = 0.8

    def __init__(self):
        self.Q = {}

    def choose_move(self, game: gridworld):

        possible_actions = game.possible_moves(self)
        state = game.pos_p1
        use_greedy = self.epsilon_greedy()

        if use_greedy:
            return self.get_best_action_based_on_Q(state, possible_actions)
        else:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

    def receive_reward(self, prev_state, action, new_state, reward, game):
        # receive reward for state_action pair
        # update Q value
        action_value = self.Q.get(prev_state, np.zeros(5))
        index_action = action_cst.ACTION_INDEX[action]
        new_state_action_value = self.Q.get(new_state, np.zeros(5))

        update = self.lr * (reward + self.discount * (np.max(new_state_action_value)) - action_value[index_action])

        action_value[index_action] += update
        self.Q[prev_state] = action_value

    def epsilon_greedy(self):
        rand1 = random.uniform(0, 1)
        use_greedy = rand1 < self.epsilon
        return use_greedy

    def get_best_action_based_on_Q(self, state, possible_moves):
        action_value = self.Q.get(state, np.zeros(5))
        max = -99999
        best_move = None
        for move in possible_moves:
            index = action_cst.ACTION_INDEX[move]
            if action_value[index] > max:
                max = action_value[index]
                best_move = move
        return best_move
