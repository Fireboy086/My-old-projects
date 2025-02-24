import pygame as PG
from pygame.math import Vector2
import math
from settings import *
from road_tiles import Particle
import random

class Car:
    def __init__(self, start_pos=(400, 300), start_rotation=0):
        # Load and scale car image
        self.original_image = PG.image.load(CAR_IMAGE_PATH).convert_alpha()
        self.original_image = PG.transform.scale(self.original_image, (CAR_WIDTH, CAR_HEIGHT))
        self.image = self.original_image
        
        # Set initial position and rotation
        self.position = Vector2(start_pos)
        self.rotation = start_rotation
        
        self.rect = self.image.get_rect(center=self.position)
        
        # Movement variables
        self.velocity = Vector2(0, 0)
        self.speed = 0
        self.acceleration = 0
        self.rotation_diff = 0
        
        # Effects
        self.drift_particles = []
        self.engine_particles = []
        
        # Define wheel positions relative to car center
        self.wheel_offsets = [
            Vector2(-CAR_WIDTH/3, -CAR_HEIGHT/3),  # Front left
            Vector2(CAR_WIDTH/3, -CAR_HEIGHT/3),   # Front right
            Vector2(-CAR_WIDTH/3, CAR_HEIGHT/3),   # Rear left
            Vector2(CAR_WIDTH/3, CAR_HEIGHT/3)     # Rear right
        ]
        
    def handle_input(self):
        keys = PG.key.get_pressed()
        
        # Acceleration
        if keys[PG.K_UP]:
            self.acceleration = ACCELERATION_FORWARD
            if abs(self.rotation_diff) < 0.1:
                self.acceleration += STRAIGHT_LINE_BOOST
        elif keys[PG.K_DOWN]:
            self.acceleration = -ACCELERATION_BACKWARD
        else:
            self.acceleration = 0
            
        # Rotation
        if keys[PG.K_LEFT]:
            self.rotation_diff = min(self.rotation_diff + MAX_ROTATION_DIFF, MAX_ROTATION_DIFF)
        elif keys[PG.K_RIGHT]:
            self.rotation_diff = max(self.rotation_diff - MAX_ROTATION_DIFF, -MAX_ROTATION_DIFF)
        else:
            self.rotation_diff *= ROTATION_DECAY
            
    def update(self, world):
        # Store previous position
        previous_pos = Vector2(self.position)
        
        # Update movement
        self.handle_input()
        
        # Update speed
        self.speed += self.acceleration
        self.speed *= SPEED_DECAY
        self.speed = max(MIN_SPEED, min(MAX_SPEED, self.speed))
        if abs(self.speed) < MIN_SPEED_THRESHOLD:
            self.speed = 0
        
        self.rotation += self.rotation_diff * (self.speed / MAX_SPEED)
        
        # Calculate movement components
        angle_rad = math.radians(self.rotation)
        speed_x = math.cos(angle_rad) * self.speed
        speed_y = -math.sin(angle_rad) * self.speed
        
        # Check collisions and get push vector
        x_blocked, y_blocked, push_vector = self.check_wall_collision(world)
        
        # First apply push-out force to prevent clipping
        if push_vector.length() > 0:
            self.position += push_vector
            
            # Reduce speed when being pushed out
            self.speed *= 0.8
        
        # Then handle movement with blocked axes
        if not x_blocked and not y_blocked:
            # No collision, move normally
            self.position += Vector2(speed_x, speed_y)
        else:
            # If hitting a wall, prevent acceleration into the wall
            if self.acceleration > 0:
                wall_angle = math.atan2(-speed_y, speed_x)
                if abs(wall_angle) < math.pi/4:  # Hitting wall head-on
                    self.acceleration = 0
                    self.speed *= 0.8
            
            # Move only on non-blocked axes
            if not x_blocked:
                self.position.x += speed_x
            if not y_blocked:
                self.position.y += speed_y
            
            # If both axes are blocked, prevent any movement
            if x_blocked and y_blocked:
                self.position = previous_pos
                self.speed *= 0.8
        
        # Update rect and rotate image
        self.rect.center = self.position
        self.image = PG.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Generate particles
        self.update_particles()
        
    def update_particles(self):
        # Add drift particles when turning at speed
        if abs(self.speed) > MAX_SPEED * 0.5 and abs(self.rotation_diff) > MAX_ROTATION_DIFF * 0.5:
            self.add_drift_particle()
            
        # Update existing particles
        self.drift_particles = [p for p in self.drift_particles if p.update()]
        self.engine_particles = [p for p in self.engine_particles if p.update()]
        
    def draw(self, screen):
        # Draw particles
        for particle in self.drift_particles + self.engine_particles:
            particle.draw(screen)
            
        # Draw car
        screen.blit(self.image, self.rect)
        
        # Draw speed indicator (optional)
        if abs(self.speed) > MIN_SPEED_THRESHOLD:
            self.draw_speed_indicator(screen)
            
    def draw_speed_indicator(self, screen):
        speed_text = f"Speed: {abs(self.speed):.1f}"
        font = PG.font.Font(None, 24)
        text_surface = font.render(speed_text, True, FONT_COLOR)
        
        # Create semi-transparent background
        bg_surface = PG.Surface((text_surface.get_width() + 20, 30))
        bg_surface.fill(UI_BACKGROUND)
        bg_surface.set_alpha(UI_TRANSPARENCY)
        
        # Draw background and text
        screen.blit(bg_surface, (10, SCREEN_HEIGHT - 40))
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 35))

    def add_drift_particle(self):
        angle_rad = math.radians(self.rotation)
        
        # Only create particles from wheels
        for wheel_offset in self.wheel_offsets:
            rotated_offset = wheel_offset.rotate(-self.rotation)
            particle_pos = self.position + rotated_offset
            
            # Create drift particle with slight randomization
            color = (80, 80, 80)  # Grey smoke color
            size = random.uniform(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
            
            # Scale velocities based on SCALE_FACTOR
            base_velocity = Vector2(-math.cos(angle_rad), math.sin(angle_rad)) * random.uniform(0.5, 1.5) * SCALE_FACTOR
            spread = Vector2(random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)) * SCALE_FACTOR
            velocity = base_velocity + spread
            
            lifetime = random.randint(15, 25)
            
            self.drift_particles.append(Particle(particle_pos, color, size, velocity, lifetime))

    def check_wall_collision(self, world):
        """Check for collisions and push car out of walls"""
        corners = self.get_corners()
        x_blocked = False
        y_blocked = False
        push_vector = Vector2(0, 0)
        
        # Check each corner for collision
        for corner in corners:
            grid_x = int(corner.x // TILE_SIZE)
            grid_y = int(corner.y // TILE_SIZE)
            
            if 0 <= grid_x < len(world.map_tiles[0]) and 0 <= grid_y < len(world.map_tiles):
                if world.map_tiles[grid_y][grid_x] == TILE_TYPES['WALL']:
                    # Calculate wall tile center
                    tile_center = Vector2(
                        grid_x * TILE_SIZE + TILE_SIZE/2,
                        grid_y * TILE_SIZE + TILE_SIZE/2
                    )
                    
                    # Calculate push direction
                    to_corner = corner - tile_center
                    push_dir = to_corner.normalize()
                    
                    # Calculate overlap depth
                    overlap = TILE_SIZE/2 - to_corner.length()
                    if overlap > 0:
                        push_vector += push_dir * overlap
                    
                    # Determine blocked axes
                    dx = abs(corner.x - tile_center.x)
                    dy = abs(corner.y - tile_center.y)
                    
                    if dx > dy:
                        x_blocked = True
                    if dy > dx:
                        y_blocked = True
                    
                    # If very close to corner, block both
                    if abs(dx - dy) < 5:
                        x_blocked = True
                        y_blocked = True
        
        return x_blocked, y_blocked, push_vector

    def get_corners(self):
        # Get rotated corners of car hitbox
        corners = [
            Vector2(-CAR_WIDTH/2, -CAR_HEIGHT/2),
            Vector2(CAR_WIDTH/2, -CAR_HEIGHT/2),
            Vector2(-CAR_WIDTH/2, CAR_HEIGHT/2),
            Vector2(CAR_WIDTH/2, CAR_HEIGHT/2)
        ]
        return [self.position + corner.rotate(-self.rotation) for corner in corners]
