if __name__ == "__main__":
    input("Please run main.py to play the game\n")
    quit()

import random

# Decklist 
decklist: list = [] # Full Deck
deck: list = [] # Currently what's in the deck

duplicate: int
variance: int = 2

# Hand
your_hand: list = []
opps_hand: list = []


# Bound
your_bound: int = 24
opps_bound: int = 24



def init_game() -> None:
    global decklist
    global duplicate
    global your_bound
    global opps_bound


    # Setup Decklist
    decklist = [x for x in range(2, 13)]
    duplicate = random.choice(decklist)
    decklist.append(duplicate)
    decklist.sort()

    # Set Bound
    your_bound = random.randint(16, 34)
    opps_bound = your_bound + random.randint(-variance, variance)

    # Gameloop, if your_turn returns false (game ended), break
    while True:
        if not your_turn(): break


def your_turn() -> bool:
    print(your_bound)
    print_display()



def print_display() -> None:
    print("------------------------------------")
    print("|                                   |")
    print("|                                   |")
    print("|                                   |")
    print("------------------------------------")
    print("Hello")

    
