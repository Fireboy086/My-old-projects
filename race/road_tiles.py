import pygame as PG
from pygame.math import Vector2
import random
from settings import *

class TileManager:
    def __init__(self):
        self.tile_cache = {}
        self.tile_definitions = {
            "walls": {
                "images": ["wall_brick.png"] * 60 + 
                         ["wall_brick(cracked).png"] * 20 + 
                         ["wall_brick(vines).png"] * 18 + 
                         ["wall_brick(kys).png"] * 1 + 
                         ["wall_brick(le_bom).png"] * 1,
            },
            "road": {
                "images": {
                    "up:down": ["road_up:down.png"],
                    "down:right": ["road_down:right.png"],
                    "down:left": ["road_down:left.png"],
                    "up:right": ["road_up:right.png"],
                    "up:left": ["road_up:left.png"],
                    "left:right": ["road_left:right.png"],
                }
            }
        }
        
    def get_tile(self, tile_type, yt, xt):
        """Get a tile image and its coordinates."""
        # Don't calculate coords here anymore, just return the image
        
        # For walls, don't use cache to ensure random variants
        if tile_type == TILE_TYPES['WALL']:
            wall_variant = random.choice(self.tile_definitions['walls']['images'])
            image_path = f"{TILE_PATHS['WALL']}{wall_variant}"
            image = PG.image.load(image_path).convert_alpha()
            scaled_image = PG.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            return scaled_image, None
        
        # For other tiles, use cache
        cache_key = f"{tile_type}"
        if cache_key in self.tile_cache:
            return self.tile_cache[cache_key], None
            
        # Load and cache new non-wall tile
        image_path = self._get_tile_path(tile_type)
        if image_path:
            image = PG.image.load(image_path).convert_alpha()
            scaled_image = PG.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            self.tile_cache[cache_key] = scaled_image
            return scaled_image, None
        return None, None
        
    def _get_tile_path(self, tile_type):
        """Get the file path for a tile type."""
        if tile_type == TILE_TYPES['WALL']:
            return f"{TILE_PATHS['WALL']}{random.choice(self.tile_definitions['walls']['images'])}"
        elif tile_type == TILE_TYPES['ROAD_VERTICAL']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['up:down'][0]}"
        elif tile_type == TILE_TYPES['ROAD_DOWN_RIGHT']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['down:right'][0]}"
        elif tile_type == TILE_TYPES['ROAD_DOWN_LEFT']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['down:left'][0]}"
        elif tile_type == TILE_TYPES['ROAD_UP_RIGHT']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['up:right'][0]}"
        elif tile_type == TILE_TYPES['ROAD_UP_LEFT']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['up:left'][0]}"
        elif tile_type == TILE_TYPES['ROAD_HORIZONTAL']:
            return f"{TILE_PATHS['ROAD']}{self.tile_definitions['road']['images']['left:right'][0]}"
        return None
        
    def clear_cache(self):
        """Clear the tile cache to force reloading with new size"""
        self.tile_cache.clear()

class Particle:
    def __init__(self, pos, color, size, velocity, lifetime):
        self.pos = Vector2(pos)
        self.color = color
        self.size = size
        self.velocity = Vector2(velocity)
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.pos += self.velocity
        self.age += 1
        self.size *= 0.95
        return self.age < self.lifetime
        
    def draw(self, screen):
        alpha = 255 * (1 - self.age / self.lifetime)
        surf = PG.Surface((self.size * 2, self.size * 2), PG.SRCALPHA)
        PG.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(surf, (self.pos.x - self.size, self.pos.y - self.size))

class GameWorld:
    def __init__(self, map_tiles):
        self.tile_manager = TileManager()
        self.tiles = []
        self.particles = []
        self.map_tiles = map_tiles
        self.load_tiles()
        
    def load_tiles(self):
        """Load all tiles from the map configuration."""
        self.tiles.clear()
        for yt in range(len(self.map_tiles)):
            for xt in range(len(self.map_tiles[yt])):
                tile_type = self.map_tiles[yt][xt]
                if tile_type != TILE_TYPES['EMPTY']:
                    image, coords = self.tile_manager.get_tile(tile_type, yt, xt)
                    if image:
                        coords = (xt * TILE_SIZE, yt * TILE_SIZE)
                        self.tiles.append((image, coords))
                        
    def resize_tiles(self):
        """Reload tiles with new scale factor"""
        self.tile_manager.clear_cache()  # Clear the tile cache
        self.load_tiles()  # Reload all tiles with new size
        
    def add_ambient_particle(self, pos):
        """Add ambient particles for visual effect."""
        color = (255, 255, 255)  # White particles
        size = random.uniform(1, 3)
        velocity = (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
        lifetime = random.randint(30, 60)
        self.particles.append(Particle(pos, color, size, velocity, lifetime))
        
    def update(self):
        """Update world state."""
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Add new ambient particles
        if random.random() < 0.1:  # 10% chance each frame
            pos = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.add_ambient_particle(pos)
            
    def draw(self, screen):
        """Draw the world."""
        # Draw tiles
        for tile, coords in self.tiles:
            screen.blit(tile, coords)
            
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
