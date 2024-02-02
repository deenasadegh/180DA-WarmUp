import random

# Function to get user input
def get_user_choice():
    while True:
        user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid input. Please choose from rock, paper, or scissors.")

# Function to generate a random choice for the bot
def get_bot_choice():
    return random.choice(["rock", "paper", "scissors"])

# Function to determine the winner
def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (
        (user_choice == "rock" and bot_choice == "scissors")
        or (user_choice == "paper" and bot_choice == "rock")
        or (user_choice == "scissors" and bot_choice == "paper")
    ):
        return "You win!"
    else:
        return "Bot wins!"

# Main game loop
while True:
    user_choice = get_user_choice()
    bot_choice = get_bot_choice()

    print(f"You chose: {user_choice}")
    print(f"Bot chose: {bot_choice}")

    result = determine_winner(user_choice, bot_choice)
    print(result)

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        break
