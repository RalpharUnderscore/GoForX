import game as Game
import os
# from rich import print


skill_id: int = 0
sklist: dict = {
    0: "RACK",
    1: "RETURN",
    2: "SPIN",
    3: "CLONE",
    4: "LUCKY DRAW",
    5: "INVERT",
    6: "BOUNTY",
    7: "UP TWO",
    8: "SAVANT",
    9: "DESPERADO",
}



def main() -> None:
    display_title()

    player_response = input(">").lower()
    match player_response:
        case "play":
            Game.init_game(skill_id)

        case "skill":
            change_skill()

        case "help":
            f = open("goforx.help", "r")
            print(f.read())
            f.close()

        case "quit":
            quit()
        
        case _:
            print(f"Unknown Command \'{player_response}\'")


def display_title() -> None:
    global skill_id
    print("-----------------------")
    print("|                     |")
    print("| Let's play GoForX!! |")
    print("|                     |")
    print("-----------------------")
    savefile = open("savefile.txt", "r")
    skill_id = make_savefile_valid(savefile)
    

    print(f"Current skill: {sklist[skill_id]}")
    print("Command List:")
    print("\'play\': Play a Round")
    print("\'skill\': Change your skill")
    print("\'help\': Displays the GoForX how-to-play")
    print("\'quit\': Quit the Game")


def make_savefile_valid(savefile) -> int:
    text = savefile.read()
    flag = False
    try:
        if int(text) not in sklist:
            flag = True
    except:
        flag = True
    
    if flag:
        # New variable to rewrite
        print("Invalid save data. Restored to default...")
        savefile2 = open("savefile.txt", "w")
        savefile2.write("0")
        savefile2.close()
        return 0

    return int(text)
    
        


def change_skill() -> None:
    try:
        f = open("goforx.sklist", "r")
        print(f.read())
        f.close()
    except FileNotFoundError:
        print("goforx.sklist not found. Please reinstall.")


    id = int(input("Change skill to (ID): "))
    
    if id > len(sklist) - 1: # Invalid skill id
        print(f"Invalid skill id: \'{id}\'")
        print("Please enter a valid skill id.")
        return
        



    savefile = open("savefile.txt", "w")
    savefile.write(str(id))
    savefile.close()
    print()
    print(f"Skill equipped: {sklist[id]}")
    print()
    print("Type \'skill\' in game to use your skill.")
    print("You will be prompted to guess the currnet game's duplicate card.")
    print("Guess correctly and you can use your skill.")
    print("You can only use your skill once per game")

    print()



if __name__ == "__main__":
    if not os.path.exists("goforx.help"): 
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("goforx.help does not exist. Please redownload game files.")
        print("\'help\' command will break the game")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

    if not os.path.exists("goforx.sklist"):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("goforx.sklist does not exist. Please redownload game files.")
        print("\'skill\' will still allow you to change your skill")
        print("but will not print skill description")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

    if not os.path.exists("savefile.txt"):
        print("No save file found.")
        print("Created new one.")
        f = open("savefile.txt", "w")
        f.write("0")
        f.close()


    while True:
        main()
