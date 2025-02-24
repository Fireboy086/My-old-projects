import pygame as PG
from settings import *

class LevelSelector:
    def __init__(self, screen, level_group):
        self.screen = screen
        self.level_group = level_group
        self.font = PG.font.Font(None, 36)
        self.small_font = PG.font.Font(None, 24)
        
    def draw(self):
        self.screen.fill((40, 40, 40))
        
        # Draw title
        title = self.font.render("Select Level to Edit", True, (255, 255, 255))
        self.screen.blit(title, (MENU_WIDTH/2 - title.get_width()/2, 50))
        
        # Draw level buttons
        y = 150
        for level_name in self.level_group.get_level_names():
            rect = PG.Rect(MENU_WIDTH/4, y, MENU_WIDTH/2, 40)
            PG.draw.rect(self.screen, (60, 60, 60), rect)
            
            text = self.font.render(level_name, True, (255, 255, 255))
            self.screen.blit(text, (rect.centerx - text.get_width()/2, rect.centery - text.get_height()/2))
            
            y += 60
        
        # Draw new level button
        new_rect = PG.Rect(MENU_WIDTH/4, y, MENU_WIDTH/2, 40)
        PG.draw.rect(self.screen, (60, 100, 60), new_rect)
        new_text = self.font.render("+ New Level", True, (255, 255, 255))
        self.screen.blit(new_text, (new_rect.centerx - new_text.get_width()/2, new_rect.centery - new_text.get_height()/2))
        
        # Draw exit button
        exit_rect = PG.Rect(MENU_WIDTH - 100, 20, 80, 30)
        PG.draw.rect(self.screen, (100, 60, 60), exit_rect)
        exit_text = self.small_font.render("Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()/2, exit_rect.centery - exit_text.get_height()/2))
        
        PG.display.flip()
        
    def handle_click(self, pos):
        # Check exit button
        exit_rect = PG.Rect(MENU_WIDTH - 100, 20, 80, 30)
        if exit_rect.collidepoint(pos):
            return None, "exit"
        
        # Check level buttons
        y = 150
        for level_name in self.level_group.get_level_names():
            rect = PG.Rect(MENU_WIDTH/4, y, MENU_WIDTH/2, 40)
            if rect.collidepoint(pos):
                return level_name, "select"
            y += 60
        
        # Check new level button
        new_rect = PG.Rect(MENU_WIDTH/4, y, MENU_WIDTH/2, 40)
        if new_rect.collidepoint(pos):
            return None, "new"
        
        return None, None 