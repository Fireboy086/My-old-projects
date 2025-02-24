import pygame as PG
import Level_data as LD
from enum import Enum

PG.init()

screen = PG.display.set_mode((800, 600))
clock = PG.time.Clock()

# Platform setup
platform_rects = []
for i in range(len(LD.platforms)):
    d = LD.platforms[f"platform{i+1}"]
    platform_rects.append(PG.Rect(d["x"], d["y"], d["width"], d["height"]))

# Player variables
player_pos = [400, 300]
player_accel = [0, 0]
player_speed = 5
jump_height = 10
gravity = 0.5
player_friction = 0.1
class Collision(Enum):
    NONE = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
collision = Collision.NONE

running = True
while running:
    for event in PG.event.get():
        if event.type == PG.QUIT:
            running = False
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_LEFT:
                player_accel[0] -= player_speed
                player_accel[0] = max(player_accel[0], -player_speed)
            elif event.key == PG.K_RIGHT:
                player_accel[0] += player_speed
                player_accel[0] = min(player_accel[0], player_speed)
            elif event.key == PG.K_UP:
                player_accel[1] = -jump_height

    # Gravity and friction
    player_accel[1] += gravity
    if player_accel[0] >= 0:
        player_accel[0] -= player_friction
    elif player_accel[0] < 0:
        player_accel[0] += player_friction
        

    # Move player
    player_pos[0] += player_accel[0]
    player_pos[1] += player_accel[1]

    # Create player rect
    player_rect = PG.Rect(player_pos[0], player_pos[1], 50, 50)

    # Check collision
    collision = Collision.NONE
    for p in platform_rects:
        if p.colliderect(player_rect):
            # Determine overlap
            dx = min(player_rect.right - p.left, p.right - player_rect.left)
            dy = min(player_rect.bottom - p.top, p.bottom - player_rect.top)
            
            if dx < dy:
                # Collision is horizontal
                if player_rect.centerx < p.centerx:
                    player_pos[0] -= dx
                    collision = Collision.RIGHT
                else:
                    player_pos[0] += dx
                    collision = Collision.LEFT
                player_accel[0] = 0
            else:
                # Collision is vertical
                if player_rect.centery < p.centery:
                    player_pos[1] -= dy
                    collision = Collision.BOTTOM
                else:
                    player_pos[1] += dy
                    collision = Collision.TOP
                player_accel[1] = 0
            break

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw player
    PG.draw.rect(screen, (0, 255, 0), (player_pos[0], player_pos[1], 50, 50))

    # Draw platforms
    for platform in platform_rects:
        PG.draw.rect(screen, (255, 255, 255), platform)

    PG.display.flip()


PG.quit()