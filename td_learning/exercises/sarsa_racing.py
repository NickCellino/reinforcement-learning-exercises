from environments.racing.racing import RaceTrack
from td_learning import td
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Sarsa Racetrack Policy Improvement')

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

def epsilon_schedule(ep, eps, r=1.001):
    return ((1 - (r**(-ep))) / (r**(-eps) - 1)) + 1


racetrack = RaceTrack(args.racetrack)
policy, Q = td.sarsa(
    racetrack,
    epsilon_func=lambda ep, eps: epsilon_schedule(ep, eps),
    episodes=args.episodes
)

np.save(args.policy, policy)
