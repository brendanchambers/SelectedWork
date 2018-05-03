__author__ = 'bc'

import gym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
env = gym.make('CartPole-v0')  # observation space: position (x), velocity (x_dot), angle (theta), angular velocity

N_epochs = 1
N_steps = 1000
N_observ = 4

K_p = 1
K_i = 1
K_d = 1

TARGET_POSITION = 0 # radians
T_RES = 1 # arbitrary regular sampling

state_measurements = np.zeros((N_steps+1, N_observ))
pid_history = np.zeros((N_steps+1, 3)) # [p, i, d]
#predictions = np.zeros((N_observ, N_steps)) # for trying out kalman filtering

for i_episode in range(N_epochs):
    observation = env.reset()
    state_measurements[0,:] = observation

    # pid init
    prior_integral = 0 # running integral (approximate)
    proportional_term = observation[2]*K_p # theta
    integral_term = (prior_integral + proportional_term*T_RES)*K_i # appx numerical integral
    derivative_term = observation[3]*K_d # theta-dot
    pid_history[0,:] = [proportional_term, integral_term, derivative_term]

    next_action = env.action_space.sample() # first action is random

    for t in range(N_steps):
        env.render()
        print(observation)

        #action = env.action_space.sample()
        action = next_action

        observation, reward, done, info = env.step(action)
        state_measurements[t+1,:] = observation

        proportional_term = observation[2]*K_p # theta
        integral_term = (prior_integral + proportional_term*T_RES)*K_i # appx integral
        derivative_term = observation[3]*K_d # theta-dot
        pid_history[t+1,:] = [proportional_term, integral_term, derivative_term]

        pid_sum = proportional_term + integral_term + derivative_term
        if pid_sum > 0:
            next_action = 1 # todo make this more general using the action_space class
        else:
            next_action = 0

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            print info
            break

plt.figure()
titles = ['x','x_dot','theta (radians)','theta_dot (radians)']
for i_observ in range(N_observ):
    plt.subplot(N_observ+1, 1, i_observ+1)
    plt.plot(state_measurements[:,i_observ])
    plt.title(titles[i_observ])
plt.show()

plt.figure()
titles = ['p','i','d']
for i in range(3):
    plt.subplot(4, 1, i+2)
    plt.plot(pid_history[:,i])
    plt.title(titles[i])
plt.subplot(4,1,1)
plt.plot(state_measurements[:,2])
plt.title('theta')
plt.show()





