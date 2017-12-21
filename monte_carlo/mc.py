import numpy as np
from tqdm import tqdm

class MonteCarlo:

    def fv_policy_evaluation(self, environment, policy, episodes=10000):
        """
        First visit MC policy evaluation

        :param environment:
            environment.num_states(): Returns the number of states in the environment
            environment.num_actions(): Returns the number of actions in the environment
            environment.get_random_state(): Returns a random state
            environment.perform_action(a): Returns a reward and the next state (r, s')
            environment.is_terminal(s): Returns whether a state is terminal or not
        :param policy:
            policy.get_action(s): Returns the action
        :return: A value function
        """
        V = np.zeros(environment.num_states())

        for episode in tqdm(range(episodes)):
            s = environment.get_random_state()
            states_seen = {}
            while not environment.is_terminal(s):
                # If this is the first time we've seen this state
                if states_seen.get(s, None) is None:
                    states_seen[s] = 0

                # Perform our action
                a = policy.get_action(s)
                (r, s_prime) = environment.perform_action(a)

                # Update our gain counters
                states_seen = {state: gain + r for state, gain in states_seen.items()}
            for state, gain in states_seen.items():
                V[state] = V[state] + (1.0/(episode+1))*(gain - V[state])

        return V