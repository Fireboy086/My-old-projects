import os
import importlib.util

class LevelGroup:
    def __init__(self):
        self.levels = {}
        self.load_levels()
    
    def load_levels(self):
        """Load all level files from the Levels directory"""
        levels_dir = os.path.dirname(os.path.abspath(__file__))
        
        for filename in os.listdir(levels_dir):
            if filename.endswith('.py') and filename != 'Level_Group.py':
                level_name = filename[:-3]  # Remove .py extension
                level_path = os.path.join(levels_dir, filename)
                
                try:
                    # Load module dynamically
                    spec = importlib.util.spec_from_file_location(level_name, level_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Store level data
                    self.levels[level_name] = {
                        'map_tiles': getattr(module, 'map_tiles', self.get_empty_map()),
                        'car_start_pos': getattr(module, 'CAR_START_POS', (400, 300)),
                        'car_start_rotation': getattr(module, 'CAR_START_ROTATION', 0)
                    }
                except Exception as e:
                    print(f"Error loading level {level_name}: {e}")
    
    def get_empty_map(self):
        """Return an empty map template"""
        return [[0] * 20 for _ in range(16)]  # 20x16 empty map with walls around
    
    def save_level(self, name, map_tiles, car_pos, car_rotation):
        """Save level data to a new or existing file"""
        level_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{name}.py")
        
        with open(level_path, 'w') as file:
            file.write("# Level configuration\n\n")
            
            # Write map tiles
            file.write("map_tiles = [\n")
            for row in map_tiles:
                file.write(f"    {row},\n")
            file.write("]\n\n")
            
            # Write car settings
            file.write(f"CAR_START_POS = {car_pos}\n")
            file.write(f"CAR_START_ROTATION = {car_rotation}\n")
        
        # Reload levels after saving
        self.load_levels()
    
    def get_level_names(self):
        """Return list of available level names"""
        return sorted(self.levels.keys())
    
    def get_level_data(self, name):
        """Get data for a specific level"""
        if name not in self.levels:
            print(f"No level called '{name}' found. Would you like to create a new one? (y/n)")
            if input().lower() == 'y':
                self.create_new_level(name)
                return self.levels.get(name)
            return None
        return self.levels.get(name)
    
    def create_new_level(self, name):
        """Create a new empty level"""
        if name not in self.levels:
            self.save_level(name, self.get_empty_map(), (400, 300), 0)
            return True
        return False
