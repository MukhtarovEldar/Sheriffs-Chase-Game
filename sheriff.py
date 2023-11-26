import pygame


class Player:
    """
    A class representing the player character.
    """
    def __init__(self, screen_width=1024):
        """
        Initialize the Sheriff object.

        Args:
            screen_width (int): The width of the game screen. Default is 1024.

        Attributes:
            images (list): A list of horse images.
            jump_images (list): A list of horse jump images.
            fall_images (list): A list of horse fall off images.
            animation_index (int): The index of the current animation frame.
            animation_timer (int): The timer for animation.
            image (Surface): The current horse image.
            jump_image (Surface): The current horse jump image.
            fall_image (Surface): The current horse fall off image.
            rect (Rect): The rectangle representing the horse's position.
            jump_rect (Rect): The rectangle representing
                the horse's jump position.
            fall_rect (Rect): The rectangle representing
                the horse's fall off position.
            jumping (bool): True if the horse is jumping, False otherwise.
            falling (bool): True if the horse is falling off, False otherwise.
            jump_timer (int): The timer for jump animation.
            fall_timer (int): The timer for fall off animation.
            animation_speed (float): The speed of the horse animation.
            jump_animation_speed (float): The speed of the jump animation.
            fall_animation_speed (float): The speed of the fall off animation.
            screen_width (int): The width of the game screen.
            original_animation_speed (float): The original speed
                of the horse animation.
            running_sound (Sound): The sound played when the horse is running.
            jumping_sound (Sound): The sound played when the horse is jumping.
            falling_sound (Sound): The sound played when the horse
                is falling off.
            has_fallen_off (bool): True if the horse has fallen off,
                False otherwise. Used to control running animation
                run after the falling animation ends.
            images_len (int): The length of the images list.
        """
        self.images = []
        for i in range(1, 9):
            self.images.append(
                pygame.transform.scale(
                    pygame.image.load(f"./Game_Files/UI/horse/{i}.png")
                    .convert_alpha(), (230, 230)))
        self.jump_images = []
        for i in range(1, 16):
            self.jump_images.append(
                pygame.transform.scale(
                    pygame.image.load(f"./Game_Files/UI/horse/jump/{i}.png")
                    .convert_alpha(), (230, 230)))
        self.fall_images = []
        for i in range(1, 35):
            self.fall_images.append(
                pygame.transform.scale(
                    pygame.image.load(f"./Game_Files/UI/horse/fall_off/{i}.png")
                    .convert_alpha(), (399, 266)))
        self.animation_index = 0
        self.animation_timer = 0
        self.image = self.images[self.animation_index]
        self.jump_image = self.jump_images[self.animation_index]
        self.fall_image = self.fall_images[self.animation_index]
        self.rect = self.image.get_rect()
        self.jump_rect = self.jump_image.get_rect()
        self.fall_rect = self.fall_image.get_rect()
        self.rect.bottomleft = (0, 380)
        self.jump_rect.bottomleft = (0, 387)
        self.fall_rect.bottomleft = (0, 387)
        self.jumping = False
        self.falling = False
        self.jump_timer = 0
        self.fall_timer = 0
        self.animation_speed = 0.05
        self.jump_animation_speed = 0.05
        self.fall_animation_speed = 0.05
        self.screen_width = screen_width
        self.original_animation_speed = self.animation_speed
        self.running_sound = pygame.mixer.Sound("./Game_Files/sound/run.mp3")
        self.jumping_sound = \
            pygame.mixer.Sound("./Game_Files/sound/jumping_clearing_throat.mp3")
        self.falling_sound = pygame.mixer.Sound("./Game_Files/sound/fall.mp3")
        self.running_sound.set_volume(0.03)
        self.jumping_sound.set_volume(0.03)
        self.falling_sound.set_volume(0.08)
        self.has_fallen_off = False
        self.images_len = 8

    def jump(self):
        """
        Makes the character jump if the player is not already falling.
        """
        if self.falling:
            return
        self.jumping = True
        self.images = self.jump_images
        self.jumping_timer = len(self.jump_images) * self.jump_animation_speed
        self.running_sound.stop()
        self.jumping_sound_channel = self.jumping_sound.play()
        self.animation_index = 0

    def move_left(self):
        """
        Move the player character to the left.
        """
        if self.jumping or self.falling:
            # Player is jumping or falling, don't move left
            return
        if self.rect.x > 0:
            self.rect.x -= 10
            self.animation_speed += 0.01
            if self.animation_speed > 0.1:
                self.animation_speed = 0.1
            if not self.running_sound.get_num_channels():
                self.running_sound_channel = self.running_sound.play()

    def move_right(self):
        """
        Move the player character to the right.
        """
        if self.jumping or self.falling:
            # Player is jumping or falling, don't move right
            return
        if self.rect.x < self.screen_width - self.rect.width:
            self.rect.x += 10
            self.animation_speed -= 0.01
            if self.animation_speed < 0.01:
                self.animation_speed = 0.01
            if not self.running_sound.get_num_channels():
                self.running_sound_channel = self.running_sound.play()

    def fall_off(self):
        """
        Sets the sheriff's state to fallen off and
        initiates the falling animation.
        """
        self.has_fallen_off = True
        self.falling = True
        self.images = self.fall_images
        self.falling_timer = len(self.fall_images) * self.fall_animation_speed
        self.running_sound.stop()
        self.falling_sound_channel = self.falling_sound.play()
        self.animation_index = 0

    def update(self, clock, scroll_speed):
        """
        Update the state of the sheriff character based on user input
        and game parameters.

        Args:
            clock (pygame.time.Clock): The game clock object.
            scroll_speed (float): The current scrolling speed of the game.

        Returns:
            None
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_right()

        if int(scroll_speed) % 10 == 0:
            self.jump_animation_speed -= 0.00004
        if self.jumping:
            self.jump_timer += clock.tick(60) / 1000
            if self.jump_timer >= self.jump_animation_speed:
                self.jump_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.images):
                    self.jumping = False
                    self.images = []
                    self.images_len = 8
                    if not self.has_fallen_off:
                        for i in range(1, 9):
                            self.images.append(pygame.transform.scale(
                                pygame.image.load
                                (f"./Game_Files/UI/horse/{i}.png")
                                .convert_alpha(), (250, 250)))
                    self.animation_index = 0
                else:
                    self.image = self.images[self.animation_index]
                    self.image = pygame.transform.scale(
                        self.image, (int(self.image.get_width() * 1.5),
                                     int(self.image.get_height() * 1.5)))
                    self.image = pygame.transform.flip(self.image, True, False)
                if self.jump_animation_speed < 0.01:
                    self.jump_animation_speed = 0.01
            if self.jump_timer >= self.jumping_timer:
                self.jumping = False
                self.images = []
                self.images_len = 8
                if not self.has_fallen_off:
                    for i in range(1, 9):
                        self.images.append(
                            pygame.transform.scale(
                                pygame.image.load
                                (f"./Game_Files/UI/horse/{i}.png")
                                .convert_alpha(), (250, 250)))
                self.animation_index = 0
                self.image = self.images[self.animation_index]
                self.image = pygame.transform.scale(
                    self.image, (int(self.image.get_width() * 1.5),
                                 int(self.image.get_height() * 1.5)))
                self.image = pygame.transform.flip(self.image, True, False)
                if not self.running_sound.get_num_channels():
                    self.running_sound_channel = self.running_sound.play()
        elif self.falling:
            self.fall_timer += clock.tick(60) / 1000
            if self.fall_timer >= self.fall_animation_speed:
                self.fall_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.images):
                    self.falling = False
                    self.images = []
                    self.images_len = 34
                    for i in range(1, 35):
                        self.images.append(pygame.transform.scale(
                            pygame.image.load
                            (f"./Game_Files/UI/horse/fall_off/{i}.png")
                            .convert_alpha(), (399, 266)))
                    self.animation_index = 0
                else:
                    self.image = self.images[self.animation_index]
                    self.image = pygame.transform.scale(
                        self.image, (int(self.image.get_width() * 1.5),
                                     int(self.image.get_height() * 1.5)))
                    self.image = pygame.transform.flip(self.image, True, False)
            if self.fall_timer >= self.falling_timer:
                self.falling = False
                self.images = []
                self.images_len = 34
                for i in range(1, 35):
                    self.images.append(pygame.transform.scale(
                        pygame.image.load
                        (f"./Game_Files/UI/horse/fall_off/{i}.png")
                        .convert_alpha(), (399, 266)))
                self.animation_index = 0
                self.image = self.images[self.animation_index]
                self.image = pygame.transform.scale(
                    self.image, (int(self.image.get_width() * 1.5),
                                 int(self.image.get_height() * 1.5)))
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.animation_timer += clock.tick(60) / 1000
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index = (
                    self.animation_index + 1) % self.images_len
                self.image = self.images[self.animation_index]
                self.image = pygame.transform.scale(
                    self.image, (int(self.image.get_width() * 1.5),
                                 int(self.image.get_height() * 1.5)))
                self.image = pygame.transform.flip(self.image, True, False)
                self.animation_speed = \
                    self.original_animation_speed - scroll_speed / 1000
                if self.animation_speed < 0.01:
                    self.animation_speed = 0.01
                if not self.running_sound.get_num_channels():
                    self.running_sound_channel = self.running_sound.play()
