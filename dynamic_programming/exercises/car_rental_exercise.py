from dynamic_programming.car_rentals import JacksCarRental

jcr = JacksCarRental()
policies, optimal_value = jcr.run_policy_improvement(gamma=0.9, convergence=1.0)
jcr.plot_results(policies, optimal_value)
