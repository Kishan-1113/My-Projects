import random


# Validating the difficulty input from user

# First layer of difficulty
difficulty1 = input("Enter difficulty level (0-6): ")
while (len(difficulty1) != 1 or not difficulty1.isdigit()):
    difficulty1 = input("Difficulty level 0 to 6 only : ")
    

# -------  Second layer of difficluty (START) ---------
difficulty2 = input("Wanna add an extra layer of difficluty (y/n): ")
while (difficulty2 not in ['y','n']):
    difficulty2 = input('"y" for yes and "n" for no : ')

available_moves = 0
if (difficulty2 == "y"):
    print("""
          ** As an extra layer of difficulty, 
    You have a total of "10" moves to reach the real number ** 
""")
    difficulty2 = True
    available_moves = 10
    
elif (difficulty2 == "n"):
    print("You have unlimited moves to reach !")
    difficulty2 = False 

# ------  Second layer of difficulty (ENDS)  ----------
    

difficulty1 = int(difficulty1)

# Random number selected by the computer in the range
com_guess = random.randint((10**(difficulty1-1)) , (10**(difficulty1) - 1))


# Validating user input
g = 0
while True:
    
    if (difficulty2):
        if ((available_moves - g) == 3):
            print("Careful! You have 3 moves left !!")
        if (g+1 > available_moves):
            print(" ---   You Lose   --- ")
            print("You ran out of moves !")
            break
    
    user_guess = input(f"Guess {g+1} : ")
    while ((len(user_guess) != difficulty1) or not user_guess.isdigit()):
        user_guess = input(f"Enter exactly {difficulty1} digits : ")
    g +=1
    
    # Create a list of all 
    user_guess = list(user_guess)

    # If I don't implement hash maps, I need to traverse the list 
    # each time I check. But it will be ok without hash maps as the list will contain
    # not more than 7 elements at max

    comp_num = list(str(com_guess))
    user_num = list(user_guess)

    comp_used = [False] * difficulty1
    user_used = [False] * difficulty1

    bulls = 0
    cows = 0
    # First pass: check for bulls
    for i in range(difficulty1):
        if user_num[i] == comp_num[i]:
            bulls += 1
            comp_used[i] = True
            user_used[i] = True

    # Second pass: check for cows
    for i in range(difficulty1):
        if not user_used[i]:
            for j in range(difficulty1):
                if not comp_used[j] and user_num[i] == comp_num[j]:
                    cows += 1
                    comp_used[j] = True
                    break
                
    print("cows : ", cows)
    print("Bulls : " , bulls)
    
    if (bulls == difficulty1):
        print("---- You Won ----")
        real = ""
        for i in user_guess:
            real += i
        print(f"You made the correct guess !! The real number is {real}")
        break
        
        
                