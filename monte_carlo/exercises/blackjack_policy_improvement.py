from monte_carlo.blackjack import Blackjack
from monte_carlo.blackjack_policies import *
from monte_carlo.mc import MonteCarlo
import argparse


parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Q Evaluation')

parser.add_argument('--episodes',
                    type=int,
                    help='Number of episodes to train over',
                    default=1)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


blackjack = Blackjack(verbose=args.verbose)
optimal_policy, Q = MonteCarlo.policy_improvement(blackjack, episodes=args.episodes)

print(optimal_policy)