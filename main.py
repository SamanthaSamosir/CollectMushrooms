import pygame
from sprites import *
from config import *
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0 #keep track the score
        self.start_time = 0
        #convert_alpha to make the image drawing faster
        self.mushroom_image = pygame.transform.scale(pygame.image.load("img/img/mushroom.png").convert_alpha(), (32,32))
        #print(type(self.mushroom_image))
        self.character_spritesheet = Spritesheet("img/img/character.png")
        self.terrain_spritesheet = Spritesheet("img/img/terrain.png")

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)  # Spawn the player at "P"
                if column == "M":
                    Mushroom(self,j,i) #to spawn the mushrooms inside the M

    def new(self):
        # Initialize sprite groups before creating the tilemap
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.mushrooms = pygame.sprite.LayeredUpdates()

        # Create the tilemap after initializing the sprite groups
        self.createTilemap()
        self.playing = True
        self.start_time = pygame.time.get_ticks() #tracking time

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        #whether it collides w our player or no
        #mushroom_hits = pygame.sprite.spritecollide(self.player,self.mushrooms, True)
        for mushroom in self.mushrooms:
            if self.player.rect.colliderect(mushroom.rect):
                mushroom.kill()
                self.score +=1
        # Check win/lose condition
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= TIME_LIMIT:
            self.playing = False
        elif self.score >= MUSHROOMS_TO_WIN:
            self.playing = False  # Player collected enough mushrooms

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.mushrooms.draw(self.screen)
        self.draw_text(f"Score: {self.score}",30,(255,255,255),WIN_WIDTH//2,10)
        #timer
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = max(0, TIME_LIMIT - elapsed_time) // 1000
        self.draw_text(f"Time Left: {remaining_time}s", 30, (255, 255, 255), WIN_WIDTH // 2, 50)

        self.clock.tick(FPS)
        pygame.display.update()

    def draw_text(self, text,size,color,x,y):
        font = pygame.font.SysFont(None, size)
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        #self.running = False

    def game_over(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if self.score >=MUSHROOMS_TO_WIN and elapsed_time <= TIME_LIMIT:
            #print("You win!")
            self.end_screen("Win")
        else:
            #print("You lose!")
            self.end_screen("Lose")

    def intro_screen(self):
        intro = True
        while intro:
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None,75)
            text = font.render("Press Any Key to Start",True, RED)
            self.screen.blit(text,(WIN_WIDTH//2-text.get_width()//2, WIN_HEIGHT//2-text.get_height()//2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro =False
                    self.running=False
                if event.type == pygame.KEYDOWN:
                    intro = False
    def end_screen(self,result):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None,75)
        if result=="Win":
            text = font.render("You Win!", True, (0, 255, 0))
        else:
            text = font.render("You Lose!", True, (255, 0, 0))
        self.screen.blit(text,(WIN_WIDTH//2-text.get_width()//2,WIN_HEIGHT//2-text.get_height()//2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting =False
                    self.running=False
                if event.type == pygame.KEYDOWN:
                    waiting = False
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()
