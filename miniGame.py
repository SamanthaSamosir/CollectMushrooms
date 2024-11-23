import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Minigame")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 55)

# Define platforms
platform_color = BLACK
platforms = [
    pygame.Rect(100, 500, 600, 20),
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20)  # Ground platform
]

# Define goal
goal = pygame.Rect(WIDTH - 100, HEIGHT - 100, 50, 50)


# Player class using sprite group
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False

    def move(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Gravity
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Jump
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -15
            self.jumping = True

        # Collision detection
        self.jumping = True
        for platform in platforms:
            if self.rect.colliderect(platform) and self.vel_y >= 0:
                self.rect.y = platform.top - self.rect.height
                self.vel_y = 0
                self.jumping = False


# Render text function
def render_text(text, color, rect):
    label = font.render(text, True, color)
    screen.blit(label, rect)


# Main loop functions
def start_screen():
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
    running = True
    while running:
        screen.fill(WHITE)

        # Draw start button and text
        pygame.draw.rect(screen, GREEN, start_button)
        render_text("Start Game", BLACK, (start_button.x + 20, start_button.y + 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        clock.tick(FPS)


def game_screen():
    # Create player sprite and add to group
    player = Player(100, 100)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    win = False
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        player.move(platforms)

        # Draw platforms and goal
        for platform in platforms:
            pygame.draw.rect(screen, platform_color, platform)
        pygame.draw.rect(screen, RED, goal)

        # Draw all sprites
        all_sprites.draw(screen)

        # Check if player wins
        if player.rect.colliderect(goal):
            win = True
            running = False

        # Check if player falls off the screen (lose condition)
        if player.rect.y > HEIGHT:
            win = False
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    return win


def end_screen(win):
    running = True
    while running:
        screen.fill(WHITE)
        if win:
            render_text("You Win!", GREEN, (WIDTH // 2 - 100, HEIGHT // 2 - 25))
        else:
            render_text("You Lose!", RED, (WIDTH // 2 - 100, HEIGHT // 2 - 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)


# Main loop
def main():
    start_screen()
    win = game_screen()
    end_screen(win)


if __name__ == "__main__":
    main()
