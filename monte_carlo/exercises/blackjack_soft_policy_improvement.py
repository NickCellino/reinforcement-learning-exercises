from monte_carlo.blackjack import Blackjack, BlackjackStates, BlackjackPlotter
from monte_carlo import mc
import argparse


parser = argparse.ArgumentParser(description='Blackjack Monte Carlo Policy Q Evaluation')

parser.add_argument('--iterations',
                    type=int,
                    help='Number of iterations to run',
                    default=1000000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


blackjack = Blackjack(verbose=args.verbose)
soft_optimal_policy, Q = mc.on_policy_fv_mc_e_soft_control(
    blackjack,
    epsilon_func=lambda ep, eps: 0.0,
    alpha_func=lambda n: 1/n,
    episodes=args.iterations,
    random_start=True
)

optimal_policy = mc.get_greedy_policy(Q)

if args.verbose:
    for state_id in range(optimal_policy.shape[0]):
        print('--------------------------------')
        BlackjackStates.print_state(state_id)
        if (optimal_policy[state_id] == Blackjack.HIT_ACTION):
            print('HIT')
        else:
            print('STAY')

BlackjackPlotter.plot_policies(optimal_policy)