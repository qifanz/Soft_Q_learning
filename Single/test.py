from Single.gridworld import GridWorld
from Single.qplayer import QPlayer
import numpy as np
import matplotlib.pyplot as plt

n_exp = 10
n_episode_per_exp = 20000
cum_reward = np.zeros(n_episode_per_exp)

for j in range(n_exp):
    q_player = QPlayer()
    for i in range(n_episode_per_exp):
        cum_reward[i] = cum_reward[i] + (GridWorld(q_player).play())
cum_reward /= n_exp
plt.plot(cum_reward)
plt.ylim((-2, 1))
plt.title(q_player.name + ' - Mean over ' + str(n_exp) + ' experiences')
plt.xlabel('Episodes')
plt.ylabel('Cumulative reward')
plt.show()
print("All done")
