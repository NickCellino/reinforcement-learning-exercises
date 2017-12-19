from dynamic_programming.car_rentals import JacksCarRental

jcr = JacksCarRental()
policies = jcr.run_policy_improvement(gamma=0.9, convergence=10.0)
jcr.plot_policies(policies)