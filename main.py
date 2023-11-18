import pygame
import game_screens
from sheriff import Player

pygame.init()

# Set up the game window
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 512
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sheriff's Chase")

# Load the background image
background = pygame.image.load("./Game_Files/background/bg.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the horse carriage image
horse_carriage = pygame.image.load("./Game_Files/horse/carriage_no_wheel.png").convert_alpha()
wheel = pygame.image.load("./Game_Files/horse/wheel.png").convert_alpha()
horse_carriage = pygame.transform.scale(horse_carriage, (350, 350))
wheel = pygame.transform.scale(wheel, (150, 150))
clock = pygame.time.Clock()

# Set up the game variables
scroll_speed = 7
timer = 0
background_index = 0

# Create the player object
player = Player()

# Game loop
running = game_screens.start_screen_loop(screen)

horse_neighing = pygame.mixer.Sound("./Game_Files/sound/horse_neighing.mp3")
player.jump()
horse_neighing.play()
horse_neighing.set_volume(0.03)

game_sound = pygame.mixer.Sound("./Game_Files/sound/game_sound.mp3")
game_sound.play(loops=-1)
game_sound.set_volume(0.03)

rotation_angle = 0

anchor_x, anchor_y = wheel.get_width() / 2, wheel.get_height() / 2

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
                running = game_screens.pause_screen_loop(screen)

    # Update the game variables
    timer += clock.tick(60) / 1000
    scroll_speed += 0.003

    # Update the position of the background image
    background_index = (background_index - scroll_speed) % background.get_width()

    # Draw the background to the screen
    screen.blit(background, (background_index, 0))
    screen.blit(background, (background_index - background.get_width(), 0))

    # Draw the horse carriage to the screen
    screen.blit(horse_carriage, (1100, 105))

    # Rotate the wheel image
    rotated_wheel = pygame.transform.rotate(wheel, rotation_angle)
    pos_x = 1240 + anchor_x - rotated_wheel.get_width() / 2
    pos_y = 303 + anchor_y - rotated_wheel.get_height() / 2
    screen.blit(rotated_wheel, (pos_x, pos_y))

    # Update the rotation angle
    rotation_angle -= 2
    rotation_angle -= scroll_speed * 0.1

    # Update the player
    player.update(clock)
    screen.blit(player.image, player.rect)

    pygame.display.update()

game_sound.stop()

pygame.quit()
