import pygame
import sys
import copy
import colorsys
import json

# Initialize Pygame
pygame.init()

# Simulation Configuration
Config = {
    # Display settings
    'width': 800,
    'height': 600,
    'fps': 60,
    
    # Physics settings
    'G': 20,  # Reduced more to ensure stable orbits
    'dt': 0.1,
    'prediction_steps': 500,
    'max_force': 2000,
    
    # Camera settings
    'zoom': 1.0,
    'zoom_speed': 0.1,
    'min_zoom': 0.1,
    'max_zoom': 5.0,
    'camera_offset': [0, 0],
    
    # Visual settings
    'colors': {
        'background': (0, 0, 0),
        'bodies': (255, 255, 255),
        'prediction': (255, 0, 0),
        'velocity': (0, 255, 0),  # Color for velocity vectors
        'trails': True,
        'trail_length': 400,  # Increased trail length to show more of the orbit
        'show_labels': True,
        'label_size': 16,
    },
    
    # Bodies configuration
    'bodies': [],
    
    # Add cursor force settings
    'cursor': {
        'force_magnitude': 100,  # Reduced to not disturb orbit too much
        'radius': 150,
        'attract_color': (255, 150, 0, 100),
        'repel_color': (0, 150, 255, 100),
    },
    
    # Time control settings
    'time_control': {
        'speed': 1.0,  # Normal speed
        'max_speed': 10.0,
        'min_speed': 0.1,
    },
    
    # Launch mode settings
    'launch_mode': {
        'active': False,
        'start_pos': None,
    },
}

# Track mouse dragging state
drag_state = {
    'dragging': False,
    'last_pos': None
}

# Set up the window
screen = pygame.display.set_mode((Config['width'], Config['height']))
pygame.display.set_caption("Orbital Simulation")
clock = pygame.time.Clock()

def world_to_screen(pos):
    """Convert world coordinates to screen coordinates"""
    x = (pos[0] + Config['camera_offset'][0]) * Config['zoom'] + Config['width']/2
    y = (pos[1] + Config['camera_offset'][1]) * Config['zoom'] + Config['height']/2
    return (int(x), int(y))

def screen_to_world(pos):
    """Convert screen coordinates to world coordinates"""
    x = (pos[0] - Config['width']/2) / Config['zoom'] - Config['camera_offset'][0]
    y = (pos[1] - Config['height']/2) / Config['zoom'] - Config['camera_offset'][1]
    return (x, y)

def calculate_force(body1, body2):
    dx = body2['position'][0] - body1['position'][0]
    dy = body2['position'][1] - body1['position'][1]
    distance = max((dx**2 + dy**2)**0.5, 1.0)  # Minimum distance of 1 pixel
    
    force_magnitude = Config['G'] * body1['mass'] * body2['mass'] / distance**2
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance
    
    # Limit maximum force
    max_force = Config['max_force']
    if abs(force_x) > max_force:
        force_x = max_force * (1 if force_x > 0 else -1)
    if abs(force_y) > max_force:
        force_y = max_force * (1 if force_y > 0 else -1)
    
    return (force_x, force_y)

def calculate_total_force(body_index, bodies):
    """Calculate total force on a body from all other bodies"""
    total_force_x = 0
    total_force_y = 0
    
    for i, other_body in enumerate(bodies):
        if i != body_index:  # Don't calculate force with itself
            force = calculate_force(bodies[body_index], other_body)
            total_force_x += force[0]
            total_force_y += force[1]
    
    return (total_force_x, total_force_y)

def update_body(body, force):
    # Calculate acceleration (F = ma)
    ax = force[0] / body['mass']
    ay = force[1] / body['mass']
    
    # Update velocity
    vx, vy = body['velocity']
    new_vx = vx + ax * Config['dt']
    new_vy = vy + ay * Config['dt']
    body['velocity'] = (new_vx, new_vy)
    
    # Update position
    x, y = body['position']
    new_x = x + new_vx * Config['dt']
    new_y = y + new_vy * Config['dt']
    body['position'] = (new_x, new_y)

def update_trails(bodies):
    """Update position history for each body"""
    for body in bodies:
        # Store world coordinates instead of screen coordinates
        body['trail'].append(body['position'])
        if len(body['trail']) > Config['colors']['trail_length']:
            body['trail'].pop(0)

def is_visible(position, radius=0):
    """Check if a position is visible on screen"""
    screen_pos = world_to_screen(position)
    margin = radius * Config['zoom']  # Add body radius to visibility check
    return (-margin <= screen_pos[0] <= Config['width'] + margin and 
            -margin <= screen_pos[1] <= Config['height'] + margin)

def predict_path(bodies, mouse_pos=None, attracting=False, repelling=False):
    predicted = copy.deepcopy(bodies)
    positions = {i: [] for i in range(len(bodies))}
    
    # Reduce prediction steps when zoomed out for better performance
    steps = min(Config['prediction_steps'], 
               int(Config['prediction_steps'] / (Config['zoom'] ** 0.5)))
    
    # Get world position of cursor for force calculation
    world_mouse_pos = screen_to_world(mouse_pos) if mouse_pos else None
    
    for _ in range(steps):
        forces = []
        visible_bodies = False
        
        # Calculate gravitational forces between bodies
        for i in range(len(predicted)):
            force = calculate_total_force(i, predicted)
            forces.append(force)
        
        # Add cursor forces if active
        if (attracting or repelling) and world_mouse_pos:
            for i, body in enumerate(predicted):
                dx = world_mouse_pos[0] - body['position'][0]
                dy = world_mouse_pos[1] - body['position'][1]
                distance = max((dx**2 + dy**2)**0.5, 1.0)
                
                # Use world-space radius for force calculation
                world_radius = Config['cursor']['radius'] / Config['zoom']
                if distance < world_radius:
                    falloff = (1 - (distance/world_radius)**2)
                    force_magnitude = Config['cursor']['force_magnitude']
                    if repelling:
                        force_magnitude = -force_magnitude
                    
                    force_x = force_magnitude * dx / distance
                    force_y = force_magnitude * dy / distance
                    
                    # Add cursor force to gravitational force
                    forces[i] = (
                        forces[i][0] + force_x * 0.5,
                        forces[i][1] + force_y * 0.5
                    )
        
        # Update positions and store if visible
        for i, body in enumerate(predicted):
            update_body(body, forces[i])
            
            if is_visible(body['position'], body['radius']):
                visible_bodies = True
                if _ % max(1, int(1 / Config['zoom'])) == 0:
                    positions[i].append(world_to_screen(body['position']))
        
        # Only stop if no bodies are visible
        if not visible_bodies and all(len(pos) > 0 for pos in positions.values()):
            break
    
    return positions

def draw_velocity_vector(body):
    start_pos = world_to_screen(body['position'])
    # Scale velocity for visualization
    scale = 2.0 * Config['zoom']
    end_pos = (int(start_pos[0] + body['velocity'][0] * scale),
               int(start_pos[1] + body['velocity'][1] * scale))
    pygame.draw.line(screen, Config['colors']['velocity'], start_pos, end_pos, 2)

def center_on_system(bodies):
    """Center the camera on the center of mass of the system"""
    total_mass = sum(body['mass'] for body in bodies)
    center_x = sum(body['position'][0] * body['mass'] for body in bodies) / total_mass
    center_y = sum(body['position'][1] * body['mass'] for body in bodies) / total_mass
    
    Config['camera_offset'] = [-center_x, -center_y]

def generate_body_color(index, total_bodies):
    """Generate a unique color for each body using HSV color space"""
    hue = index / total_bodies
    saturation = 0.8
    value = 1.0
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple(int(x * 255) for x in rgb)

def initialize_bodies():
    """Initialize bodies with unique colors and empty trails"""
    bodies = copy.deepcopy(Config['bodies'])
    for i, body in enumerate(bodies):
        if 'color' not in body:
            body['color'] = generate_body_color(i, len(bodies))
        body['trail'] = []
        # Scale radius by mass (optional)
        body['radius'] = max(5, int((body['mass'] ** 0.3) * 5))
    return bodies

def draw_trails(screen, bodies):
    """Draw motion trails for each body with smooth color gradient"""
    trail_surface = pygame.Surface((Config['width'], Config['height']), pygame.SRCALPHA)
    
    for body in bodies:
        if len(body['trail']) > 1 and is_visible(body['position'], body['radius']):
            screen_trail = [world_to_screen(pos) for pos in body['trail']]
            
            # Create segments for smooth gradient
            for i in range(len(screen_trail) - 1):
                # Calculate alpha based on position in trail
                alpha = int(255 * (i / len(screen_trail)) ** 1.5)  # Exponential fade
                color = (*body['color'], alpha)
                
                # Draw line segment with current alpha
                if i < len(screen_trail) - 1:
                    pygame.draw.line(trail_surface, color,
                                   screen_trail[i], screen_trail[i + 1], 
                                   max(1, int(3 * (i / len(screen_trail)))))  # Width fades too
    
    screen.blit(trail_surface, (0, 0))

def draw_cursor_radius(screen, mouse_pos):
    """Draw the cursor's radius of effect"""
    cursor_surface = pygame.Surface((Config['width'], Config['height']), pygame.SRCALPHA)
    radius = int(Config['cursor']['radius'] * Config['zoom'])
    
    # Draw outer circle (always visible)
    pygame.draw.circle(cursor_surface, (100, 100, 100, 50), mouse_pos, radius, 2)
    screen.blit(cursor_surface, (0, 0))

def apply_cursor_force(bodies, mouse_pos, attracting, repelling):
    """Apply force from cursor to bodies"""
    if not (attracting or repelling):
        return
    
    world_pos = screen_to_world(mouse_pos)
    cursor_surface = pygame.Surface((Config['width'], Config['height']), pygame.SRCALPHA)
    
    # Draw filled circle when attracting/repelling
    color = Config['cursor']['attract_color'] if attracting else Config['cursor']['repel_color']
    radius = int(Config['cursor']['radius'] * Config['zoom'])
    pygame.draw.circle(cursor_surface, color, mouse_pos, radius)
    screen.blit(cursor_surface, (0, 0))
    
    # Apply force to bodies
    for body in bodies:
        dx = world_pos[0] - body['position'][0]
        dy = world_pos[1] - body['position'][1]
        distance = max((dx**2 + dy**2)**0.5, 1.0)
        
        # Use world-space radius for force calculation
        world_radius = Config['cursor']['radius'] / Config['zoom']
        if distance < world_radius:
            falloff = (1 - (distance/world_radius)**2)
            # Scale force magnitude with zoom to maintain consistent feel
            force_magnitude = Config['cursor']['force_magnitude']
            if repelling:
                force_magnitude = -force_magnitude
                
            force_x = force_magnitude * dx / distance
            force_y = force_magnitude * dy / distance
            
            body['velocity'] = (
                body['velocity'][0] + force_x * Config['dt'] / body['mass'] * 0.5,
                body['velocity'][1] + force_y * Config['dt'] / body['mass'] * 0.5
            )

def draw_orbit_circles(screen):
    """Draw circular guidelines for orbital distances"""
    surface = pygame.Surface((Config['width'], Config['height']), pygame.SRCALPHA)
    center = world_to_screen(bodies[0]['position'])
    
    for r in range(100, 1000, 100):
        radius = int(r * Config['zoom'])
        pygame.draw.circle(surface, (50, 50, 50, 100), center, radius, 1)
        
        # Draw orbital velocity for this radius
        if Config['colors']['show_labels']:
            orbital_v = (Config['G'] * bodies[0]['mass'] / r) ** 0.5
            text = f"v={orbital_v:.1f}"
            font = pygame.font.Font(None, Config['colors']['label_size'])
            text_surface = font.render(text, True, (50, 50, 50))
            pos = (center[0] + radius, center[1])
            screen.blit(text_surface, pos)
    
    screen.blit(surface, (0, 0))

# Initialize bodies and simulation state
bodies = []
paused = False

# Load stable orbit parameters
try:
    with open('stable_orbit_params.json', 'r') as f:
        stable_params = json.load(f)
        Config['G'] = stable_params['G']
        Config['bodies'] = stable_params['bodies']
        bodies = initialize_bodies()  # Initialize with loaded bodies
except FileNotFoundError:
    print("No stable_orbit_params.json found. Starting with empty system.")
except json.JSONDecodeError:
    print("Error reading stable_orbit_params.json. Starting with empty system.")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset simulation
                bodies = copy.deepcopy(Config['bodies'])
                Config['zoom'] = 1.0
                Config['camera_offset'] = [0, 0]
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_RETURN:
                center_on_system(bodies)
            elif event.key == pygame.K_RIGHT:
                Config['prediction_steps'] += 100
            elif event.key == pygame.K_LEFT:
                Config['prediction_steps'] -= 100
            elif event.key == pygame.K_UP:
                Config['time_control']['speed'] = min(Config['time_control']['speed'] * 1.5, 
                                                    Config['time_control']['max_speed'])
            elif event.key == pygame.K_DOWN:
                Config['time_control']['speed'] = max(Config['time_control']['speed'] / 1.5, 
                                                    Config['time_control']['min_speed'])
            elif event.key == pygame.K_n:  # Add new planet at mouse position
                mouse_pos = pygame.mouse.get_pos()
                world_pos = screen_to_world(mouse_pos)
                new_planet = {
                    'name': f'Planet {len(bodies)}',
                    'mass': 1,
                    'radius': 10,
                    'position': world_pos,
                    'velocity': (0, 0),
                    'trail': [],
                    'color': generate_body_color(len(bodies), len(bodies) + 1)
                }
                bodies.append(new_planet)
        elif event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shift + Mouse wheel for mass
                # Find nearest planet (excluding star)
                pos = screen_to_world(pygame.mouse.get_pos())
                if len(bodies) > 1:  # Only if there are planets besides the star
                    nearest = min(bodies[1:], key=lambda b: ((b['position'][0] - pos[0])**2 + 
                                                           (b['position'][1] - pos[1])**2))
                    # Use y for vertical wheel and precise_y for trackpad/high precision wheel
                    scroll_up = event.y > 0 or (hasattr(event, 'precise_y') and event.precise_y > 0)
                    if scroll_up:
                        nearest['mass'] *= 1.1
                    else:
                        nearest['mass'] = max(0.1, nearest['mass'] * 0.9)
                    nearest['radius'] = max(5, int((nearest['mass'] ** 0.3) * 5))
            else:  # Regular mouse wheel for zoom
                # Get mouse position before zoom
                mouse_pos = pygame.mouse.get_pos()
                world_pos = screen_to_world(mouse_pos)
                
                # Update zoom
                old_zoom = Config['zoom']
                Config['zoom'] = max(Config['min_zoom'], 
                                   min(Config['max_zoom'], 
                                       Config['zoom'] * (1 + event.y * Config['zoom_speed'])))
                
                # Adjust offset to keep mouse position fixed
                screen_pos_after = world_to_screen(world_pos)
                dx = mouse_pos[0] - screen_pos_after[0]
                dy = mouse_pos[1] - screen_pos_after[1]
                Config['camera_offset'][0] += dx / Config['zoom']
                Config['camera_offset'][1] += dy / Config['zoom']
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # Middle mouse button
                drag_state['dragging'] = True
                drag_state['last_pos'] = pygame.mouse.get_pos()
            elif event.button == 3 and pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shift + Right click
                # Delete nearest planet (except star)
                if len(bodies) > 1:  # Only if there are planets to delete
                    pos = screen_to_world(pygame.mouse.get_pos())
                    nearest_idx = min(range(1, len(bodies)), 
                                    key=lambda i: ((bodies[i]['position'][0] - pos[0])**2 + 
                                                 (bodies[i]['position'][1] - pos[1])**2))
                    bodies.pop(nearest_idx)
            elif event.button == 1 and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Ctrl + Left click
                Config['launch_mode']['active'] = True
                Config['launch_mode']['start_pos'] = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle mouse button
                drag_state['dragging'] = False
            elif event.button == 1 and Config['launch_mode']['active']:
                end_pos = pygame.mouse.get_pos()
                start_world = screen_to_world(Config['launch_mode']['start_pos'])
                
                # Calculate velocity from drag distance
                dx = (end_pos[0] - Config['launch_mode']['start_pos'][0]) * 0.1
                dy = (end_pos[1] - Config['launch_mode']['start_pos'][1]) * 0.1
                
                new_planet = {
                    'name': f'Planet {len(bodies)}',
                    'mass': 1,
                    'radius': 10,
                    'position': start_world,
                    'velocity': (dx, dy),
                    'trail': [],
                    'color': generate_body_color(len(bodies), len(bodies) + 1)
                }
                bodies.append(new_planet)
                Config['launch_mode']['active'] = False
        elif event.type == pygame.MOUSEMOTION:
            if drag_state['dragging']:
                current_pos = pygame.mouse.get_pos()
                dx = current_pos[0] - drag_state['last_pos'][0]
                dy = current_pos[1] - drag_state['last_pos'][1]
                Config['camera_offset'][0] += dx / Config['zoom']
                Config['camera_offset'][1] += dy / Config['zoom']
                drag_state['last_pos'] = current_pos
    
    mods = pygame.key.get_mods()
    attracting = pygame.mouse.get_pressed()[0] and not mods  # Left button, no modifiers
    repelling = pygame.mouse.get_pressed()[2] and not mods   # Right button, no modifiers

    if not paused:
        # Draw cursor radius (always visible)
        draw_cursor_radius(screen, pygame.mouse.get_pos())
        
        # Update physics
        forces = []
        for i in range(len(bodies)):
            force = calculate_total_force(i, bodies)
            forces.append(force)
        
        # Update all bodies with their total forces
        for i, body in enumerate(bodies):
            update_body(body, forces[i])
        
        # Update trails
        update_trails(bodies)
    
    # Draw
    screen.fill(Config['colors']['background'])
    
    # Draw trails if enabled
    if Config['colors']['trails']:
        draw_trails(screen, bodies)
    
    # Draw prediction paths
    if not paused:
        predicted_positions = predict_path(bodies, 
                                        pygame.mouse.get_pos() if (attracting or repelling) else None,
                                        attracting, 
                                        repelling)
        prediction_surface = pygame.Surface((Config['width'], Config['height']), pygame.SRCALPHA)
        for i, positions in predicted_positions.items():
            if len(positions) > 1 and is_visible(bodies[i]['position'], bodies[i]['radius']):
                prediction_color = (*bodies[i]['color'], 100)
                pygame.draw.lines(prediction_surface, prediction_color, False, positions, 1)
        screen.blit(prediction_surface, (0, 0))
        
        # Apply cursor forces (moved force application here but keep drawing separate)
        apply_cursor_force(bodies, pygame.mouse.get_pos(), attracting, repelling)
    
    # Draw bodies and velocity vectors
    for body in bodies:
        if is_visible(body['position'], body['radius']):
            screen_pos = world_to_screen(body['position'])
            pygame.draw.circle(screen, body['color'],
                             screen_pos,
                             int(body['radius'] * Config['zoom']))
            draw_velocity_vector(body)
            
            # Draw labels only for visible bodies
            if Config['colors']['show_labels']:
                font = pygame.font.Font(None, Config['colors']['label_size'])
                label = f"{body['name']} (m={body['mass']})"
                text = font.render(label, True, body['color'])
                text_rect = text.get_rect(midtop=(screen_pos[0], 
                                                screen_pos[1] + body['radius'] * Config['zoom'] + 5))
                screen.blit(text, text_rect)
    
    if Config['launch_mode']['active']:
        start_pos = Config['launch_mode']['start_pos']
        end_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)
    
    pygame.display.flip()
    clock.tick(Config['fps'])
