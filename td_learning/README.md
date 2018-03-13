# Temporal-Difference Learning

In this chapter, we learn about temporal difference (TD) learning. Like Monte Carlo methods, temporal difference
learning methods allow us to learn an optimal policy in a model-free environment. This means that we learn the
optimal policy through experience.

The difference between TD and Monte Carlo is that TD using a technique called bootstrapping. Basically, Monte Carlo methods
determine the value of a state based on a sample of all of the rewards that follow from it for the rest of the episode.
So if I am in state 1, then go to state 2, 3, 4, etc up to state 10 and then the episode terminates and I get a reward
of +1 at the end, I update my value estimate for each of those states with that final reward.

TD learning methods use the knowledge that has already been accumulated to update value estimates instead of visited
states. So if I am in state 1, then go to state 2, I update my value estimate for state 1 with the immediate reward I
obtained plus my current value estimate for state 2. So I am updating my value estimate based on other estimates- this
is bootstrapping. This is the same idea that Dynamic Programming methods use.

## SARSA: On-Policy TD Control for the Racetrack Problem

Coming soon...

## Q-Learning: Off-Policy TD Control for the Racetrack Problem

Coming soon...

#### Sources:
1. Sutton, Richard S., and Andrew G. Barto. Reinforcement Learning: an Introduction. 2nd ed., The MIT Press, 2012.