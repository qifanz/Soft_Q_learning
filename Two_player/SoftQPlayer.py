import random
import Two_player.Reference as ref
import math


class SoftQPlayer:
    epsilon = 0.9
    beta = 5
    def __init__(self):
        pass

    def choose_move(self, game):
        possible_actions = game.possible_moves()
        use_greedy = self.epsilon_greedy()

        if use_greedy:
            return self.get_best_action_based_on_Q(game, possible_actions)
        else:
            return possible_actions[random.randint(0, len(possible_actions) - 1)]

    def epsilon_greedy(self):
        rand1 = random.uniform(0, 1)
        use_greedy = rand1 < self.epsilon
        return use_greedy

    def get_best_action_based_on_Q(self, game, possible_actions):
        '''
        Calculate PI (possibility of choosing different actions), random between [1,max],
        return the corresponding action
        :param game: current game
        :param possible_actions: possible actions of player
        :return:
        '''
        possibility_array = []
        action_array = []
        for action in possible_actions:
            possibility = self.get_reference(game.get_state(), action, len(possible_actions)) * math.exp(
                self.beta * game.Q.get_Q_player(game, action))
            if len(possibility_array) == 0:
                possibility_array.append(possibility)
            else:
                possibility_array.append(possibility_array[-1] + possibility)
            action_array.append(action)
        hit_value = random.uniform(0, possibility_array[-1])

        previous = 0
        for i in range(len(possibility_array)):
            if hit_value>previous and hit_value < possibility_array[i]:
                return action_array[i]
            else:
                previous = possibility_array[i]
        return action_array[-1]


    def get_reference(self, state, action, len_actions):
        return ref.ref_player(state, action, len_actions)
