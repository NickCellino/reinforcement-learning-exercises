# Chapter 4 - Dynamic Programming

In this chapter, we learn about using dynamic programming techniques to solve
finite MDPs. By "solve," in this context, we mean find the optimal way to behave
in the MDP so as to maximize our return.

## Policy Evaluation

The first important idea from this chapter is policy **evaluation**. This simply refers
to the process of determining the value functions for a certain policy. One way
to do this using dynamic programming is by taking an iterative approach.

We start with a given policy π and an arbitrary state-value function v(s)- we can
choose the state-value function that is 0 for all states. Then, we try to calculate v(s)
for each state in the state space. To do so, we look ahead one action,
and for each action, we look ahead at
the possible next states. For each of these actions a and next states s', we calculate
the return, which is the sum of the expected immediate reward and the discounted sum of
the return of the next state. We sum all these together, with each weighted
by their probability of occurring. Since the return of the next state is not actually
known, this is still only an estimate, but if we apply this procedure iteratively,
we are guaranteed to converge to the true value function.

## Policy Improvement

Okay, so with policy evaluation, we have a method to learn the value function
for a given policy in an environment. But our goal is to find the optimal way
to behave in this environment- the optimal policy.

Once we have the value function, this is actually pretty easy. If we know the
value function for a certain policy, we can look at each state and see if the
policy takes the optimal action from that state- remember that we know at this point
the value of all possible next states, the expected rewards from each action, and the
probability of transitioning from state s to state s' given the action a. If it does not
take the optimal action, then there is clearly an opportunity to **improve** this policy.
We can improve the policy by, from each state, selecting the action that gives us
the most return. Put another way, we should be **greedy** with respect to the policy's
value function. Once we do this, we end up with another policy which is better than
the one we started with. More formally, the state-value function of this policy is greater
than or equal to the state-value function of the previous policy for every state s.
If the state-value function is higher for every state, that intuitively means this policy can
extract more return from this environment in the long run.

## Policy Iteration

The policy iteration algorithm combines these two algorithms in order to find the optimal policy. We start with
an arbitrary policy and value function. Then, we evaluate this policy. Then, we improve that policy. Then, we evaluate
this policy. And so on, until the policy remains the same for two steps in a row. At this point, the policy is greedy
with respect to its own value function. This implies that this policy's value function satisfies the Bellman
optimality equation and thus, this is an optimal policy.


### Exercise: Jack's Car Rental

Jack's Car Rental problem is described in Sutton and Barto **Example 4.2** and **Exercise 4.5**.

The basic problem is this: Jack manages two dealerships for his car rental business. Let's call them A and B.
Every day, some customers arrive at each location and request cars. If Jack has a car for them, he can rent it to them
and get $10. If he does not have a car, he loses their business and makes no money. Jack can move cars between dealerships
at night for a cost of $2/car to help make sure he has cars where they are needed, but he can only move a maximum of 5 cars
per night.  Every day, some number of people
also return cars to each dealership, and those are available for rental the next day. The number of people who
request and return cars to each dealership are Poisson random variables.

For dealership A, the request and return probabilities have expected values 3 and 3, respectively.

For dealership B, the request and return probabilities have expected values 4 and 2, respectively.

Also, there can be no more than 20 cars at each location- any additional cars get returned to the nationwide company.

We can use policy iteration to find the optimal policy for this environment. The states in this environment are how many
cars are at each dealership. The actions are how many cars we move from A to B (a negative number means we move cars from
B to A). So the actions are integers in the range \[-5, 5\]. The rewards are how much money Jack makes in each time step.
The book says to use a discount factor of 0.9, so that's what we'll do.

Here are my results for running policy iteration on this problem:

![Policy 0](./results/jack_policy_0.png)

![Policy 1](./results/jack_policy_1.png)

![Policy 2](./results/jack_policy_2.png)

![Policy 3](./results/jack_policy_3.png)

![Policy 4](./results/jack_policy_4.png)

![Policy 5](./results/jack_policy_5.png)

![Optimal Policy](./results/jack_optimal_policy.png)

![Optimal Value](./results/jack_optimal_value.png)

As you can see, I started with the policy that moves 0 cars no matter what. At each iteration,
the policy changes slightly until there is no difference between policy 5 and the optimal policy. I'm not sure
why my results differ slightly from those shown in the book (Figure 4.4).
Policy 1 is slightly different when dealer B has 20 cars and my optimal value function looks
to max out at a slightly higher value. This may be due to mistakes on my part or different convergence
criteria.

#### Sources:
1. Sutton, Richard S., and Andrew G. Barto. Reinforcement Learning: an Introduction. 2nd ed., The MIT Press, 2012.
