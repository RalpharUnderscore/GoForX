if __name__ == "__main__":
    input("Please run main.py to play the game\n")
    quit()

import random as Random

# GameID (for events random from the beginning)
game_id: int = 0

# Deck list
VARIANCE: int = 3
decklist: list = []
duplicate: int

# in_deck and removed
in_deck: list = []
shown_on_display: list = []


# Set Hand
your_hand: list = []
opps_hand: list = []


your_hand_value: int
opps_hand_value: int

# Set Bound
your_bound: int = 24
opps_bound: int = 24



def init_game() -> None:
    global game_id
    global decklist
    global in_deck
    global shown_on_display

    global duplicate

    global your_hand
    global opps_hand

    global your_bound
    global opps_bound

    game_id = Random.randint(0, 4294967295)


    # Setup Decklist and duplicate
    decklist = [x for x in range(2, 13)]
    duplicate = Random.choice(decklist)
    decklist.append(duplicate)
    decklist.sort()

    # in_deck and removed
    in_deck = decklist.copy()
    shown_on_display = []


    # Set Hand
    your_hand = []
    opps_hand = []


    # Set Bound
    your_bound = Random.randint(18, 34)
    opps_bound = your_bound + Random.randint(-VARIANCE, VARIANCE)

    hit(True)
    hit(False, True)


    # Gameloop, if your_turn returns false (game ended), break
    while True:
        if not your_turn(): break
    
    # Calculate results
    calculate_results()


def your_turn() -> bool:
    global your_hand_value
    global opps_hand_value
    
    your_hand_value = 0
    for i in your_hand:
        your_hand_value += i

    opps_hand_value = 0
    for i in opps_hand:
        opps_hand_value += i

    print_display()

    player_input = input(">").lower()
    match player_input:
        case "hit":
            hit(True)
            opps_decide()
        
        case "stand":
            if not opps_decide(): return False
        case "bound":
            print(your_bound)
        case _:
            print(f"Unknown command: \'{player_input}\'")
    return True


def opps_decide() -> bool: # Returns true if opps hits
    if len(decklist) == 0:
        stand(False)
        return False

    # Get the sum of cards in the deck
    total_deck_value: int = 0
    for item in in_deck:
        total_deck_value += item
    
    # Subtract first card in your hand from the data since the AI doesn't know it
    total_deck_value -= your_hand[0]
    average_deck_value: float = total_deck_value/(len(in_deck) - 1)

    # If the average deck value is less than distance, draw a card
    # Use the player's bound because AI doesn't know its bound. It also does not care
    # if its bound is higher or lower
    if average_deck_value < your_bound - opps_hand_value: 
        hit(False)
        return True
    else:
        stand(False)
        return False





def print_display() -> None:
    print("\n==========================\n")
    display: list = ["_" for i in range(12)]
    
    for item in shown_on_display:
        if item in decklist: # Create a list with "_", replaced the _ with the number at the same position as it was sorted in decklists
            if not (item == duplicate and item in display):
                position = decklist.index(item)
                display[position] = item
            else: # If it is a duplicate and duplicate is already in, move the pointer by 1 (.index always finds the first copy)
                position = decklist.index(item)
                display[position + 1] = item

        else:
            raise(Exception(f"cannot find {item} in decklist"))
    print(display)




    print(f"Cards in Deck: {len(in_deck)} Variance: {VARIANCE}")
    print(show_if_bound_higher())

    print(f"{your_hand_value}   /?? | Your Hand      : {your_hand}")

    # The first card for opps is hidden, when displaying total take their hand value and subtract by the first number
    display_opps_hand = ["??"] + opps_hand[1:len(opps_hand)]
    # print(["??"].extend(opps_hand[0:len(opps_hand)-1]))
    print(f"{opps_hand_value - opps_hand[0]}+??/{opps_bound} | Opponent's Hand: {display_opps_hand}")


def show_if_bound_higher() -> str:
    bound_case: int
    if your_bound > opps_bound:
        bound_case = 0
    elif your_bound < opps_bound:
        bound_case = 1
    else:
        bound_case = game_id % 2
    

    match bound_case:
        case 0:
            return "Your Bound is: Higher"
        case 1:
            return "Your Bound is: Lower"


# Hit a player,
# If is_you is true, hits the player, otherwise hits opponent
# If sneak is true, the number will not be added to shown_on_display (used for opps first card, which is not visible)
def hit(is_you: bool, sneak: bool = False) -> None:
    if len(in_deck) == 0: 
        print("No more cards left in the deck.")
        return
    hit_card = in_deck.pop(Random.randint(0, len(in_deck) - 1))
    if is_you:
        your_hand.append(hit_card)
    else:
        opps_hand.append(hit_card)
    
    if not sneak:
        if not is_you: print("Opponent Hits!")
        shown_on_display.append(hit_card)


def stand(is_you: bool) -> None:
    if not is_you:
        print("Opponent Stands!")


def calculate_results() -> None:
    you_bust: bool = your_hand_value > your_bound
    opps_bust: bool = opps_hand_value > opps_bound

    your_distance: bool = your_bound - your_hand_value
    opps_distance: bool = opps_bound - opps_hand_value

    print("\n==========================\n")

    print(f"Your Hand Value: {your_hand_value}")
    print(f"Your Bound: {your_bound}")
    print(f"Your Distance: {your_distance}")
    print("\n")
    print(f"Opponent's Hand Value: {opps_hand_value}")
    print(f"Opponent's Bound: {opps_bound}")
    print(f"Opponent's Distance: {opps_distance}")

    print("\n==========================\n")

    you_win: bool = True
    # If neither bust
    if not you_bust and not opps_bust:
        you_win = your_distance < opps_distance
    
    # If both bust
    elif you_bust and opps_bust:
        you_win = your_distance > opps_distance # Your number is less negative/closer to bound than opps
    
    # If one player busts
    else:
        you_win = opps_bust # Either you or your opponent busts, if your opponent does, then you didn't therefore win
    

    # Tie Breaker and Finding Winner
    if your_distance == opps_distance: 
        you_win = tie_breaker()
    

    if you_win:
       print("You Win!!!")
    else:
        print("Opponent Wins...")
    
    input(">")
    return


def tie_breaker() -> bool:
    # Both players have the same distance
    if len(your_hand) > len(opps_hand):
        return True
    elif len(your_hand) < len(opps_hand):
        return False
    else:
        return True # For now, you win if even the cards tie
