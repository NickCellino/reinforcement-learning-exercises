"""
Temporal Difference learning methods

An environment is assumed to support the following operations:
    environment.num_states(): Returns the number of states in the environment
    environment.num_actions(): Returns the number of actions in the environment
    environment.get_random_state(): Returns a random state
    environment.perform_action(a): Returns a reward, the next state (r, s'), and whether
                                   the episode is over

A deterministic policy is a environment.num_states x 1 array
A non-deterministic policy is a environment.num_states x environment.num_actions array
"""
import numpy as np
from tqdm import tqdm

from lib.policy import sample_action, get_epsilon_greedy_policy

def sarsa(
        environment,
        epsilon_func=lambda ep, eps: 0.1,
        alpha_func=lambda n: 0.1,
        episodes=10000
    ):
    Q = np.zeros((environment.num_states(), environment.num_actions()))
    N = np.zeros((environment.num_states(), environment.num_actions()))
    policy = get_epsilon_greedy_policy(Q, (1.0/environment.num_actions()))
    for ep in tqdm(range(episodes)):
        episode_over = False
        s = environment.get_starting_state()
        a = sample_action(policy, s)
        while not episode_over:
            (r, s_prime, episode_over) = environment.perform_action(s, a)

            N[s, a] = N[s, a] + 1

            policy = get_epsilon_greedy_policy(Q, epsilon_func(ep, episodes))
            a_prime = sample_action(policy, s)

            Q[s, a] = Q[s, a] + alpha_func(N[s, a]) * (r + Q[s_prime, a_prime] - Q[s, a])

            s = s_prime
            a = a_prime
    return policy, Q

def q_learning(
        environment,
        epsilon=0.3,
        alpha_func=lambda n: 0.2,
        convergence=0.1
    ):
    Q = np.zeros((environment.num_states(), environment.num_actions()))
    N = np.zeros((environment.num_states(), environment.num_actions()))
    diff = np.inf
    while diff > convergence:
        temp = np.copy(Q)
        # Perform 10,000 episodes, then check how much q has changed
        for ep in tqdm(range(10000)):
            episode_over = False
            s = environment.get_starting_state()
            while not episode_over:
                policy = get_epsilon_greedy_policy(Q, epsilon)
                a = sample_action(policy, s)

                (r, s_prime, episode_over) = environment.perform_action(s, a)

                N[s, a] = N[s, a] + 1
                Q[s, a] = Q[s, a] + alpha_func(N[s, a]) * (r + np.amax(Q[s_prime]) - Q[s, a])

                s = s_prime
        diff = np.sum(np.fabs(np.subtract(Q, temp)))
        print(f'Diff: {diff}')

    return get_epsilon_greedy_policy(Q, 0.0), Q
