import json
import sys
import pygame
import math
import colorsys

pygame.init()

WindowWidth = 400
WindowHeight = 400
FPS = 60
Title = "Not a Game"
FontSize = 36
Font = pygame.font.Font(None, FontSize)

with open("settings.json", "w") as f:
            difficulties = ["easy", "medium", "hard"]
            current_difficulty = "easy"
            data = {"current": current_difficulty, "levels": difficulties}
            json.dump(data, f)

class Button:
    def __init__(self, x, y, width, height, color, text,id=None,customfont=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.id = id
        if customfont:
            self.font = customfont
        else:
            self.font = Font
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

class Game:
    def __init__(self, mcfont):
        self.screen = pygame.display.set_mode((WindowWidth, WindowHeight))
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.titlecolor = (255, 0, 0)
        self.titlerot =0
        self.titlescale = 1
        self.timepassed = 0
        self.mcfont = mcfont
        # Load from JSON file
        f = open("settings.json", "r")
        data = json.load(f)
        f.close()
        
        self.current_difficulty = data["current"]
        self.difficulties = data["levels"]
        
        # Make buttons
        self.buttons.append(Button(25, 300, 100, 50, (0, 255, 0), "Play", "st"))
        self.buttons.append(Button(150, 300, 100, 50, (0, 128, 128), f"Difficulty: \n {self.current_difficulty}", "diff", customfont=pygame.font.Font(None, 28)))
        self.buttons.append(Button(275, 300, 100, 50, (255, 255, 255), "Exit", "x"))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(pygame.mouse.get_pos()):
                            if button.id == "st":
                                print(f"Game started! Difficulty selected: {self.current_difficulty}")
                            elif button.id == "diff":
                                # Change difficulty
                                diffIndex = self.difficulties.index(self.current_difficulty)
                                self.current_difficulty = self.difficulties[(diffIndex + 1) % len(self.difficulties)]
                                button.text = f"Difficulty: \n {self.current_difficulty}"
                                # Save to file
                                f = open("settings.json", "w")
                                data = {"current": self.current_difficulty, "levels": self.difficulties}
                                json.dump(data, f)
                                f.close()
                                
                                print(f"Difficulty changed to: {self.current_difficulty}")
                            elif button.id == "x":
                                pygame.quit()
                                sys.exit()
            self.update_title()
            self.screen.fill((0, 0, 0))
            if self.mcfont:
                title_text = pygame.font.SysFont("Minecraft", 65).render("Not a Game", True, self.titlecolor)
            else:
                title_text = pygame.font.Font(None, 100).render("Not a Game", True, self.titlecolor)
            # Use rotozoom for smooth rotation. I also did not know how useful it was
            rotated_title = pygame.transform.rotozoom(title_text, self.titlerot, self.titlescale)
            title_rect = rotated_title.get_rect(center=(WindowWidth / 2, 150))
            self.screen.blit(rotated_title, title_rect)
            self.timepassed+=1
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(FPS)
            

    def update_title(self):
            # Hue shift titleColor variable
            h, s, v = colorsys.rgb_to_hsv(self.titlecolor[0]/255.0, self.titlecolor[1]/255.0, self.titlecolor[2]/255.0)
            h = (h + 0.01) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            self.titlecolor = (int(r * 255), int(g * 255), int(b * 255))
            
            # Make the title swing back and forth
            self.titlerot = 10 * math.sin(self.timepassed * 0.05)
            # Scale the title
            self.titlescale = 1 + 0.1 * math.cos(self.timepassed * 0.05)

if __name__ == "__main__":
    # This line checks if the argument '--mcfont' is passed when running the script
    mcfont = "--mcfont" in sys.argv
    print("Minecraft font selected" if mcfont else "Default font selected")
    game = Game(mcfont=mcfont)
    game.run()
