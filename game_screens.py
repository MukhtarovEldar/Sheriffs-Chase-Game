import pygame
import webbrowser

font_name = "./Game_Files/UI/TEXAT BOLD PERSONAL USE___.otf"

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
    if outline_color != -1:
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            for i in range(outline_size):
                surface.blit(font.render(text, True, outline_color), (x + dx*i, y + dy*i))
    surface.blit(font.render(text, True, text_color), (x, y))


def start_screen_loop(screen, WINDOW_WIDTH=1440, WINDOW_HEIGHT=512):
    """
    This function sets up the game window, loads the intro image and sound, and creates the start screen loop.
    The loop waits for user input to either start the game or quit the game.
    If the user starts the game, the function returns True, otherwise it returns False.
    """
    pygame.display.set_caption("Sheriff's Chase")

    intro_image = pygame.image.load("./Game_Files/UI/intro.png").convert()
    intro_image = pygame.transform.scale(intro_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    intro_sound = pygame.mixer.Sound("./Game_Files/sound/581415__peanut_shaman__western-bass.wav")
    intro_sound.play(loops=-1)

    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen = False
                    intro_sound.stop()
                    return story(screen, 1440)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_screen = False
                    intro_sound.stop()
                    return story(screen, 1440)
                elif quit_button_rect.collidepoint(event.pos):
                    start_screen = False
                    running = False
                elif contribute_button_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/MukhtarovEldar/Sheriffs-Chase-Game")

        # font_name = "./Game_Files/UI/TEXAT BOLD PERSONAL USE___.otf"
        font = pygame.font.Font(font_name, 30)

        screen.blit(intro_image, (0, 0))
        start_button_rect = pygame.draw.rect(screen, (65, 31, 41, 0), (WINDOW_WIDTH // 2 - 107, 178, 199, 63), 1)
        quit_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (WINDOW_WIDTH // 2 - 107, 268, 199, 63), 1)
        contribute_button_rect = pygame.draw.rect(screen, (180, 84, 60, 0), (WINDOW_WIDTH // 2 - 130, 385, 249, 45), 1)
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Start", font, WINDOW_WIDTH // 2 - 60, 188, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Start", font, WINDOW_WIDTH // 2 - 60, 188, (40, 20, 22))

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 46, 278, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 46, 278, (40, 20, 22))

        if contribute_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 107, 387, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 107, 387, (40, 20, 22))

        draw_text_with_outline(screen, "Press space to play", pygame.font.Font(font_name, 15), WINDOW_WIDTH // 2 - 97, 445, (255, 255, 255))

        pygame.display.update()

    intro_sound.stop()
    
    return running


def pause_screen_loop(screen, WINDOW_WIDTH=1440, WINDOW_HEIGHT=512):
    """
    This function creates the pause screen loop.
    The loop waits for user input to either continue the game or quit the game.
    If the user continues the game, the function returns True, otherwise it returns False.
    """
    # Load the pause image
    pause_image = pygame.image.load("./Game_Files/UI/pause.png").convert_alpha()
    pause_image = pygame.transform.scale(pause_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Load the pause sound
    pause_sound = pygame.mixer.Sound("./Game_Files/sound/581415__peanut_shaman__western-bass.wav")
    pause_sound.play(loops=-1)

    # Create the pause screen loop
    pause_screen = True
    while pause_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    pause_screen = False
                    running = True
            elif event.type == pygame.QUIT:
                pause_screen = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    pause_screen = False
                    running = True
                elif quit_button_rect.collidepoint(event.pos):
                    pause_screen = False
                    running = False
                elif contribute_button_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/MukhtarovEldar/Sheriffs-Chase-Game")

        screen.blit(pause_image, (0, 0))

        font = pygame.font.Font(font_name, 30)

        resume_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (WINDOW_WIDTH // 2 - 107, 178, 199, 63), 1)
        quit_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (WINDOW_WIDTH // 2 - 107, 268, 199, 63), 1)
        contribute_button_rect = pygame.draw.rect(screen, (180, 84, 60, 0), (WINDOW_WIDTH // 2 - 130, 385, 249, 45), 1)

        if resume_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Resume", font, WINDOW_WIDTH // 2 - 70, 188, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Resume", font, WINDOW_WIDTH // 2 - 70, 188, (40, 20, 22))

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 46, 278, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 46, 278, (40, 20, 22))

        if contribute_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 107, 387, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 107, 387, (40, 20, 22))

        draw_text_with_outline(screen, "Press space to play", pygame.font.Font(font_name, 15), WINDOW_WIDTH // 2 - 97, 445, (255, 255, 255))

        pygame.display.update()

    pause_sound.stop()

    return running


def story(screen, WINDOW_WIDTH=1440, WINDOW_HEIGHT=512):
    """
    This function creates the story screen loop.
    The loop waits for 4 seconds for each image to be displayed.
    """
    # Load the story images
    story_images = []
    for i in range(1, 5):
        story_images.append(pygame.image.load(f"./Game_Files/UI/background/scene{i}.png").convert_alpha())
    story_images = [pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT)) for image in story_images]

    pygame.mixer.music.load("./Game_Files/sound/story_sound.mp3")
    pygame.mixer.music.play()

    story_screen = True
    current_image = 0
    start_time = pygame.time.get_ticks()
    running = False
    while story_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    story_screen = False
                    running = True
            elif event.type == pygame.QUIT:
                story_screen = False
                running = False

        screen.blit(story_images[current_image], (0, 0))

        draw_text_with_outline(screen, "Press space to skip", pygame.font.Font(font_name, 15), WINDOW_WIDTH // 2 - 80, 445, (255, 255, 255))

        pygame.display.update()

        time_elapsed = pygame.time.get_ticks() - start_time
        if time_elapsed >= 5000:
            current_image += 1
            start_time = pygame.time.get_ticks()

        if current_image == 4:
            story_screen = False
            running = True

    fade_to_black(screen, WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.mixer.music.stop()

    return running


def game_over_screen_loop(screen, best_score, current_score, WINDOW_WIDTH=1440, WINDOW_HEIGHT=512):
    """
    This function creates the try again screen loop.
    The loop waits for user input to either try again or quit the game.
    If the user chooses to try again, the function returns True, otherwise it returns False.
    """

    # Load the game over sound
    game_over_sound = pygame.mixer.Sound("./Game_Files/sound/581415__peanut_shaman__western-bass.wav")
    game_over_sound.play(loops=-1)

    game_over_image = pygame.image.load("./Game_Files/UI/game_over.png").convert_alpha()
    game_over_image = pygame.transform.scale(game_over_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_sound.stop()
                    return True
            elif event.type == pygame.QUIT:
                game_over_sound.stop()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_button_rect.collidepoint(event.pos):
                    game_over_sound.stop()
                    return True
                elif quit_button_rect.collidepoint(event.pos):
                    game_over_sound.stop()
                    return False
                elif contribute_button_rect.collidepoint(event.pos):
                    webbrowser.open("https://github.com/MukhtarovEldar/Sheriffs-Chase-Game")

        screen.blit(game_over_image, (0, 0))

        font = pygame.font.Font(font_name, 30)

        try_again_button_rect = pygame.draw.rect(screen, (65, 31, 41, 0), (WINDOW_WIDTH // 2 - 118, 202, 235, 63), 1)
        quit_button_rect = pygame.draw.rect(screen, (0, 0, 0, 0), (WINDOW_WIDTH // 2 - 118, 292, 235, 63), 1)
        contribute_button_rect = pygame.draw.rect(screen, (180, 84, 60, 0), (WINDOW_WIDTH // 2 - 123, 400, 249, 45), 1)
        if try_again_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Try Again", font, WINDOW_WIDTH // 2 - 90, 210, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Try Again", font, WINDOW_WIDTH // 2 - 90, 210, (40, 20, 22))

        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 38, 302, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Quit", font, WINDOW_WIDTH // 2 - 38, 302, (40, 20, 22))

        if contribute_button_rect.collidepoint(pygame.mouse.get_pos()):
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 100, 401, (253, 236, 193), (0, 24, 29))
        else:
            draw_text_with_outline(screen, "Contribute", font, WINDOW_WIDTH // 2 - 100, 401, (40, 20, 22))

        draw_text_with_outline(screen, "Press space to replay", pygame.font.Font(font_name, 15), WINDOW_WIDTH // 2 - 97, 460, (255, 255, 255))

        font_score = pygame.font.Font("./Game_Files/UI/Carnevalee Freakshow.ttf", 35)

        # Write best_score and current_score to the screen
        draw_text_with_outline(screen, str(best_score), font_score, WINDOW_WIDTH // 2 + 55, 90, (253, 236, 193), (0, 24, 29))
        draw_text_with_outline(screen, str(current_score), font_score, WINDOW_WIDTH // 2 + 55, 125, (253, 236, 193), (0, 24, 29))

        pygame.display.update()


def fade_to_black(screen, WINDOW_WIDTH=1440, WINDOW_HEIGHT=512):
    """
    This function creates a black fading effect.
    """
    fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)