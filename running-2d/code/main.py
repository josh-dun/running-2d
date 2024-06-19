# i used sublime text so to import  an image i do  
# pygame.image.load("../graphics/other/splash.png")
# if you are using vscode or there is a error like that 
# just change the code to 
# pygame.image.load("graphics/other/splash.png")

import pygame, time, random
from sprites import Background, Block, Player,  Coins, Crash
from settings import * 

pygame.init()

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()        
        self.coin_sprites = pygame.sprite.Group()

        Background(self.all_sprites)
        self.blocks = [Block([self.all_sprites, self.block_sprites], (WIDTH // 1.5, HEIGHT), 400)]
        self.player = Player(self.all_sprites, (self.blocks[0].rect.x + self.blocks[0].width // 10, self.blocks[0].rect.y + 1))

        # coins 
        self.coins = 0 
        coin_img = pygame.image.load("../graphics/other/coin.png")
        self.coin_surf = pygame.transform.scale(coin_img, (30, 30))  

        # active
        self.active = "start_game" 
        self.points = 0
        self.crash = Crash()

    def display_coins_amount(self):
        font = pygame.font.SysFont("comicsans", WIDTH // 40)
        text = font.render(str(self.coins), True, "yellow")
        x = WIDTH - text.get_width() - 10
        y =  WIDTH // 60
        self.win.blit(self.coin_surf, (x - 6 - self.coin_surf.get_width(), y))
        self.win.blit(text, (x, y - 6))

    def display_points(self):
        font = pygame.font.SysFont("comicsans", WIDTH // 40)
        text = font.render(f"Points: {self.points}", True, "black")

        self.win.blit(text, (10, 10))


        

    def check_player_fall(self):
        if self.player.rect.centerx <= 0 or self.player.rect.centerx >= WIDTH:
            self.active = "end_game"

        elif self.player.rect.bottom >= HEIGHT:
            self.active = "end_game"
            fall_image = pygame.image.load("../graphics/other/fall.png")
            self.player.image = pygame.transform.scale(fall_image, (self.player.width * 2, self.player.height * 2))
            self.player.pos.y = HEIGHT - self.player.image.get_height()
            self.player.rect.y = round(self.player.pos.y)
            self.player.speed = 0 
            self.player.on_land = True 

    def collect_coins(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.coin_sprites, False, pygame.sprite.collide_mask)

        for coin in overlap_sprites:
            if not coin.kill_time:
                self.coins += 1
                splash_image = pygame.image.load("../graphics/other/splash.png")
                scaled_splash_image = pygame.transform.scale(splash_image, (COIN_WIDTH, COIN_HEIGHT))
                coin.image = scaled_splash_image

                coin.kill_time = time.time()

    def resetGame(self):
        self.active = "start_game"

        self.all_sprites.empty()
        self.block_sprites.empty()        
        self.coin_sprites.empty()

        Background(self.all_sprites)
        self.blocks = [Block([self.all_sprites, self.block_sprites], (WIDTH // 1.5, HEIGHT), 400)]
        self.player = Player(self.all_sprites, (self.blocks[0].rect.x + self.blocks[0].width // 10, self.blocks[0].rect.y + 1))
        self.crash = Crash()
        
        self.coins = 0 
        self.points = 0 

    def create_new_block(self):
        if self.blocks[0].rect.x < 200:
            self.points += 1 

            block = self.blocks.pop(0)
            
            speed = block.speed + ACCELERATE
            block.speed = speed
            self.blocks.append(Block([self.all_sprites, self.block_sprites], (WIDTH, HEIGHT), speed))
            
            block = self.blocks[0]
            if block.has_coins > 0:

                for i in range(block.coins_amount):
                    distance = (block.width - block.coins_amount * COIN_WIDTH) // (block.coins_amount + 1)
                    x = block.rect.x + distance * (i + 1) + i * COIN_WIDTH
                    Coins([self.all_sprites, self.coin_sprites], (x, block.rect.top - COIN_BLOCK_GAP), speed)

     

    def run(self):
        run = True 
        last_time = time.time()

        while run:  
            keys = pygame.key.get_pressed()

            dt = time.time() - last_time 
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if self.active == "playing" and self.player.jump_count < 2:
                            self.player.jump()
                            self.player.jump_count += 1 

                        elif self.active == "start_game":
                            self.active = "playing"

            
            self.create_new_block()
            self.player.player_block_collision(self.block_sprites)
            self.collect_coins()
            self.check_player_fall()

            # update the game
           
            self.all_sprites.update(dt, self.active)
            self.all_sprites.draw(self.win)
            self.display_coins_amount()
            self.display_points()

            if self.active == "end_game":
                if self.crash.height < HEIGHT:
                    self.crash.increaseSize(dt)
                else:
                    self.resetGame()


            # update window
            pygame.display.update()

        pygame.quit()


game = Game()
game.run()
