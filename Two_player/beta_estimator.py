import Two_player.util as util
import math
import Two_player.Reference as ref
import numpy as np


class beta_estimator:
    def __init__(self, init_estimation, lr):
        self.beta_estimation = init_estimation
        self.lr = lr

    def get_estimation(self):
        return self.beta_estimation

    def get_normalizer(self, state, Q):
        possible_actions = util.possible_moves(state, 'opponent')
        sum = 0
        for action in possible_actions:
            sum += ref.ref_opponent(state, action, len(possible_actions)) * math.exp(
                self.beta_estimation * Q.get_Q_opponent(state, action))
        return sum / 1

    '''
        def get_gradient(self, state, action, Q):
        normalizer = self.get_normalizer(state, Q)
        possible_actions = util.possible_moves(state, 'opponent')
        p_ref = ref.ref_opponent(state, action, len(possible_actions))
        return 2 * Q.get_Q_opponent(state, action) * math.log(p_ref / normalizer * math.exp(
           self.beta_estimation * Q.get_Q_opponent(state, action)))
    '''

    def get_gradient(self, state, action, Q):
        b = self.beta_estimation
        possible_actions = util.possible_moves(state, 'opponent')
        Qs = []
        for possible_action in possible_actions:
            Qs.append(Q.get_Q_opponent(state, possible_action))
        Q_action = Q.get_Q_opponent(state, action)
        upper_left = 0
        for i in range(len(Qs)):
            upper_left += Qs[i] * math.exp(Qs[i] * b)
        upper_left_divisor = 0
        for i in range(len(Qs)):
            upper_left_divisor += math.exp(Qs[i] * b)
        return upper_left / upper_left_divisor - Q_action

    def stochastic_gradient_descent(self, dataset, Q):
        '''
        :param dataset: dataset should be a list of tuple. {state, action}
        :return: void
        '''
        update = 0
        for pair in dataset:
            update += self.lr * self.get_gradient(pair[0], pair[1], Q)
        self.beta_estimation -= update
