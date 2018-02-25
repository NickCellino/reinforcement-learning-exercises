from random import randint
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class BlackjackPlotter:

    @staticmethod
    def plot_value_functions(value):
        reshaped_value = np.reshape(value, BlackjackStates.state_space_shape())
        BlackjackPlotter.plot_value_function(
            reshaped_value[:, :, 0],
            title='Value Function (Usable ace)',
            figure=1
        )
        BlackjackPlotter.plot_value_function(
            reshaped_value[:, :, 1],
            title='Value Function (No usable ace)',
            figure=2)
        plt.show()

    @staticmethod
    def plot_value_function(value_function, title='Value Function', figure=1):
        fig = plt.figure(figure)
        ax = fig.add_subplot(111, projection='3d')
        x = np.arange(12, 22)
        y = np.arange(1, 11)
        X, Y = np.meshgrid(x, y)
        ax.plot_wireframe(X, Y, value_function)
        fig.suptitle(title)
        plt.xlabel('Player sum')
        plt.ylabel('Dealer showing')

    @staticmethod
    def plot_policies(policies):
        reshaped_policy = policies.reshape(BlackjackStates.state_space_shape())
        ace_policy = reshaped_policy[:, :, 0]
        BlackjackPlotter.plot_policy(ace_policy, title='Ace policy', figure=1)
        no_ace_policy = reshaped_policy[:, :, 1]
        BlackjackPlotter.plot_policy(no_ace_policy, title='No ace policy', figure=2)
        plt.show()

    @staticmethod
    def plot_policy(policy, title='Blackjack Policy', figure=1):
        policy = np.transpose(policy)
        fig = plt.figure(figure)
        ax = fig.subplots()
        fig.suptitle(title)
        plt.imshow(policy, cmap='jet')
        plt.gca().invert_yaxis()

        plt.xlabel('Dealer showing')
        plt.xticks(np.arange(0, len(BlackjackStates.DEALER_CARDS), 1))
        ax.set_xticklabels(BlackjackStates.DEALER_CARDS)

        plt.ylabel('Agent sum')
        plt.yticks(np.arange(0, len(BlackjackStates.AGENT_SUMS), 1))
        ax.set_yticklabels(BlackjackStates.AGENT_SUMS)

        for i in range(policy.shape[0]):
            for j in range(policy.shape[1]):
                if policy[i, j] == Blackjack.HIT_ACTION:
                    label = 'HIT'
                else:
                    label = 'STAY'
                plt.text(j, i, f'{label}', horizontalalignment='center', verticalalignment='center')


class BlackjackStates:

    DEALER_CARDS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
    AGENT_SUMS = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    USABLE_ACE = [True, False]
    STATES = []
    for dealer_card in DEALER_CARDS:
        for agent_sum in AGENT_SUMS:
            for _usable_ace in USABLE_ACE:
                STATES.append((dealer_card, agent_sum, _usable_ace))

    @staticmethod
    def state_space_shape():
        return (len(BlackjackStates.DEALER_CARDS),
                len(BlackjackStates.AGENT_SUMS),
                len(BlackjackStates.USABLE_ACE))

    @staticmethod
    def num_states():
        return (len(BlackjackStates.DEALER_CARDS) *
                len(BlackjackStates.AGENT_SUMS) *
                len(BlackjackStates.USABLE_ACE))

    @staticmethod
    def id_to_state(id):
        return BlackjackStates.STATES[id]

    @staticmethod
    def state_to_id(state):
        dealer_card_index = BlackjackStates.DEALER_CARDS.index(state[0])
        agent_sum_index = BlackjackStates.AGENT_SUMS.index(state[1])
        usable_ace_index = BlackjackStates.USABLE_ACE.index(state[2])
        return (
            dealer_card_index * len(BlackjackStates.AGENT_SUMS) * len(BlackjackStates.USABLE_ACE) +
            agent_sum_index * len(BlackjackStates.USABLE_ACE) +
            usable_ace_index
        )

    @staticmethod
    def print_state(state):
        if type(state) is int:
            state = BlackjackStates.id_to_state(state)
        dealer_card = state[0]
        agent_sum = state[1]
        usable_ace = state[2]
        print(f'Dealer: {dealer_card}, Agent sum: {agent_sum}, Ace: {usable_ace}')


class Blackjack:

    GAME_OVER_STATE = -1
    HIT_ACTION = 0
    STAY_ACTION = 1
    HIT_CARDS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, verbose=True):
        self._states = []
        self._verbose = verbose

    def _blackjack_sum(self, hand):
        """
        Sums a list of cards with blackjack rules.
        In other words, if a hand contains an ace, it counts it as
        a 1 or 11 depending on what is appropriate.

        If a hand has more than 1 ace, at most 1 can count as 11.
        """
        running_total = 0
        num_aces = 0
        for card in hand:
            if card == 'A':
                num_aces += 1
            else:
                running_total += card

        # Count all aces as 1s by default
        running_total += num_aces

        if num_aces > 0 and running_total + 10 <= 21:
            # Count 1 ace as 11
            running_total += 10

        return running_total

    def _draw_card(self):
        return self.HIT_CARDS[randint(0, len(self.HIT_CARDS) - 1)]

    def _player_draw_card(self):
        """
        Returns a card value in the range [1, 10] because a player can't draw
        another usable ace.
        """
        card = self._draw_card()
        if card == 'A':
            return 1
        else:
            return card

    def debug_print(self, message):
        if self._verbose:
            print(message)

    def num_states(self):
        return BlackjackStates.num_states()

    def num_actions(self):
        return 2

    def get_starting_state(self):
        return self.get_random_state()

    def get_random_state(self):
        return randint(0, self.num_states() - 1)

    def perform_action(self, state_id, action):
        state = BlackjackStates.id_to_state(state_id)
        dealer_card = state[0]
        player_sum = state[1]
        usable_ace = state[2]
        if action == self.HIT_ACTION:
            self.debug_print(f'You hit!')
            card = self._player_draw_card()
            self.debug_print(f'You drew {card}')
            player_sum += card
            if player_sum > 21:
                if usable_ace:
                    # Ace becomes 1
                    player_sum -= 10
                    next_state = (dealer_card, player_sum, False)
                    return (0, BlackjackStates.state_to_id(next_state), False)
                else:
                    # Lose
                    self.debug_print(f'You busted with {player_sum}.')
                    return (-1, self.GAME_OVER_STATE, True)
            else:
                # Still <= 21
                next_state = (dealer_card, player_sum, usable_ace)
                return (0, BlackjackStates.state_to_id(next_state), False)
        elif action == self.STAY_ACTION:
            self.debug_print(f'You stayed!')
            # Dealer's turn
            dealer_cards = [dealer_card]
            dealer_sum = self._blackjack_sum(dealer_cards)

            blackjack = False
            if player_sum == 21 and usable_ace:
                self.debug_print(f'You have a blackjack!')
                blackjack = True

            # Dealer must hit until he has over 17
            while dealer_sum < 17:
                card = self._draw_card()
                self.debug_print(f'Dealer had {dealer_sum}, and drew {card}')
                dealer_cards.append(card)
                dealer_sum = self._blackjack_sum(dealer_cards)
                if dealer_sum != 21 and blackjack:
                    # If dealer doesn't have 21 after first draw,
                    # player immediately wins.
                    self.debug_print(f'You win!')
                    return (1, self.GAME_OVER_STATE, True)

            if dealer_sum > 21:
                # Dealer busted
                self.debug_print(f'Dealer busted.')
                return (1, self.GAME_OVER_STATE, True)
            else:
                if dealer_sum > player_sum:
                    # Lose
                    self.debug_print(f'Dealer won with {dealer_sum}.')
                    return (-1, self.GAME_OVER_STATE, True)
                elif dealer_sum == player_sum:
                    self.debug_print(f'Draw. Dealer and player both have {player_sum}.')
                    return (0, self.GAME_OVER_STATE, True)
                else:
                    # Win
                    self.debug_print(f'You won! Dealer: {dealer_sum}. You: {player_sum}.')
                    return (1, self.GAME_OVER_STATE, True)
        else:
            raise ValueError('This is not a valid action.')

    def is_terminal(self, state):
        return state == self.GAME_OVER_STATE
