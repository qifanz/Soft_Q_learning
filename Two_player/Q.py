import math


class Q:
    def __init__(self):
        self.gamma = 0.9
        self.alpha = 0.5
        self.values = {}  # state -> pair of action -> value

    def update(self, reward, previous_state, actions, game):
        old_value = self.values.get(previous_state, {}).get(actions, 0)  # Qk(s, apl, aop)
        v_new_state_estimate = self.estimate_v_new_state(game)
        new_value = old_value + self.alpha * (reward + self.gamma * v_new_state_estimate - old_value)
        value_action = self.values.get(previous_state, {})
        value_action[actions] = new_value
        self.values[previous_state] = value_action

    def estimate_v_new_state(self, game):
        possible_actions_player = game.possible_moves()
        sum = 0
        for action in possible_actions_player:
            Q_player = self.get_Q_player(game, action)
            sum += (game.player.get_reference(game.get_state(), action, len(possible_actions_player)) * math.exp(game.player.beta * Q_player))

        return math.log(sum) / game.player.beta

    def get_Q_player(self, game, action):
        possible_actions_opponent = game.possible_moves(player='opponent')
        sum = 0
        for action_op in possible_actions_opponent:
            sum += (game.opponent.get_reference(game.get_state(), action_op, len(possible_actions_opponent)) * math.exp(
                game.opponent.beta * self.values.get(game.get_state(), {}).get((action_op, action),0)))
        return math.log(sum) / game.opponent.beta

    def get_Q_opponent(self, game, action):
        possible_actions_player = game.possible_moves(player='player')
        sum = 0
        for action_pl in possible_actions_player:
            sum += (game.player.get_reference(game.get_state(), action_pl, len(possible_actions_player)) * math.exp(
                game.player.beta * self.values.get(game.get_state(), {}).get((action_pl, action),0)))
        return math.log(sum) / game.player.beta
