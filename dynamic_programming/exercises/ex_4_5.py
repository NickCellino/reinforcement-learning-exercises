from dynamic_programming.car_rentals import JacksCarRentalWithHelp

jcr = JacksCarRentalWithHelp()
policies, optimal_value = jcr.run_policy_improvement(gamma=0.9, convergence=1.0)
jcr.plot_results(policies, optimal_value)
