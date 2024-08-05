import game as Game


skill_id: int = 0
sklist: dict = {
    0: "RACK II",
    1: "RETURN",
    2: "SPIN",
    3: "CLONE",
    4: "LUCKY DRAW",
    5: "MINUS TWO",
    6: "CLAMP",
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
    skill_id = make_sklist_is_valid(savefile)
    

    print(f"Current skill: {sklist[skill_id]}")
    print("Command List:")
    print("\'play\': Play a Round")
    print("\'skill\': Change your skill")
    print("\'help\': Displays the GoForX how-to-play")
    print("\'quit\': Quit the Game")


def make_sklist_is_valid(savefile) -> int:
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
    f = open("goforx.sklist", "r")
    print(f.read())
    f.close()


    id = int(input("Change skill to (ID): "))
    
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
    f.close()


if __name__ == "__main__":
    while True:
        main()
