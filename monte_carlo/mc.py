"""
Monte Carlo methods

An environment is assumed to support the following operations:
    environment.num_states(): Returns the number of states in the environment
    environment.num_actions(): Returns the number of actions in the environment
    environment.get_random_state(): Returns a random state
    environment.perform_action(a): Returns a reward and the next state (r, s')
    environment.is_terminal(s): Returns whether a state is terminal or not

A (deterministic) policy is a environment.num_states x 1 array
"""
import numpy as np
from tqdm import tqdm


def on_policy_fv_mc_e_soft_control():
    pass


def get_greedy_policy(Q):
    return np.argmax(Q, axis=1)


def policy_improvement(environment, iterations=100000):
    policy = np.zeros(environment.num_states(), dtype=int)
    Q = np.zeros((environment.num_states(), environment.num_actions()))
    N = np.zeros((environment.num_states(), environment.num_actions()))
    for i in tqdm(range(iterations)):

        states_seen = one_episode_state_action_values(environment, policy, random_start=True)

        for state, actions_performed in states_seen.items():
            for action, gain in actions_performed.items():
                N[state, action] = N[state, action] + 1
                Q[state, action] = Q[state, action] + (1.0/(N[state, action]))*(gain - Q[state, action])

        policy = get_greedy_policy(Q)

    return policy, Q


def one_episode_state_action_values(environment, policy, random_start=True):
    s = environment.get_random_state()
    states_seen = {}
    first_action = True
    while not environment.is_terminal(s):
        # If this is the first time we've seen this state
        if states_seen.get(s, None) is None:
            states_seen[s] = {}

        if first_action and random_start:
            a = np.random.randint(0, environment.num_actions())
            first_action = False
        else:
            # Perform our action
            a = policy[s]

        # If this is the first time we've performed this action
        # in this state
        if states_seen[s].get(a, None) is None:
            states_seen[s][a] = 0

        (r, s_prime) = environment.perform_action(s, a)

        # Update our gain counters
        states_seen = \
            {
                state: {action: gain + r for action, gain in actions_performed.items()}
                for state, actions_performed
                in states_seen.items()
                }

        # Update current state
        s = s_prime

    return states_seen


def fv_policy_q_evaluation(environment, policy, episodes=10000):
    """
    First visit MC action-value policy evaluation with exploring starts.

    Returns the action-value function.
    """
    Q = np.zeros((environment.num_states(), environment.num_actions()))
    N = np.zeros((environment.num_states(), environment.num_actions()))

    for episode in tqdm(range(episodes)):
        states_seen = one_episode_state_action_values(environment, policy, random_start=True)
        for state, actions_performed in states_seen.items():
            for action, gain in actions_performed.items():
                N[state, action] = N[state, action] + 1
                Q[state, action] = Q[state, action] + (1.0/(N[state, action]))*(gain - Q[state, action])

    return Q


def fv_policy_evaluation(environment, policy, episodes=10000):
    """
    First visit MC policy evaluation.

    Returns the state-value function.
    """
    V = np.zeros(environment.num_states())
    N = np.zeros(environment.num_states())

    for episode in tqdm(range(episodes)):
        s = environment.get_random_state()
        states_seen = {}
        while not environment.is_terminal(s):
            # If this is the first time we've seen this state
            if states_seen.get(s, None) is None:
                states_seen[s] = 0

            # Perform our action
            a = policy[s]
            (r, s_prime) = environment.perform_action(s, a)

            # Update our gain counters
            states_seen = {state: gain + r for state, gain in states_seen.items()}

            # Update current state
            s = s_prime
        for state, gain in states_seen.items():
            N[state] = N[state] + 1
            V[state] = V[state] + (1.0/(N[state]))*(gain - V[state])

    return V