import pygame
import sys
import random
from math import *

# Initialize Pygame
pygame.init()
width = 700
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Shooter Game")
clock = pygame.time.Clock()

# Variables for drawing and score
margin = 100
lowerBound = 100
score = 0
timer_limit = 30  # Time limit in seconds
target_balloons = 5  # Set the target balloons for Easy level

# Balloon speed, number of balloons, and timer limit by difficulty
difficulty_settings = {
    "easy": {"speed": 0.8, "target_balloons": 5, "timer_limit": 40},  # Slower speed for easy
    "medium": {"speed": 2, "target_balloons": 10, "timer_limit": 30},
    "hard": {"speed": 3, "target_balloons": 15, "timer_limit": 20},
}

# Generate random colors
skyBlue = (135, 206, 235)  # Sky blue color
white = (255, 255, 255)  # White color for clouds and text
darkBlue = (64, 178, 239)
red = (231, 76, 60)
green = (35, 155, 86)  # Green color for the button
purple = (155, 89, 182)
yellow = (244, 208, 63)
blue = (46, 134, 193)

# Set the general font of the project
font = pygame.font.SysFont("Snap ITC", 35)


# Function to draw clouds
def draw_cloud(x, y):
    pygame.draw.ellipse(display, white, (x, y, 60, 40))  # Main cloud body
    pygame.draw.ellipse(display, white, (x + 10, y - 10, 60, 40))  # Top left puff
    pygame.draw.ellipse(display, white, (x + 40, y - 10, 60, 40))  # Top right puff
    pygame.draw.ellipse(display, white, (x + 20, y + 10, 60, 40))  # Bottom puff


# Balloon class
class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound  # Start from the bottom of the screen
        self.angle = 90
        self.speed = -speed
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, yellow, blue])

    def move(self):
        direct = random.choice(self.proPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b),
                         (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if isonBalloon(self.x, self.y, self.a, self.b, pos):
            score += 1  # Increase score when a balloon is burst
            self.reset()

    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, yellow, blue])


# List of balloons for the main game
balloons = []


# Function to check if mouse is on the balloon
def isonBalloon(x, y, a, b, pos):
    return (x < pos[0] < x + a) and (y < pos[1] < y + b)


# Function to control pointer (crosshair)
def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = red
    for balloon in balloons:  # Use game balloons for pointer color
        if isonBalloon(balloon.x, balloon.y, balloon.a, balloon.b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r / 2, pos[1] - r / 2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l / 2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l / 2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l / 2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l / 2, pos[1]), (pos[0] - l, pos[1]), 4)


# Function to create lower platform
def lowerPlatform():
    pygame.draw.rect(display, darkBlue, (0, height - lowerBound, width, lowerBound))


# Function to show score on screen
def showScore():
    scoreText = font.render("Balloons Bursted : " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 50))


# Function to show timer on screen
def show_timer(remaining_time):
    timer_text = font.render(f"Time Left: {int(remaining_time)}", True, white)
    display.blit(timer_text, (10, 10))  # Position timer at top left corner


# Function to show target balloons
def show_target_balloons(target):
    target_text = font.render(f"Target Balloons: {target}", True, white)
    display.blit(target_text, (10, height - lowerBound + 20))  # Position target balloons text just below the score


# Function to close the game
def close():
    pygame.quit()
    sys.exit()


# Function to display the pause/resume button
def display_pause_button(paused):
    button_width = 100
    button_height = 40
    pause_button_rect = pygame.Rect(width - button_width - 20, 20, button_width, button_height)

    # Draw button background (green color)
    pygame.draw.rect(display, green, pause_button_rect)

    # Button text (Pause or Resume)
    button_text = "Resume" if paused else "Pause"
    button_text_surface = font.render(button_text, True, white)
    button_text_rect = button_text_surface.get_rect(center=pause_button_rect.center)
    display.blit(button_text_surface, button_text_rect)

    # Return the button rectangle for handling clicks
    return pause_button_rect


# Function to pause or resume the game
def toggle_pause(paused):
    paused = not paused
    return paused


# Function to show the difficulty selection screen
def difficulty_screen():
    difficulty_font = pygame.font.SysFont("Snap ITC", 35)
    navyBlue = pygame.Color('navy')  # Define navy blue color

    while True:
        display.fill(skyBlue)  # Change to sky blue background

        # Draw clouds in the background
        draw_cloud(100, 100)
        draw_cloud(400, 150)
        draw_cloud(600, 80)

        # Title text in navy blue and center-aligned
        title_text = difficulty_font.render("Choose Difficulty", True, navyBlue)
        title_rect = title_text.get_rect(center=(width // 2, height // 3))  # Center the title
        display.blit(title_text, title_rect)

        # Difficulty options (center-aligned)
        easy_text = difficulty_font.render("Easy (Press 1)", True, navyBlue)
        medium_text = difficulty_font.render("Medium (Press 2)", True, navyBlue)
        hard_text = difficulty_font.render("Hard (Press 3)", True, navyBlue)

        easy_rect = easy_text.get_rect(center=(width // 2, height // 2))
        medium_rect = medium_text.get_rect(center=(width // 2, height // 2 + 50))
        hard_rect = hard_text.get_rect(center=(width // 2, height // 2 + 100))

        display.blit(easy_text, easy_rect)
        display.blit(medium_text, medium_rect)
        display.blit(hard_text, hard_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"


# Function to get the player's name
def enter_name():
    input_box = pygame.Rect(width // 2 - 100, height // 2 + 40, 200, 50)  # Adjusted input box position
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.SysFont("Snap ITC", 35)
    clock = pygame.time.Clock()

    navyBlue = pygame.Color('navy')  # Define navy blue color

    label_font = pygame.font.SysFont("Snap ITC", 35)  # Font for the label
    welcome_text = label_font.render("Welcome to Balloon Shooter!", True, navyBlue)  # Welcome message in navy blue
    welcome_rect = welcome_text.get_rect(center=(width // 2, height // 2 - 100))  # Position above the label

    label_text = label_font.render("Enter Your Name:", True, navyBlue)  # Label text in navy blue
    label_rect = label_text.get_rect(center=(width // 2, height // 2 - 40))  # Position the label above the input box

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text  # Return the player's name when they press Enter
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]  # Remove last character if backspace is pressed
                    else:
                        text += event.unicode  # Add character to the text input

        display.fill(skyBlue)  # Set the background color
        display.blit(welcome_text, welcome_rect)  # Display the welcome message
        display.blit(label_text, label_rect)  # Draw the label
        pygame.draw.rect(display, color, input_box, 2)  # Draw the input box
        text_surface = font.render(text, True, navyBlue)  # Render the entered text in navy blue
        display.blit(text_surface, (input_box.x + 5, input_box.y + 5))  # Draw the text
        pygame.display.update()  # Update the display
        clock.tick(30)




# Main game loop
def game(difficulty, player_name):
    global score
    global balloons
    paused = False  # Game is not paused initially

    score = 0  # Reset score for a new game
    target_balloons = difficulty_settings[difficulty]["target_balloons"]
    balloons = [Balloon(difficulty_settings[difficulty]["speed"]) for _ in range(target_balloons)]  # Create a new set of balloons

    elapsed_time = 0  # Timer variable
    loop = True
    game_over_screen_shown = False  # Flag to check if game over screen is already shown

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:  # Check if R is pressed to restart the game
                    if game_over_screen_shown or paused:  # Only allow restart if the game is over or paused
                        return enter_name(), difficulty_screen()  # Restart the game with new name and difficulty

            if event.type == pygame.MOUSEBUTTONDOWN:
                if display_pause_button(paused).collidepoint(event.pos):  # Check if pause/resume button is clicked
                    paused = toggle_pause(paused)
                for balloon in balloons:
                    balloon.burst()  # Burst the balloons when clicked

        if not paused:  # If the game is not paused, update game state
            display.fill(skyBlue)  # Fill the background with sky blue for the game

            # Draw clouds in the background
            draw_cloud(100, 100)
            draw_cloud(400, 150)
            draw_cloud(600, 80)

            for balloon in balloons:
                balloon.show()

            pointer()

            for balloon in balloons:
                balloon.move()

            lowerPlatform()
            showScore()  # Show the score
            show_target_balloons(target_balloons)

            # Update and show timer
            elapsed_time += clock.get_time() / 1000  # Convert milliseconds to seconds
            remaining_time = difficulty_settings[difficulty]["timer_limit"] - elapsed_time
            show_timer(remaining_time)

            # Check if the time is up or if the target balloons are burst
            if remaining_time <= 0:
                if game_over("YOU LOSE!"):
                    game_over_screen_shown = True  # Set flag when game over screen is shown
                    return enter_name(), difficulty_screen()  # Restart the game

            if score >= target_balloons:
                if game_over("You Win!"):
                    game_over_screen_shown = True  # Set flag when game over screen is shown
                    return enter_name(), difficulty_screen()  # Restart the game
        else:  # If paused, display paused screen text
            paused_text = font.render("Game Paused", True, white)
            display.blit(paused_text, (width // 2 - 100, height // 2 - 20))

        display_pause_button(paused)  # Draw pause button

        if paused or game_over_screen_shown:  # Show restart prompt when paused or game over
            restart_text = font.render("Press R to Restart", True, white)
            display.blit(restart_text, (width // 2 - 120, height // 2 + 50))

        pygame.display.update()
        clock.tick(60)




# Function to show game over screen
def game_over(message):
    game_over_font = pygame.font.SysFont("Snap ITC", 50)
    game_over_text = game_over_font.render(message, True, red)
    display.blit(game_over_text, (width // 2 - 150, height // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Show the message for 2 seconds
    return True


# Start the game
player_name = enter_name()  # Show the name input screen
difficulty = difficulty_screen()  # Show the difficulty selection screen
while True:
    game(difficulty, player_name)  # Start the main game loop