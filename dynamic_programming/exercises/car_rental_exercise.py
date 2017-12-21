from dynamic_programming.car_rentals import JacksCarRental
import argparse

parser = argparse.ArgumentParser(description="Car Rental Exercise")

parser.add_argument('--convergence',
                    type=float,
                    help='Convergence criteria for policy evaluation',
                    default=1.0)
args = parser.parse_args()

jcr = JacksCarRental()
policies, optimal_value = jcr.run_policy_improvement(gamma=0.9, convergence=args.convergence)
jcr.plot_results(policies, optimal_value)
