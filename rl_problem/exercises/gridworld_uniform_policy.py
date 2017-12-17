from rl_problem.gridworld import GridWorld

# Using uniform policy
g = GridWorld()
uniform_policy = g.get_uniform_policy()
value_func = g.get_value_function(uniform_policy).reshape(5, 5)
print(value_func)

