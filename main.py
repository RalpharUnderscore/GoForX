import game as Game


skill_id: int = 0

def main() -> None:
    display_title()

    player_response = input(">").lower()
    match player_response:
        case "play":
            Game.init_game()

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
    print("-----------------------")
    print("|                     |")
    print("| Let's play GoForX!! |")
    print("|                     |")
    print("-----------------------")
    print("Current skill: Rack")
    
    print("Command List:")
    print("\'play\': Play a Round")
    print("\'skill\': Change your skill")
    print("\'help\': Displays the GoForX manual")
    print("\'quit\': Quit the Game")


def change_skill() -> None:
    id = int(input("Change skill to: "))
    f = open("savefile.txt", "w")
    print(f.write(str(id)))
    f.close()


if __name__ == "__main__":
    while True:
        main()
