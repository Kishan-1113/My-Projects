import random

# I will manually provide a list of words


text_1 = "Hello agent that arsenic humidity people vilage town home rickshaw cases can make videos photos also music help find new voices veo name home manual farmer shipment little mother marriage become"

text_2 = "cameraman working agriculture automation engineering background rootcauses grandmother grandfather grand-daughter childhood motherland simulation guinnessbook worldrecords olympicgames homedelivery"

text_3 = "hemoglobin neurotransmitter meteorological configuration refrigeration photosynthesis nanotechnology cryptography bioluminescence electromagneticinduction biodegradable electrocardiogram haemodialysis "


level = input("Level (1-4) : ")
while (level not in ['1','2','3','4']):
    level = input("4 levels are availavble currently : ")

# Level 1
if (level == "1"):
    words = text_1.split()
    hint = False
    life_use = False
    atmpt = False
    lifelines = 3
    dynamic_revealing = False

# Level 2
elif (level == "2"):
    print("____   LEVEL : 2    ____")
    hint = False
    atmpt = False
    life_use = False
    dynamic_revealing = False
    
    lifelines = 3
    print(" --  Note : Words are a bit longer  -- ")
    words = text_2.split()

# Level 3
elif (level == "3"):
    print("____   LEVEL : 3    ____")
    print("--- Longer words and 10 attempts to reach ---")
    hint = False
    atmpt = True
    life_use = True
    dynamic_revealing = False
    
    words = text_2.split()
    attempts = 20
    lifelines = 3
    
# Level 4
elif (level == "4"):
    print("____   LEVEL : 4    ____")
    hint = True
    atmpt = True
    life_use = False        # As we already have dynamic revealing
    dynamic_revealing = True
    
    words = text_3.split()
    attempts = 10
    lifelines = 3
    

# ____________________   Hint system    ______________________#

hints = {
    "hemoglobin": "RBS Protein, carries oxygen",
    "neurotransmitter": "Chemical messenger in CNS",
    "meteorological": "Weather and atmosphere related",
    "configuration": "Arrangement of parts or elements",
    "refrigeration": "Process of cooling for preservation",
    "photosynthesis": "Process by which plants make food using sunlight",
    "nanotechnology": "Manipulating matter at atomic scale",
    "cryptography": "Art of writing or solving codes",
    "bioluminescence": "Light emission by living organisms",
    "electromagneticinduction": "Relating to electric and magnetic fields",
    "biodegradable": "Capable of being decomposed by bacteria",
    "electrocardiogram": "Related to heart-beat measurement",
    "haemodialysis" : "Applied in kidney failled patients"
}


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
wrong_count = 0

# Starting of the main logic
g = 0
while ("_" in display):     # Winning condition
    
    print("".join(display))
    
    
    # Checking the number of attempts
    if atmpt:
        if (g+1 > attempts):
            print("Out of moves !! ")
            print("##     --- You lose ---    ##")
            print("The secret word was : ",secret_word)
            res = False
            break
    
    # Checking for a valid user input
    # User input is a single alphabet only
    user = input(f"Guess {g+1} : ").lower()
    while (len(user) != 1 or not user.isalpha()):
        user = input("Only one 'alphabet' allowed : ").lower()
    
    # Check if already guessed or not
    if user in guessd:
        print("Already guessed. Try a new one!")
        wrong_count += 1
        # Whenever there is wrong guess or such a guess that was 
        # already guessed, wrong_count increments
        continue
    
    g += 1    
    guessd.add(user)
    
    
    flag = True
    
    remaining = []      # Collects those indexes that are yet to be guessed
    
    for idx in range(len(secret_word)):
        
        # Collects those indexes that have been guessed in this turn
        if secret_word[idx] == user:
            display[idx] = user
            flag = False
            wrong_count *= 0         # Means the user got a correct alphabet

        # Collects those indexes that are remaining to be guessed
        if display[idx] == "_":
            remaining.append(idx)
        

    # If no match found
    if flag:
        wrong_count += 1
        print("No matches found! Try again")
        
        
    # User need to make atleast 3 wrong guesses to use lifelines
    # User can't directly use the lifelines
    
    if (life_use):
        if (wrong_count > 2):
            life = input("\n  Wanna use lifelines? (y/n) : ")
            while life not in ["y","n"]:
                life = input("'y' for yes and 'n' for no : ")
            
            if life == "n":
                wrong_count = 0
                continue
                
            if (life == "y"):
                if (lifelines != 0 and remaining):
                    display[remaining[-1]] = secret_word[remaining[-1]]
                    lifelines -= 1
                    print("\tRemaining lifelines : ",lifelines)
                    
                else:
                    print("No lifelines available to use !!")
                    
    
    # Dynamic reveal system. Allows user to chose the character to reveal
    if (dynamic_revealing):
        
        if (wrong_count >= 3):
            print("\n   Hint   ")
            print(hints[secret_word])
        
        if (wrong_count > 5 and lifelines != 0):
            life1 = input("\n  Wanna use lifelines? (y/n) : ")
            while life1 not in ["y","n"]:
                life1 = input("'y' for yes and 'n' for no : ")
            
            if (life1 == 'y'):
                
                reveal = input(f"Choose an index to reveal (1 to {len(secret_word)}): ")
                while (not reveal.isdigit() or (int(reveal) - 1 not in remaining)):
                    reveal = input(f"Invalid input! chose unrevealed indexes only: ")

                display[int(reveal) - 1] = secret_word[int(reveal) - 1]
                
                lifelines -= 1
            
            elif (life1 == 'n'):
                print("\n   Hint    ")
                print(hints[secret_word])
                print("")

            
if res:
    print("\n   You won!!!   ")
    print("The secret word is ", secret_word)



## Improvements :

#  Scoring tracking system
#  Refactoring into seperate functions
#  ****  Time based user input, if you can, implement!!  *****
#  Visual Hangman diagrams, if possible
#  Clear game instructions at start
#  Track history and of multiple winners
#  Starting of another game without restarting the whole program


# Think of creating another level