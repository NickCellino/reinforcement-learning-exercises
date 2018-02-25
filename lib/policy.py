import numpy as np


def sample_action(policy, state):
    """
    Samples a policy for an action given the current state.
    """
    choices = np.arange(0, policy.shape[1])
    probabilities = policy[state]

    return np.random.choice(choices, p=probabilities)


def get_epsilon_greedy_policy(Q, epsilon):
    num_actions = Q.shape[1]
    policy = (epsilon/num_actions) * np.ones(Q.shape)

    greedy_action_indices = np.argmax(Q, axis=1)
    policy[np.arange(0, Q.shape[0]), greedy_action_indices] += (1 - epsilon)

    return policy


def get_greedy_policy(Q):
    return np.argmax(Q, axis=1)