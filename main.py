import pygame

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
scroll_speed = 3
timer = 0
background_index = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the game variables
    timer += clock.tick(60) / 1000
    scroll_speed += 0.003

    # Update the position of the background image
    background_index = (background_index - scroll_speed) % background.get_width()

    # Draw the background to the screen
    screen.blit(background, (background_index, 0))
    screen.blit(background, (background_index - background.get_width(), 0))

    pygame.display.update()

pygame.quit()
