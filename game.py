if __name__ == "__main__":
    input("Please run main.py to play the game\n")
    quit()

import random as Random

# Deck list
VARIANCE: int = 2
decklist: list = []
duplicate: int

# in_deck and removed
in_deck: list = []
shown_on_display: list = []


# Set Hand
your_hand: list = []
opps_hand: list = []


# Set Bound
your_bound: int = 24
opps_bound: int = 24



def init_game() -> None:
    
    global decklist
    global in_deck
    global shown_on_display

    global duplicate

    global your_hand
    global opps_hand

    global your_bound
    global opps_bound

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
    your_bound = Random.randint(16, 34)
    opps_bound = your_bound + Random.randint(-VARIANCE, VARIANCE)


    # Gameloop, if your_turn returns false (game ended), break
    while True:
        if not your_turn(): break





def your_turn() -> bool:
    print(your_bound)
    print_display()
    return True



def print_display() -> None:
    print(your_hand)
    print(in_deck)
    player_input = input(">").lower()
    match player_input:
        case "hit":
            hit(True)
    # print("------------------------------------")
    # print("|                                   |")
    # print("|                                   |")
    # print("|                                   |")
    # print("|                                   |")
    # print("|                                   |")
    # print("------------------------------------")



# Hit a player,
# If is_you is true, hits the player, otherwise hits opponent
# If sneak is true, the number will not be added to shown_on_display (used for opps first card, which is not visible)
def hit(is_you: bool, sneak: bool = False):
    hit_card = in_deck.pop(Random.randint(0, len(in_deck) - 1))
    if is_you:
        your_hand.append(hit_card)
    else:
        opps_hand.append(hit_card)
    
    if not sneak: shown_on_display.append(hit_card)
    

