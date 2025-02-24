import pygame as PG
import sys
from settings import *
import ast
from road_tiles import TileManager
import math
from pygame.math import Vector2
from Levels.Level_Group import LevelGroup
from level_selector import LevelSelector

class LevelEditor:
    def __init__(self, level_group):
        PG.init()
        self.level_group = level_group
        self.current_level_name = None
        
        # Create a larger screen to accommodate the bottom buffer zone
        self.total_height = SCREEN_HEIGHT + int(40 * SCALE_FACTOR)
        self.screen = PG.display.set_mode((SCREEN_WIDTH, self.total_height))
        self.update_caption()
        
        # Initialize tile manager for random wall variants
        self.tile_manager = TileManager()
        
        # Load tile images
        self.tiles = {
            0: self.create_empty_tile(),
            1: self.tile_manager.get_tile(TILE_TYPES['WALL'], 0, 0)[0],
            2: PG.image.load("assets/tiles/road/road_up:down.png").convert_alpha(),
            3: PG.image.load("assets/tiles/road/road_down:right.png").convert_alpha(),
            4: PG.image.load("assets/tiles/road/road_down:left.png").convert_alpha(),
            5: PG.image.load("assets/tiles/road/road_up:right.png").convert_alpha(),
            6: PG.image.load("assets/tiles/road/road_up:left.png").convert_alpha(),
            7: PG.image.load("assets/tiles/road/road_left:right.png").convert_alpha()
        }
        
        # Scale all tiles
        for key in self.tiles:
            if self.tiles[key]:
                self.tiles[key] = PG.transform.scale(self.tiles[key], (TILE_SIZE, TILE_SIZE))
        
        self.current_tile = 0
        self.grid = None  # Will be set when loading level
        self.font = PG.font.Font(None, 24)
        self.show_help = False
        self.show_selector = False
        self.show_level_select = True  # Start with level selector
        
        # Selector panel settings
        self.selector_height = int(40 * SCALE_FACTOR)
        self.selector_y = self.total_height - self.selector_height
        self.tile_preview_size = self.selector_height - 0
        
        self.wall_variants = {}
        self.start_pos = None  # Will be set when loading level
        self.moving_start = False
        self.start_block_size = int(20 * SCALE_FACTOR)
        self.start_rotation = 0
        self.rotating_start = False
        self.rotation_start_angle = 0
        self.rotation_start_pos = None
        self.rotation_speed = 0.3
        
        # Create level selector
        self.level_selector = LevelSelector(self.screen, self.level_group)

    def update_caption(self):
        caption = "Level Editor"
        if self.current_level_name:
            caption += f" - {self.current_level_name}"
        PG.display.set_caption(caption)

    def load_level(self, level_name):
        level_data = self.level_group.get_level_data(level_name)
        if level_data:
            self.current_level_name = level_name
            self.grid = [row[:] for row in level_data['map_tiles']]
            self.start_pos = list(level_data['car_start_pos'])
            self.start_rotation = level_data['car_start_rotation']
            self.update_caption()
            self.wall_variants.clear()
            return True
        return False

    def save_level(self):
        if self.current_level_name:
            self.level_group.save_level(
                self.current_level_name,
                self.grid,
                tuple(self.start_pos),
                self.start_rotation
            )
            print(f"Level '{self.current_level_name}' saved successfully!")

    def create_new_level(self, name):
        if self.level_group.create_new_level(name):
            self.load_level(name)
            return True
        return False

    def run(self):
        running = True
        drawing = False
        
        while running:
            if self.show_level_select:
                self.level_selector.draw()
                
                for event in PG.event.get():
                    if event.type == PG.QUIT:
                        running = False
                    elif event.type == PG.MOUSEBUTTONDOWN:
                        level_name, action = self.level_selector.handle_click(event.pos)
                        
                        if action == "exit":
                            running = False
                        elif action == "select":
                            self.load_level(level_name)
                            self.show_level_select = False
                        elif action == "new":
                            name = input("Enter new level name: ")
                            if name:
                                if self.create_new_level(name):
                                    self.show_level_select = False
                                else:
                                    print(f"Level '{name}' already exists!")
            else:
                # Normal editor operation
                for event in PG.event.get():
                    if event.type == PG.QUIT:
                        running = False
                    
                    elif event.type == PG.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        mouse_pos = Vector2(event.pos)
                        center = Vector2(self.start_pos)
                        
                        # Check if clicking start position or rotation handle
                        start_rect = PG.Rect(
                            self.start_pos[0] - self.start_block_size,
                            self.start_pos[1] - self.start_block_size,
                            self.start_block_size * 2,
                            self.start_block_size * 2
                        )
                        
                        is_near_center = (center - mouse_pos).length() < self.start_block_size * 3
                        is_on_rotation_ring = abs((center - mouse_pos).length() - self.start_block_size * 2) < 5
                        
                        if event.button == 1:  # Left click
                            if is_near_center:
                                if is_on_rotation_ring:
                                    self.rotating_start = True
                                    self.rotation_start_angle = self.start_rotation
                                    self.rotation_start_pos = mouse_pos
                                elif start_rect.collidepoint(x, y):
                                    self.moving_start = True
                                else:
                                    drawing = True
                            else:
                                drawing = True
                        elif event.button == 3:  # Right click
                            if not (is_near_center and (is_on_rotation_ring or start_rect.collidepoint(x, y))):
                                drawing = True
                
                    elif event.type == PG.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.moving_start = False
                            self.rotating_start = False
                        if event.button in (1, 3):
                            drawing = False
                
                    elif event.type == PG.MOUSEMOTION:
                        if self.moving_start:
                            x, y = event.pos
                            keys = PG.key.get_pressed()
                            if keys[PG.K_LSHIFT] or keys[PG.K_RSHIFT]:
                                grid_x = (x // TILE_SIZE) * TILE_SIZE + TILE_SIZE//2
                                grid_y = (y // TILE_SIZE) * TILE_SIZE + TILE_SIZE//2
                                self.start_pos = [grid_x, grid_y]
                            else:
                                self.start_pos = [x, y]
                    
                        if self.rotating_start:
                            mouse_pos = Vector2(event.pos)
                            center = Vector2(self.start_pos)
                            
                            old_angle = math.atan2(self.rotation_start_pos.y - center.y, 
                                                 self.rotation_start_pos.x - center.x)
                            new_angle = math.atan2(mouse_pos.y - center.y, 
                                                 mouse_pos.x - center.x)
                            
                            delta_angle = math.degrees(new_angle - old_angle) * self.rotation_speed
                            
                            keys = PG.key.get_pressed()
                            if keys[PG.K_LSHIFT] or keys[PG.K_RSHIFT]:
                                self.start_rotation = round((self.rotation_start_angle + delta_angle) / 90) * 90
                            else:
                                self.start_rotation = self.rotation_start_angle + delta_angle
                
                    elif event.type == PG.KEYDOWN:
                        if event.key == PG.K_ESCAPE:
                            self.show_level_select = True
                        elif event.key == PG.K_s:
                            self.save_level()
                        elif event.key == PG.K_F1:
                            self.show_help = not self.show_help
                        elif event.unicode.isdigit():
                            num = int(event.unicode)
                            if num in self.tiles:
                                self.current_tile = num
                
                # Handle continuous drawing while mouse button is held
                if drawing and not (self.moving_start or self.rotating_start):
                    x, y = PG.mouse.get_pos()
                    if y < SCREEN_HEIGHT:  # Only place tiles in editor area
                        grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
                        if 0 <= grid_y < len(self.grid) and 0 <= grid_x < len(self.grid[0]):
                            if PG.mouse.get_pressed()[0]:  # Left click held
                                if self.current_tile == TILE_TYPES['WALL']:
                                    self.grid[grid_y][grid_x] = TILE_TYPES['WALL']
                                    self.place_wall(grid_x, grid_y)
                                else:
                                    self.grid[grid_y][grid_x] = self.current_tile
                            elif PG.mouse.get_pressed()[2]:  # Right click held
                                self.grid[grid_y][grid_x] = 0
                
                # Draw everything
                self.screen.fill((53, 136, 37))
                self.draw_grid()
                self.draw_current_tile_preview()
                self.draw_ui()
                self.draw_selector_panel()
                
                PG.display.flip()
        
        PG.quit()

    def create_empty_tile(self):
        """Create an empty tile surface with green background"""
        surface = PG.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(BACKGROUND_COLOR)  # Use the same green as the background
        return surface

    def draw_grid(self):
        """Draw the tile grid and start position"""
        # Draw tiles
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                tile_type = self.grid[y][x]
                if tile_type == TILE_TYPES['WALL']:
                    # Use existing wall variant or create new one
                    if (x, y) not in self.wall_variants:
                        self.wall_variants[(x, y)] = self.place_wall(x, y)
                    self.screen.blit(self.wall_variants[(x, y)], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    self.screen.blit(self.tiles[tile_type], (x * TILE_SIZE, y * TILE_SIZE))
        
        # Draw grid lines
        grid_surface = PG.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), PG.SRCALPHA)
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            PG.draw.line(grid_surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            PG.draw.line(grid_surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(grid_surface, (0, 0))
        
        # Draw start position with rotation
        if self.start_pos:
            start_surface = PG.Surface((self.start_block_size * 2, self.start_block_size * 2), PG.SRCALPHA)
            
            # Draw the main square
            PG.draw.rect(start_surface, (255, 255, 255, 128), (0, 0, self.start_block_size * 2, self.start_block_size * 2))
            
            # Draw direction indicator
            arrow_points = [
                (self.start_block_size, 0),  # Tip
                (self.start_block_size * 1.5, self.start_block_size),  # Right base
                (self.start_block_size * 0.5, self.start_block_size)   # Left base
            ]
            PG.draw.polygon(start_surface, (255, 255, 255, 180), arrow_points)
            
            # Rotate and position the start marker
            rotated_surface = PG.transform.rotate(start_surface, -self.start_rotation)
            pos = (self.start_pos[0] - rotated_surface.get_width()//2,
                   self.start_pos[1] - rotated_surface.get_height()//2)
            self.screen.blit(rotated_surface, pos)
            
            # Draw rotation handle when mouse is near
            mouse_pos = PG.mouse.get_pos()
            center = Vector2(self.start_pos)
            if (center - Vector2(mouse_pos)).length() < self.start_block_size * 3:
                radius = self.start_block_size * 2
                PG.draw.circle(self.screen, (255, 255, 255, 64), center, radius, 2)

    def draw_current_tile_preview(self):
        """Draw preview of current tile at mouse position"""
        mouse_pos = PG.mouse.get_pos()
        if mouse_pos[1] < SCREEN_HEIGHT:  # Only show when in editor area
            preview_size = TILE_SIZE
            preview = PG.transform.scale(self.tiles[self.current_tile], (preview_size, preview_size))
            preview.set_alpha(128)
            grid_x = (mouse_pos[0] // TILE_SIZE) * TILE_SIZE
            grid_y = (mouse_pos[1] // TILE_SIZE) * TILE_SIZE
            self.screen.blit(preview, (grid_x, grid_y))

    def draw_ui(self):
        """Draw UI elements"""
        # Draw top bar
        ui_height = 40
        ui_surface = PG.Surface((SCREEN_WIDTH, ui_height))
        ui_surface.fill((40, 40, 40))
        ui_surface.set_alpha(230)
        self.screen.blit(ui_surface, (0, 0))
        
        # Draw current tile indicator and other info
        current_tile_text = self.font.render(f'Selected: {self.current_tile}', True, (255, 255, 255))
        help_text = self.font.render('F1: Help | S: Save | ESC: Exit', True, (255, 255, 255))
        
        self.screen.blit(current_tile_text, (20, 10))
        self.screen.blit(help_text, (SCREEN_WIDTH - help_text.get_width() - 20, 10))
        
        if self.show_help:
            self.draw_help_panel()

    def draw_help_panel(self):
        """Draw help information panel"""
        help_text = [
            'Controls:',
            'Left Click: Place tile',
            'Right Click: Remove tile',
            'Number Keys 0-7: Select tile',
            'Mouse to bottom: Show tile selector',
            'Hold Shift: Snap start position to grid',
            'S: Save map',
            'ESC: Back to level select'
        ]
        
        # Create semi-transparent panel
        panel_width = 300
        panel_height = len(help_text) * 30 + 20
        panel_surface = PG.Surface((panel_width, panel_height))
        panel_surface.fill((40, 40, 40))
        panel_surface.set_alpha(230)
        
        # Position panel in center
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Draw help text
        for i, text in enumerate(help_text):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (panel_x + 20, panel_y + 20 + i * 30))

    def draw_selector_panel(self):
        """Draw the bottom tile selector panel"""
        mouse_pos = PG.mouse.get_pos()
        self.show_selector = mouse_pos[1] > self.total_height - 120
        
        if self.show_selector:
            # Draw selector background
            selector_surface = PG.Surface((SCREEN_WIDTH, self.selector_height))
            selector_surface.fill((60, 70, 80))
            selector_surface.set_alpha(230)
            self.screen.blit(selector_surface, (0, self.selector_y))
            
            # Draw tile options
            spacing = 10
            start_x = (SCREEN_WIDTH - (len(self.tiles) * (self.tile_preview_size + spacing))) // 2
            
            for i in range(len(self.tiles)):
                x = start_x + i * (self.tile_preview_size + spacing)
                y = self.selector_y + (self.selector_height - self.tile_preview_size) // 2
                
                # Draw tile preview
                preview_rect = PG.Rect(x, y, self.tile_preview_size, self.tile_preview_size)
                
                # Check if mouse is over this tile
                if preview_rect.collidepoint(mouse_pos):
                    PG.draw.rect(self.screen, (100, 100, 255), preview_rect, 3)
                
                # Highlight current selection
                if i == self.current_tile:
                    PG.draw.rect(self.screen, (255, 255, 255), preview_rect, 3)
                
                # Scale and draw tile preview
                scaled_tile = PG.transform.scale(self.tiles[i], (self.tile_preview_size - 4, self.tile_preview_size - 4))
                self.screen.blit(scaled_tile, (x + 2, y + 2))
                
                # Draw number key hint
                key_text = self.font.render(str(i), True, (255, 255, 255))
                self.screen.blit(key_text, (x + 5, y + 5))

    def place_wall(self, grid_x, grid_y):
        """Generate new random wall variant"""
        wall_tile = self.tile_manager.get_tile(TILE_TYPES['WALL'], grid_y, grid_x)[0]
        wall_tile = PG.transform.scale(wall_tile, (TILE_SIZE, TILE_SIZE))
        self.wall_variants[(grid_x, grid_y)] = wall_tile
        return wall_tile

if __name__ == "__main__":
    level_group = LevelGroup()
    editor = LevelEditor(level_group)
    editor.run()
