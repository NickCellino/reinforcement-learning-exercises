# Reinforcement Learning: An Introduction

This repository contains (some of the) programming exercises from [Reinforcement Learning: An Introduction (Second Edition)](https://mitpress.mit.edu/books/reinforcement-learning)
by Richard S. Sutton and Andrew G. Barto. Each subdirectory in this project contains an overview of a topic covered
in the book, the results from the exercises, and Python code for the exercises. There are also reproductions of some
of the figures from the book and Python code to go along with them as well.

This is a work in progress.

## Topics

1. [Chapter 2 - Bandit Problems](./bandit_problems)
2. [Chapter 3 - The Reinforcement Learning Problem](./rl_problem)
3. [Chapter 4 - Dynamic Programming](./dynamic_programming)
4. [Chapter 5 - Monte Carlo Methods](./monte_carlo)

## Getting Started
This project uses Python 3.6 and [venv](https://docs.python.org/3/library/venv.html)
(Note: This is distinct from [virtualenv](https://virtualenv.pypa.io/en/stable/). There
are some issues using matplotlib on OSX with virtualenv).
Ensure that you have both of these installed on your system.

Then, in the project directory, create your virtual environment:
```
python3.6 -m venv venv
```
This creates a folder called `venv` in which we can install Python libraries
like [numpy](http://www.numpy.org/) and [matplotlib](http://matplotlib.org/).

To tell your system to use this environment instead of the system-wide python environment, run:
```
source venv/bin/activate
```
You will need to do this anytime you want to run examples.


Next, to install the required libraries into the virtual environment, run:
```
pip install -r requirements.txt
```

All set! Run exercises by calling runner.py followed by the path to the exercise. For example:
```
python runner.py bandit_problems/exercises/ex_2_2_a.py
```

For some of the exercises, you can pass arguments to specify certain things about their execution (for example, number of trials in the case
of the n-armed-bandit problems). You can see what these parameters are by passing `-h` like so:
```
python runner.py bandit_problems/exercises/ex_2_2_a.py -h
```
