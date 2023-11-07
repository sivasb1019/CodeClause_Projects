import pygame
import random

# Initialize pygame
pygame.init()

# Game parameters and window setup
run = True
fps = 60
clock = pygame.time.Clock()
screen_width = 800
screen_height = 700

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
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

# Load game assets (images)
bg_image = pygame.image.load("Icons/bg-image1.png")
ground = pygame.image.load("Icons/ground.png")
restart_img = pygame.image.load("Icons/restart.png")
getready_img = pygame.image.load("Icons/getready.png")
gameover_img = pygame.image.load("Icons/gameover.png")

# Function to draw text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Function to reset the game state
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


# Bird class for the player character
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'Icons/Bird{i}.png') for i in range(1, 4)]
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
        self.image = pygame.image.load("Icons/pipe.png")
        self.rect = self.image.get_rect()
        pipe_gap = random.randint(50,100)
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
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Create the button instances
restart_btn = Button(screen_width // 2 - 45, screen_height // 2 - 60, restart_img)
getready_btn = Button2(screen_width // 2 - 80, screen_height // 2 - 200, getready_img)
gameover_btn = Button2(screen_width // 2 - 80, screen_height // 2 - 130, gameover_img)

# Main game loop
while run:
    clock.tick(fps)

    # Draw the background
    screen.blit(bg_image, (0, 0))

    # Update and draw the bird
    bird_group.draw(screen)
    bird_group.update()

    # Draw the pipes
    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground, (ground_scroll, 550))

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

    draw_text(str(score), font, color, int(screen_width / 2) - 5, 20)

    # Check for collisions
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Check if the bird hits the ground
    if flappy.rect.bottom >= 550:
        game_over = True
        fly = False

    # Display get ready button
    if not fly and not game_over:
        getready_btn.draw()

    # Update the game state when not in game over mode and the bird is flying
    if not game_over and fly:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-150, 50)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # Scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # Update the pipes
        pipe_group.update()

    # Handle game over and provide a restart option
    if game_over and not fly:
        if restart_btn.draw():
            game_over = False
            score = reset_game()

    # Event handling, including quitting the game and making the bird jump
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not fly and not game_over:
            fly = True

    # Update the display
    pygame.display.update()
pygame.quit()