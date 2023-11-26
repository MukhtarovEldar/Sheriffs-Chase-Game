import pygame
import random

import game_screens
from sheriff import Player
from scoring import ScoringSystem
from obstacles import move_and_rotate_obstacles


def game_running(WINDOW_WIDTH, screen, background, obstacle,
                 horse_carriage, wheel, horse_neighing,
                 sheriff_speak, barrel_hit, game_sound,
                 player, background_index, running):
    """
    Function that represents the main game loop.

    Args:
        WINDOW_WIDTH (int): The width of the game window.
        WINDOW_HEIGHT (int): The height of the game window.
        screen (pygame.Surface): The surface representing the game window.
        background (pygame.Surface): The background image of the game.
        obstacle (pygame.Surface): The image of the obstacle.
        horse_carriage (pygame.Surface): The image of the horse carriage.
        wheel (pygame.Surface): The image of the wheel.
        horse_neighing (pygame.mixer.Sound): The sound effect of horse neighing.
        sheriff_speak (pygame.mixer.Sound): The sound effect of sheriff speaking
        barrel_hit (pygame.mixer.Sound): The sound effect of barrel hit.
        game_sound (pygame.mixer.Sound): The background music of the game.
        player (Player): The player object.
        background_index (int): The index of the background image.
        running (bool): Flag indicating whether the game is running.

    Returns:
        The result of game_over_screen_loop() function call which is a boolean
        value indicating whether the player wants to play again.
    """

    clock = pygame.time.Clock()

    player.jump()

    # Create Channels for Sound Effects
    horse_neighing_channel = horse_neighing.play()
    sheriff_speak_channel = sheriff_speak.play()
    game_sound_channel = game_sound.play(loops=-1)

    # Wheel and barrel rotation angle
    rotation_angle = 0

    anchor_x_wheel = wheel.get_width() / 2
    anchor_y_wheel = wheel.get_height() / 2
    anchor_x_obstacle = obstacle.get_width() / 2
    anchor_y_obstacle = obstacle.get_height() / 2

    obstacle_positions = []

    horse_carriage_x = 1100
    wheel_x = 1240

    scoring_system = ScoringSystem()
    original_scroll_speed = None

    flag_collision = False
    flag_falling = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP \
                        or event.key == pygame.K_w:
                    if not player.jumping:
                        player.jump()
                elif event.key == pygame.K_a:
                    player.move_left()
                elif event.key == pygame.K_d:
                    player.move_right()
                elif event.key == pygame.K_ESCAPE:
                    # Pause the game sound
                    game_sound_channel.pause()
                    if not player.jumping:
                        player.running_sound_channel.pause()
                    player.jumping_sound_channel.pause()
                    horse_neighing_channel.pause()
                    sheriff_speak_channel.pause()

                    running = game_screens.pause_screen_loop(screen)

                    # Unpause the game sound
                    game_sound_channel.unpause()
                    if not player.jumping:
                        player.running_sound_channel.unpause()
                    player.jumping_sound_channel.unpause()
                    horse_neighing_channel.unpause()
                    sheriff_speak_channel.unpause()

        # Update the game variables
        if player.falling:
            if original_scroll_speed is None:
                original_scroll_speed = scoring_system.scroll_speed
            scoring_system.scroll_speed = 3
            speed_change = -2
            scoring_system.update(clock, speed_change)
        else:
            scoring_system.update(clock)

        # Update the position of the background image
        background_index = (background_index - scoring_system.scroll_speed) % \
            background.get_width()
        # Draw the background to the screen
        screen.blit(background, (background_index, 0))
        screen.blit(background, (background_index - background.get_width(), 0))

        # Draw the score to the screen
        scoring_system.draw(screen)

        # Generate new obstacles randomly if there are no existing obstacles
        # or if the existing obstacles have moved off the screen
        if not player.falling:
            if len(obstacle_positions) == 0 or \
                    obstacle_positions[-1][0] + \
                    obstacle.get_width() + 350 < WINDOW_WIDTH:
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
        obstacle_positions = \
            move_and_rotate_obstacles(WINDOW_WIDTH, obstacle_positions,
                                      obstacle, rotation_angle,
                                      anchor_x_obstacle, anchor_y_obstacle,
                                      scoring_system, screen, barrel_hit)

        if player.falling:
            # Move the horse carriage and wheel on x axis to the right
            horse_carriage_x += original_scroll_speed
            wheel_x += original_scroll_speed

        # Rotate the wheel image
        rotated_wheel = pygame.transform.rotate(wheel, rotation_angle)
        pos_x_wheel = wheel_x + anchor_x_wheel - rotated_wheel.get_width() // 2
        pos_y_wheel = 303 + anchor_y_wheel - rotated_wheel.get_height() // 2

        # Draw the horse carriage and the wheel to the screen
        screen.blit(horse_carriage, (horse_carriage_x, 105))
        screen.blit(rotated_wheel, (pos_x_wheel, pos_y_wheel))

        # Update the rotation angle
        rotation_angle -= 2 + scoring_system.scroll_speed * 0.1

        # Update the player
        player.update(clock, scoring_system.scroll_speed)
        screen.blit(player.image, player.rect)

        # Create collision masks for player and obstacle images
        player_mask = pygame.mask.from_surface(player.image)
        obstacle_mask = pygame.mask.from_surface(obstacle)

        # Check for collisions between player and obstacles
        for obstacle_pos in obstacle_positions:
            obstacle_mask_offset = (obstacle_pos[0] - player.rect.x,
                                    obstacle_pos[1] - player.rect.y)
            collision = player_mask.overlap(obstacle_mask, obstacle_mask_offset)

            if flag_collision or collision:
                if flag_falling:
                    player.fall_off()
                    flag_collision = True
                    flag_falling = False

        if not flag_falling and not player.falling:
            scores = scoring_system.calculate_score()

            # Game Sound Effects stop
            game_sound.stop()
            if not player.jumping and not \
                    player.jumping_sound_channel.get_busy():
                player.running_sound_channel.stop()
            player.jumping_sound_channel.stop()
            horse_neighing_channel.stop()
            sheriff_speak_channel.stop()

            # Load the game over screen
            game_screens.fade_to_black(screen)
            return game_screens.game_over_screen_loop(screen,
                                                      scores[0], scores[1])
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()

    flag_play_intro = True
    while True:
        WINDOW_WIDTH = 1440
        WINDOW_HEIGHT = 512

        # Set up the game window
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sheriff's Chase")

        # Load the background image
        background = pygame.image.load("./Game_Files/UI/background/bg.png") \
            .convert()
        background = pygame.transform.scale(background, (2048, WINDOW_HEIGHT))

        # Load the obstacle image
        obstacle = pygame.image.load("./Game_Files/UI/horse/barrel.png") \
            .convert_alpha()
        obstacle = pygame.transform.scale(obstacle, (83, 83))

        # Load the horse carriage and the wheel images
        horse_carriage = \
            pygame.image.load("./Game_Files/UI/horse/carriage_no_wheel.png") \
            .convert_alpha()
        wheel = pygame.image.load("./Game_Files/UI/horse/wheel.png") \
            .convert_alpha()
        horse_carriage = pygame.transform.scale(horse_carriage, (350, 350))
        wheel = pygame.transform.scale(wheel, (150, 150))

        # Load Sound Effects
        horse_neighing = \
            pygame.mixer.Sound("./Game_Files/sound/horse_neighing.mp3")
        horse_neighing.set_volume(0.03)
        sheriff_speak = \
            pygame.mixer.Sound("./Game_Files/sound/sheriff_speak.mp3")
        sheriff_speak.set_volume(0.05)
        barrel_hit = pygame.mixer.Sound("./Game_Files/sound/barrel_hit.mp3")
        barrel_hit.set_volume(0.05)

        game_sound = pygame.mixer.Sound("./Game_Files/sound/game_sound.mp3")
        game_sound.set_volume(0.03)

        # Set up the game variables
        background_index = 0

        # Create the player object
        player = Player()

        # Game loop
        if flag_play_intro:
            running = game_screens.start_screen_loop(screen)
            flag_play_intro = False

        if not game_running(WINDOW_WIDTH, screen, background, obstacle,
                            horse_carriage, wheel, horse_neighing,
                            sheriff_speak, barrel_hit, game_sound,
                            player, background_index, running):
            break

    pygame.quit()
