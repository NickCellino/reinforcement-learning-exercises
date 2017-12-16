import numpy as np
from numpy.linalg import inv
from rl_problem.gridworld import GridWorld

GRID_SIZE = 5

trans_prob = np.zeros((GRID_SIZE ** 2, GRID_SIZE ** 2))
rewards = np.zeros(GRID_SIZE ** 2)


def to1d(row, col):
    return row * GRID_SIZE + col


# Initialize transition probabilities
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        left = to1d(row, col - 1)
        right = to1d(row, col + 1)
        up = to1d(row - 1, col)
        down = to1d(row + 1, col)
        current = to1d(row, col)
        if row == 0:
            # In the first row
            trans_prob[current, current] = 0.25
            rewards[current] = -0.25
            if col == 0:
                # Top left corner
                trans_prob[current, current] += 0.25
                trans_prob[current, right] = 0.25
                trans_prob[current, down] = 0.25
                rewards[current] = -0.5
            elif col == (GRID_SIZE - 1):
                # Top right corner
                trans_prob[current, current] += 0.25
                trans_prob[current, left] = 0.25
                trans_prob[current, down] = 0.25
                rewards[current] = -0.5
            else:
                trans_prob[current, left] = 0.25
                trans_prob[current, right] = 0.25
                trans_prob[current, down] = 0.25
        elif row == GRID_SIZE - 1:
            # In the last row
            trans_prob[current, current] = 0.25
            rewards[current] = -0.25
            if col == 0:
                # Bottom left corner
                trans_prob[current, current] += 0.25
                trans_prob[current, right] = 0.25
                trans_prob[current, up] = 0.25
                rewards[current] = -0.5
            elif col == (GRID_SIZE - 1):
                # Bottom right corner
                trans_prob[current, current] += 0.25
                trans_prob[current, left] = 0.25
                trans_prob[current, up] = 0.25
                rewards[current] = -0.5
            else:
                trans_prob[current, left] = 0.25
                trans_prob[current, right] = 0.25
                trans_prob[current, up] = 0.25
        elif col == 0:
            trans_prob[current, current] = 0.25
            trans_prob[current, right] = 0.25
            trans_prob[current, down] = 0.25
            trans_prob[current, up] = 0.25
            rewards[current] = -0.25
        elif col == GRID_SIZE - 1:
            trans_prob[current, current] = 0.25
            trans_prob[current, left] = 0.25
            trans_prob[current, down] = 0.25
            trans_prob[current, up] = 0.25
            rewards[current] = -0.25
        else:
            # Inner square
            trans_prob[current, down] = 0.25
            trans_prob[current, up] = 0.25
            trans_prob[current, right] = 0.25
            trans_prob[current, left] = 0.25
            rewards[current] = 0

# Handle special cases A (0, 1) and B (0, 3)
A = to1d(0, 1)
A_prime = to1d(4, 1)
trans_prob[A, :] = 0.0
trans_prob[A, A_prime] = 1.0

B = to1d(0, 3)
B_prime = to1d(2, 3)
trans_prob[B, :] = 0.0
trans_prob[B, B_prime] = 1.0

rewards[A] = 10
rewards[B] = 5

inverse = inv(np.identity(trans_prob.shape[0]) - 0.9 * trans_prob)
value = np.matmul(inverse, rewards)
value = value.reshape((GRID_SIZE, GRID_SIZE))
# print(value)

g = GridWorld()
uniform_policy = g.get_uniform_policy()
transition_probs = g.get_transition_probabilities(uniform_policy)

# print(trans_prob.reshape(5, 5, 5, 5))
# tp = transition_probs.reshape(5,5,5,5)
print(np.array_equal(transition_probs, trans_prob))
# print(transition_probs == trans_prob)
