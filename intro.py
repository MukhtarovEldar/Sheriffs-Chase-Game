import pygame
import webbrowser

def draw_text_with_outline(surface, text, font, x, y, text_color, outline_color=-1, outline_size=2):
    """
    Renders text with an optional outline onto a given surface.

    Args:
        surface: The surface to render the text onto.
        text: The text to render.
        font: The font to use for rendering.
        x: The x-coordinate of the top-left corner of the rendered text.
        y: The y-coordinate of the top-left corner of the rendered text.
        text_color: The color of the rendered text.
        outline_color: The color of the outline. If set to -1, no outline will be rendered.
        outline_size: The size of the outline. Defaults to 2 if not set.

    Returns:
        None
    """
    # Render the outline
    if outline_color != -1:
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            for i in range(outline_size):
                surface.blit(font.render(text, True, outline_color), (x + dx*i, y + dy*i))
    # Render the text
    surface.blit(font.render(text, True, text_color), (x, y))

def start_screen_loop():
    """
    This function sets up the game window, loads the intro image and sound, and creates the start screen loop.
    The loop waits for user input to either start the game or quit the game.
    If the user starts the game, the function returns True, otherwise it returns False.
    """
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_screen = False
                    running = True
                elif quit_button_rect.collidepoint(event.pos):
                    start_screen = False
                    running = False
                elif contribute_button_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/MukhtarovEldar/Sheriffs-Chase-Game")

        # Draw the start screen elements to the screen
        font_name = "./Game_Files/UI/TEXAT BOLD PERSONAL USE___.otf"
        font = pygame.font.Font(font_name, 30)

        screen.blit(intro_image, (0, 0))
        start_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (420, 178, 199, 63), 1)
        quit_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (420, 268, 199, 63), 1)
        contribute_button_rect = pygame.draw.rect(screen, (180, 84, 60, 0), (396, 385, 249, 45), 1)
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Start", font, 470, 188, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Start", font, 470, 188, (40, 20, 22))

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Quit", font, 480, 278, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Quit", font, 480, 278, (40, 20, 22))

        if contribute_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Contribute", font, 420, 387, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Contribute", font, 420, 387, (40, 20, 22))

        draw_text_with_outline(screen, "Press space to play", pygame.font.Font(font_name, 15), 430, 445, (255, 255, 255))

        pygame.display.update()

    intro_sound.stop()
    
    return running
