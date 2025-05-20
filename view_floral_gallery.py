import pygame
import time
import os

# Image files
images = [
    "cairo_floral_mandala.png",
    "kaleidoscope_tiling.png",
    "spiral_bloom_field.png"
]

# Fullscreen setup
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
SCENE_DURATION = FPS * 10  # 10 seconds per image

# Load and scale images
loaded_images = []
for img_name in images:
    if os.path.exists(img_name):
        img = pygame.image.load(img_name).convert_alpha()
        scaled = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
        loaded_images.append(scaled)

if not loaded_images:
    raise FileNotFoundError("None of the images were found in the current directory.")

# Viewer loop
running = True
current_index = 0
frame_count = 0

while running:
    screen.fill((10, 10, 30))
    screen.blit(loaded_images[current_index], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

    if frame_count >= SCENE_DURATION:
        frame_count = 0
        current_index = (current_index + 1) % len(loaded_images)

pygame.quit()