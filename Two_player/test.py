import Two_player.GridWorld
import Two_player.Q
import Two_player.SoftQOpponent
import Two_player.SoftQPlayer
import numpy as np
import matplotlib.pyplot as plt

for beta_player in [20]:
    for beta_op in [-5]:
        n_experience = 10
        n_episode_per_exp = 15000
        cum_reward = np.zeros(n_episode_per_exp)
        beta_estimation = np.zeros(n_episode_per_exp)
        for j in range(n_experience):
            player = Two_player.SoftQPlayer.SoftQPlayer(beta_player, True)
            op = Two_player.SoftQOpponent.SoftQOpponent(beta_op)
            Q = Two_player.Q.Q(player, op)

            for i in range(n_episode_per_exp):
                if i % 10000 == 0 and not i == 0:
                    print(str(i), ' episodes played.')
                game = Two_player.GridWorld.GridWorld(op, player, Q, i)
                reward, error = game.play()
                cum_reward[i] += reward
                beta_estimation[i] += error

            print('Finished ',str(j+1), ' experiences.')
            '''for i in range(10):
                print('Example '+str(i))
                print('********************************************')
                Two_player.GridWorld.GridWorld(op, player, Q).play(print_board=True)
                print('********************************************')
            '''
        cum_reward /= n_experience
        beta_estimation/= n_experience

        smooth_factor = 20
        for i in range(0, n_episode_per_exp, smooth_factor):
            cum_reward[i:i + smooth_factor] = np.mean(cum_reward[i:i + smooth_factor])

        print('beta opponent  = ', beta_op, ' beta player = ', beta_player, ' equilibrium reward = ',
              np.mean(cum_reward[n_episode_per_exp- 500:n_episode_per_exp-1]))
        #np.save('reward.npy',cum_reward)

        plt.plot(cum_reward)
        title = 'Cumulative Reward beta_pl = ' +str(beta_player) +' beta_op = '+str(beta_op)
        plt.title(title)
        plt.xlabel('Episodes')
        plt.ylabel('Cumulative reward')

        plt.plot(beta_estimation)
        title = 'Beta estimation'
        plt.title(title)
        plt.xlabel('Episodes')
        plt.ylabel('Estimated beta')
        plt.show()


