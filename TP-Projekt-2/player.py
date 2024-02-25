import pygame

class Player():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        """
        Creates a player character.

        Parameters:
            player (int): Player number.
            x (int): X-coordinate for the player.
            y (int): Y-coordinate for the player.
            flip (bool): True if the player should be flipped.
            data (list): List containing player information: [size, image_scale, offset].
            sprite_sheet (Surface): Sprite-sheet for the player.
            animation_steps (list): List containing the number of steps for each animation.
            sound (Sound): Sound effect for the player.
        """
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0 idle, 1 run, 2 jump, 3 attack, 4 attack2, 5 hit, 6 death.
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.velocity_y = 0
        self.running = False
        self.is_jumping = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.is_hit = False
        self.health = 100
        self.is_alive = True

    def load_images(self, sprite_sheet, animation_steps):
        """
        Loads images for player animations from the sprite-sheet.

        Parameters:
            sprite_sheet (Surface): Sprite-sheet for the player.
            animation_steps (list): List containing the number of steps for each animation.

        Returns:
            list: List containing loaded images for each animation.
        """
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        """
        Handles player movement.

        Parameters:
            screen_width (int): Width of the player's screen.
            screen_height (int): Height of the player's screen.
            surface (Surface): Surface where the player will draw.
            target (Player): Target for the player.
            round_over (bool): True if the round is over.
        """
        SPEED = 9
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if self.is_alive == True:
            if self.attacking == False and self.is_alive == True and round_over == False:
                if self.player == 1:
                    if key[pygame.K_a]:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_d]:
                        dx = SPEED
                        self.running = True
                    if key[pygame.K_w] and self.is_jumping== False:
                        self.velocity_y = -30
                        self.is_jumping = True
                    if key[pygame.K_r] or key[pygame.K_t]:
                        self.attack(target)
                        if key[pygame.K_r]:
                            self.attack_type = 1
                        if key[pygame.K_t]:
                            self.attack_type = 2 

                if self.player == 2:
                    if key[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = SPEED
                        self.running = True
                    if key[pygame.K_UP] and self.is_jumping == False:
                        self.velocity_y = -30
                        self.is_jumping = True
                    if key[pygame.K_k] or key[pygame.K_l]:
                        self.attack(target)
                        if key[pygame.K_k]:
                            self.attack_type = 1
                        if key[pygame.K_l]:
                            self.attack_type = 2 

        self.velocity_y += GRAVITY
        dy += self.velocity_y
        
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right    
        if self.rect.bottom + dy > screen_height - 90:
            self.velocity_y = 0
            self.is_jumping = False
            dy = screen_height - 90 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        """
        Updates player stats and animations.
        """
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            self.update_action(6)
        elif self.is_hit== True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.is_jumping == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.is_alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:    
                if self.action == 3 or self.action == 4: 
                    self.attacking = False
                    self.attack_cooldown = 30
                if self.action == 5:
                    self.is_hit= False
                    self.attacking = False
                    self.attacking_cooldown = 20

    def attack(self, target):
        """
        Executes an attack towards the target.

        Parameters:
            target (Player): Target for the attack.
        """
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 *self.rect.width * self.flip), self.rect.y, 2* self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.is_hit= True

    def update_action(self, new_action):
        """
        Updates player action.

        Parameters:
            new_action (int): New action for the player.
        """
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        """
        Draws the player on the surface and makes sure the players characters are facing eachother.

        Parameters:
            surface (Surface): Surface where the player will be drawn.
        """
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
