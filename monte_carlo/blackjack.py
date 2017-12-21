from random import randint


# class BlackjackStates:
#
#     dealer_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
#
# class BlackjackPolicy:
#
#     def _id_to_state(self, state_id):
#
#     def get_action(self, state):
#         pass

class Blackjack:

    GAME_OVER_STATE = -1
    HIT_ACTION = 0
    STAY_ACTION = 1
    HIT_CARDS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, verbose=True):
        self._dealer_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self._agent_sums = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        self._usable_ace = [True, False]
        self._states = []
        self._verbose = verbose
        for dealer_card in self._dealer_cards:
            for agent_sum in self._agent_sums:
                for usable_ace in self._usable_ace:
                    self._states.append((dealer_card, agent_sum, usable_ace))

    def _id_to_state(self, id):
        return self._states[id]

    def _state_to_id(self, state):
        dealer_card_index = self._dealer_cards.index(state[0])
        agent_sum_index = self._agent_sums.index(state[1])
        usable_ace_index = self._usable_ace.index(state[2])
        return (
            dealer_card_index*len(self._agent_sums)*len(self._usable_ace) +
            agent_sum_index*len(self._usable_ace) +
            usable_ace_index
        )

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
        return len(self._dealer_cards) * len(self._agent_sums) * len(self._usable_ace)

    def get_random_state(self):
        return randint(0, self.num_states() - 1)

    def perform_action(self, state_id, action):
        state = self._id_to_state(state_id)
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
                    return (0, self._state_to_id(next_state))
                else:
                    # Lose
                    debug_print(f'You busted.')
                    return (-1, self.GAME_OVER_STATE)
            else:
                # Still <= 21
                next_state = (dealer_card, player_sum, usable_ace)
                return (0, self._state_to_id(next_state))
        elif action == self.STAY_ACTION:
            self.debug_print(f'You stayed!')
            # Dealer's turn
            dealer_cards = [dealer_card]
            dealer_sum = self._blackjack_sum(dealer_cards)

            # Dealer must hit until he has over 17
            while dealer_sum < 17:
                card = self._draw_card()
                self.debug_print(f'Dealer drew {card}')
                dealer_cards.append(card)
                dealer_sum = self._blackjack_sum(dealer_cards)
                print(f'Dealer has {dealer_sum}')

            if dealer_sum > 21:
                # Dealer busted
                self.debug_print(f'Dealer busted.')
                return (1, self.GAME_OVER_STATE)
            else:
                if dealer_sum >= player_sum:
                    # Lose
                    self.debug_print(f'Dealer won with {dealer_sum}.')
                    return (-1, self.GAME_OVER_STATE)
                else:
                    # Win
                    self.debug_print(f'Dealer: {dealer_sum}. You: {player_sum}.')
                    self.debug_print(f'You won.')
                    return (1, self.GAME_OVER_STATE)
        else:
            raise ValueError('This is not a valid action.')

    def is_terminal(self, state):
        return state == self.GAME_OVER_STATE
