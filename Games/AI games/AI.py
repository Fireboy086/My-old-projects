import pygame
import sys
import pickle
import numpy as np
import random
import os
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRAVITY = 0.5
JUMP_STRENGTH = 10
MOVE_SPEED = 5
AI_POPULATION = 50
AI_MUTATION_RATE = 0.03  # Base mutation rate
AI_MUTATION_STRENGTH = 0.3  # Base mutation strength
AI_EXPLORER_RATIO = 0.3  # Percentage of population that will be explorers
AI_EXPLORER_MUTATION_RATE = 0.15  # Higher mutation rate for explorers
AI_WEIGHT_STABILITY_THRESHOLD = 0.25  # Threshold to consider a weight stable
FULLSCREEN = False  # Initial fullscreen state

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
CHECKPOINT_COLOR = (255, 140, 0)  # Bright orange for checkpoints

# Initialize screen - modified to support fullscreen toggling
def initialize_screen():
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer with AI")

# Call this initially
initialize_screen()

clock = pygame.time.Clock()

# Create directories for saving levels and AI models
if not os.path.exists("levels"):
    os.makedirs("levels")
if not os.path.exists("ai_models"):
    os.makedirs("ai_models")

class Block:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

class Player:
    def __init__(self, x, y, width=GRID_SIZE, height=GRID_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.dead = False
        self.reached_goal = False
        self.start_pos = (x, y)
        self.steps = 0
        self.time_alive = 0
        
    def reset(self):
        self.rect.x, self.rect.y = self.start_pos
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.dead = False
        self.reached_goal = False
        self.steps = 0
        self.time_alive = 0
        self.collected_checkpoints = []  # Clear collected checkpoints on reset
    
    def update(self, blocks, goal):
        if self.dead or self.reached_goal:
            return
            
        self.time_alive += 1
        
        # Apply gravity
        self.y_vel += GRAVITY
        
        # Move horizontally
        self.rect.x += self.x_vel
        
        # Check horizontal collisions
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.x_vel > 0:  # Moving right
                    self.rect.right = block.rect.left
                elif self.x_vel < 0:  # Moving left
                    self.rect.left = block.rect.right
                self.x_vel = 0
        
        # Check boundary collisions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        # Move vertically
        self.rect.y += self.y_vel
        self.on_ground = False
        
        # Check vertical collisions
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.y_vel > 0:  # Falling
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
                elif self.y_vel < 0:  # Jumping
                    self.rect.top = block.rect.bottom
                self.y_vel = 0
        
        # Check if fell off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.dead = True
            
        # Check goal
        if self.rect.colliderect(goal.rect):
            self.reached_goal = True
    
    def jump(self):
        if self.on_ground:
            self.y_vel = -JUMP_STRENGTH
            
    def move_left(self):
        self.x_vel = -MOVE_SPEED
        self.steps += 1
        
    def move_right(self):
        self.x_vel = MOVE_SPEED
        self.steps += 1
        
    def stop(self):
        self.x_vel = 0
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

class Goal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = GREEN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

class Checkpoint:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.color = CHECKPOINT_COLOR
        self.is_active = True  # Tracks if the checkpoint has been collected
        
    def draw(self):
        # Draw a diamond shape for checkpoints
        if self.is_active:
            points = [
                (self.rect.centerx, self.rect.y),
                (self.rect.x + self.rect.width, self.rect.centery),
                (self.rect.centerx, self.rect.y + self.rect.height),
                (self.rect.x, self.rect.centery)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, BLACK, points, 2)  # Border
        else:
            # Draw a faded version when collected
            points = [
                (self.rect.centerx, self.rect.y),
                (self.rect.x + self.rect.width, self.rect.centery),
                (self.rect.centerx, self.rect.y + self.rect.height),
                (self.rect.x, self.rect.centery)
            ]
            faded_color = (min(self.color[0] + 50, 255), min(self.color[1] + 50, 255), min(self.color[2] + 50, 255))
            pygame.draw.polygon(screen, faded_color, points, 1)

    def reset(self):
        self.is_active = True

class AIPlayer(Player):
    def __init__(self, x, y, width=GRID_SIZE, height=GRID_SIZE, generation=0):
        super().__init__(x, y, width, height)
        self.color = RED
        self.nn_weights = self.initialize_weights()
        self.fitness = 0
        self.is_explorer = False
        self.generation = generation
        self.collected_checkpoints = []
        
        # Better tracking variables
        self.position_history = []
        self.last_goal_distance = float('inf')
        self.stuck_timer = 0
        self.movement_pattern = []  # Track last few movement actions
        self.jump_timer = 0  # Prevent rapid jump spamming
        self.last_action_time = {}  # Track when actions were last performed
        
        # Store some metrics for evaluation
        self.total_distance_traveled = 0
        self.prev_position = (x, y)
        self.vertical_progress = 0  # Track upward movement progress
        self.highest_y = y
    
    def reset(self):
        # Reset to starting position
        self.rect.x, self.rect.y = self.start_pos
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.dead = False
        self.reached_goal = False
        self.steps = 0
        self.time_alive = 0
        self.collected_checkpoints = []
        
        # Reset tracking variables
        self.position_history = []
        self.last_goal_distance = float('inf')
        self.stuck_timer = 0
        self.movement_pattern = []
        self.jump_timer = 0
        self.last_action_time = {}
        self.total_distance_traveled = 0
        self.prev_position = self.start_pos
        self.vertical_progress = 0
        self.highest_y = self.start_pos[1]
    
    def initialize_weights(self):
        # Count the inputs correctly
        # 10 basic inputs + raycast inputs (8 directions + 1 target ray)
        input_size = 19  # Updated from 12 to match actual input count
        hidden_size = 10
        output_size = 3  # Jump, move left, move right
        
        w1 = np.random.randn(input_size, hidden_size) * 0.1
        w2 = np.random.randn(hidden_size, output_size) * 0.1
        
        return [w1, w2]
    
    def ai_action(self, blocks, goal, checkpoints=None):
        if self.dead or self.reached_goal:
            return
        
        # Update metrics
        current_pos = (self.rect.centerx, self.rect.centery)
        
        # Track position history (every 5 frames)
        if self.time_alive % 5 == 0:
            self.position_history.append(current_pos)
            if len(self.position_history) > 20:  # Store more history
                self.position_history.pop(0)
        
        # Calculate distance moved since last frame
        dist_moved = ((current_pos[0] - self.prev_position[0])**2 + 
                      (current_pos[1] - self.prev_position[1])**2)**0.5
        self.total_distance_traveled += dist_moved
        self.prev_position = current_pos
        
        # Track vertical progress (lower y is higher up the screen)
        if current_pos[1] < self.highest_y:
            self.highest_y = current_pos[1]
            self.vertical_progress = self.start_pos[1] - self.highest_y
        
        # Check if AI is stuck
        is_stuck = self.detect_stuckness()
        
        # Update goal distance
        current_goal_dist = ((self.rect.centerx - goal.rect.centerx)**2 + 
                           (self.rect.centery - goal.rect.centery)**2)**0.5
        
        # Update stuck timer based on progress
        if current_goal_dist >= self.last_goal_distance and dist_moved < 2:
            self.stuck_timer += 1
        else:
            self.stuck_timer = max(0, self.stuck_timer - 1)
        
        self.last_goal_distance = current_goal_dist
        
        # Get target (checkpoint or goal)
        target_x, target_y = self.get_target(goal, checkpoints)
        
        # Cast rays to detect nearby blocks
        ray_distances = self.cast_rays(blocks, target_x, target_y)
        
        # Prepare inputs for neural network
        inputs = np.array([
            self.rect.centerx / SCREEN_WIDTH,  # X position
            self.rect.centery / SCREEN_HEIGHT,  # Y position
            self.x_vel / 20,  # Normalized X velocity
            self.y_vel / 20,  # Normalized Y velocity
            self.on_ground,  # Ground contact
            goal.rect.centerx / SCREEN_WIDTH,  # Goal X
            goal.rect.centery / SCREEN_HEIGHT,  # Goal Y
            target_x / SCREEN_WIDTH,  # Target X
            target_y / SCREEN_HEIGHT,  # Target Y
            self.vertical_progress / SCREEN_HEIGHT,  # Vertical progress
            *[d/500 for d in ray_distances]  # Ray distances
        ])
        
        # Feed forward through neural network
        w1, w2 = self.nn_weights
        hidden = np.tanh(np.dot(inputs, w1))
        output = np.tanh(np.dot(hidden, w2))
        
        # Apply random exploratory behavior occasionally or when stuck
        if (random.random() < 0.01 or 
            (is_stuck and random.random() < 0.2) or
            (self.is_explorer and random.random() < 0.1)):
            
            self.apply_exploratory_actions()
            return
        
        # Otherwise, use neural network outputs
        # Decrease jump spam by enforcing cooldown
        jump_cooldown = 10  # frames
        can_jump = self.jump_timer <= 0
        
        if output[0] > 0.5 and self.on_ground and can_jump:
            self.jump()
            self.jump_timer = jump_cooldown
            self.movement_pattern.append('jump')
        else:
            self.jump_timer = max(0, self.jump_timer - 1)
        
        # Apply horizontal movement with some constraints to prevent oscillation
        if len(self.movement_pattern) > 10:
            self.movement_pattern.pop(0)
        
        # Get horizontal direction to target
        target_dir = 1 if target_x > self.rect.centerx else -1 if target_x < self.rect.centerx else 0
        
        # Neural network output for movement
        if output[1] > 0.3:  # Left threshold
            self.move_left()
            self.movement_pattern.append('left')
        elif output[2] > 0.3:  # Right threshold
            self.move_right()
            self.movement_pattern.append('right')
        else:
            # If network is indecisive, move toward target
            if target_dir > 0:
                self.move_right()
                self.movement_pattern.append('right')
            elif target_dir < 0:
                self.move_left()
                self.movement_pattern.append('left')
            else:
                self.stop()
                self.movement_pattern.append('stop')
        
        # Update step counter
        self.steps += 1
    
    def detect_stuckness(self):
        """Improved stuck detection that considers multiple factors"""
        if len(self.position_history) < 10:
            return False
        
        # Calculate area covered
        min_x = min(pos[0] for pos in self.position_history)
        max_x = max(pos[0] for pos in self.position_history)
        min_y = min(pos[1] for pos in self.position_history)
        max_y = max(pos[1] for pos in self.position_history)
        
        area_width = max_x - min_x
        area_height = max_y - min_y
        
        # Check for repetitive movement pattern
        pattern_stuck = False
        if len(self.movement_pattern) >= 8:
            # Check if the last 8 actions are just alternating left-right or jump-jump-jump
            left_right_pattern = all(a in ['left', 'right'] for a in self.movement_pattern[-8:])
            jump_spam = self.movement_pattern[-8:].count('jump') >= 6
            pattern_stuck = left_right_pattern or jump_spam
        
        # Different stuck criteria
        area_stuck = area_width < GRID_SIZE * 3 and area_height < GRID_SIZE * 3
        side_to_side = area_width < GRID_SIZE * 6 and area_height < GRID_SIZE * 2
        
        return area_stuck or side_to_side or pattern_stuck or self.stuck_timer > 60
    
    def apply_exploratory_actions(self):
        """Apply intelligent exploratory actions to escape stuck situations"""
        # Decide on an action based on context and stuck pattern
        
        if self.on_ground and random.random() < 0.4:
            # Jump with good probability when on ground
            self.jump()
            self.movement_pattern.append('jump')
        
        # For horizontal movement, favor changing direction to break patterns
        if len(self.movement_pattern) >= 3:
            last_moves = self.movement_pattern[-3:]
            if all(move == 'left' for move in last_moves):
                self.move_right()  # Change direction if was moving left
                self.movement_pattern.append('right')
            elif all(move == 'right' for move in last_moves):
                self.move_left()  # Change direction if was moving right
                self.movement_pattern.append('left')
            else:
                # Otherwise random horizontal movement
                if random.random() < 0.5:
                    self.move_left()
                    self.movement_pattern.append('left')
                else:
                    self.move_right()
                    self.movement_pattern.append('right')
        else:
            # No pattern detected yet, just move randomly
            if random.random() < 0.5:
                self.move_left()
                self.movement_pattern.append('left')
            else:
                self.move_right()
                self.movement_pattern.append('right')
    
    def get_target(self, goal, checkpoints=None):
        """Determine the target (checkpoint or goal)"""
        if not checkpoints:
            return goal.rect.centerx, goal.rect.centery
        
        # Find uncollected checkpoints
        uncollected = [cp for cp in checkpoints if cp not in self.collected_checkpoints]
        
        if not uncollected:
            return goal.rect.centerx, goal.rect.centery
        
        # Find best checkpoint to target
        best_score = float('-inf')
        best_target = None
        
        for cp in uncollected:
            # Distance to checkpoint
            dist = ((self.rect.centerx - cp.rect.centerx)**2 + 
                   (self.rect.centery - cp.rect.centery)**2)**0.5
            
            # Vertical component (higher priority to checkpoints above)
            vert_factor = 2.0 if cp.rect.centery < self.rect.centery else 1.0
            
            # Goal alignment
            cp_to_goal = ((cp.rect.centerx - goal.rect.centerx)**2 + 
                         (cp.rect.centery - goal.rect.centery)**2)**0.5
            
            # Score based on proximity and vertical priority
            score = (1000 / (dist + 1)) * vert_factor
            
            if score > best_score:
                best_score = score
                best_target = cp
        
        if best_target:
            return best_target.rect.centerx, best_target.rect.centery
        
        return goal.rect.centerx, goal.rect.centery
    
    def cast_rays(self, blocks, target_x, target_y):
        """Cast rays in multiple directions to detect nearby blocks"""
        directions = [
            (0, -1),    # Up
            (1, -1),    # Up-right
            (1, 0),     # Right
            (1, 1),     # Down-right
            (0, 1),     # Down
            (-1, 1),    # Down-left
            (-1, 0),    # Left
            (-1, -1)    # Up-left
        ]
        
        ray_range = 300  # Maximum ray distance
        ray_results = []
        
        # Cast rays in 8 directions
        for dx, dy in directions:
            closest_hit = ray_range
            
            # Normalize direction vector
            mag = (dx**2 + dy**2)**0.5
            if mag > 0:
                dx, dy = dx/mag, dy/mag
            
            # Step along ray
            for step in range(1, ray_range, 10):
                x = self.rect.centerx + dx * step
                y = self.rect.centery + dy * step
                
                # Check if ray hit a block
                for block in blocks:
                    if block.rect.collidepoint(x, y):
                        closest_hit = step
                        break
                
                if closest_hit < ray_range:
                    break
                
                # Check if ray is out of bounds
                if (x < 0 or x > SCREEN_WIDTH or 
                    y < 0 or y > SCREEN_HEIGHT):
                    closest_hit = step
                    break
            
            ray_results.append(closest_hit)
        
        # Additional directional ray toward target
        target_dir_x = target_x - self.rect.centerx
        target_dir_y = target_y - self.rect.centery
        
        # Normalize target direction
        target_dist = (target_dir_x**2 + target_dir_y**2)**0.5
        if target_dist > 0:
            target_dir_x /= target_dist
            target_dir_y /= target_dist
        
        target_ray_hit = ray_range
        for step in range(1, ray_range, 10):
            x = self.rect.centerx + target_dir_x * step
            y = self.rect.centery + target_dir_y * step
            
            # Check if ray hit a block
            for block in blocks:
                if block.rect.collidepoint(x, y):
                    target_ray_hit = step
                    break
            
            if target_ray_hit < ray_range:
                break
        
        ray_results.append(target_ray_hit)
        
        return ray_results
    
    def calculate_fitness(self, goal, checkpoints=None):
        """Calculate fitness with focus on progress and exploration"""
        # Base distance component
        dist_to_goal = ((self.rect.centerx - goal.rect.centerx)**2 + 
                       (self.rect.centery - goal.rect.centery)**2)**0.5
        
        # Start with base fitness inversely proportional to distance
        self.fitness = 1000 / (1 + dist_to_goal**0.5)  # Square root for diminishing returns
        
        # Substantial checkpoint bonuses with increasing multiplier
        checkpoint_multiplier = 1.0
        for i in range(len(self.collected_checkpoints)):
            checkpoint_reward = 2000 * checkpoint_multiplier  # Higher base value
            self.fitness += checkpoint_reward
            checkpoint_multiplier += 0.7  # Steeper increase for later checkpoints
        
        # Vertical progress bonus - heavily reward upward movement
        self.fitness += self.vertical_progress * 20
        
        # Distance traveled bonus (encourages exploration)
        self.fitness += min(self.total_distance_traveled, 5000) * 0.1
        
        # Time alive bonus (smaller component)
        self.fitness += self.time_alive * 0.05
        
        # Major goal-reaching bonus
        if self.reached_goal:
            checkpoint_count = len(self.collected_checkpoints) if checkpoints else 0
            self.fitness += 15000 + (checkpoint_count * 3000)
        
        # Massive penalty for repetitive behavior
        if self.detect_stuckness():
            stuck_penalty = 2000 + (self.stuck_timer ** 1.5)
            self.fitness -= stuck_penalty
            
            # Severely penalize AIs that get permanently stuck
            if self.stuck_timer > 150:
                self.fitness -= 5000
                
            # Mark as dead if hopelessly stuck for a very long time
            if self.stuck_timer > 250:
                self.dead = True
        
        # Penalty for death
        if self.dead:
            self.fitness *= 0.5
        
        return self.fitness
    
    def draw_neural_network(self, x, y, width, height):
        # Neural network visualization
        input_size = 6
        hidden_size = 8
        output_size = 3
        
        # Calculate node positions
        input_x = x + 30
        hidden_x = x + width // 2
        output_x = x + width - 30
        
        input_y_start = y + 50
        input_y_end = y + height - 50
        input_y_step = (input_y_end - input_y_start) // (input_size - 1) if input_size > 1 else 0
        
        hidden_y_start = y + 50
        hidden_y_end = y + height - 50
        hidden_y_step = (hidden_y_end - hidden_y_start) // (hidden_size - 1) if hidden_size > 1 else 0
        
        output_y_start = y + height // 4
        output_y_end = y + height - height // 4
        output_y_step = (output_y_end - output_y_start) // (output_size - 1) if output_size > 1 else 0
        
        # Calculate node colors based on activation values
        def get_activation_color(value):
            if value > 0:
                # Positive activations: white -> green
                intensity = min(abs(value), 1.0)
                return (int(255 * (1 - intensity)), 255, int(255 * (1 - intensity)))
            else:
                # Negative activations: white -> red
                intensity = min(abs(value), 1.0)
                return (255, int(255 * (1 - intensity)), int(255 * (1 - intensity)))
        
        # Draw connections first (so they're behind nodes)
        w1, w2 = self.nn_weights
        for i in range(input_size):
            input_y = input_y_start + i * input_y_step
            for h in range(hidden_size):
                hidden_y = hidden_y_start + h * hidden_y_step
                # Connection weight determines line thickness
                weight = w1[i, h]
                thickness = max(1, min(int(abs(weight) * 5), 4))
                # Positive weights are green, negative are red
                color = GREEN if weight > 0 else RED
                # Alpha based on weight magnitude
                alpha = min(int(abs(weight) * 200) + 55, 255)
                color_with_alpha = (*color, alpha)
                # Create a new surface for the semi-transparent line
                line_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.line(line_surface, color_with_alpha, (input_x, input_y), (hidden_x, hidden_y), thickness)
                screen.blit(line_surface, (0, 0))
        
        for h in range(hidden_size):
            hidden_y = hidden_y_start + h * hidden_y_step
            for o in range(output_size):
                output_y = output_y_start + o * output_y_step
                # Connection weight determines line thickness
                weight = w2[h, o]
                thickness = max(1, min(int(abs(weight) * 5), 4))
                # Positive weights are green, negative are red
                color = GREEN if weight > 0 else RED
                # Alpha based on weight magnitude
                alpha = min(int(abs(weight) * 200) + 55, 255)
                color_with_alpha = (*color, alpha)
                # Create a new surface for the semi-transparent line
                line_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.line(line_surface, color_with_alpha, (hidden_x, hidden_y), (output_x, output_y), thickness)
                screen.blit(line_surface, (0, 0))
        
        # Draw nodes
        font = pygame.font.Font(None, 14)
        
        # Input layer
        input_labels = ["Player X", "Player Y", "Block X", "Block Y", "Goal X", "Goal Y"]
        for i in range(input_size):
            input_y = input_y_start + i * input_y_step
            color = get_activation_color(self.activation_values['inputs'][i])
            pygame.draw.circle(screen, color, (input_x, input_y), 10)
            pygame.draw.circle(screen, BLACK, (input_x, input_y), 10, 1)  # Border
            
            # Node label
            label = font.render(input_labels[i], True, BLACK)
            screen.blit(label, (input_x - 50, input_y - 5))
            
            # Activation value
            value = font.render(f"{self.activation_values['inputs'][i]:.2f}", True, BLACK)
            screen.blit(value, (input_x + 15, input_y - 5))
        
        # Hidden layer
        for h in range(hidden_size):
            hidden_y = hidden_y_start + h * hidden_y_step
            color = get_activation_color(self.activation_values['hidden'][h])
            pygame.draw.circle(screen, color, (hidden_x, hidden_y), 10)
            pygame.draw.circle(screen, BLACK, (hidden_x, hidden_y), 10, 1)  # Border
            
            # Activation value
            value = font.render(f"{self.activation_values['hidden'][h]:.2f}", True, BLACK)
            screen.blit(value, (hidden_x + 15, hidden_y - 5))
        
        # Output layer
        output_labels = ["Jump", "Left", "Right"]
        for o in range(output_size):
            output_y = output_y_start + o * output_y_step
            color = get_activation_color(self.activation_values['outputs'][o])
            pygame.draw.circle(screen, color, (output_x, output_y), 10)
            pygame.draw.circle(screen, BLACK, (output_x, output_y), 10, 1)  # Border
            
            # Node label
            label = font.render(output_labels[o], True, BLACK)
            screen.blit(label, (output_x + 15, output_y - 5))
            
            # Activation value
            value = font.render(f"{self.activation_values['outputs'][o]:.2f}", True, BLACK)
            screen.blit(value, (output_x - 40, output_y - 5))
        
        # Draw layer labels
        font = pygame.font.Font(None, 24)
        input_label = font.render("Input Layer", True, BLACK)
        hidden_label = font.render("Hidden Layer", True, BLACK)
        output_label = font.render("Output Layer", True, BLACK)
        
        screen.blit(input_label, (input_x - 40, y + 10))
        screen.blit(hidden_label, (hidden_x - 40, y + 10))
        screen.blit(output_label, (output_x - 40, y + 10))

class Level:
    def __init__(self):
        self.blocks = []
        self.player_start = (50, 50)
        self.goal_pos = (700, 500)
        self.checkpoints = []  # List to store checkpoints
    
    def reset(self):
        self.blocks = []
        self.player_start = (50, 50)
        self.goal_pos = (700, 500)
        self.checkpoints = []
        
    def add_block(self, x, y, width, height):
        self.blocks.append(Block(x, y, width, height))
        
    def remove_block(self, x, y):
        for block in self.blocks:
            if block.rect.collidepoint(x, y):
                self.blocks.remove(block)
                return True
        return False
    
    def save(self, filename):
        level_data = {
            "blocks": [(b.rect.x, b.rect.y, b.rect.width, b.rect.height) for b in self.blocks],
            "player_start": self.player_start,
            "goal_pos": self.goal_pos,
            "checkpoints": [(c.rect.x, c.rect.y) for c in self.checkpoints]  # Save checkpoint positions
        }
        
        with open(f"levels/{filename}.pkl", "wb") as f:
            pickle.dump(level_data, f)
        return True
    
    def load(self, filename):
        try:
            with open(f"levels/{filename}.pkl", "rb") as f:
                level_data = pickle.load(f)
                
            self.blocks = [Block(x, y, w, h) for x, y, w, h in level_data['blocks']]
            self.player_start = (level_data['player_start'][0], level_data['player_start'][1])
            self.goal_pos = level_data['goal_pos']
            
            # Load checkpoints if they exist in the saved data
            self.checkpoints = []
            if 'checkpoints' in level_data:
                self.checkpoints = [Checkpoint(x, y) for x, y in level_data['checkpoints']]
            
            return True
        except Exception as e:
            print(f"Error loading level: {e}")
            return False

class LevelEditor:
    def __init__(self, level=None):
        # Create a new level if none is provided
        self.level = level if level is not None else Level()
        self.start_pos = None
        self.current_rect = None
        self.placing_player = False
        self.placing_goal = False
        self.placing_checkpoint = False
        self.grid_snap = True
        self.saved_message = ""
        self.saved_message_timer = 0
        self.confirm_state = None
        self.confirm_message = ""
        self.confirm_filename = ""
        
        # Add checkpoint management
        self.removing_checkpoint = False  # New state for removing checkpoints
        
        # Add help toggle flag
        self.show_help = False  # Only show help when requested
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                x, y = event.pos
                if self.placing_player:
                    if self.grid_snap:
                        x = (x // GRID_SIZE) * GRID_SIZE
                        y = (y // GRID_SIZE) * GRID_SIZE
                    self.level.player_start = (x, y)
                    self.placing_player = False
                elif self.placing_goal:
                    if self.grid_snap:
                        x = (x // GRID_SIZE) * GRID_SIZE
                        y = (y // GRID_SIZE) * GRID_SIZE
                    self.level.goal_pos = (x, y)
                    self.placing_goal = False
                elif self.placing_checkpoint:
                    # Place a checkpoint at mouse position
                    mouse_x, mouse_y = event.pos
                    if self.grid_snap:
                        mouse_x = (mouse_x // GRID_SIZE) * GRID_SIZE
                        mouse_y = (mouse_y // GRID_SIZE) * GRID_SIZE
                    
                    # Add the checkpoint
                    self.level.checkpoints.append(Checkpoint(mouse_x, mouse_y))
                    
                    # Immediately turn off checkpoint placement mode after placing one
                    self.placing_checkpoint = False
                    
                    # Provide visual feedback
                    self.saved_message = "Checkpoint placed"
                    self.saved_message_timer = 30
                    
                    return None
                elif self.removing_checkpoint:
                    # Handle checkpoint removal
                    mouse_x, mouse_y = event.pos
                    removed = False
                    
                    # Check each checkpoint for a hit
                    for i, cp in enumerate(self.level.checkpoints):
                        # Use a slightly larger area for easier selection
                        hit_rect = pygame.Rect(cp.rect.x - 5, cp.rect.y - 5, 
                                             cp.rect.width + 10, cp.rect.height + 10)
                        if hit_rect.collidepoint(mouse_x, mouse_y):
                            # Remove this checkpoint
                            self.level.checkpoints.pop(i)
                            removed = True
                            
                            # Provide visual feedback
                            self.saved_message = f"Checkpoint #{i} removed"
                            self.saved_message_timer = 30
                            break
                    
                    if not removed:
                        self.saved_message = "No checkpoint selected"
                        self.saved_message_timer = 30
                    
                    return None
                else:
                    if pygame.key.get_mods() & KMOD_CTRL:
                        # Remove block - fix this functionality
                        if self.level.remove_block(x, y):
                            self.saved_message = "Block removed"
                            self.saved_message_timer = 30
                    else:
                        # Start placing a block
                        if self.grid_snap:
                            x = (x // GRID_SIZE) * GRID_SIZE
                            y = (y // GRID_SIZE) * GRID_SIZE
                        self.start_pos = (x, y)
                        self.current_rect = pygame.Rect(x, y, 0, 0)

            # Add right-click to remove blocks too
            elif event.button == 3:  # Right click
                x, y = event.pos
                if self.level.remove_block(x, y):
                    self.saved_message = "Block removed"
                    self.saved_message_timer = 30
        
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 and self.start_pos and self.current_rect:  # Left click release
                # Finalize block placement
                start_x, start_y = self.start_pos
                end_x, end_y = event.pos
                
                if self.grid_snap:
                    end_x = (end_x // GRID_SIZE) * GRID_SIZE
                    end_y = (end_y // GRID_SIZE) * GRID_SIZE
                
                # Calculate top-left corner and dimensions
                x = min(start_x, end_x)
                y = min(start_y, end_y)
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                
                # Only add block if it has positive dimensions
                if width > 0 and height > 0:
                    self.level.add_block(x, y, width, height)
                
                self.start_pos = None
                self.current_rect = None
                
        elif event.type == MOUSEMOTION:
            if self.start_pos:
                end_x, end_y = event.pos
                if self.grid_snap:
                    end_x = (end_x // GRID_SIZE) * GRID_SIZE
                    end_y = (end_y // GRID_SIZE) * GRID_SIZE
                
                # Get the original start position
                start_x, start_y = self.start_pos
                
                # Calculate top-left corner and dimensions for display
                x = min(start_x, end_x)
                y = min(start_y, end_y)
                width = abs(end_x - start_x)
                height = abs(end_y - start_y)
                
                # Update the current rectangle with correct positioning
                self.current_rect = pygame.Rect(x, y, width, height)
                
        elif event.type == KEYDOWN:
            if event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                filename = "level1"  # Default name, can be improved with text input
                
                # Add warning/confirmation before saving
                self.confirm_state = "save"
                self.confirm_message = f"Are you sure you want to save as '{filename}'? (Y/N)"
                self.confirm_filename = filename
                return None
            
            elif event.key == K_l and pygame.key.get_mods() & KMOD_CTRL:
                filename = "level1"  # Default name, can be improved with text input
                
                # Add warning/confirmation before loading
                self.confirm_state = "load"
                self.confirm_message = f"Loading will replace your current level. Load '{filename}'? (Y/N)"
                self.confirm_filename = filename
                return None
            
            elif event.key == K_y and self.confirm_state:
                # Confirm action (Y was pressed)
                if self.confirm_state == "save":
                    self.level.save(self.confirm_filename)
                    self.saved_message = f"Level saved as {self.confirm_filename}"
                    self.saved_message_timer = 60
                elif self.confirm_state == "load":
                    if self.level.load(self.confirm_filename):
                        self.saved_message = f"Level {self.confirm_filename} loaded"
                    else:
                        self.saved_message = f"Failed to load level {self.confirm_filename}"
                    self.saved_message_timer = 60
                elif self.confirm_state == "clear":
                    # Properly implement clearing the level
                    self.level.reset()
                    self.saved_message = "Level cleared"
                    self.saved_message_timer = 60
                
                self.confirm_state = None
                return None
            
            elif event.key == K_n and self.confirm_state:
                # Cancel action (N was pressed)
                self.saved_message = f"Action cancelled"
                self.saved_message_timer = 60
                self.confirm_state = None
                return None
            
            elif event.key == K_c:  # C to clear the level
                self.confirm_state = "clear"
                self.confirm_message = "Are you sure you want to clear the level? (Y/N)"
                return None
            
            elif event.key == K_q:  # Q to place checkpoints
                self.placing_player = False
                self.placing_goal = False
                self.placing_checkpoint = True
                self.current_rect = None
                
                # Add visual feedback
                self.saved_message = "Click to place a checkpoint"
                self.saved_message_timer = 60
                return None
            
            elif event.key == K_p:
                self.placing_player = True
            elif event.key == K_g:
                self.placing_goal = True
            elif event.key == K_SPACE:
                return "play"  # Switch to play mode
            elif event.key == K_a:
                return "ai_train"  # Switch to AI training mode
            elif event.key == K_t:
                self.grid_snap = not self.grid_snap
            elif event.key == K_x:  # X to toggle checkpoint removal mode
                self.placing_player = False
                self.placing_goal = False
                self.placing_checkpoint = False
                self.removing_checkpoint = not self.removing_checkpoint
                
                if self.removing_checkpoint:
                    self.saved_message = "Click on a checkpoint to remove it"
                else:
                    self.saved_message = "Checkpoint removal mode off"
                    
                self.saved_message_timer = 60
                return None
            
            # Add help toggle key
            elif event.key == K_h:
                self.show_help = not self.show_help
                return None
                
            # If help is showing, any key closes it
            if self.show_help:
                self.show_help = False
                return None
    
    def update(self):
        if self.saved_message_timer > 0:
            self.saved_message_timer -= 1
            if self.saved_message_timer == 0:
                self.saved_message = ""
    
    def draw(self):
        screen.fill(WHITE)
        
        # Draw grid
        if self.grid_snap:
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, (220, 220, 220), (0, y), (SCREEN_WIDTH, y))
        
        # Draw blocks
        for block in self.level.blocks:
            block.draw()
        
        # Draw current rectangle if placing
        if self.current_rect:
            pygame.draw.rect(screen, BLUE, self.current_rect, 2)
        
        # Draw player start position
        pygame.draw.rect(screen, BLUE, (self.level.player_start[0], self.level.player_start[1], GRID_SIZE, GRID_SIZE))
        
        # Draw goal position
        pygame.draw.rect(screen, GREEN, (self.level.goal_pos[0], self.level.goal_pos[1], GRID_SIZE, GRID_SIZE))
        
        # Draw checkpoints
        for i, cp in enumerate(self.level.checkpoints):
            pygame.draw.rect(screen, CHECKPOINT_COLOR, cp.rect)
            
            # Draw index number on each checkpoint
            font = pygame.font.SysFont(None, 24)
            index_text = font.render(str(i), True, BLACK)
            # Center the text on the checkpoint
            text_x = cp.rect.centerx - index_text.get_width() // 2
            text_y = cp.rect.centery - index_text.get_height() // 2
            screen.blit(index_text, (text_x, text_y))
        
        # Draw saved message
        if self.saved_message:
            font = pygame.font.Font(None, 36)
            text = font.render(self.saved_message, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))
        
        # Draw confirmation message if active
        if self.confirm_state:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            screen.blit(overlay, (0, 0))
            
            # Draw confirmation dialog
            dialog_width, dialog_height = 500, 150
            dialog_x = SCREEN_WIDTH//2 - dialog_width//2
            dialog_y = SCREEN_HEIGHT//2 - dialog_height//2
            
            pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)
            
            # Draw message
            font = pygame.font.Font(None, 28)
            text = font.render(self.confirm_message, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, dialog_y + 40))
            
            # Draw options
            options = font.render("Press Y to confirm, N to cancel", True, BLACK)
            screen.blit(options, (SCREEN_WIDTH//2 - options.get_width()//2, dialog_y + 80))
        
        # Draw mode indicator text
        mode_text = None
        if self.placing_player:
            mode_text = "Placing Player Start"
        elif self.placing_goal:
            mode_text = "Placing Goal"
        elif self.placing_checkpoint:
            mode_text = "Placing Checkpoint - Click Once"
        
        if mode_text:
            font = pygame.font.Font(None, 32)
            text = font.render(mode_text, True, BLUE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 10))
        
        # Only show help if toggled on
        if self.show_help:
            self.draw_help()
        else:
            # Just show compact controls in top corner when help is off
            font = pygame.font.SysFont(None, 24)
            help_text = font.render("Press H for help", True, BLACK)
            screen.blit(help_text, (10, 10))
        
        # Highlight active mode with different colored text
        if self.placing_player:
            active_message = "Placing Player (P)"
            active_color = GREEN
        elif self.placing_goal:
            active_message = "Placing Goal (G)"
            active_color = RED
        elif self.placing_checkpoint:
            active_message = "Placing Checkpoint (Q)"
            active_color = CHECKPOINT_COLOR
        elif self.removing_checkpoint:
            active_message = "Removing Checkpoint (X)"
            active_color = PURPLE
        else:
            active_message = "Placing Blocks"
            active_color = BLACK
        
        # Draw mode text
        mode_font = pygame.font.SysFont(None, 26)
        mode_text = mode_font.render(active_message, True, active_color)
        screen.blit(mode_text, (10, 40))

    def draw_help(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw help text
        font = pygame.font.SysFont(None, 30)
        y_offset = 100
        
        help_lines = [
            "LEVEL EDITOR CONTROLS",
            "",
            "P: Place player",
            "G: Place goal",
            "Q: Place checkpoint",
            "X: Remove checkpoint mode",
            "Left-click: Place object/Start drawing block",
            "Right-click: Remove a block",
            "ESC: Return to main menu",
            "H: Toggle help screen",
            "CTRL+S: Save level",
            "CTRL+L: Load level",
            "C: Clear level",
            "F11: Toggle fullscreen",
            "SPACE: Test play level",
            "T: Train AI on this level",
        ]
        
        for line in help_lines:
            if line == "LEVEL EDITOR CONTROLS":
                # Make the title larger and green
                title_font = pygame.font.SysFont(None, 40)
                text = title_font.render(line, True, GREEN)
            elif line == "":
                # Skip empty lines
                y_offset += 15
                continue
            else:
                text = font.render(line, True, WHITE)
            
            # Center text horizontally
            x = (SCREEN_WIDTH - text.get_width()) // 2
            screen.blit(text, (x, y_offset))
            y_offset += 40
        
        # Draw note to press any key
        note_font = pygame.font.SysFont(None, 25)
        note = note_font.render("Press any key to return", True, YELLOW)
        note_x = (SCREEN_WIDTH - note.get_width()) // 2
        screen.blit(note, (note_x, SCREEN_HEIGHT - 100))

class PlayMode:
    def __init__(self, level):
        self.level = level
        self.player = Player(*level.player_start, GRID_SIZE, GRID_SIZE)
        self.goal = Goal(*level.goal_pos)
        
        # Create checkpoints from level data
        self.checkpoints = []
        for cp_data in self.level.checkpoints:
            self.checkpoints.append(Checkpoint(cp_data.rect.x, cp_data.rect.y))
        
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.player.jump()
            elif event.key == K_r:
                self.player.reset()
            elif event.key == K_ESCAPE:
                return "editor"  # Return to editor
        
        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.player.move_left()
        elif keys[K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()
    
    def update(self):
        self.player.update(self.level.blocks, self.goal)
        
        # Check for checkpoint collisions
        for checkpoint in self.checkpoints:
            if checkpoint.is_active and self.player.rect.colliderect(checkpoint.rect):
                checkpoint.is_active = False  # Mark as collected
    
    def draw(self):
        screen.fill(WHITE)
        
        # Draw blocks
        for block in self.level.blocks:
            block.draw()
        
        # Draw goal
        self.goal.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw checkpoints
        for checkpoint in self.checkpoints:
            checkpoint.draw()
        
        # Draw status info
        font = pygame.font.Font(None, 36)
        
        if self.player.reached_goal:
            text = font.render("Goal Reached!", True, GREEN)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))
        elif self.player.dead:
            text = font.render("You Died!", True, RED)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))
        
        # Draw help text
        font = pygame.font.Font(None, 24)
        instructions = [
            "Left/Right: Move",
            "Space: Jump",
            "R: Reset",
            "Esc: Return to editor"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, BLACK)
            screen.blit(text, (10, 10 + i * 25))

class AITrainer:
    def __init__(self, level):
        self.level = level
        self.goal = Goal(*level.goal_pos)
        self.population = [AIPlayer(*level.player_start) for _ in range(AI_POPULATION)]
        self.generation = 0
        self.best_fitness = 0
        self.best_ai = None
        self.generation_timer = 0
        self.max_generation_time = 1000  # Frames before starting a new generation
        self.running = False
        self.fast_mode = False
        self.visualize_best_only = False
        self.spectate_mode = False
        self.top_performers = []
        self.spectate_index = 0
        self.show_neural_network = False
        self.best_of_previous_gen = []  # Add this line to store best AIs from previous gen
        self.hall_of_fame = []  # Store best AI from each generation
        
        # Create checkpoints
        self.checkpoints = []
        for cp in level.checkpoints:
            self.checkpoints.append(Checkpoint(cp.rect.x, cp.rect.y))
    
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.spectate_mode:
                    self.spectate_mode = False
                    return None
                else:
                    return "editor"  # Return to editor
            elif event.key == K_SPACE:
                if not self.spectate_mode:
                    self.running = not self.running
            elif event.key == K_f:
                if not self.spectate_mode:
                    self.fast_mode = not self.fast_mode
            elif event.key == K_v:
                if not self.spectate_mode:
                    self.visualize_best_only = not self.visualize_best_only
            elif event.key == K_s and pygame.key.get_mods() & KMOD_CTRL:
                self.save_best_ai()
            elif event.key == K_l and pygame.key.get_mods() & KMOD_CTRL:
                self.load_best_ai()
            elif event.key == K_RETURN:
                if not self.spectate_mode:
                    self.update_top_performers()
                    self.spectate_mode = True
                    self.spectate_index = 0
                    # Reset and prepare for spectating
                    for ai in self.top_performers:
                        ai.reset()
            elif event.key == K_n:
                if self.spectate_mode:
                    self.show_neural_network = not self.show_neural_network
            elif event.key == K_LEFT:
                if self.spectate_mode:
                    self.spectate_index = (self.spectate_index - 1) % len(self.top_performers)
                    self.top_performers[self.spectate_index].reset()
            elif event.key == K_RIGHT:
                if self.spectate_mode:
                    self.spectate_index = (self.spectate_index + 1) % len(self.top_performers)
                    self.top_performers[self.spectate_index].reset()
            
        return None
    
    def update_top_performers(self):
        # Calculate fitness for all AIs
        for ai in self.population:
            ai.calculate_fitness(self.goal, self.checkpoints)
        
        # Sort by fitness
        sorted_population = sorted(self.population, key=lambda ai: ai.fitness, reverse=True)
        
        # Take top 10 or less if population is smaller
        num_top = min(10, len(sorted_population))
        self.top_performers = [sorted_population[i] for i in range(num_top)]
    
    def save_best_ai(self):
        if self.best_ai:
            # Save weights to file
            filename = f"best_ai_gen_{self.generation}"
            with open(f"ai_models/{filename}.pkl", "wb") as f:
                pickle.dump(self.best_ai.nn_weights, f)
            print(f"Saved best AI to ai_models/{filename}.pkl")
    
    def load_best_ai(self):
        try:
            # Ask for filename or use default
            filename = "best_ai_gen_latest"  # Could be improved with text input
            
            with open(f"ai_models/{filename}.pkl", "rb") as f:
                weights = pickle.load(f)
            
            # Create a new AI with these weights
            loaded_ai = AIPlayer(*self.level.player_start)
            loaded_ai.nn_weights = weights
            
            # Add to hall of fame and current population
            self.hall_of_fame.append(loaded_ai)
            
            # Replace worst performer with this loaded AI
            if self.population:
                worst_fitness = float('inf')
                worst_index = 0
                
                for i, ai in enumerate(self.population):
                    fitness = ai.calculate_fitness(self.goal, self.checkpoints)
                    if fitness < worst_fitness:
                        worst_fitness = fitness
                        worst_index = i
                
                self.population[worst_index] = loaded_ai
            
            print(f"Loaded AI from ai_models/{filename}.pkl")
            return True
        except Exception as e:
            print(f"Failed to load AI: {e}")
            return False
    
    def evolve_population(self):
        # Calculate fitness for all AIs
        for ai in self.population:
            ai.calculate_fitness(self.goal, self.checkpoints)
        
        # Store best AIs from this generation
        current_gen_best = sorted(self.population, key=lambda ai: ai.fitness, reverse=True)[:3]
        self.best_of_previous_gen = []
        for ai in current_gen_best:
            copy_ai = AIPlayer(*self.level.player_start, generation=self.generation)
            copy_ai.nn_weights = [w.copy() for w in ai.nn_weights]
            copy_ai.fitness = ai.fitness
            copy_ai.collected_checkpoints = ai.collected_checkpoints.copy() if hasattr(ai, 'collected_checkpoints') else []
            self.best_of_previous_gen.append(copy_ai)
        
        # Filter out dead AIs
        living_ais = [ai for ai in self.population if not ai.dead]
        
        # Handle case where all AIs died
        if not living_ais:
            print("All AIs died! Using best 3 from previous generation.")
            if self.best_of_previous_gen:
                breeding_pool = self.best_of_previous_gen
                print(f"Using {len(breeding_pool)} AIs from previous generation")
            else:
                print("No previous generation available. Creating fresh population.")
                self.population = [AIPlayer(*self.level.player_start) for _ in range(AI_POPULATION)]
                self.generation += 1
                for ai in self.population:
                    ai.reset()
                return
        else:
            # Multi-criteria selection
            # 1. First sort by checkpoint count (most important)
            checkpoint_sorted = sorted(living_ais, key=lambda ai: len(ai.collected_checkpoints), reverse=True)
            
            # Find maximum checkpoint count
            max_checkpoints = len(checkpoint_sorted[0].collected_checkpoints) if checkpoint_sorted else 0
            
            # 2. For AIs with same checkpoint count, sort by distance to goal
            distance_grouped = []
            for i in range(max_checkpoints + 1):
                # Get all AIs with this checkpoint count
                same_checkpoints = [ai for ai in checkpoint_sorted 
                                   if len(ai.collected_checkpoints) == max_checkpoints - i]
                
                if same_checkpoints:
                    # Sort this group by distance to goal
                    for ai in same_checkpoints:
                        ai.distance_to_goal = ((ai.rect.centerx - self.goal.rect.centerx)**2 + 
                                             (ai.rect.centery - self.goal.rect.centery)**2)**0.5
                    
                    goal_sorted = sorted(same_checkpoints, key=lambda ai: ai.distance_to_goal)
                    distance_grouped.extend(goal_sorted)
                
                # Once we have enough candidates, stop processing lower checkpoint counts
                if len(distance_grouped) >= 10:
                    break
            
            # 3. Take top candidates and sort by total fitness
            candidates = distance_grouped[:10] if len(distance_grouped) >= 10 else distance_grouped
            fitness_sorted = sorted(candidates, key=lambda ai: ai.fitness, reverse=True)
            
            # Select top 5 for breeding
            breeding_pool = fitness_sorted[:5] if len(fitness_sorted) >= 5 else fitness_sorted
        
        # Store best AI info for hall of fame
        best_ai = breeding_pool[0] if breeding_pool else None
        if best_ai and (not self.best_ai or best_ai.fitness > self.best_fitness):
            self.best_fitness = best_ai.fitness
            self.best_ai = AIPlayer(*self.level.player_start, generation=self.generation)
            self.best_ai.nn_weights = [w.copy() for w in best_ai.nn_weights]
            self.best_ai.fitness = best_ai.fitness
            
            # Add to hall of fame
            hall_entry = AIPlayer(*self.level.player_start, generation=self.generation)
            hall_entry.nn_weights = [w.copy() for w in best_ai.nn_weights]
            hall_entry.fitness = best_ai.fitness
            self.hall_of_fame.append(hall_entry)
            if len(self.hall_of_fame) > 10:
                self.hall_of_fame.pop(0)
        
        # Create new population
        new_population = []
        
        # Always keep the best performers
        for i, ai in enumerate(breeding_pool):
            if i < len(breeding_pool):  # Keep all in breeding pool
                new_ai = AIPlayer(*self.level.player_start, generation=self.generation)
                new_ai.nn_weights = [w.copy() for w in ai.nn_weights]
                new_ai.collected_checkpoints = ai.collected_checkpoints.copy() if hasattr(ai, 'collected_checkpoints') else []
                new_population.append(new_ai)
        
        # Fill the rest with offspring
        while len(new_population) < AI_POPULATION:
            # Select parents from the breeding pool
            if len(breeding_pool) >= 2:
                # Weighted selection favoring higher ranked AIs
                weights = [5 - i for i in range(min(5, len(breeding_pool)))]
                parents = random.choices(breeding_pool[:5], weights=weights, k=2)
                parent1, parent2 = parents[0], parents[1]
            else:
                parent1 = breeding_pool[0]
                parent2 = parent1  # Self-breed if only one parent available
            
            # Create child with crossover
            child = AIPlayer(*self.level.player_start, generation=self.generation)
            
            # Apply crossover
            w1 = parent1.nn_weights[0].copy()
            w2 = parent1.nn_weights[1].copy()
            
            # Crossover method: either take whole layers from one parent or do element-wise mixing
            if random.random() < 0.5:
                # Take either first or second layer from parent2
                if random.random() < 0.5:
                    w1 = parent2.nn_weights[0].copy()
                else:
                    w2 = parent2.nn_weights[1].copy()
            else:
                # Element-wise mixing
                mask1 = np.random.random(w1.shape) < 0.5
                mask2 = np.random.random(w2.shape) < 0.5
                
                w1[mask1] = parent2.nn_weights[0][mask1]
                w2[mask2] = parent2.nn_weights[1][mask2]
            
            # Set child's weights
            child.nn_weights = [w1, w2]
            
            # Apply mutation - higher mutation for variety
            mutation_rate = AI_MUTATION_RATE * 1.5
            
            # Apply mutations
            for i, w in enumerate(child.nn_weights):
                # Each weight has a chance to mutate
                mask = np.random.random(w.shape) < mutation_rate
                mutation = np.random.randn(np.sum(mask)) * AI_MUTATION_STRENGTH
                w[mask] += mutation
            
            # Add child to new population
            new_population.append(child)
        
        # Set explorer status for some AIs to encourage exploration
        explorer_count = int(AI_POPULATION * AI_EXPLORER_RATIO)
        for i in range(explorer_count):
            if i < len(new_population):
                new_population[-(i+1)].is_explorer = True  # Mark last few as explorers
                new_population[-(i+1)].color = ORANGE
        
        # Replace population
        self.population = new_population
        self.generation += 1
        
        # Reset all AIs
        for ai in self.population:
            ai.reset()
    
    def update(self):
        if self.spectate_mode:
            # Update only the AI being spectated
            current_ai = self.top_performers[self.spectate_index]
            current_ai.ai_action(self.level.blocks, self.goal, self.checkpoints)
            current_ai.update(self.level.blocks, self.goal)
            
            # Check for checkpoint collisions for this specific AI
            for checkpoint in self.checkpoints:
                if checkpoint not in current_ai.collected_checkpoints and current_ai.rect.colliderect(checkpoint.rect):
                    current_ai.collected_checkpoints.append(checkpoint)
                    print(f"Spectated AI collected checkpoint! ({len(current_ai.collected_checkpoints)} total)")
            
            # Check if AI reached goal or died
            if current_ai.reached_goal or current_ai.dead:
                # Wait a moment and reset
                self.generation_timer += 1
                if self.generation_timer > 60:  # Wait 1 second
                    self.generation_timer = 0
                    current_ai.reset()
            
            return
            
        if not self.running:
            return
            
        # Update all AIs
        active_ais = 0
        for ai in self.population:
            if not ai.dead and not ai.reached_goal:
                active_ais += 1
                ai.ai_action(self.level.blocks, self.goal, self.checkpoints)
                ai.update(self.level.blocks, self.goal)
                
                # Debug checkpoint detection
                previous_checkpoint_count = len(ai.collected_checkpoints)
                
                # Check for checkpoint collisions for this specific AI
                for checkpoint in self.checkpoints:
                    if checkpoint not in ai.collected_checkpoints and ai.rect.colliderect(checkpoint.rect):
                        ai.collected_checkpoints.append(checkpoint)
                
                # Debug output if checkpoint count changed
                if len(ai.collected_checkpoints) > previous_checkpoint_count:
                    print(f"AI collected checkpoint! Now has {len(ai.collected_checkpoints)} checkpoints")
        
        # Check if all AIs have finished or if time is up
        self.generation_timer += 1
        
        if active_ais == 0 or self.generation_timer >= self.max_generation_time:
            # Evolve population
            self.evolve_population()
            self.generation_timer = 0
            
            # Update top performers list
            self.update_top_performers()
    
    def draw(self):
        screen.fill(WHITE)
        
        if self.spectate_mode:
            # Draw blocks
            for block in self.level.blocks:
                block.draw()
            
            # Draw goal
            self.goal.draw()
            
            # Draw checkpoints with collection status specific to current AI
            current_ai = self.top_performers[self.spectate_index]
            for checkpoint in self.checkpoints:
                # Draw collected or uncollected based on this AI's status
                is_collected = checkpoint in current_ai.collected_checkpoints
                self.draw_checkpoint(checkpoint, is_collected)
            
            # Draw the spectated AI
            current_ai.draw()
            
            # Draw neural network visualization if enabled
            if self.show_neural_network:
                # Draw the neural network in a panel on the right side
                nn_panel_rect = pygame.Rect(SCREEN_WIDTH - 350, 50, 340, 500)
                pygame.draw.rect(screen, (240, 240, 240), nn_panel_rect)
                pygame.draw.rect(screen, BLACK, nn_panel_rect, 2)
                
                # Draw the neural network inside the panel
                current_ai.draw_neural_network(nn_panel_rect.x, nn_panel_rect.y, nn_panel_rect.width, nn_panel_rect.height)
            
            # Draw spectate info
            font = pygame.font.Font(None, 28)
            
            # AI index and status
            ai_info = f"Spectating AI #{self.spectate_index + 1}/{len(self.top_performers)} - Fitness: {current_ai.fitness:.2f}"
            text = font.render(ai_info, True, BLACK)
            screen.blit(text, (10, 10))
            
            # Status message
            status = "Reached Goal!" if current_ai.reached_goal else "Dead!" if current_ai.dead else "Active"
            color = GREEN if current_ai.reached_goal else RED if current_ai.dead else BLUE
            status_text = font.render(f"Status: {status}", True, color)
            screen.blit(status_text, (10, 40))
            
            # Controls help
            controls = [
                "LEFT/RIGHT: Switch AI",
                "N: Toggle Neural Network",
                "ESC: Return to Training"
            ]
            
            for i, control in enumerate(controls):
                text = font.render(control, True, BLACK)
                screen.blit(text, (10, SCREEN_HEIGHT - 30 * (len(controls) - i)))
        
        # Draw blocks
        for block in self.level.blocks:
            block.draw()
        
        # Draw goal
        self.goal.draw()
        
        # Draw AIs
        if self.visualize_best_only and self.best_ai:
            # Show only the best AI
            self.best_ai.draw()
        else:
            # Show all active AIs
            for ai in self.population:
                if not ai.dead:
                    ai.draw()
        
        # Draw checkpoints as uncollected (showing base state)
        for checkpoint in self.checkpoints:
            self.draw_checkpoint(checkpoint, False)
        
        # Draw training info
        font = pygame.font.Font(None, 28)
        
        # Generation info
        generation_text = font.render(f"Generation: {self.generation}", True, BLACK)
        screen.blit(generation_text, (10, 10))
        
        # Best fitness info
        fitness_text = font.render(f"Best Fitness: {self.best_fitness:.2f}", True, BLACK)
        screen.blit(fitness_text, (10, 40))
        
        # Active AIs
        active_count = sum(1 for ai in self.population if not ai.dead and not ai.reached_goal)
        active_text = font.render(f"Active AIs: {active_count}/{len(self.population)}", True, BLACK)
        screen.blit(active_text, (10, 70))
        
        # Timer
        timer_text = font.render(f"Time: {self.generation_timer}/{self.max_generation_time}", True, BLACK)
        screen.blit(timer_text, (10, 100))
        
        # Status message
        status = "Running" if self.running else "Paused"
        speed = "Fast Mode" if self.fast_mode else "Normal Speed"
        view = "Best AI Only" if self.visualize_best_only else "All AIs"
        
        status_text = font.render(f"Status: {status} - {speed} - {view}", True, BLACK)
        screen.blit(status_text, (10, 130))
        
        # Add explorer info
        explorer_count = sum(1 for ai in self.population if ai.is_explorer)
        explorer_text = font.render(f"Explorers: {explorer_count}/{len(self.population)}", True, ORANGE)
        screen.blit(explorer_text, (10, 160))
        
        # Controls help
        controls = [
            "SPACE: Start/Pause training",
            "F: Toggle fast mode",
            "V: Toggle view mode",
            "ENTER: Spectate best AIs",
            "CTRL+S: Save best AI",
            "CTRL+L: Load AI",
            "ESC: Return to editor"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, BLACK)
            screen.blit(text, (10, SCREEN_HEIGHT - 30 * (len(controls) - i)))
            
    def draw_checkpoint(self, checkpoint, collected):
        # Draw a diamond shape
        points = [
            (checkpoint.rect.centerx, checkpoint.rect.y),
            (checkpoint.rect.x + checkpoint.rect.width, checkpoint.rect.centery),
            (checkpoint.rect.centerx, checkpoint.rect.y + checkpoint.rect.height),
            (checkpoint.rect.x, checkpoint.rect.centery)
        ]
        
        if collected:
            # Draw a faded version when collected
            faded_color = (min(checkpoint.color[0] + 50, 255), 
                          min(checkpoint.color[1] + 50, 255), 
                          min(checkpoint.color[2] + 50, 255))
            pygame.draw.polygon(screen, faded_color, points, 1)
        else:
            # Draw normal version
            pygame.draw.polygon(screen, checkpoint.color, points)
            pygame.draw.polygon(screen, BLACK, points, 2)  # Border

def toggle_fullscreen():
    global FULLSCREEN
    FULLSCREEN = not FULLSCREEN
    initialize_screen()

def main():
    # Initialize the game
    current_mode = "editor"
    level_editor = LevelEditor()
    play_mode = None
    ai_trainer = None
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Add fullscreen toggle with F11
            if event.type == KEYDOWN and event.key == K_F11:
                toggle_fullscreen()
            
            # Handle mode-specific events
            if current_mode == "editor":
                new_mode = level_editor.handle_event(event)
                if new_mode:
                    current_mode = new_mode
                    if current_mode == "play":
                        play_mode = PlayMode(level_editor.level)
                    elif current_mode == "ai_train":
                        ai_trainer = AITrainer(level_editor.level)
            elif current_mode == "play":
                new_mode = play_mode.handle_event(event)
                if new_mode:
                    current_mode = new_mode
            elif current_mode == "ai_train":
                new_mode = ai_trainer.handle_event(event)
                if new_mode:
                    current_mode = new_mode
        
        # Update
        if current_mode == "editor":
            level_editor.update()
        elif current_mode == "play":
            play_mode.update()
        elif current_mode == "ai_train":
            # Handle fast mode
            update_count = 10 if ai_trainer.fast_mode else 1
            for _ in range(update_count):
                ai_trainer.update()
        
        # Draw
        if current_mode == "editor":
            level_editor.draw()
        elif current_mode == "play":
            play_mode.draw()
        elif current_mode == "ai_train":
            ai_trainer.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()