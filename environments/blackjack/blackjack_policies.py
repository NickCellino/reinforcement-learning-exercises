import numpy as np

from environments.blackjack.blackjack import Blackjack, BlackjackStates


class BlackjackPolicy:

    def _get_action_by_state(self, state):
        raise NotImplementedError('This must be implemented.')

    def get_action(self, state_id):
        blackjack_state = BlackjackStates.id_to_state(state_id)
        return self._get_action_by_state(blackjack_state)

    @staticmethod
    def generate_policy(stay_on=[]):
        policy = np.zeros(BlackjackStates.num_states())
        for state_id in range(policy.shape[0]):
            state = BlackjackStates.id_to_state(state_id)
            dealer_card = state[0]
            agent_sum = state[1]
            ace = state[2]
            if agent_sum in stay_on:
                policy[state_id] = Blackjack.STAY_ACTION
            else:
                policy[state_id] = Blackjack.HIT_ACTION
        return policy
