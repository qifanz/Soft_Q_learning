import gym

env = gym.make('Acrobot-v1')
env.reset()

cumulative_reward = 0
for _ in range(1000):
    env.render()
    observation, reward, done, _ = env.step(env.action_space.sample()) # take a random action
    cumulative_reward += reward
    if done:
        print ('game ends, cumulative reward = ', str(cumulative_reward))
        break

