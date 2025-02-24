import pygame as PG
from Car_script import Car
from road_tiles import GameWorld
from settings import *
from math import *
from Levels.Level_Group import LevelGroup
from level_selector import LevelSelector

class Game:
    def __init__(self):
        PG.init()
        # Fixed size camera view
        self.screen = PG.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
        PG.display.set_caption("Racing Game")
        
        self.clock = PG.time.Clock()
        self.running = True
        
        # Level selection
        self.level_group = LevelGroup()
        self.level_selector = LevelSelector(self.screen, self.level_group)
        self.current_level = None
        self.show_level_select = True
        
        # Create game world surface
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.game_surface = PG.Surface((self.world_width, self.world_height))
        
        # Camera tracking
        self.camera_offset = [0, 0]
        
        # Game objects
        self.world = None
        self.car = None
        
        # UI elements
        self.font = PG.font.Font(FONT_PATH, FONT_SIZE)
        self.message = ""
        self.message_timer = 0
        
    def load_level(self, level_name):
        level_data = self.level_group.get_level_data(level_name)
        if level_data:
            self.current_level = level_name
            # Initialize game objects with level data
            self.world = GameWorld(level_data['map_tiles'])
            self.car = Car(level_data['car_start_pos'], level_data['car_start_rotation'])
            PG.display.set_caption(f"Racing Game - {level_name}")
            return True
        return False

    def handle_events(self):
        for event in PG.event.get():
            if event.type == PG.QUIT:
                self.running = False
                
            elif event.type == PG.VIDEORESIZE:
                self.handle_resize(event)
                
            elif event.type == PG.KEYDOWN:
                self.handle_keydown(event)
                
    # def handle_resize(self, event):
    #     new_w, new_h = event.w, event.h
        
    #     # Calculate the aspect ratio of the original map
    #     original_aspect = BASE_SCREEN_WIDTH / BASE_SCREEN_HEIGHT
        
    #     # Calculate new dimensions maintaining aspect ratio
    #     if new_w / new_h > original_aspect:
    #         # Window is too wide, use height as reference
    #         scale_factor = round((new_h / BASE_SCREEN_HEIGHT), 2) #rounded to hundreths
    #         scaled_w = int(BASE_SCREEN_WIDTH * scale_factor)
    #         scaled_h = new_h
    #         x_offset = (new_w - scaled_w) // 2
    #         y_offset = 0
    #     else:
    #         # Window is too tall, use width as reference
    #         scale_factor = round((new_w / BASE_SCREEN_WIDTH), 2) #rounded to hundreths
    #         scaled_w = new_w
    #         scaled_h = int(BASE_SCREEN_HEIGHT * scale_factor)
    #         x_offset = 0
    #         y_offset = (new_h - scaled_h) // 2
        
    #     # Update screen and create game surface
    #     self.screen = PG.display.set_mode((new_w, new_h), PG.RESIZABLE)
    #     self.game_surface = PG.Surface((scaled_w, scaled_h))
        
    #     # Store scaling info for drawing
    #     self.scale_factor = scale_factor
    #     self.screen_offset = (x_offset, y_offset)
        
    #     # Update all scaled values in settings
    #     tiles_need_update = update_scaled_values(scale_factor)
        
    #     # If tile size changed, reload all tiles
    #     if tiles_need_update:
    #         self.world.resize_tiles()
        
    def handle_keydown(self, event):
        if event.key == PG.K_SPACE:
            self.car.position.x = SCREEN_WIDTH / 2
            self.car.position.y = SCREEN_HEIGHT / 2
            self.car.speed = 0
            self.car.rotation = 0
            self.show_message("Car Reset")
        elif event.key == PG.K_w:
            global WRAPPING_ENABLED
            WRAPPING_ENABLED = not WRAPPING_ENABLED
            self.show_message("Wrapping " + ("Enabled" if WRAPPING_ENABLED else "Disabled"))
            
    def show_message(self, text, duration=60):
        self.message = text
        self.message_timer = duration
        
    def update(self):
        self.world.update()
        self.car.update(self.world)
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            
        # Handle wrapping
        if WRAPPING_ENABLED:
            self.handle_wrapping()
            
    def handle_wrapping(self):
        if self.car.position.x < 0:
            self.car.position.x = SCREEN_WIDTH
        elif self.car.position.x > SCREEN_WIDTH:
            self.car.position.x = 0
        if self.car.position.y < 0:
            self.car.position.y = SCREEN_HEIGHT
        elif self.car.position.y > SCREEN_HEIGHT:
            self.car.position.y = 0
            
    def draw(self):
        if self.show_level_select:
            self.level_selector.draw()
        else:
            # Draw world and objects to game surface
            self.game_surface.fill(BACKGROUND_COLOR)
            self.world.draw(self.game_surface)
            self.car.draw(self.game_surface)
            
            # Update camera position
            self.update_camera()
            
            # Draw visible portion to screen
            self.screen.fill((0, 0, 0))
            visible_area = PG.Rect(self.camera_offset[0], self.camera_offset[1], 
                                 CAMERA_WIDTH, CAMERA_HEIGHT)
            self.screen.blit(self.game_surface, (0, 0), visible_area)
            
            # Draw UI elements on top
            self.draw_ui()
            
            PG.display.flip()
        
    def draw_ui(self):
        # Draw message if active
        if self.message_timer > 0:
            alpha = min(255, self.message_timer * 4)
            self.draw_message(self.message, alpha)
            
        # Draw FPS counter
        fps_text = f"FPS: {int(self.clock.get_fps())}"
        self.draw_text(fps_text, (10, 10))
        
    def draw_message(self, text, alpha):
        text_surface = self.font.render(text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, 50))
        
        # Draw background
        bg_surface = PG.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
        bg_surface.fill(UI_BACKGROUND)
        bg_surface.set_alpha(min(UI_TRANSPARENCY, alpha))
        bg_rect = bg_surface.get_rect(center=text_rect.center)
        
        self.screen.blit(bg_surface, bg_rect)
        text_surface.set_alpha(alpha)
        self.screen.blit(text_surface, text_rect)
        
    def draw_text(self, text, pos):
        text_surface = self.font.render(text, True, FONT_COLOR)
        bg_surface = PG.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
        bg_surface.fill(UI_BACKGROUND)
        bg_surface.set_alpha(UI_TRANSPARENCY)
        
        self.screen.blit(bg_surface, (pos[0] - 10, pos[1] - 5))
        self.screen.blit(text_surface, pos)
        
    def update_camera(self):
        if self.car:
            # Center camera on car
            target_x = self.car.position.x - CAMERA_WIDTH // 2
            target_y = self.car.position.y - CAMERA_HEIGHT // 2
            
            # Keep camera within world bounds
            self.camera_offset[0] = max(0, min(target_x, self.world_width - CAMERA_WIDTH))
            self.camera_offset[1] = max(0, min(target_y, self.world_height - CAMERA_HEIGHT))
        
    def run(self):
        while self.running:
            if self.show_level_select:
                self.level_selector.draw()
                
                for event in PG.event.get():
                    if event.type == PG.QUIT:
                        self.running = False
                    elif event.type == PG.MOUSEBUTTONDOWN:
                        level_name, action = self.level_selector.handle_click(event.pos)
                        
                        if action == "exit":
                            self.running = False
                        elif action == "select":
                            if self.load_level(level_name):
                                self.show_level_select = False
            else:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        
        PG.quit()

if __name__ == "__main__":
    game = Game()
    game.run()