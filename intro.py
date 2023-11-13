import pygame

pygame.init()

# Set up the game window
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 512
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sheriff's Chase")

# Load the intro image
intro_image = pygame.image.load("./Game_Files/UI/intro.png").convert()
intro_image = pygame.transform.scale(intro_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the intro sound
intro_sound = pygame.mixer.Sound("./Game_Files/sound/581415__peanut_shaman__western-bass.wav")
intro_sound.play(loops=-1)

# Create the start screen loop
start_screen = True
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_screen = False
                running = True
            elif event.key == pygame.K_ESCAPE:
                start_screen = False
                running = False

    screen.blit(intro_image, (0, 0))
        
    pygame.display.update()

intro_sound.stop()

pygame.quit()
