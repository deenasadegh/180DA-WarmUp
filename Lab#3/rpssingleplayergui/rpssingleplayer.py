import pygame
import random
import sys
import os  # Import the os module

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption('Rock, Paper, Scissors Game')

# Load and scale images
def load_image(name, size=(100, 100)):
    # Define the base path to the 'rpsSingleplayer' folder
    base_path = r'C:\Users\Deena\GITrepoEnv\Lab#3\rpssingleplayer'  # Update this path as necessary
    image_path = os.path.join(base_path, f'{name}.png')
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, size)

rock_img = load_image('rock')
paper_img = load_image('paper')
scissors_img = load_image('scissors')
win_img = load_image('win', (200, 200))
lose_img = load_image('lose', (200, 200))
tie_img = load_image('tie', (200, 200))

# Initialize font
font = pygame.font.Font(None, 36)

def get_bot_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "tie"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        return "win"
    else:
        return "lose"

# Main game loop
running = True
game_state = 'awaiting input'
user_choice = None
bot_choice = None
game_result = None
change_time = None

while running:
    screen.fill((0, 0, 0))  # Fill the screen with black
    current_time = pygame.time.get_ticks()

    if game_state == 'awaiting input':
        # Display the prompt
        prompt_text = font.render("Choose Rock (R), Paper (P), or Scissors (S)", True, (255, 255, 255))
        text_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, 50))
        screen.blit(prompt_text, text_rect)
    elif game_state == 'showing bot choice':
        if current_time - change_time > 3000:  # 3 seconds have passed
            game_state = 'displaying result'
            change_time = current_time
        else:
            bot_choice_text = font.render(f"The bot's choice is...", True, (255, 255, 255))
            text_rect = bot_choice_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(bot_choice_text, text_rect)
    elif game_state == 'displaying result':
        if current_time - change_time > 3000:  # 3 seconds have passed
            game_state = 'awaiting input'
        else:
            # Map bot choice to image
            bot_choice_img = None
            if bot_choice == 'rock':
                bot_choice_img = rock_img
            elif bot_choice == 'paper':
                bot_choice_img = paper_img
            elif bot_choice == 'scissors':
                bot_choice_img = scissors_img

            if bot_choice_img:
                screen.blit(bot_choice_img, (3 * SCREEN_WIDTH / 4 - bot_choice_img.get_width() / 2, SCREEN_HEIGHT / 2 - bot_choice_img.get_height() / 2))
           
            # Display the game result
            result_img = None
            if game_result == 'win':
                result_img = win_img
            elif game_result == 'lose':
                result_img = lose_img
            elif game_result == 'tie':
                result_img = tie_img

            if result_img:
                screen.blit(result_img, (SCREEN_WIDTH / 2 - result_img.get_width() / 2, SCREEN_HEIGHT / 2 - result_img.get_height() / 2 + 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif game_state == 'awaiting input' and event.key in [pygame.K_r, pygame.K_p, pygame.K_s]:
                if event.key == pygame.K_r:
                    user_choice = 'rock'
                elif event.key == pygame.K_p:
                    user_choice = 'paper'
                elif event.key == pygame.K_s:
                    user_choice = 'scissors'
               
                bot_choice = get_bot_choice()
                game_result = determine_winner(user_choice, bot_choice)
                game_state = 'showing bot choice'
                change_time = current_time

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
