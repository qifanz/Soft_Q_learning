import action_cst


class GridWorld:
    box_picked = False
    pos_box = (1, 5)
    n_row = 5
    n_col = 6

    p1 = None
    pos_p1 = (0, 0)
    cumulative_reward_p1 = 0

    def __init__(self, p1, n_row=5, n_col=6):
        self.p1 = p1
        self.n_col = n_col
        self.n_row = n_row

    def possible_moves(self, player):
        actions = [action_cst.DOWN, action_cst.LEFT, action_cst.RIGHT, action_cst.UP]
        if player == self.p1:
            pos_cur = self.pos_p1
            if pos_cur == self.pos_box:
                actions.append(action_cst.PICKUP)
            if pos_cur[1] == 0:
                actions.remove(action_cst.LEFT)
            if pos_cur[1] >= self.n_col - 1:
                actions.remove(action_cst.RIGHT)
            if pos_cur[0] == 0:
                actions.remove(action_cst.UP)
            if pos_cur[0] >= self.n_row - 1:
                actions.remove(action_cst.DOWN)
        return actions

    def move_p1(self):
        a = self.p1.choose_move(self)
        previous_state = self.pos_p1
        self.pos_p1 = (self.pos_p1[0] + a[0], self.pos_p1[1] + a[1])
        if a == action_cst.PICKUP and self.pos_p1 == self.pos_box:
            self.box_picked = True
            self.p1.receive_reward(previous_state, a, self.pos_p1, 1, self)
            self.cumulative_reward_p1 += 1
        self.p1.receive_reward(previous_state, a, self.pos_p1, -0.02, self)
        self.cumulative_reward_p1 -= 0.02

    def play(self):
        while not self.box_picked:
            # self.print_board()
            self.move_p1()
        print('Episode cumulative reward: ', str(self.cumulative_reward_p1))
        return self.cumulative_reward_p1

    def print_board(self):
        print('************************')
        for i in range(0, self.n_row):
            row = '|'
            row2 = '-'
            for j in range(0, self.n_col):
                row2 += '--'
                if self.pos_p1 == (i, j):
                    row += 'X|'
                elif self.pos_box == (i, j):
                    row += 'O|'
                else:
                    row += ' |'
            print(row)
            print(row2)

        print('************************')
