import random

# I will manually provide a list of words


text_1 = "Hello agent that can make videos photos also music help find new voices veo name home"

text_2 = "cameraman working agriculture farming background rootcauses grandmother grandfather grand-daughter childhood motherland"

level = input("Level (1-3) : ")
while (level not in ['1','2','3']):
    level = input("3 levels are availavble currently : ")

if (level == "1"):
    words = text_1.split()

elif (level == "2"):
    print(" --  Note : Words are a bit longer  -- ")
    words = text_2.split()

elif (level == "3"):
    print("--- You have 10 attempts to reach ---")
    atmpt = True
    words = text_2.split()
    attempts = 10

secret_word = random.choice(words)
secret_word = secret_word.lower()
print(secret_word)

# Tracking the already guessed alphabets
guessd = set()

# Logic for checking the guess if it is correct
display = ["_" for _ in range(len(secret_word))]
    
# Takes user input
print("\n----- Guess word letter by letter and 'one alphabet at a time' ----")

res = True

g = 0
while "_" in display:
    
    if atmpt:
        if (g+1 > attempts):
            print("Out of moves !! ")
            print("##     --- You lose ---    ##")
            res = False
            break
    
    print("".join(display))
    
    # Checking for a valid user input
    # User input is a single alphabet only
    user = input(f"Guess {g+1} : ").lower()
    while (len(user) != 1 or not user.isalpha()):
        user = input("Only one 'alphabet' allowed : ").lower()
    
    
    if user in guessd:
        print("Already guessed. Try a new one!")
        continue
    g += 1    
    guessd.add(user)
    
    # Collecting all those indexes in random word that matches the user input
    flag = True
    occurance = []
    for idx in range(len(secret_word)):
        if secret_word[idx] == user:
            occurance.append(idx)
            display[idx] = user
            flag = False

    # If no match found
    if flag:
        print("No matches found! Try again")
        continue
        
if res:
    print("You won!!!")
