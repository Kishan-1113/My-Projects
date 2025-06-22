
# .........The first Game created by me "Pig Dice Multiplayer Game" .......

import random

players = int(input("Number of players : "))
while (players < 2):
    print("Atleast 2 players needed !!")
    players = int(input("Players : "))

scores = [0 for _ in range(players)]

while True:
    
    # Each Player plays the move
    for i in range(players):
        
        print(f'\n{"-"*40}')
        print(f" ____ Player {i+1}'s turn ____ ")
        score = 0
             
        st_rolling = input("Start rolling? (y/n): ").lower()
        while st_rolling not in ["y","n"]:
            st_rolling = input('"y" for yes and "n" for no : ').lower()
        
        if (st_rolling == "y"):
            pass
        elif (st_rolling == "n"): 
            continue
            
        # This while loop will be executed for each player
        # So you can break out of it any time
        
        while True:
                
            roll = random.randint(1,6)
            print(f"You rolled a {roll} ")
            
            score += roll
            
            if (roll ==  1):
                print("\n ...You lose all earnings of this turn...")
                print("Roll passed to next player")
                
                score = 0
                break
                       
            # Winning conditions
            if (scores[i] + score >= 100):
                print(f"Player {i+1} won!")
                scores[i] += score
                
                print("\n Overall score each made : \n")
                for j,scr in enumerate(scores):
                    print(f"Player {j+1} : {scr}")
                exit()
            
            # Validate the input (check)
            
            choice = input("Roll again? (y/n) : ").lower()
            while choice not in ["y","n"]:
                choice = input('"y" for yes and "n" for no : ').lower()
                
            if (choice == "n"):
                print("Turn ended. " , end="")
                print(f"You earned {score} this round")
                scores[i] += score
                print(f"Current total score {scores[i]}")
                               
                break         
    
    print("\n Current score : \n")
    for j,scr in enumerate(scores):
        print(f"Player {j+1} : {scr}") 
        
    