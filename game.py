if __name__ == "__main__":
    input("Please run main.py to play the game\n")
    quit()

import random
import time

# Skill ID
skill_id: int = 0
used_skill: bool

# GameID (for events random from the beginning)
game_id: int = 0

# Deck list
variance: int = 3
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
show_your_bound: bool = False # SAVANT Skill
your_bound: int = 24
opps_bound: int = 24


# Draw Limit (defaults at -1: no limit. Some skills limit your draw)
draw_limit: int = -1
status_desperado: bool = False

# AI only knows duplicate if one card in deck OR duplicate already drawn
opps_knows_duplicate: bool = False


def init_game(_skill_id: int) -> None:
    global skill_id
    global used_skill

    global game_id
    global decklist
    global in_deck
    global shown_on_display

    global duplicate
    global variance

    global your_hand
    global opps_hand

    global show_your_bound
    global your_bound
    global opps_bound

    global draw_limit

    global status_desperado

    global opps_knows_duplicate

    game_id = random.randint(1, 1000)

    # Set Skill ID
    skill_id = _skill_id
    used_skill = False


    # Setup Decklist and duplicate
    decklist = [x for x in range(2, 13)]
    duplicate = random.choice(decklist)
    decklist.append(duplicate)
    decklist.sort()

    # in_deck and removed
    in_deck = decklist.copy()
    shown_on_display = []


    # Set Hand
    your_hand = []
    opps_hand = []

    # Variance, maybe don't randomize
    # variance = random.randint(2, 5)


    # Set Bound
    show_your_bound = False
    your_bound = random.randint(26, 35)
    opps_bound = your_bound + random.randint(-variance, variance)

    hit(True, False)
    hit(False, False)

    hit(True, False)
    hit(False, False)

    # Status
    draw_limit = -1
    status_desperado = False

    opps_knows_duplicate = False

    # Gameloop, if turn returns false (game ended), break
    while True:
        if not turn(): break
    
    # Calculate results
    calculate_results()


def turn() -> bool:
    global your_hand_value
    global opps_hand_value
    
    global used_skill

    global draw_limit

    # Player's Turn
    your_hand_value = 0
    for i in your_hand:
        your_hand_value += i

    opps_hand_value = 0
    for i in opps_hand:
        opps_hand_value += i

    print_display()

    player_stand: bool = False
    player_input = input(">").lower()
    match player_input:
        case "hit":
            if draw_limit != 0:
                if draw_limit > 0: draw_limit -= 1


                print("\n==========================\n")
                print(f"You drew {hit(True)}!")
                print("\n==========================\n")
            else:
                print("You may not draw anymore cards.")
                return True
        case "stand":
            player_stand = True
            print("")
        case "quit":
            quit()
        case "skill":
            if used_skill:
                print("You've already used your skill.")
                return True # Don't go to opps turn
            else:
                used_skill = True
                guess_duplicate()

        
        case "dupe":
            print(duplicate)
            return True

        case _:
            print(f"Unknown command: \'{player_input}\'")
            return True # Don't go to opps turn
    
    # Opps Turn
    print("Waiting for Opponent...")

    # Opponent decides, returns false if opponent stands.
    # If both opponent and player stands, this func returns false and ends the game.
    if not opps_decide() and player_stand: return False 
    else: return True



def opps_decide() -> bool: # Returns true if opps hits
    global opps_knows_duplicate
    
    time.sleep(0.1)
    
    if len(in_deck) == 0:
        opps_knows_duplicate = True
        stand(False)
        return False

    time.sleep(random.uniform(0.2, 2))

    # Get the sum of cards in the deck
    total_deck_value: int = 0
    for item in in_deck:
        total_deck_value += item



    # If duplicate revealed or one card left (prevent 0 div err), calculate like normal (AI now knows duplicate)
    if duplicate not in in_deck or len(in_deck) == 1:
        opps_knows_duplicate = True
        average_deck_value: float = total_deck_value/(len(in_deck))

    else: # If duplicate not revealed, remove duplicate from average calculation
        total_deck_value -= duplicate # don't add duplicate into data
        average_deck_value: float = total_deck_value/(len(in_deck) - 1)


    
    global status_desperado
    if status_desperado: 
        average_deck_value *= 2


    opps_dist_to_your_bound = your_bound - opps_hand_value
    if your_bound > opps_bound:
        opps_dist_to_opps_bound = opps_dist_to_your_bound - variance/2.0
    elif your_bound < opps_bound:
        opps_dist_to_opps_bound = opps_dist_to_your_bound + variance/2.0
    else: # AI has advantage when bounds are the same
        opps_dist_to_opps_bound = opps_dist_to_your_bound

    # If the average deck value is less than distance, hit
    # Use the player's bound because AI doesn't know its bound.
    # print("\n==========================\n")
    # print(f"Average Deck Value: {average_deck_value}")
    # print(f"Est. Distance: {opps_dist_to_opps_bound}")
    # print("\n==========================\n")
    if average_deck_value < opps_dist_to_opps_bound: 
        print(f"Drew a {hit(False)}!")
        if status_desperado:
            print("x2 - Desperado Effect")
            opps_hand[-1] *= 2
            status_desperado = False
            print(f"Drew a {opps_hand[-1]}!")
        
        return True
    else:
        stand(False)
        return False





def print_display() -> None:
    print("\n==========================\n")
    display: list = ["_" for i in range(12)]
    
    # for item in shown_on_display:
    #     if item in decklist: # Create a list with "_", replaced the _ with the number at the same position as it was sorted in decklists
    #         if not (item == duplicate and item in display):
    #             position = decklist.index(item)
    #             display[position] = item
    #         else: # If it is a duplicate and duplicate is already in, move the pointer by 1 (.index always finds the first copy)
    #             position = decklist.index(item)
    #             display[position + 1] = item

    for item in shown_on_display:
        # Create a list with "_", replaced the _ with the number at the same position as it was sorted in decklists
        if item in decklist: 
            # If item is not a duplicate add it normally
            if item != duplicate:
                position = decklist.index(item)
                display[position] = item
            
            # If item IS a duplicate but its copy is not revealed
            elif item not in display: 
            #     if game_id > 500:
            #         position = decklist.index(item)
            #         display[position + 1] = item
                # else:
                position = decklist.index(item)
                display[position] = item

            # If it IS a duplicate and its copy IS revealed, place it in the location opposite of where the copy is revealed
            else: 
                # if game_id > 500:
                #     position = decklist.index(item)
                #     display[position] = item
                # else:
                position = decklist.index(item)
                display[position + 1] = item
        

        else:
            raise(Exception(f"cannot find {item} (which comes from shown_on_display) in decklist"))
    print(display)






    # print(f"Cards in Deck: {len(in_deck)} variance: {variance}")
    print(f"Variance: {variance}")
    print(show_if_bound_higher())
    print()


    your_bound_display = your_bound if show_your_bound else "??" 

    if your_hand_value < 10: # For formatting
        print(f"{your_hand_value} /{your_bound_display} | Your Hand      : {your_hand}")
    else:
        print(f"{your_hand_value}/{your_bound_display} | Your Hand      : {your_hand}")

    
    
    if opps_hand_value < 10: 
        print(f"{opps_hand_value} /{opps_bound} | Opponent's Hand: {opps_hand}")
    else:
        print(f"{opps_hand_value}/{opps_bound} | Opponent's Hand: {opps_hand}")



    print()
    command_list = "Command: \'hit\', \'stand\'"
    if not used_skill:
        command_list += ", \'skill\'"

    print(command_list)


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
# Returns the card drawn
def hit(is_you: bool, display_message: bool = True, draw_card: int = 0) -> int:
    global status_desperado
    if len(in_deck) == 0: 
        print("No more cards left in the deck.")
        return
    
    
    if draw_card == 0: # Draw card defaults to 0, which means random card
        hit_card = in_deck.pop(random.randint(0, len(in_deck) - 1))
    else: # Otherwise, tries to draw a specific card from the deck
        if draw_card in in_deck:
            hit_card = in_deck.pop(in_deck.index(draw_card))
        else:
            print(f"The {draw_card} card is not in the deck. Drawing from topdeck instead...")
            hit_card = in_deck.pop(random.randint(0, len(in_deck) - 1))



    if is_you:
        your_hand.append(hit_card)
        
        if display_message: 
            print("Giving you a card...")
            time.sleep(1)
    else:
        opps_hand.append(hit_card)

        if display_message: 
            print("Opponent Hits!")
            time.sleep(1)
    
    shown_on_display.append(hit_card)

    return hit_card


def stand(is_you: bool) -> None:
    if not is_you:
        print("Opponent Stands!")



def guess_duplicate():
    while True:
        call = input("The duplicate card is: ")
        if call == "quit":
            quit()
        
        if call.isnumeric():
            call = int(call)
            if 2 <= call <= 12:
                break
        
        print("Input a number between 2-12")
    
    if call == duplicate:
        print("Correct!!!")
        print()
        skill()
    else:
        print("Incorrect.") 
        print(f"The duplicate is not {call}.")






def skill() -> None:
    global skill_id
    match skill_id:
        case 0:
            print("Skill: RACK")
            print("Discards the top 2 cards of the deck.")
            print()
            time.sleep(1.5)
            for _ in range(2):
                print("Racking...")    
                hit_card = in_deck.pop(random.randint(0, len(in_deck) - 1))
                shown_on_display.append(hit_card)
                time.sleep(1.5)
                print(f"Racked a {hit_card}!")

        case 1:
            print("Skill: RETURN")
            print("Returns your last drawn card into the deck.")
            print()
            time.sleep(1.5)

            card = your_hand.pop(-1)
            in_deck.append(card)
            in_deck.sort()
            shown_on_display.remove(card)
            

            old_hand_value = your_hand_value # Because this doesn't update until it passes this function
            new_hand_value = 0
            for i in your_hand:
                new_hand_value += i

            print(f"Returned {card} from your hand.")
            print(f"Your hand value: {old_hand_value} -> {new_hand_value}")
            time.sleep(1)
        
        case 2:
            print("Skill: SPIN")
            print("Returns your opponent's last drawn card into the deck.")
            print()
            time.sleep(1.5)

            if len(opps_hand) == 1:
                print("You may not spin your opponent's face down card.")
                return


            card = opps_hand.pop(-1)
            in_deck.append(card)
            in_deck.sort()
            shown_on_display.remove(card)
            

            old_hand_value = opps_hand_value - opps_hand[0]
            new_hand_value = 0
            for i in opps_hand:
                new_hand_value += i

            new_hand_value -= opps_hand[0]

            print(f"Returned {card} from your opponent's hand.")
            print(f"Opponent's hand value: {old_hand_value} + ?? -> {new_hand_value} + ??")
            time.sleep(1)

        case 3:
            print("Skill: CLONE")
            print("Clone your last drawn card.")
            print()
            time.sleep(1.5)


            card = your_hand[-1]
            your_hand.append(card)
            print(f"Cloned a {card} in your hand.")

            time.sleep(1)
        
        case 4:
            print("Skill: LUCKY DRAW")
            print("Draw the duplicate if it is in the deck, otherwise draw the top card of the deck.")
            print()
            time.sleep(1.5)

            print(f"You drew a {hit(True, False, duplicate)}!")
            time.sleep(1)


        case 5:
            print("Skill: INVERT")
            print("The value of your last drawn card becomes inverted.")
            print()
            time.sleep(1.5)

            print(f"Inverted Card: {your_hand[-1]} -> {-your_hand[-1]}")
            print(f"Youu Hand Value: {your_hand_value} -> {your_hand_value - 2*your_hand[-1]}")

            your_hand[-1] *= -1

            time.sleep(1)

        
        
        case 6:
            print("Skill: BOUNTY")
            print("Removes the single highest value card in both players' hands.")
            print()
            time.sleep(1.5)

            your_highest = max(your_hand)
            opps_highest = max(opps_hand)

            if your_highest >= opps_highest:
                print(f"Removed a {your_highest} from your hand!")
                your_hand.remove(your_highest)
            else:
                print(f"Removed a {opps_highest} from your opponent's hand!")
                opps_hand.remove(opps_highest)
            
            time.sleep(1)

        case 7:
            global your_bound
            global opps_bound
            print("Skill: UP TWO")
            print("Increase both player's bounds by 2.")
            print()
            time.sleep(1.5)

            print(f"Your Bound: ?? -> ?? + 2")
            print(f"Opponent's Bound: {opps_bound} -> {opps_bound + 2}")

            your_bound += 2
            opps_bound += 2

            time.sleep(1)

        case 8:
            global show_your_bound
            global draw_limit
            print("Skill: SAVANT")
            print("Reveals your bound, you may only draw 1 other card.")
            print()
            time.sleep(1.5)

            show_your_bound = True
            if draw_limit > 1 or draw_limit == -1: draw_limit = 1
            
            print(f"Your bound is {your_bound}")
            print("You may only draw 1 more card this round.")
            time.sleep(1)

        case 9:
            global status_desperado
            # global draw_limit
            print("Skill: DESPERADO")
            print("Double the value of the next card your opponent draws. You may not draw anymore cards.")
            print()
            time.sleep(1.5)

            print("Desperado is active.")
            print("You may not draw anymore cards this round.")
            draw_limit = 0
            status_desperado = True

            time.sleep(1)


        # Unused

        case 15:
            print("Skill: MINUS THREE")
            print("Draw a \"-3\" card.")
            print()
            time.sleep(1.5)

            print("You drew a -3!")
            your_hand.append(-3)
            time.sleep(1)

        case 19:
            print("Skill: DESPERADO")
            print("Force your opponent to draw a card, you may not draw anymore cards.")
            print()
            time.sleep(1.5)

            in_deck.sort()
            print(f"Forced opponent to draw a {hit(False, True, in_deck[0])}!")
            print("You may not draw anymore cards this round.")
            draw_limit = 0
            time.sleep(1)






            









def calculate_results() -> None:
    you_bust: bool = your_hand_value > your_bound
    opps_bust: bool = opps_hand_value > opps_bound

    your_distance: bool = your_bound - your_hand_value
    opps_distance: bool = opps_bound - opps_hand_value

    print("\n==========================\n")

    print(f"Duplicate Card: {duplicate}")

    print("\n")

    print(f"Your Hand: {your_hand}")
    print(f"Your Hand Value: {your_hand_value}")
    print(f"Your Bound: {your_bound}")
    print(f"Your Distance: {your_distance}")
    print("\n")
    print(f"Opponent's Hand: {opps_hand}")
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
        print("\n==========================\n")
    

    if you_win:
       print("You Win!!!")
    else:
        print("Opponent Wins...")
    
    if input(">").lower() == "quit":
        quit()
    
    return


def tie_breaker() -> bool:
    # Both players have the same distance
    print("Tie Breaker: Cards in Hand")
    if len(your_hand) > len(opps_hand):
        print("You have more cards than your opponent")
        return True
    elif len(your_hand) < len(opps_hand):
        print("Your opponent has more cards than you")
        return False
    # else:
    #     return True # For now, you win if even the cards tie

    print("Same number of cards in both players hands\n")
    
    
    # Both players have the same distance and same number of cards in hard
    print("Tie Breaker: Highest Value Card")
    
    your_hand.sort()
    opps_hand.sort()
    
    print(f"Your highest card: {your_hand[-1]}")
    print(f"Opponent's highest card: {opps_hand[-1]}")

    if your_hand[-1] > opps_hand[-1]:
        return True
    elif your_hand[-1] < opps_hand[-1]:
        return False
    
    print("Both players have the same highest value card\n") # In case both players happen to draw the duplicate, which is the highest value card


    # Same distance, same no. cards in hand, same highest value
    print("Tie Breaker: Second Highest Value Card")

    print(f"Your second highest card: {your_hand[-2]}")
    print(f"Opponent's second highest card: {opps_hand[-2]}")


    if your_hand[-2] > opps_hand[-2]:
        return True
    elif your_hand[-2] < opps_hand[-2]:
        return False
    
    print("that isn't supposed to happen. you win i guess") # Should be impossible because there should be only 1 duplicate in the deck.
    return True
    

    