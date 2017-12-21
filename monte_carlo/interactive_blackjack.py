from monte_carlo.blackjack import *

blackjack = Blackjack()
state = blackjack.get_random_state()

while not blackjack.is_terminal(state):
    (dealer_card, player_sum, usable_ace) = BlackjackStates.id_to_state(state)

    if usable_ace:
        ace_string = 'with ace'
    else:
        ace_string = 'no ace'
    print(f'--- Dealer showing: {dealer_card} --- You: {player_sum} ({ace_string}) ---')

    action = None
    while action is None:
        action = input('Hit (0) or stay (1)?: ')
        if action in ['0', '1']:
            action = int(action)
        else:
            action = None
            print('Invalid action')

    print()
    reward, state = blackjack.perform_action(state, action)
