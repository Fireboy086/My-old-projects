import pygame
import sys
import colorsys

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600  # Window size
INITIAL_CELL_SIZE = 20    # Initial size of each cell
FPS_RUNNING = 10          # Frames per second when running
FPS_PAUSED = 240          # Frames per second when paused

# Define colors
BG_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)

# Define grid size (independent of window size)
GRID_WIDTH = 1000   # Total number of cells horizontally
GRID_HEIGHT = 1000  # Total number of cells vertically

class GameOfLife:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        self.running = False

        # Initialize color cycling
        self.hue = 0.0         # Hue value between 0.0 and 1.0
        self.frame_counter = 0 # Counts frames to change color every few frames
        self.current_color = self.hsv_to_rgb(self.hue)

        # Initialize view parameters for scrolling and scaling
        self.offset_x = 0
        self.offset_y = 0
        self.cell_size = INITIAL_CELL_SIZE
        self.min_cell_size = 5
        self.max_cell_size = 40

        # Font for indicator
        self.font = pygame.font.SysFont(None, 24)

    def hsv_to_rgb(self, hue):
        """Convert HSV color to RGB tuple scaled to 0-255."""
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)  # Full saturation and value
        return tuple(int(c * 255) for c in rgb)

    def update_color(self, running):
        """Update the color of live cells every few frames based on FPS."""
        if running:
            frame_threshold = FPS_RUNNING // 5
        else:
            frame_threshold = FPS_PAUSED // 5

        self.frame_counter += 1
        if self.frame_counter >= frame_threshold:
            self.frame_counter = 0
            self.hue += 0.01  # Increment hue
            if self.hue > 1.0:
                self.hue -= 1.0  # Wrap around
            self.current_color = self.hsv_to_rgb(self.hue)

    def draw_grid(self):
        """Draw the grid lines on the screen."""
        # Vertical lines
        for x in range(0, WIDTH, self.cell_size):
            adjusted_x = x - (self.offset_x % self.cell_size)
            pygame.draw.line(self.screen, GRID_COLOR, (adjusted_x, 0), (adjusted_x, HEIGHT))
        # Horizontal lines
        for y in range(0, HEIGHT, self.cell_size):
            adjusted_y = y - (self.offset_y % self.cell_size)
            pygame.draw.line(self.screen, GRID_COLOR, (0, adjusted_y), (WIDTH, adjusted_y))

    def draw_cells(self):
        """Draw the live cells with the current dynamic color."""
        # Determine the range of cells to draw based on the current view
        start_x = self.offset_x // self.cell_size
        start_y = self.offset_y // self.cell_size
        end_x = (self.offset_x + WIDTH) // self.cell_size + 1
        end_y = (self.offset_y + HEIGHT) // self.cell_size + 1

        # Clamp the values to grid boundaries
        start_x = max(start_x, 0)
        start_y = max(start_y, 0)
        end_x = min(end_x, GRID_WIDTH)
        end_y = min(end_y, GRID_HEIGHT)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if self.grid[x][y] == 1:
                    rect = pygame.Rect(
                        (x * self.cell_size - self.offset_x),
                        (y * self.cell_size - self.offset_y),
                        self.cell_size,
                        self.cell_size
                    )
                    pygame.draw.rect(self.screen, self.current_color, rect)

    def update_grid(self):
        """Update the grid based on Conway's Game of Life rules."""
        new_grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                neighbors = self.count_neighbors(x, y)
                if self.grid[x][y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[x][y] = 0
                    else:
                        new_grid[x][y] = 1
                else:
                    if neighbors == 3:
                        new_grid[x][y] = 1
        self.grid = new_grid

    def count_neighbors(self, x, y):
        """Count the number of alive neighbors around a cell."""
        directions = [(-1, -1), (0, -1), (1, -1),
                      (-1,  0),         (1,  0),
                      (-1,  1), (0,  1), (1,  1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                count += self.grid[nx][ny]
        return count

    def handle_events(self):
        """Handle user input and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
                if event.key == pygame.K_c:
                    self.grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.zoom(1)
                if event.key == pygame.K_MINUS:
                    self.zoom(-1)

        # Handle continuous key presses for movement
        keys = pygame.key.get_pressed()
        move_speed = self.cell_size  # Move by one cell size per frame
        if keys[pygame.K_UP]:
            self.offset_y -= move_speed
        if keys[pygame.K_DOWN]:
            self.offset_y += move_speed
        if keys[pygame.K_LEFT]:
            self.offset_x -= move_speed
        if keys[pygame.K_RIGHT]:
            self.offset_x += move_speed

        # Clamp the offsets to prevent scrolling beyond the grid
        self.offset_x = max(0, min(self.offset_x, GRID_WIDTH * self.cell_size - WIDTH))
        self.offset_y = max(0, min(self.offset_y, GRID_HEIGHT * self.cell_size - HEIGHT))

        # Handle continuous mouse actions
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left click to add cell
            pos = pygame.mouse.get_pos()
            x, y = (pos[0] + self.offset_x) // self.cell_size, (pos[1] + self.offset_y) // self.cell_size
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                self.grid[x][y] = 1

        if mouse_buttons[2]:  # Right click to remove cell
            pos = pygame.mouse.get_pos()
            x, y = (pos[0] + self.offset_x) // self.cell_size, (pos[1] + self.offset_y) // self.cell_size
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                self.grid[x][y] = 0

    def zoom(self, direction):
        """Zoom in or out based on direction."""
        if direction > 0 and self.cell_size < self.max_cell_size:
            self.cell_size += 1
            self.adjust_offsets_after_zoom(increased=True)
        elif direction < 0 and self.cell_size > self.min_cell_size:
            self.cell_size -= 1
            self.adjust_offsets_after_zoom(increased=False)

    def adjust_offsets_after_zoom(self, increased):
        """
        Adjust offsets to keep the view centered after zooming.
        """
        # Get the center of the screen in world coordinates before zoom
        center_x = self.offset_x + WIDTH // 2
        center_y = self.offset_y + HEIGHT // 2

        # Calculate the new offsets to keep the center consistent
        self.offset_x = center_x - WIDTH // 2
        self.offset_y = center_y - HEIGHT // 2

        # Clamp the offsets to prevent scrolling beyond the grid
        self.offset_x = max(0, min(self.offset_x, GRID_WIDTH * self.cell_size - WIDTH))
        self.offset_y = max(0, min(self.offset_y, GRID_HEIGHT * self.cell_size - HEIGHT))

    def draw_indicator(self):
        """Draw the running status indicator on the screen."""
        status_text = "Running" if self.running else "Paused"
        color = (0, 255, 0) if self.running else (255, 0, 0)
        text_surface = self.font.render(f"Status: {status_text}", True, color)
        self.screen.blit(text_surface, (10, 10))

    def run(self):
        """Main loop to run the Game of Life simulation."""
        while True:
            self.handle_events()

            if self.running:
                self.update_grid()

            # Update color regardless of simulation state
            self.update_color(self.running)

            self.screen.fill(BG_COLOR)
            self.draw_cells()
            self.draw_grid()
            self.draw_indicator()  # Add indicator to the screen
            pygame.display.flip()

            # Set FPS based on simulation state
            current_fps = FPS_RUNNING if self.running else FPS_PAUSED
            self.clock.tick(current_fps)

if __name__ == "__main__":
    GameOfLife().run()