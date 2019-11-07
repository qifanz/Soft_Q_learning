import Two_player.util as util
import math
import Two_player.Reference as ref


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

    def get_gradient(self, state, action, Q):
        normalizer = self.get_normalizer(state, Q)
        possible_actions = util.possible_moves(state, 'opponent')
        p_ref = ref.ref_opponent(state, action, len(possible_actions))
        return 2 * Q.get_Q_opponent(state, action) * math.log(p_ref / normalizer * math.exp(
           self.beta_estimation * Q.get_Q_opponent(state, action)))

    def update(self, state, action, Q):
        self.beta_estimation -= self.lr * self.get_gradient(state, action, Q)

    def stochastic_gradient_descent(self, dataset, Q):
        '''
        :param dataset: dataset should be a list of tuple. {state, action}
        :return: void
        '''
        for pair in dataset:
            self.update(pair[0], pair[1], Q)
        pass
