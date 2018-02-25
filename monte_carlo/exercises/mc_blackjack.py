import argparse

from environments.blackjack.blackjack import Blackjack, BlackjackPlotter
from environments.blackjack.blackjack_policies import BlackjackPolicy
from monte_carlo import mc

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


blackjack = Blackjack(verbose=args.verbose)
policy = BlackjackPolicy.generate_policy(stay_on=[20, 21])

value = mc.fv_policy_evaluation(blackjack, policy, episodes=args.episodes)
BlackjackPlotter.plot_value_functions(value)
