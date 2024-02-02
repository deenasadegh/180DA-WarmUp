import paho.mqtt.client as mqtt

# MQTT Broker settings
broker_address = "mqtt.eclipseprojects.io"
port = 1883

# Game state
choices = {'client1': None, 'client2': None}
results = {'Client1 wins': 0, 'Client2 wins': 0, 'Tie': 0}  # Initialize results

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("rps/client1/choice")
    client.subscribe("rps/client2/choice")

def on_message(client, userdata, msg):
    client_id = msg.topic.split('/')[1]
    choice = msg.payload.decode()
    print(f"{client_id} chose {choice}")
    choices[client_id] = choice

    # Check if both clients have made their choices
    if all(choices.values()):
        winner = determine_winner(choices['client1'], choices['client2'])
        print("Winner:", winner)
        results[winner] += 1  # Update results
        print("Results:", results)  # Print results
        # Publish the result back to both clients
        client.publish("rps/client1/result", winner)
        client.publish("rps/client2/result", winner)
        # Reset choices for the next round
        choices['client1'], choices['client2'] = None, None

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "Tie"
    elif (choice1 == "rock" and choice2 == "scissors") or \
         (choice1 == "scissors" and choice2 == "paper") or \
         (choice1 == "paper" and choice2 == "rock"):
        return "Client1 wins"
    else:
        return "Client2 wins"

# Set up MQTT client
server = mqtt.Client()
server.on_connect = on_connect
server.on_message = on_message
server.connect(broker_address, port, 60)

# Start the loop
server.loop_forever()