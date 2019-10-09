import Two_player.GridWorld
import Two_player.Q
import Two_player.SoftQOpponent
import Two_player.SoftQPlayer
import numpy as np
import matplotlib.pyplot as plt

for beta_player in [20,10,5]:
    for beta_op in [20,10,0.1,-5,-10,-20]:
        n_experience = 20
        n_episode_per_exp = 30000
        cum_reward = np.zeros(n_episode_per_exp)
        bellman_error = np.zeros(n_episode_per_exp)
        for j in range(n_experience):
            player = Two_player.SoftQPlayer.SoftQPlayer(beta_player)
            op = Two_player.SoftQOpponent.SoftQOpponent(beta_op)
            Q = Two_player.Q.Q(player, op)

            for i in range(n_episode_per_exp):
                game = Two_player.GridWorld.GridWorld(op, player, Q, i)
                reward, error = game.play()
                cum_reward[i] += reward
                bellman_error[i] += error

           # print('Finished ',str(j+1), ' experiences')
            '''for i in range(10):
                print('Example '+str(i))
                print('********************************************')
                Two_player.GridWorld.GridWorld(op, player, Q).play(print_board=True)
                print('********************************************')
            '''
        cum_reward /= n_experience
        bellman_error/= n_experience

        smooth_factor = 20
        for i in range(0, n_episode_per_exp, smooth_factor):
            cum_reward[i:i + smooth_factor] = np.mean(cum_reward[i:i + smooth_factor])

        print('beta opponent  = ', beta_op, ' beta player = ', beta_player, ' equilibrium reward = ',
              np.mean(cum_reward[n_episode_per_exp- 500:n_episode_per_exp-1]))
        #np.save('reward.npy',cum_reward)

        plt.plot(cum_reward)
       # plt.ylim((-2, 1))
        title = 'Cumulative Reward beta_pl = ' +str(beta_player) +' beta_op = '+str(beta_op)
        plt.title(title)
        plt.xlabel('Episodes')
        plt.ylabel('Cumulative reward')
        plt.show()
'''
        plt.plot(bellman_error)
        plt.title('bellman reward '+str(beta_player)+ " " +str(beta_op))
        plt.xlabel('Episodes')
        plt.ylabel('Bellman error')
        plt.show()
'''