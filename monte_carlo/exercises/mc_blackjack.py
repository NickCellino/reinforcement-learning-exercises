import matplotlib.pyplot as plt
from monte_carlo.blackjack import *
from monte_carlo.mc import MonteCarlo
import argparse


parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Evaluation')

parser.add_argument('--episodes',
                    type=int,
                    help='Number of episodes to train over',
                    default=10000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


class TwentyTwentyOnePolicy(BlackjackPolicy):

    def _get_action_by_state(self, state):
        player_sum = state[1]
        if player_sum == 20 or player_sum == 21:
            return Blackjack.STAY_ACTION
        return Blackjack.HIT_ACTION


blackjack = Blackjack(verbose=args.verbose)
policy = TwentyTwentyOnePolicy()

value = MonteCarlo.fv_policy_evaluation(blackjack, policy, episodes=args.episodes)

reshaped_value = np.reshape(value, BlackjackStates.value_function_shape())

BlackjackPlotter.plot_value_function(
    reshaped_value[:, :, 0],
    title='Value Function (Usable ace)',
    figure=1
)

BlackjackPlotter.plot_value_function(
    reshaped_value[:, :, 1],
    title='Value Function (No usable ace)',
    figure=2)

plt.show()
