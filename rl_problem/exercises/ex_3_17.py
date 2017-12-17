from rl_problem.gridworld import GridWorld

g = GridWorld()

optimal_value_function = g.get_optimal_value_function()
print(optimal_value_function.reshape(5, 5))
