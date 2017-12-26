from monte_carlo.racetrack import RaceTrack
from monte_carlo import mc
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Monte Carlo Racetrack Policy Improvement')

parser.add_argument('racetrack',
                    type=str,
                    help='Path to racetrack csv file')
parser.add_argument('policy',
                    type=str,
                    help='Path at which to save policy file')
parser.add_argument('--episodes',
                    type=int,
                    help='Number of episodes to train over',
                    default=1000)
parser.add_argument('--verbose',
                    type=bool,
                    help='Print (a lot of) log messages',
                    default=False)
args = parser.parse_args()


racetrack = RaceTrack(args.racetrack)
policy, Q = mc.on_policy_fv_mc_e_soft_control(
    racetrack,
    epsilon_func=lambda ep, eps: 1 - (ep/eps),
    alpha_func=lambda n: 0.1,
    episodes=args.episodes
)

np.save(args.policy, policy)
