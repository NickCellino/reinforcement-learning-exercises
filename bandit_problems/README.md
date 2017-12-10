# Chapter 2 - Bandit Problems

## Overview
In this chapter, we learn about the N-Armed-Bandit problem. Consider this problem:

There are 10 different slot machines. For each slot machine, you pull a lever and
get a certain reward, maybe 0 tokens, maybe 10, maybe a million. You get 1000 pulls.
Your job is to end up with as many tokens as you can by the end of the 1000 pulls. 
What is your strategy?

If the slot machines are all exactly the same, then it doesn't really matter what you do.
You could use all your pulls on 1 machine or choose randomly for each pull and, on average,
you'll get the same result. But what if the machines are not all the same? What if
some of the machines are better than others? For example, say you tried slot machine 1 for
a few pulls and got the following results:

1. 3 tokens
2. 7 tokens
3. 6 tokens
4. 5 tokens
5. 7 tokens
6. 4 tokens

Then you try machine 2 for a few pulls and get the following results:

1. 8 tokens
2. 6 tokens
3. 9 tokens
4. 8 tokens
5. 10 tokens
6. 7 tokens

While the rewards are still random, machine 2 seems to be giving better results than machine 1
on average. So we need to come up with a strategy that exploits that information in order to get
the most possible tokens at the end.

This is the essence of the N-Armed-Bandit problem. How do we come up with a strategy to maximize
our reward?

### How we approach the problem

So we need to figure out what the best slot machine is and choose that one as much as possible.
In order to determine which slot machine is the best one, we need to try all the different
slot machines and see which ones give the best rewards. 

So if we have 1000 pulls, we can try each slot machine 100 times, average the results, 
and then we'll have a pretty good estimate of how good each slot machine is, right? 
Well yeah, but then we've spent all of our pulls so we can't exploit that information. 
So how about we try each machine once, then spend the rest of our pulls on whichever one
gave us the best reward? Well that doesn't really guarantee that we've found the best
machine because we only tried each once.

So we need to balance exploration (finding which machine is the best) with exploitation
(exploiting our knowledge to get the most possible reward).

### Epsilon Greedy Method

The epsilon greedy method is very simple. Basically, we use the reward from each pull
to maintain an estimate for how good each slot machine is. For some percentage of
our pulls, we pick the slot machine that we estimate to be the best. For the rest of our
pulls, we pick a slot machine randomly.

The percentage of pulls that we choose randomly is ε (epsilon). So for example, 
ε = 0.1 means we choose randomly 10% of the time and are greedy (choose our best estimate)
90% of the time.

Here are some results showing the performance of the epsilon greedy methods.

![Epsilon Greedy Methods](./results/exercise_2_2_a.png)

We can see that ε=0 does not perform too well. This is because it does not spend any
time exploring. It picks some slot machine as the best and chooses it every time no
matter what. With ε=0.1, we can see that we do a little better. We spend more time exploring
so we are able to get better results, but we plateau because we only ever choose our best
estimate for 90% of pulls. With ε=0.01, we do not learn as fast, but we eventually reach a
higher average reward than ε=0.1 because we choose our best estimate 99% of the time.

### Softmax Method

![Softmax Methods](./results/exercise_2_2_b.png)

More details soon...