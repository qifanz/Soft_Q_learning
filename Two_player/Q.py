import math
import Two_player.util as util


class Q:
    def __init__(self, player, opponent):
        self.gamma = 0.95
        self.alpha = 0.1
        self.values = {}  # state -> pair of action -> value
        self.player = player
        self.opponent = opponent

    def update(self, reward, previous_state, actions, new_state):
        old_value = self.values.get(previous_state, {}).get(actions, 0)  # Qk(s, apl, aop)
        v_new_state_estimate = self.estimate_v_new_state(new_state)
        new_value = old_value + self.alpha * (reward + self.gamma * v_new_state_estimate - old_value)
        value_action = self.values.get(previous_state, {})
        value_action[actions] = new_value
        self.values[previous_state] = value_action
        return (new_value - old_value) ** 2

    def estimate_v_new_state(self, new_state):
        possible_actions_player = util.possible_moves(new_state)
        sum = 0
        for action in possible_actions_player:
            Q_player = self.get_Q_player(new_state, action, self.player.use_estimation,
                                         self.player.get_beta_estimation())
            sum += (self.player.get_reference(new_state, action, len(possible_actions_player)) * math.exp(
                self.player.beta * Q_player))

        return math.log(sum) / self.player.beta

    def get_Q_player(self, state, action, use_estimation, beta_estimation):
        possible_actions_opponent = util.possible_moves(state, player='opponent')
        sum = 0
        if use_estimation:
            beta = beta_estimation
        else:
            beta = self.opponent.beta
        for action_op in possible_actions_opponent:
            sum += (self.opponent.get_reference(state, action_op, len(possible_actions_opponent)) * math.exp(
                beta * self.values.get(state, {}).get((action, action_op), 0)))
        return math.log(sum) / beta

    def get_Q_opponent(self, state, action):
        possible_actions_player = util.possible_moves(state, player='player')
        sum = 0
        for action_pl in possible_actions_player:
            sum += (self.player.get_reference(state, action_pl, len(possible_actions_player)) * math.exp(
                self.player.beta * self.values.get(state, {}).get((action_pl, action), 0)))
        return math.log(sum) / self.player.beta
