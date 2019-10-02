import action_cst


class GridWorld:


    def __init__(self, p1, p2, Q, episode, n_row=5, n_col=6):
        self.opponent = p1
        self.player = p2
        self.n_col = n_col
        self.n_row = n_row
        self.Q = Q
        self.pos_box = (1, 5)
        self.box_picked = False
        self.pos_opponent = (1, 5)
        self.pos_player = (0, 0)
        self.cumulative_reward = 0
        self.episode = episode

    def get_state(self):
        return self.pos_opponent, self.pos_player

    def possible_moves(self, player="player"):
        actions = [action_cst.DOWN, action_cst.LEFT, action_cst.RIGHT, action_cst.UP]

        if player == "player":
            pos_cur = self.pos_player
        else:
            pos_cur = self.pos_opponent

        if pos_cur[1] == 0:
            actions.remove(action_cst.LEFT)
        if pos_cur[1] >= self.n_col - 1:
            actions.remove(action_cst.RIGHT)
        if pos_cur[0] == 0:
            actions.remove(action_cst.UP)
        if pos_cur[0] >= self.n_row - 1:
            actions.remove(action_cst.DOWN)

        if player == "player":
            if pos_cur == self.pos_box:
                actions.append(action_cst.PICKUP)
        return actions

    def move(self):
        action_player = self.player.choose_move(self)
        action_opponent = self.opponent.choose_move(self)

        previous_state = (self.pos_opponent, self.pos_player)

        valid_op, new_pos_op = self.update_pos(action_opponent, previous_state[1], previous_state[0], previous_state[1])
        if valid_op:
            self.pos_opponent = new_pos_op

        valid_pl, new_pos_pl = self.update_pos(action_player, previous_state[0], previous_state[1], self.pos_opponent)
        if valid_pl:
            self.pos_player = new_pos_pl

        if self.pos_box == self.pos_player and action_player == action_cst.PICKUP:
            self.box_picked = True

        return action_opponent, action_player

    def update_pos(self, action, previous_pos_op, previous_pos_self, current_pos_op):
        new_x_self = previous_pos_self[0] + action[0]
        new_y_self = previous_pos_self[1] + action[1]
        if new_x_self == previous_pos_op[0] and new_y_self == previous_pos_op[1]:
            return False, None
        if new_x_self == current_pos_op[0] and new_y_self == current_pos_op[1]:
            return False, None
        return True, (new_x_self, new_y_self)

    def reward(self):
        if self.box_picked:
            reward = 1
        else:
            reward = -0.02
        self.cumulative_reward += reward
        return reward

    def play(self, print_board = False):
        n_moves = 0
        while not self.box_picked and n_moves < 100:
            if print_board:
                self.print_board()
            previous_state = (self.pos_opponent, self.pos_player)
            actions = self.move()
            self.Q.update(self.reward(), previous_state,actions, self)
            n_moves+=1
        #print('Episode cumulative reward: ', str(self.cumulative_reward))
        return self.cumulative_reward

    def print_board(self):
        print('************************')
        for i in range(0, self.n_row):
            row = '|'
            row2 = '-'
            for j in range(0, self.n_col):
                row2 += '--'
                if self.pos_opponent == (i, j):
                    row += 'X|'
                elif self.pos_player == (i, j):
                    row += 'Y|'
                elif self.pos_box == (i, j):
                    row += 'O|'
                else:
                    row += ' |'
            print(row)
            print(row2)

        print('************************')
