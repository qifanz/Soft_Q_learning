import action_cst


def possible_moves(state, player='player'):
    actions = [action_cst.DOWN, action_cst.LEFT, action_cst.RIGHT, action_cst.UP]

    if player == "player":
        pos_cur = state[1]
    else:
        pos_cur = state[0]

    if pos_cur[1] == 0:
        actions.remove(action_cst.LEFT)
    if pos_cur[1] >= 5:
        actions.remove(action_cst.RIGHT)
    if pos_cur[0] == 0:
        actions.remove(action_cst.UP)
    if pos_cur[0] >= 4:
        actions.remove(action_cst.DOWN)

    if player == "player":
        if pos_cur == (1, 5):
            actions.append(action_cst.PICKUP)
    return actions
