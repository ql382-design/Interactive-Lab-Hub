import pygame, sys, time, random
from gpiozero import Button
from threading import Thread

# -----------------------
# Configure GPIO Buttons (MiniPiTFT)
# -----------------------
btn1 = Button(23, pull_up=True)  # Reverse time
btn2 = Button(24, pull_up=True)  # Pause/unpause

# -----------------------
# Initialize Pygame
# -----------------------
pygame.init()
WIDTH, HEIGHT = 800, 480  # Change to your VNC desktop size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River of Time")

# Colors
BLUE = (30, 144, 255)      # Background river
WHITE = (255, 255, 255)    # Normal particle
MEMORY_COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0)]  # Special memory particles

# State variables
paused = False
reverse = False
particles = []  # Each particle = [x, y, color, alpha, created_time]
last_spawn = time.time()

# -----------------------
# Handle MiniPiTFT button presses in a separate thread
# -----------------------
def handle_buttons():
    global paused, reverse, particles
    while True:
        if btn1.is_pressed and not btn2.is_pressed:
            reverse = True
        elif btn2.is_pressed and not btn1.is_pressed:
            paused = not paused
            time.sleep(0.3)  # debounce
        elif btn1.is_pressed and btn2.is_pressed:
            # Generate colorful memory particle
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice(MEMORY_COLORS)
            particles.append([x, y, color, 255, time.time()])
            time.sleep(0.5)

Thread(target=handle_buttons, daemon=True).start()

# -----------------------
# Main loop
# -----------------------
clock = pygame.time.Clock()

while True:
    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -----------------------
    # Keyboard input for VNC
    # -----------------------
    keys = pygame.key.get_pressed()
    reverse = False  # Default forward
    if keys[pygame.K_r]:      # Press R to reverse
        reverse = True
    if keys[pygame.K_p]:      # Press P to toggle pause
        paused = not paused
        time.sleep(0.3)
    if keys[pygame.K_m] and keys[pygame.K_n]:  # Press M+N to generate memory
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(MEMORY_COLORS)
        particles.append([x, y, color, 255, time.time()])
        time.sleep(0.5)

    # -----------------------
    # MiniPiTFT button input
    # -----------------------
    if btn1.is_pressed and not btn2.is_pressed:
        reverse = True
    if btn2.is_pressed and not btn1.is_pressed:
        paused = not paused
        time.sleep(0.3)
    if btn1.is_pressed and btn2.is_pressed:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(MEMORY_COLORS)
        particles.append([x, y, color, 255, time.time()])
        time.sleep(0.5)

    # -----------------------
    # Spawn normal particle every second
    # -----------------------
    if not paused and time.time() - last_spawn >= 1:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        particles.append([x, y, WHITE, 255, time.time()])
        last_spawn = time.time()

    # -----------------------
    # Update particles
    # -----------------------
    new_particles = []
    for p in particles:
        x, y, color, alpha, born = p

        if not paused:
            if reverse:
                y -= 1   # Move up
            else:
                y += 1   # Move down

            alpha -= 2
            if alpha > 0:
                new_particles.append([x, y, color, alpha, born])
        else:
            new_particles.append(p)

    particles = new_particles

    # -----------------------
    # Draw particles
    # -----------------------
    screen.fill(BLUE)
    for x, y, color, alpha, born in particles:
        s = pygame.Surface((10, 10), pygame.SRCALPHA)
        s.fill((*color, alpha))
        screen.blit(s, (x, y))

    pygame.display.flip()
    clock.tick(60)

