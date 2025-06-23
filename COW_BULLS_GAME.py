import random

# ------ DECLARATION --------
# A cow means that the digit is correct but is at the wrong position
# A bulls means that the digit is correct and also at the correct position 


# Validating the difficulty input from user
difficulty = input("Enter difficulty level (0-6): ")
while (len(difficulty) != 1 or not difficulty.isdigit()):
    difficulty = input("Difficulty level 0 to 6 only : ")
    
difficulty = int(difficulty)

# Random number selected by the computer in the range
com_guess = random.randint((10**(difficulty-1)) , (10**(difficulty) - 1))


# Validating user input
g = 0
while True:
    user_guess = input(f"Guess {g+1} : ")
    while ((len(user_guess) != difficulty) or not user_guess.isdigit()):
        user_guess = input(f"Enter exactly {difficulty} digits : ")
    g +=1
    
    # Create a list of all 
    user_guess = list(user_guess)

    # If I don't implement hash maps, I need to traverse the list 
    # each time I check. But it will be ok without hash maps as the list will contain
    # not more than 7 elements at max

    comp_num = list(str(com_guess))
    user_num = list(user_guess)

    comp_used = [False] * difficulty
    user_used = [False] * difficulty

    bulls = 0
    cows = 0
    
    # First pass: check for bulls
    for i in range(difficulty):
        if user_num[i] == comp_num[i]:
            bulls += 1
            comp_used[i] = True
            user_used[i] = True

    # Second pass: check for cows
    for i in range(difficulty):
        if not user_used[i]:
            for j in range(difficulty):
                if not comp_used[j] and user_num[i] == comp_num[j]:
                    cows += 1
                    comp_used[j] = True
                    break
                
    print("cows : ", cows)
    print("Bulls : " , bulls)
    
    # Winning condition
    if (bulls == difficulty):
        print("---- You Won ----")
        real = ""
        for i in user_guess:
            real += i
        print(f"You made the correct guess !! The real number is {real}")
        break
        
        
                