# settings.py

# Game Constants
SCALE_FACTOR = 2  # Reduced from 10 to 2
TILE_SIZE = 32 * SCALE_FACTOR  # Now 64x64 instead of 320x320
FPS = 60
BACKGROUND_COLOR = (53, 136, 37)
GRID_COLOR = (100, 100, 100, 50)

# Base Settings (unscaled)
MENU_WIDTH = 640*2
MENU_HEIGHT = 512*2
SCREEN_WIDTH = TILE_SIZE*20  # Default width for 20 tiles
SCREEN_HEIGHT = TILE_SIZE*16  # Default height for 16 tiles
BASE_CAR_WIDTH = 32  # Reduced base size
BASE_CAR_HEIGHT = 16

# Car Settings
CAR_IMAGE_PATH = "assets/car/car.png"
CAR_WIDTH = BASE_CAR_WIDTH * SCALE_FACTOR  # Now 64 pixels wide
CAR_HEIGHT = BASE_CAR_HEIGHT * SCALE_FACTOR  # Now 32 pixels high

# Asset Paths
TILE_PATHS = {
    'WALL': 'assets/tiles/wall/',
    'ROAD': 'assets/tiles/road/'
}

# UI Settings
FONT_COLOR = (255, 255, 255)
UI_BACKGROUND = (0, 0, 0)
UI_TRANSPARENCY = 128
UI_PADDING = 10
FONT_PATH = None

# Game Features
WRAPPING_ENABLED = False

# Tile Definitions
TILE_TYPES = {
    'EMPTY': 0,
    'WALL': 1,
    'ROAD_VERTICAL': 2,
    'ROAD_DOWN_RIGHT': 3,
    'ROAD_DOWN_LEFT': 4,
    'ROAD_UP_RIGHT': 5,
    'ROAD_UP_LEFT': 6,
    'ROAD_HORIZONTAL': 7
}

# Camera settings
CAMERA_WIDTH = 1280  # Fixed camera viewport width
CAMERA_HEIGHT = 720  # Fixed camera viewport height

# World dimensions
WORLD_WIDTH = TILE_SIZE * 20  # 1280 pixels (20 tiles * 64)
WORLD_HEIGHT = TILE_SIZE * 16  # 1024 pixels (16 tiles * 64)


def update_scaled_values(new_scale_factor):
    """
    Updates all size-related values based on the new scale factor.
    This function should be called whenever the window is resized.
    """
    global SCALE_FACTOR, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT
    global CAR_WIDTH, CAR_HEIGHT, PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE
    global MAX_SPEED, MIN_SPEED, ACCELERATION_FORWARD, ACCELERATION_BACKWARD
    global FONT_SIZE, MIN_SPEED_THRESHOLD, TURNING_SPEED_REDUCTION
    global MAX_ROTATION_DIFF, ROTATION_DECAY, STRAIGHT_LINE_BOOST
    global SPEED_DECAY
    
    # Store old tile size to check if it changed
    old_tile_size = TILE_SIZE if 'TILE_SIZE' in globals() else None
    
    # Update basic dimensions
    # SCREEN_WIDTH = BASE_SCREEN_WIDTH
    # SCREEN_HEIGHT = BASE_SCREEN_HEIGHT
    # TILE_SIZE = BASE_TILE_SIZE
    
    #update world size
    WORLD_WIDTH = TILE_SIZE*20  # Default width for 20 tiles
    WORLD_HEIGHT = TILE_SIZE*16  # Default height for 16 tiles
    
    # Update car dimensions
    CAR_WIDTH = BASE_CAR_WIDTH*2
    CAR_HEIGHT = BASE_CAR_HEIGHT*2
    
    # Update particle sizes (tied to car scale)
    PARTICLE_MIN_SIZE = CAR_WIDTH / 24  # Makes particles 1/24th of car width
    PARTICLE_MAX_SIZE = CAR_WIDTH / 12  # Makes particles 1/12th of car width
    
    # Update physics values
    MAX_SPEED = 8
    MIN_SPEED = -4
    ACCELERATION_FORWARD = 0.4
    ACCELERATION_BACKWARD = 0.2
    MIN_SPEED_THRESHOLD = 0.1
    TURNING_SPEED_REDUCTION = 0.2
    MAX_ROTATION_DIFF = 2.5  # def = 2.5
    ROTATION_DECAY = 0.1
    STRAIGHT_LINE_BOOST = 0.1
    SPEED_DECAY = 0.98  # This value doesn't need scaling, but needs to be global
    
    # Update UI values
    FONT_SIZE = 36
    
    # Return True if tile size changed
    tile_size_changed = old_tile_size != TILE_SIZE
    
    return tile_size_changed  # Return True if tile size changed

# Initialize scaled values with default scale factor
update_scaled_values(SCALE_FACTOR)

if __name__ == "__main__":
    import pygame as PG
    from main import main
