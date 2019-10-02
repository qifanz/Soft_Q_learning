import action_cst

row_box = 1
col_box = 5
pos_box = (1, 5)


def ref_player(state, action, len_actions):
    if state == pos_box:
        if action == action_cst.PICKUP:
            return 0.96
        else:
            return 0.04 / (len_actions - 1)

    if state[0][0] > row_box and state[1][0] == col_box:
        if action == action_cst.DOWN:
            return 0.96
        else:
            return 0.04 / (len_actions - 1)

    if state[0][0] < row_box and state[1][0] == col_box:
        if action == action_cst.UP:
            return 0.96
        else:
            return 0.04 / (len_actions - 1)

    if state[0][0] == row_box and state[1][0] < col_box:
        if action == action_cst.RIGHT:
            return 0.96
        else:
            return 0.04 / (len_actions - 1)

    if state[0][0] == row_box and state[1][0] > col_box:
        if action == action_cst.LEFT:
            return 0.96
        else:
            return 0.04 / (len_actions - 1)

    return 1 / len_actions


def ref_opponent(state, action, len_actions):
    return 1 / len_actions
