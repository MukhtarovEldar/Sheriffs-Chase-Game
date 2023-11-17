import pygame
import game_screens
from sheriff import Player

pygame.init()

# Set up the game window
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sheriff's Chase")

# Load the background image
background = pygame.image.load("./Game_Files/background/bg.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

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
horse_neighing.set_volume(0.01)

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

    # Update the player
    player.update(clock)
    screen.blit(player.image, player.rect)

    pygame.display.update()

pygame.quit()
