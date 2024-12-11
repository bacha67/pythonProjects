response = input("Would you like food? (Y/N): ")

if response.upper() == "Y":  # Convert input to uppercase for case insensitivity
    print("WELL, you want some food!")

    # Ask for the type of food
    food = input("What would you like to eat? (1. Dabo be muze 2. Shayi be enjera 3. Water pump be muze): ")
    
    if food == "1":  # Match input as a string
        print("Great! You have chosen Dabo be muze! It will be brought to you soon!")
    elif food == "2":
        print("Great! You have chosen Shayi be enjera! It will be brought to you soon!")
    elif food == "3":
        print("Great! You have chosen Water pump be muze! It will be brought to you soon!")
    else:
        print("Please select one of the foods from the menu.")
else:
    print("Well, your stomach is full!")
