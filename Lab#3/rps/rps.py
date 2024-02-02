#Function to get user input
def get_user_choice():
    while True:
        user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid input. Please choose from rock, paper, or scissors.")

#Function to generate a random choice for the bot
def get_bot_choice():
    return random.choice(["rock", "paper", "scissors"])

#Function to determine the winner
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

#Main game loop
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
import random


def get_user_choice():
    while True:
        user_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid input. Please choose from rock, paper, or scissors.")


def get_bot_choice():
    return random.choice(["rock", "paper", "scissors"])


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
player 2: 

import paho.mqtt.client as mqtt
import random


mqtt_player2 = mqtt.Client("player2")
mqtt_player2.connect("localhost", 1883)


def get_user_choice():
    while True:
        user_choice = input("Player 2, enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid input. Please choose from rock, paper, or scissors.")


user_choice = get_user_choice()
mqtt_player2.publish("player1_choice", user_choice)


def on_message(client, userdata, message):
    opponent_choice = message.payload.decode()
    print("Player 1 chose:", opponent_choice)
    determine_winner(user_choice, opponent_choice)

choice
mqtt_player2.on_message = on_message
mqtt_player2.subscribe("player1_choice")

#Start the MQTT client
mqtt_player2.loop_start()


def determine_winner(choice1, choice2):
    if choice1 == choice2:
        print("It's a tie!")
    elif (
        (choice1 == "rock" and choice2 == "scissors")
        or (choice1 == "paper" and choice2 == "rock")
        or (choice1 == "scissors" and choice2 == "paper")
    ):
        print("Player 2 wins!")
    else:
        print("Player 1 wins!")


try:
    while True:
        pass
except KeyboardInterrupt:
    mqtt_player2.disconnect()