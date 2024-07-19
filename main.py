def main() -> None:
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
    
    player_response = input().lower()
    match player_response:
        case "play":
            pass

        case "skill":
            pass

        case "help":
            f = open("goforx.help", "r")
            print(f.read())
            f.close()
        
        case "quit":
            quit()
        
        case _:
            print(f"Unknown Command \'{player_response}\'")


if __name__ == "__main__":
    while True:
        main()