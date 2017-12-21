from dynamic_programming.car_rentals import JacksCarRentalWithHelp
import argparse

parser = argparse.ArgumentParser(description="Exercise 4.5")

parser.add_argument('--convergence',
                    type=float,
                    help='Convergence criteria for policy evaluation',
                    default=1.0)
args = parser.parse_args()

jcr = JacksCarRentalWithHelp()
policies, optimal_value = jcr.run_policy_improvement(gamma=0.9, convergence=args.convergence)
jcr.plot_results(policies, optimal_value)
