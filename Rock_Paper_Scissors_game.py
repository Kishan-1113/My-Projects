import random
choices = ("r","p","s")
emojis = {"r" :" 🪨", "p" : "📃", "s" : "✂️"}

while True:
    user_choice = input("Rock, Paper, Scissors? Choose one (r/p/s): ").lower()
    if user_choice not in choices:
        print("Invalid Choice " )
        continue
        
        
    computer_choice = random.choice(choices)
    print(f"You chose :{emojis[user_choice]}")
    print(f"Computer chose: {emojis[computer_choice]}")

    #Game Logic //

    if user_choice == computer_choice:
        print(f"Both players selected {user_choice}. It's a tie!")
    elif (
    (user_choice == "r" and computer_choice == "s") or 
    (user_choice == "p" and computer_choice == "r") or 
    (user_choice == "s" and computer_choice == "p")):
        print("You Win! ")
    else:
        print("You loose !, Computer Wins")
        
    should_continue = input("Want to continue (y/n): ").lower()
    if should_continue == "n":
        break
    
    
