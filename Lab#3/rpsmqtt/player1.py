# Client1.py
import paho.mqtt.client as mqtt
import random
import time

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("client2/choice")

def on_message(client, userdata, msg):
    userdata['opponent_choice'] = msg.payload.decode()
    print(f"Opponent chose: {userdata['opponent_choice']}")

client_userdata = {'opponent_choice': None, 'score': {'wins': 0, 'losses': 0, 'ties': 0}}
client = mqtt.Client(userdata=client_userdata)
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("mqtt.eclipseprojects.io")
client.loop_start()

# Rock-paper-scissors functions
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

# Main game loop
while True:
    user_choice = get_user_choice()
    client.publish("client1/choice", user_choice)
   
    # Wait for opponent's choice
    while client_userdata['opponent_choice'] is None:
        time.sleep(0.1)  # Don't busy-wait too quickly
   
    opponent_choice = client_userdata['opponent_choice']
    client_userdata['opponent_choice'] = None  # Reset for the next round

    result = determine_winner(user_choice, opponent_choice)
    print(result)
   
     # Update score
    if result == "It's a tie!":
        client_userdata['score']['ties'] += 1
    elif result == "You win!":
        client_userdata['score']['wins'] += 1
    else:
        client_userdata['score']['losses'] += 1
   
    # Print score
    print(f"Score - Wins: {client_userdata['score']['wins']}, Losses: {client_userdata['score']['losses']}, Ties: {client_userdata['score']['ties']}")
   
    # Ask for the next user input
    continue_playing = input("Play again? (yes/no): ").lower()
    if continue_playing != "yes":
        break

# Cleanup
client.loop_stop()
client.disconnect()
