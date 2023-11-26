import pygame
from math import sin

played_obstacles = []


def move_and_rotate_obstacles(WINDOW_WIDTH, obstacle_positions, obstacle,
                              rotation_angle, anchor_x_obstacle,
                              anchor_y_obstacle, scoring_system,
                              screen, barrel_hit):
    """
    Moves and rotates the obstacles in the game.

    Args:
        WINDOW_WIDTH (int): The width of the game window.
        obstacle_positions (list): List of current obstacle positions.
        obstacle (pygame.Surface): The obstacle image.
        rotation_angle (float): The angle of rotation for the obstacles.
        anchor_x_obstacle (int): The x-coordinate of the obstacle anchor point.
        anchor_y_obstacle (int): The y-coordinate of the obstacle anchor point.
        scoring_system (ScoringSystem): The scoring system object.
        screen (pygame.Surface): The game screen surface.
        barrel_hit (pygame.mixer.Sound): The sound effect for hitting a barrel.

    Returns:
        list: Updated obstacle positions.
    """
    new_positions = []
    # Played obstacles is a list of y-coordinates of obstacles that have been
    # played. This is used to play the barrel hit sound effect only once per
    # obstacle.
    global played_obstacles
    for position in obstacle_positions:
        new_x = position[0] - (2 + scoring_system.scroll_speed * 0.1)
        if position[1] < 360:
            # Curved path animation
            new_y = position[1] + (new_x - (WINDOW_WIDTH - 150)) * \
                sin((new_x - (WINDOW_WIDTH - 150)) * 0.0005)
        else:
            new_y = position[1]

            if position[1] not in played_obstacles:
                played_obstacles.append(position[1])
                barrel_hit.play()

        new_positions.append((new_x, new_y))
    obstacle_positions = new_positions

    # Move the obstacles
    new_positions = []
    for position in obstacle_positions:
        new_position = (position[0] - scoring_system.scroll_speed, position[1])
        new_positions.append(new_position)
    obstacle_positions = new_positions

    # Rotate the obstacles
    for position in obstacle_positions:
        rotated_obstacle = pygame.transform.rotate(obstacle, -rotation_angle)
        pos_x_obstacle = position[0] + anchor_x_obstacle \
            - rotated_obstacle.get_width() // 2
        pos_y_obstacle = position[1] + anchor_y_obstacle \
            - rotated_obstacle.get_height() // 2
        screen.blit(rotated_obstacle, (pos_x_obstacle, pos_y_obstacle))

    # Remove obstacles that have gone off the screen
    obstacle_positions = [position for position in obstacle_positions
                          if position[0] + obstacle.get_width() > 0]

    return obstacle_positions
