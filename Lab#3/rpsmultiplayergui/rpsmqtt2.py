import pygame
import paho.mqtt.client as mqtt
import sys

# Initialize Pygame and set up the screen
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Rock, Paper, Scissors - Client 2')

# Load and scale images
def load_image(name, size=(100, 100)):
    return pygame.transform.scale(pygame.image.load(f'rpsMultiplayer/{name}.png').convert_alpha(), size)

# Image assets
rock_img = load_image('rock')
paper_img = load_image('paper')
scissors_img = load_image('scissors')
win_img = load_image('win', (200, 200))
lose_img = load_image('lose', (200, 200))
tie_img = load_image('tie', (200, 200))

# Initialize font
font = pygame.font.Font(None, 36)

# MQTT client setup
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("rps/client2/result")

def on_message(client, userdata, msg):
    global result_img
    result = msg.payload.decode()
    if result == "Client1 wins":
        result_img = lose_img  # Client2 loses if Client1 wins
    elif result == "Client2 wins":
        result_img = win_img
    elif result == "Tie":
        result_img = tie_img

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.loop_start()

# Game state variables
user_choice_img = None
result_img = None
game_state = 'awaiting input'

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == 'awaiting input':
                if event.key == pygame.K_r:
                    user_choice_img = rock_img
                    client.publish("rps/client2/choice", "rock")
                elif event.key == pygame.K_p:
                    user_choice_img = paper_img
                    client.publish("rps/client2/choice", "paper")
                elif event.key == pygame.K_s:
                    user_choice_img = scissors_img
                    client.publish("rps/client2/choice", "scissors")
                if user_choice_img:
                    game_state = 'waiting for result'

    # Game state handling
    if game_state == 'awaiting input':
        prompt_text = font.render("Press R, P, or S for Rock, Paper, Scissors", True, (255, 255, 255))
        screen.blit(prompt_text, (SCREEN_WIDTH / 2 - prompt_text.get_width() / 2, 50))
    elif game_state == 'waiting for result':
        waiting_text = font.render("Awaiting opponent... Your choice was:", True, (255, 255, 255))
        screen.blit(waiting_text, (SCREEN_WIDTH / 3 - waiting_text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
        screen.blit(user_choice_img, (SCREEN_WIDTH / 4 - user_choice_img.get_width() / 2, SCREEN_HEIGHT / 2))
    if result_img:
        screen.blit(result_img, (3 * SCREEN_WIDTH / 4 - result_img.get_width() / 2, SCREEN_HEIGHT / 2 - result_img.get_height() / 2))
        pygame.display.flip()  # Update the screen
        pygame.time.wait(3000)  # Show result for 3 seconds
        game_state = 'awaiting input'
        user_choice_img = None
        result_img = None

    pygame.display.flip()  # Update the screen
    pygame.time.Clock().tick(60)  # Cap the frame rate

# Clean up
client.loop_stop()
client.disconnect()
pygame.quit()
sys.exit()