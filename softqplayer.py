import gridworld
import random
import numpy as np
import action_cst
import math


class SoftQPlayer:
    name = 'Soft Q player'
    Q = {}  # dictionary of vector
    lr = 0.05
    discount = 0.9
    epsilon = 0.8
    beta = 10

    def __init__(self):
        self.Q = {}

    def choose_move(self, game: gridworld):

        possible_actions = game.possible_moves(self)
        state = game.pos_p1
        use_greedy = self.epsilon_greedy()

        if use_greedy:
            return self.get_best_action_based_on_Q(state, possible_actions, game.pos_box)
        else:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

    def receive_reward(self, prev_state, action, new_state, reward, game):
        # receive reward for state_action pair
        # update Q value

        action_value = self.Q.get(prev_state, np.zeros(5))
        index_action = action_cst.ACTION_INDEX[action]
        update = self.lr * (
                    reward + self.discount * self.v_estimate_with_kl(new_state, game.possible_moves(self), game.pos_box) -
                    action_value[index_action])

        action_value[index_action] += update
        self.Q[prev_state] = action_value

    def epsilon_greedy(self):
        rand1 = random.uniform(0, 1)
        use_greedy = rand1 < self.epsilon
        return use_greedy

    def get_best_action_based_on_Q(self, state, possible_moves, pos_box):
        action_value = self.Q.get(state, np.zeros(5))
        max = -99999
        best_move = None
        for move in possible_moves:
            index = action_cst.ACTION_INDEX[move]
            pi_star = self.get_reference(state, move, len(possible_moves), pos_box) * math.exp(self.beta * action_value[index])
            if pi_star > max:
                max = pi_star
                best_move = move
        return best_move

    def v_estimate_with_kl(self, new_state, new_actions, pox_box):
        sum = 0
        for action in new_actions:
            reference = self.get_reference(new_state, action, len(new_actions), pox_box)
            expo = math.exp(self.beta * self.Q.get(new_state, np.zeros(5))[action_cst.ACTION_INDEX[action]])
            sum += reference * expo

        return math.log(sum) / self.beta

    def get_reference(self, state, action, count_actions, pos_box):
        row_box = pos_box[0]
        col_box = pos_box[1]
        if state == pos_box:
            if action == action_cst.PICKUP:
                return 0.96
            else:
                return 0.04 / (count_actions - 1)

        if state[0] > row_box and state[1] == col_box:
            if action == action_cst.DOWN:
                return 0.96
            else:
                return 0.04 / (count_actions - 1)

        if state[0] < row_box and state[1] == col_box:
            if action == action_cst.UP:
                return 0.96
            else:
                return 0.04 / (count_actions - 1)

        if state[0] == row_box and state[1] < col_box:
            if action == action_cst.RIGHT:
                return 0.96
            else:
                return 0.04 / (count_actions - 1)

        if state[0] == row_box and state[1] > col_box:
            if action == action_cst.LEFT:
                return 0.96
            else:
                return 0.04 / (count_actions - 1)

        return 1 / count_actions
