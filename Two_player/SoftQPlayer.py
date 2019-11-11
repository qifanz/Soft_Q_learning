import random
import Two_player.Reference as ref
import math
import Two_player.util as util
from Two_player.beta_estimator import beta_estimator

class SoftQPlayer:
    def __init__(self, beta, use_estimation = False):
        self.epsilon = 0.9
        self.beta = beta
        self.use_estimation = use_estimation
        if use_estimation:
            self.beta_estimator = beta_estimator(-15, 0.005)

    def perform_estimation(self, history, Q):
        self.beta_estimator.stochastic_gradient_descent(history, Q)

    def get_beta_estimation(self):
        return self.beta_estimator.get_estimation()

    def choose_move(self, state, Q):
        possible_actions = util.possible_moves(state)
        use_greedy = self.epsilon_greedy()

        if use_greedy:
            return self.get_best_action_based_on_Q(Q, state, possible_actions)
        else:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

    def epsilon_greedy(self):
        rand1 = random.uniform(0, 1)
        use_greedy = rand1 < self.epsilon
        return use_greedy

    def get_best_action_based_on_Q(self, Q, state, possible_actions):
        '''
        Calculate PI (possibility of choosing different actions), random between [1,max],
        return the corresponding action
        :param game: current game
        :param possible_actions: possible actions of player
        :return:
        '''
        possibility_array, action_array = self.get_policy(Q, state, possible_actions)
        hit_value = random.uniform(0, possibility_array[-1])

        previous = 0
        for i in range(len(possibility_array)):
            if hit_value > previous and hit_value < possibility_array[i]:
                return action_array[i]
            else:
                previous = possibility_array[i]
        return action_array[-1]

    def get_policy(self, Q, state, possible_actions):
        possibility_array = []
        action_array = []
        for action in possible_actions:
            if self.beta == 0:
                # Special case: choose from reference directly
                possibility = self.get_reference(state, action, len(possible_actions))
            else:
                possibility = self.get_reference(state, action, len(possible_actions)) * math.exp(
                    self.beta * Q.get_Q_player(state, action, self.use_estimation, self.beta_estimator.get_estimation()))
            if len(possibility_array) == 0:
                possibility_array.append(possibility)
            else:
                possibility_array.append(possibility_array[-1] + possibility)
            action_array.append(action)
        return possibility_array, action_array

    def get_reference(self, state, action, len_actions):
        return ref.ref_player(state, action, len_actions)
