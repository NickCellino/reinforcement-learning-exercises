# The Reinforcement Learning Problem

Our first task is to come up with three example tasks that we can fit into
the reinforcement learning framework. Here are mine:

1. A program that plays blackjack. The state is made up of the cards
that it can see on the table. The possible actions are hit or stay. The rewards
would simply be +1 if the hand is won, -1 if the hand is lost, and 0 for any
action that does not cause the hand to end.
2. A traffic light controller. The reward is the number of cars it is
allowing to pass through so that it promotes effective traffic flow. The state
is readings from distant sensors that the controller has on each side which
tell it how far a car is from each side. The controller can make each of its
four sides one of three colors so there are 3^4 possible actions.
3. A piano playing program. The action in this case is very simple- which keys 
do we press and lift? The state is the keys that have already been played or are already
currently pressed. The reward could be supplied by human listeners and could be a numerical
representation of how much they are currently enjoying the music.

