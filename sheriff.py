import pygame

class Player:
    def __init__(self, screen_width=1024):
        self.images = []
        for i in range(1, 9):
            self.images.append(pygame.transform.scale(pygame.image.load(f"./Game_Files/horse/{i}.png").convert_alpha(), (230, 230)))
        self.jump_images = []
        for i in range(1, 16):
            self.jump_images.append(pygame.transform.scale(pygame.image.load(f"./Game_Files/horse/jump/{i}.png").convert_alpha(), (230, 230)))
        self.animation_speed = 0.05
        self.animation_index = 0
        self.animation_timer = 0
        self.image = self.images[self.animation_index]
        self.jump_image = self.jump_images[self.animation_index]
        self.rect = self.image.get_rect()
        self.jump_rect = self.jump_image.get_rect()
        self.rect.bottomleft = (0, 380)
        self.jump_rect.bottomleft = (0, 387)
        self.jumping = False
        self.jump_timer = 0
        self.jumping_timer = len(self.jump_images) * self.animation_speed
        self.screen_width = screen_width
        self.mask = pygame.mask.from_surface(self.image)
        self.original_animation_speed = self.animation_speed
        self.jump_animation_speed = 0.05
        self.running_sound = pygame.mixer.Sound("./Game_Files/sound/run.mp3")
        self.jumping_sound = pygame.mixer.Sound("./Game_Files/sound/jumping_clearing_throat.mp3")
        self.running_sound.set_volume(0.03)
        self.jumping_sound.set_volume(0.03)

    def jump(self):
        keys = pygame.key.get_pressed()
        self.jumping = True
        self.animation_index = 0
        self.animation_timer = 0
        self.images = self.jump_images
        self.jumping_timer = len(self.jump_images) * self.jump_animation_speed
        self.running_sound.stop()
        self.jumping_sound_channel = self.jumping_sound.play()

    def move_left(self):
        if self.jumping:
            # Player is jumping, don't move left
            return
        if self.rect.x > 0:
            self.rect.x -= 10
            self.animation_speed += 0.01
            if self.animation_speed > 0.1:
                self.animation_speed = 0.1
            if not self.running_sound.get_num_channels():
                self.running_sound_channel = self.running_sound.play()

    def move_right(self):
        if self.jumping:
            # Player is jumping, don't move right
            return
        if self.rect.x < self.screen_width - self.rect.width:
            self.rect.x += 10
            self.animation_speed -= 0.01
            if self.animation_speed < 0.01:
                self.animation_speed = 0.01
            if not self.running_sound.get_num_channels():
                self.running_sound_channel = self.running_sound.play()

    def update(self, clock):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_right()

        if self.jumping:
            self.jump_timer += clock.tick(60) / 1000
            if self.jump_timer >= self.jump_animation_speed:
                self.jump_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.images):
                    self.jumping = False
                    self.images = []
                    for i in range(1, 9):
                        self.images.append(pygame.transform.scale(pygame.image.load(f"./Game_Files/horse/{i}.png").convert_alpha(), (250, 250)))
                    self.animation_index = 0
                else:
                    self.image = self.images[self.animation_index]
                    self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))
                    self.image = pygame.transform.flip(self.image, True, False)
            if self.jump_timer >= self.jumping_timer:
                self.jumping = False
                self.images = []
                for i in range(1, 9):
                    self.images.append(pygame.transform.scale(pygame.image.load(f"./Game_Files/horse/{i}.png").convert_alpha(), (250, 250)))
                self.animation_index = 0
                self.image = self.images[self.animation_index]
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))
                self.image = pygame.transform.flip(self.image, True, False)
                if not self.running_sound.get_num_channels():
                    self.running_sound_channel = self.running_sound.play()
        else:
            self.animation_timer += clock.tick(60) / 1000
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]
                self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.5), int(self.image.get_height() * 1.5)))
                self.image = pygame.transform.flip(self.image, True, False)
                self.animation_speed = self.original_animation_speed
                if not self.running_sound.get_num_channels():
                    self.running_sound_channel = self.running_sound.play()
