from dynamic_programming.car_rentals import JacksCarRental

jcr = JacksCarRental()
policies = jcr.run_policy_improvement()
jcr.plot_policies(policies)