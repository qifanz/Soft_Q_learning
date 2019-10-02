import Two_player.GridWorld
import Two_player.Q
import Two_player.SoftQOpponent
import Two_player.SoftQPlayer
import numpy as np
import matplotlib.pyplot as plt



n_experience = 25
n_episode_per_exp = 10000
cum_reward = np.zeros(n_episode_per_exp)
for j in range(n_experience):
    Q = Two_player.Q.Q()
    player = Two_player.SoftQPlayer.SoftQPlayer()
    op = Two_player.SoftQOpponent.SoftQOpponent()
    for i in range(n_episode_per_exp):
        game = Two_player.GridWorld.GridWorld(op, player, Q, i)
        cum_reward[i] += game.play()

    print('Finished ',str(j+1), ' experiences')
    '''for i in range(10):
        print('Example '+str(i))
        print('********************************************')
        Two_player.GridWorld.GridWorld(op, player, Q).play(print_board=True)
        print('********************************************')
    '''
cum_reward/=n_experience

smooth_factor = 10
for i in range (0,n_episode_per_exp,smooth_factor):
    cum_reward[i:i+smooth_factor] = np.mean(cum_reward[i:i+smooth_factor])

np.save('reward.npy',cum_reward)

plt.plot(cum_reward)
plt.ylim((-2, 1))
plt.title('')
plt.xlabel('Episodes')
plt.ylabel('Cumulative reward')
plt.show()
