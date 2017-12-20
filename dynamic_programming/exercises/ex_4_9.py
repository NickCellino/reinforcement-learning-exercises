import matplotlib.pyplot as plt
from dynamic_programming.gamblers import GamblersProblem

# Win probability 0.25
gambler = GamblersProblem(win_probability=0.25)
value_funcs = gambler.value_iteration()
policy = gambler.get_greedy_policy(value_funcs[-1])
next_figure = gambler.plot_results(value_funcs[0:5], policy)

# Win probability 0.55
gambler = GamblersProblem(win_probability=0.55)
value_funcs = gambler.value_iteration()
policy = gambler.get_greedy_policy(value_funcs[-1])
gambler.plot_results(value_funcs[0:5], policy, figure=next_figure)

plt.show()
