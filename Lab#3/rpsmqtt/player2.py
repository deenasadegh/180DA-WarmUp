import paho.mqtt.client as mqtt
import random

# Initialize MQTT client for Player 2
mqtt_player2 = mqtt.Client("player2")
mqtt_player2.connect("localhost", 1883)

# Function to get user input
def get_user_choice():
    while True:
        user_choice = input("Player 2, enter your choice (rock, paper, or scissors): ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid input. Please choose from rock, paper, or scissors.")

# Send player's choice to Player 1
user_choice = get_user_choice()
mqtt_player2.publish("player1_choice", user_choice)

# Function to handle messages from Player 1
def on_message(client, userdata, message):
    opponent_choice = message.payload.decode()
    print("Player 1 chose:", opponent_choice)
    determine_winner(user_choice, opponent_choice)

# Set up message callback to receive Player 1's choice
mqtt_player2.on_message = on_message
mqtt_player2.subscribe("player1_choice")

# Start the MQTT client
mqtt_player2.loop_start()

# Function to determine the winner
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

# Main loop
try:
    while True:
        pass
except KeyboardInterrupt:
    mqtt_player2.disconnect()
