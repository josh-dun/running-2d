# sprites 

# i used sublime text so to import  an image i do  
# pygame.image.load("../graphics/other/splash.png")
# if you are using vscode or there is a error like that 
# just change the code to 
# pygame.image.load("graphics/other/splash.png")

import pygame, random, time
from settings import * 


class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        colors = ["blue"]
        color = random.choice(colors)
        bg_image = pygame.image.load(f"../graphics/other/background.jpg").convert_alpha()

        scale_factor = HEIGHT / bg_image.get_height()


        self.image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.speed = 300


class Coins(pygame.sprite.Sprite):
    def __init__(self, groups, pos, speed):
        super().__init__(groups)

        coin_img = pygame.image.load("../graphics/other/coin.png")
        self.image = pygame.transform.scale(coin_img, (COIN_WIDTH, COIN_HEIGHT))
        
        self.rect = self.image.get_rect(bottomleft = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = speed

        self.mask = pygame.mask.from_surface(self.image)

        self.kill_time = 0 

    def update(self, dt, active):
        if active == "playing":
            self.pos.x -= self.speed * dt 
            self.rect.x = round(self.pos.x)

            if self.kill_time and time.time() - self.kill_time >= 0.2:
                self.kill()

class Block(pygame.sprite.Sprite):
    def __init__(self, groups, pos, speed):
        super().__init__(groups)
        self.width = random.randint(WIDTH // 4, WIDTH // 3)
        self.height = random.randint(HEIGHT // 6, HEIGHT // 3)
        color = random.choice(["red", "brown", "blue", "grey", "green"])

        block_img = pygame.image.load(f"../graphics/bricks/{color}-brick.png")
        self.image = pygame.transform.scale(block_img, (self.width, self.height))

        self.rect = self.image.get_rect(bottomleft = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.coins_amount = random.randint(0, 10)

        self.has_coins = False
        if self.coins_amount >= 4:
            self.has_coins = True

        self.speed = speed

    def update(self, dt, active):
        if active == "playing":
            self.pos.x -= self.speed * dt 
            self.rect.x = round(self.pos.x)

            if self.rect.right <= 0:
                self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        # create imge
        player_img = pygame.image.load("../graphics/player/idle.png")
        self.scaled_player_img = pygame.transform.scale(player_img, (player_img.get_width() * 2, player_img.get_height() * 2))
        self.image = pygame.Surface((self.scaled_player_img.get_width() // 11, self.scaled_player_img.get_height()))
        self.image.blit(self.scaled_player_img, (0, 0))
        self.image.set_colorkey((0,0,0))

        # size
        self.width = self.scaled_player_img.get_width() // 11
        self.height = self.scaled_player_img.get_height()

        # position
        self.rect = self.image.get_rect(midbottom = pos)
        self.old_rect = self.rect.copy()
        self.old_rect.y -= 1
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # setup
        self.speed = 0
        self.gravity = 600 
        self.on_land = True

        self.mask = pygame.mask.from_surface(self.image)
        self.jump_count = 0 

    def jump(self):
        self.speed = -300 
        self.rect.y -= 1 
        self.pos.y = self.rect.y

        self.on_land = False 

    def move_left_and_right(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
                self.rect.x += 300 * dt
                self.pos.x = self.rect.x 

        if keys[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.pos.x = self.rect.x

    def update_image(self):
        if self.speed < 0:
            jump_img = pygame.image.load("../graphics/player/jump.png")
            scaled_jump_img = pygame.transform.scale(jump_img, (self.width, self.height))

            self.image = scaled_jump_img

        elif self.speed > 0:
            fall_img = pygame.image.load("../graphics/player/fall.png")
            scaled_fall_img = pygame.transform.scale(fall_img, (self.width, self.height))

            self.image = scaled_fall_img

        else:
            self.image = pygame.Surface((self.scaled_player_img.get_width() // 11, self.scaled_player_img.get_height()))
            self.image.blit(self.scaled_player_img, (0, 0))
            self.image.set_colorkey((0,0,0))
       

    def player_block_collision(self, block_sprites):
        overlap_sprites = pygame.sprite.spritecollide(self, block_sprites, False)

        if overlap_sprites:
            for block in overlap_sprites:
                if self.rect.bottom > block.rect.top and (self.old_rect.bottom <= block.rect.top or self.on_land == True):                    

                    self.on_land = True
                    self.speed = 0 
                    self.jump_count = 0  

                    self.rect.bottom = block.rect.top + 1
                    self.pos.y = self.rect.y


                elif self.rect.right > block.rect.left and (self.old_rect.left <= block.rect.left):
                    self.rect.right = block.rect.left
                    self.on_land = False

                else:
                    self.rect.left = block.rect.right
                    self.on_land = False

        else:
            if self.on_land:
                self.on_land = False 


    def update(self, dt, active):
        if active == "playing":
            self.old_rect = self.rect.copy()

            if not self.on_land:
                self.speed += self.gravity * dt

                self.pos.y += self.speed * dt
                self.rect.y = round(self.pos.y)

            self.update_image()
            self.move_left_and_right(dt)


class Crash:
    def __init__(self):
        self.win = pygame.display.get_surface()
        self.crash_png = pygame.image.load("../graphics/other/crash.png")
        self.width = 0
        self.height = 0

        self.crash_image = pygame.transform.scale(self.crash_png, (0, 0))
        self.speed = 300 
        self.x = 0 
        self.y = 0 

    def increaseSize(self, dt):
        self.height += 10
        self.width = self.height * (WIDTH // HEIGHT)
        
        self.crash_image = pygame.transform.scale(self.crash_png, (int(self.width), int(self.height)))

        self.x = WIDTH // 2 - int(self.width) // 2
        self.y = HEIGHT // 2 - int(self.height) // 2


        self.win.blit(self.crash_image, (self.x, self.y))
