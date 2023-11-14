import pygame
import random

# Initialize pygame
pygame.init()

# Game parameters and window setup
RUN = True
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define fonts and colors
font = pygame.font.SysFont('impact', 50)
color = (255, 255, 255)

# Define game variables
ground_scroll = 0
scroll_speed = 3
fly = False
game_over = False
pipe_frequency = 1400  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
hit_sound = False
die_sound = False

# Load game assets (images)
bg_img = pygame.image.load("assets/images/bg-image1.png")
ground_img = pygame.image.load("assets/images/ground.png")
restart_img = pygame.image.load("assets/images/restart.png")
getready_img = pygame.image.load("assets/images/getready.png")
gameover_img = pygame.image.load("assets/images/gameover.png")

# Load game assets (audios)
swoosh_aud = pygame.mixer.Sound("assets/audio/swoosh.wav")
swoosh_aud.set_volume(0.10)
hit_aud = pygame.mixer.Sound("assets/audio/hit.wav")
hit_aud.set_volume(0.04)
die_aud = pygame.mixer.Sound("assets/audio/die.wav")
die_aud.set_volume(0.20)


# Function to reset the game state
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    points = 0
    global hit_sound, die_sound
    hit_sound = False
    die_sound = False
    return points


# Bird class for the player character
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'assets/images/Bird{i}.png') for i in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False

    def update(self):
        # Bird movement and animation logic
        if fly:
            # Apply gravity
            self.velocity += 0.2
            self.velocity = min(self.velocity, 6)  # Limit maximum downward velocity
            if self.rect.bottom < 550:
                self.rect.y += int(self.velocity)

        if not game_over:
            # Jump when the mouse is clicked
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.velocity = -6
                swoosh_aud.play()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Bird animation and rotation
            self.counter += 1
            flap_countdown = 10

            if self.counter > flap_countdown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -1.5)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# Pipe class for obstacles
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/pipe.png")
        self.rect = self.image.get_rect()
        pipe_gap = random.randint(50, 100)
        if position == -1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap]
        if position == 1:
            self.rect.topleft = [x, y + pipe_gap]

    def update(self):
        # Move the pipes to the left
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


# Function to display the score on the screen
def display_score(points):
    score_str = str(score)
    for digit in reversed(score_str):  # Iterate through digits in reverse order
        digit_image = pygame.image.load(f"assets/images/{digit}.png")
        screen.blit(digit_image, (int(SCREEN_WIDTH/2) - 5, 20))  # Display the digit image at (x, 10)


# Button class for the restart button
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        # Check if the mouse is over the button and clicked
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


class Button2(Button):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Create sprite groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Create the player's bird and add it to the bird group
flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)

# Create the button instances
restart_btn = Button(SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 - 60, restart_img)
getready_btn = Button2(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 200, getready_img)
gameover_btn = Button2(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 130, gameover_img)

# Main game loop
while RUN:
    CLOCK.tick(FPS)

    # Draw the background
    screen.blit(bg_img, (0, 0))

    # Update and draw the bird
    bird_group.draw(screen)
    bird_group.update()

    # Draw the pipes
    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground_img, (ground_scroll, 550))

    # Calculate and display the player's score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and not pass_pipe:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    display_score(score)
    # draw_text(str(score), font, color, int(SCREEN_WIDTH / 2) - 5, 20)

    # Check for collisions
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        if not hit_sound and not die_sound:
            hit_aud.play()  # Play hit sound effects when bird hit an object
            hit_sound = True
            die_aud.play()
            die_sound = True

    # Check if the bird hits the ground
    if flappy.rect.bottom >= 550:
        game_over = True
        fly = False

    # Update the game state when not in game over mode and the bird is flying
    if not game_over and fly:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-150, 50)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # Update the pipes
        pipe_group.update()

    # Display get ready button
    if not fly and not game_over:
        getready_btn.draw()

    # Handle game over and provide a restart option
    if game_over and not fly:
        gameover_btn.draw()
        if restart_btn.draw():
            game_over = False
            score = reset_game()

    # Event handling, including quitting the game and making the bird jump
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.MOUSEBUTTONDOWN and not fly and not game_over:
            fly = True

    # Update the display
    pygame.display.update()
pygame.quit()
