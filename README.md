# Reinforcement Learning: An Introduction

This repository contains exercises from [Reinforcement Learning: An Introduction (Second Edition)](https://mitpress.mit.edu/books/reinforcement-learning).
Each subdirectory in this project contains an overview of a topic covered
in the book, the results from the exercises, and Python code for the exercises.

## Topics

1. [Chapter 2 - Bandit Problems](./bandit_problems)

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

All set! Now we can go into any of the subdirectories and run examples by running
```
python example_name.py
```
