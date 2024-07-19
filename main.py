
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
    print("\'help\': Show how to play")
    print("\'quit\': Quit the Game")
    
    player_response = input()
    match player_response:
        case "play":
            pass
        case "skill":
            pass
        case "help":
            print("sum")
        case "quit":
            quit()




if __name__ == "__main__":
    while True:
        main()