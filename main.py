import pygame
import random

import game_screens
from sheriff import Player
from scoring import ScoringSystem
from obstacles import move_and_rotate_obstacles


pygame.init()

# Set up the game window
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 512
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sheriff's Chase")

# Load the background image
background = pygame.image.load("./Game_Files/background/bg.png").convert()
background = pygame.transform.scale(background, (2048, WINDOW_HEIGHT))

# Load the obstacle image
obstacle = pygame.image.load("./Game_Files/horse/barrel.png").convert_alpha()
obstacle = pygame.transform.scale(obstacle, (90, 90))

# Load the horse carriage and the wheel image
horse_carriage = pygame.image.load("./Game_Files/horse/carriage_no_wheel.png").convert_alpha()
wheel = pygame.image.load("./Game_Files/horse/wheel.png").convert_alpha()
horse_carriage = pygame.transform.scale(horse_carriage, (350, 350))
wheel = pygame.transform.scale(wheel, (150, 150))
clock = pygame.time.Clock()

# Set up the game variables
timer = 0
background_index = 0

# Create the player object
player = Player()

# Game loop
running = game_screens.start_screen_loop(screen)
# running = True

# Load Sound Effects
horse_neighing = pygame.mixer.Sound("./Game_Files/sound/horse_neighing.mp3")
player.jump()
horse_neighing_channel = horse_neighing.play()
horse_neighing.set_volume(0.03)
sheriff_speak = pygame.mixer.Sound("./Game_Files/sound/sheriff_speak.mp3")
sheriff_speak_channel = sheriff_speak.play()
sheriff_speak.set_volume(0.05)
barrel_hit = pygame.mixer.Sound("./Game_Files/sound/barrel_hit.mp3")
barrel_hit.set_volume(0.03)

game_sound = pygame.mixer.Sound("./Game_Files/sound/game_sound.mp3")
game_sound_channel = game_sound.play(loops=-1)
game_sound.set_volume(0.03)

rotation_angle = 0

anchor_x_wheel, anchor_y_wheel = wheel.get_width() // 2, wheel.get_height() // 2
anchor_x_obstacle, anchor_y_obstacle = obstacle.get_width() // 2, obstacle.get_height() // 2

obstacle_positions = []

scoring_system = ScoringSystem()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                if not player.jumping:
                    player.jump()
            elif event.key == pygame.K_a:
                player.move_left()
            elif event.key == pygame.K_d:
                player.move_right()
            elif event.key == pygame.K_ESCAPE:
                game_sound_channel.pause()
                if not player.jumping and not player.jumping_sound_channel.get_busy():
                    player.running_sound_channel.pause()
                player.jumping_sound_channel.pause()
                horse_neighing_channel.pause()
                sheriff_speak_channel.pause()
                running = game_screens.pause_screen_loop(screen)
                game_sound_channel.unpause()
                if not player.jumping and not player.jumping_sound_channel.get_busy():
                    player.running_sound_channel.unpause()
                player.jumping_sound_channel.unpause()
                horse_neighing_channel.unpause()
                sheriff_speak_channel.unpause()

    # Update the game variables
    scoring_system.update(clock)

    # Update the position of the background image
    background_index = (background_index - scoring_system.scroll_speed) % background.get_width()

    # Draw the background to the screen
    screen.blit(background, (background_index, 0))
    screen.blit(background, (background_index - background.get_width(), 0))

    # Update the player
    player.update(clock)
    screen.blit(player.image, player.rect)

    scoring_system.draw(screen)

    # Generate new obstacles randomly if there are no existing obstacles or if the existing obstacles have moved off the screen
    if len(obstacle_positions) == 0 or obstacle_positions[-1][0] + obstacle.get_width() + 350 < WINDOW_WIDTH:
        if random.random() < 0.02:  # Adjust the probability
            min_space = 550
            max_space = 1000
            x = WINDOW_WIDTH - 150
            y = 150
            space = random.randint(min_space, max_space)
            if len(obstacle_positions) > 0:
                last_obstacle_position = obstacle_positions[-1]
                if x - last_obstacle_position[0] >= space:
                    obstacle_positions.append((x, y))
            else:
                obstacle_positions.append((x, y))
    
    # Move and rotate the obstacles
    obstacle_positions = move_and_rotate_obstacles(WINDOW_WIDTH, obstacle_positions, obstacle, rotation_angle, anchor_x_obstacle, anchor_y_obstacle, scoring_system, screen, barrel_hit)

    # Draw the horse carriage to the screen
    screen.blit(horse_carriage, (1100, 105))

    # Rotate the wheel image
    rotated_wheel = pygame.transform.rotate(wheel, rotation_angle)
    pos_x_wheel = 1240 + anchor_x_wheel - rotated_wheel.get_width() // 2
    pos_y_wheel = 303 + anchor_y_wheel - rotated_wheel.get_height() // 2
    screen.blit(rotated_wheel, (pos_x_wheel, pos_y_wheel))

    # Update the rotation angle
    rotation_angle -= 2 + scoring_system.scroll_speed * 0.1

    pygame.display.update()

game_sound.stop()

pygame.quit()
