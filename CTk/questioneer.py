import customtkinter as ctk
import random
from tkinter import Toplevel
import os
from PIL import Image, ImageTk
import urllib.request
import time
import threading
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SurveyApp:
    def __init__(self):
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Social Survey")
        self.root.geometry("400x300")
        self.root.resizable(True, True)  # Make window resizable
        self.root.minsize(300, 250)  # Set minimum window size
        
        # Set custom color scheme
        self.primary_color = "#3B3B3B"        # Dark gray for backgrounds
        self.accent_color = "#6C63FF"         # Purple accent
        self.text_color = "#F0F0F0"           # Light text color
        self.logika_purple = "#8A2BE2"        # Purple for Logika text
        self.logika_outline = "#D8BFD8"       # Light purple for outline
        
        # Configure window appearance
        self.root.configure(fg_color=self.primary_color)
        
        # Current window size parameters
        self.current_width = 400
        self.current_height = 300
        self.window_growth_step = 10  # Pixels to grow each time
        self.max_width = self.root.winfo_screenwidth() - 100  # Maximum width (with margin)
        self.max_height = self.root.winfo_screenheight() - 100  # Maximum height (with margin)
        
        # Flag to track if max size was reached
        self.reached_max_size = False
        
        # Get screen dimensions for later use
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        logger.debug(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
        
        # Center the window on screen
        self.center_window(self.root)
        
        # Set window to be topmost
        self.root.attributes('-topmost', True)
        
        # Create header frame
        self.header_frame = ctk.CTkFrame(self.root, fg_color=self.primary_color, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(10, 0))
        
        # Create title label
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Student Survey",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        )
        self.title_label.pack(pady=(5, 0))
        
        # Create question label with highlighted "Logika School" text
        question_text = "Do you like studying at"
        self.question_label1 = ctk.CTkLabel(
            self.root, 
            text=question_text,
            font=("Arial", 16),
            text_color=self.text_color
        )
        self.question_label1.pack(pady=(20, 0))
        
        # Create Logika School label with custom styling
        self.logika_label = ctk.CTkLabel(
            self.root,
            text="Logika School",
            font=("Arial", 18, "bold"),
            text_color=self.logika_purple
        )
        self.logika_label.pack(pady=(0, 5))
        
        # Create button frame
        self.button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.button_frame.pack(pady=10, fill="both", expand=True)
        
        # Create Yes button with improved styling
        self.yes_button = ctk.CTkButton(
            self.button_frame,
            text="Yes",
            command=None,  # Remove direct command binding
            width=100,
            height=40,
            fg_color=self.accent_color,
            hover_color="#5851D8",  # Slightly darker shade for hover
            corner_radius=10,
            font=("Arial", 14, "bold")
        )
        self.yes_button.place(relx=0.3, rely=0.5, anchor="center")
        
        # Add proper click handling
        self.yes_button.bind("<ButtonPress-1>", self.on_button_press)
        self.yes_button.bind("<ButtonRelease-1>", self.on_yes_release)
        self.dragging = False
        
        # Flags to prevent multiple activations
        self.no_button_clicked = False
        self.explosion_in_progress = False
        
        # Create No button with improved styling
        self.no_button = ctk.CTkButton(
            self.button_frame,
            text="No",
            width=100,
            height=40,
            command=None,  # Remove direct command binding
            fg_color="#FF5252",  # Red color for No button
            hover_color="#D32F2F",  # Darker red for hover
            corner_radius=10,
            font=("Arial", 14, "bold")
        )
        self.no_button.place(relx=0.7, rely=0.5, anchor="center")
        
        # Add proper click handling for No button
        self.no_button.bind("<ButtonPress-1>", self.on_button_press)
        self.no_button.bind("<ButtonRelease-1>", self.on_no_release)
        
        # Bind mouse hover event to No button
        self.no_button.bind("<Enter>", self.move_no_button)
        
        # Initialize explosion path but don't download yet
        self.explosion_path = None
        self.prepare_explosion_path()
        
        # Reference to current response window
        self.current_response_window = None
        
    def prepare_explosion_path(self):
        """Set up the path for the explosion GIF, but don't download it yet"""
        # Get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.explosion_path = os.path.join(script_dir, "explosion.gif")
        logger.debug(f"Explosion path prepared: {self.explosion_path}")
    
    def no_button_clicked_handler(self):
        """Handler for No button click to prevent multiple activations"""
        if not self.no_button_clicked:
            self.no_button_clicked = True
            # Disable the button to prevent further clicks
            self.no_button.configure(state="disabled")
            # Remove the hover event
            self.no_button.unbind("<Enter>")
            # Call the actual handler (user actually clicked the button)
            self.WOW_noWasActuallyClicked(button_pressed=True)
    
    def expand_window(self):
        """Expand the window by a small amount and re-center it"""
        # Increase current window dimensions
        self.current_width = min(self.current_width + self.window_growth_step, self.max_width)
        self.current_height = min(self.current_height + self.window_growth_step, self.max_height)
        
        # Apply new dimensions
        new_geometry = f"{self.current_width}x{self.current_height}"
        logger.debug(f"Expanding window to {new_geometry}")
        self.root.geometry(new_geometry)
        
        # Re-center the window
        self.center_window(self.root)
        
        # Check if we've reached maximum size (both width and height are at max)
        if (not self.reached_max_size and 
            self.current_width >= self.max_width and 
            self.current_height >= self.max_height):
            self.reached_max_size = True
            logger.debug("Maximum window size reached, triggering 'No' button action")
            
            # Disable the No button
            self.no_button.configure(state="disabled")
            self.no_button.unbind("<Enter>")
            
            # Call the No button action but with button_pressed=False
            self.WOW_noWasActuallyClicked(button_pressed=False)
    
    def download_explosion_gif(self):
        """Download the explosion GIF and then show it"""
        # Check if we're already processing an explosion
        if self.explosion_in_progress:
            logger.debug("Explosion already in progress, ignoring duplicate call")
            return
            
        self.explosion_in_progress = True
        logger.debug("Starting download_explosion_gif process")
        
        if os.path.exists(self.explosion_path):
            logger.debug(f"Explosion GIF already exists: {self.explosion_path}")
            # File already exists, show explosion immediately
            self.show_explosion()
            return
                
        logger.debug("Starting explosion GIF download...")
        try:
            # Source: Explosion GIF
            url = "https://media.tenor.com/DqOx5At4J4cAAAAj/explosion.gif"
            urllib.request.urlretrieve(url, self.explosion_path)
            logger.debug(f"Downloaded explosion GIF to {self.explosion_path}")
            
            # Verify the file exists and has content
            if os.path.exists(self.explosion_path):
                size = os.path.getsize(self.explosion_path)
                logger.debug(f"GIF size: {size} bytes")
                if size == 0:
                    logger.warning("GIF file size is 0 bytes")
            else:
                logger.error("GIF still doesn't exist after download attempt")
            
            # Show explosion after download completes
            self.show_explosion()
        except Exception as e:
            logger.error(f"Error downloading explosion GIF: {e}")
            self.explosion_path = None
            self.explosion_in_progress = False
            # Just destroy windows if download failed
            self.root.after(1000, self.destroy_all_windows)
        
    def yes_clicked(self):
        # Create a new window for the positive response
        response_window = ctk.CTkToplevel(self.root)
        response_window.title("Thank you!")
        response_window.geometry("300x150")
        response_window.resizable(True, True)  # Make response window resizable
        response_window.minsize(300, 150)  # Set minimum size
        response_window.configure(fg_color=self.primary_color)
        
        # Center the window
        self.center_window(response_window)
        
        # Set window to be topmost
        response_window.attributes('-topmost', True)
        # Force focus
        response_window.focus_force()
        
        # Add decorative header
        header_frame = ctk.CTkFrame(response_window, fg_color=self.accent_color, height=40, corner_radius=0)
        header_frame.pack(fill="x")
        header_label = ctk.CTkLabel(
            header_frame,
            text="THANK YOU",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        header_label.pack(pady=5)
        
        # Add message with improved styling
        message = ctk.CTkLabel(
            response_window,
            text="Very nice to hear!!!",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        )
        message.pack(pady=30, expand=True)
        
        # Add decorative footer
        footer_frame = ctk.CTkFrame(response_window, fg_color=self.accent_color, height=10, corner_radius=0)
        footer_frame.pack(side="bottom", fill="x")
    
    def on_button_press(self, event):
        """Handle mouse button press"""
        self.dragging = False
        
    def on_yes_release(self, event):
        """Handle Yes button release"""
        if not self.dragging:
            self.yes_clicked()
            
    def on_no_release(self, event):
        """Handle No button release"""
        if not self.dragging and not self.no_button_clicked:
            self.no_button_clicked_handler()
            
    def move_no_button(self, event):
        """Move the No button to a random position when mouse hovers over it"""
        # Set dragging flag when mouse moves
        self.dragging = True
        
        # Only move if not clicked yet
        if not self.no_button_clicked:
            # Calculate safe zones using relative positioning
            # Safety margins: 10% from each edge
            margin = 0.1
            
            # Generate random position within safe area (between margin and 1-margin)
            new_x = random.uniform(margin, 0.9)
            new_y = random.uniform(margin, 0.9)
            
            # Move button to new position using relative coordinates
            self.no_button.place(relx=new_x, rely=new_y, anchor="center")
            
            # Expand the window by a small amount
            self.expand_window()
        
    def WOW_noWasActuallyClicked(self, button_pressed=True):
        """Handle the No button click event"""
        # Create a new window for the negative response
        response_window = ctk.CTkToplevel(self.root)
        self.current_response_window = response_window
        response_window.title("Feedback")
        response_window.geometry("400x300")
        response_window.configure(fg_color="#2C2C2C")  # Darker background for contrast
        self.center_window(response_window)
        response_window.attributes('-topmost', True)
        
        # Add a decorative header
        header_frame = ctk.CTkFrame(response_window, fg_color="#FF5252", height=40, corner_radius=0)
        header_frame.pack(fill="x")
        header_label = ctk.CTkLabel(
            header_frame,
            text="FEEDBACK RECEIVED",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        header_label.pack(pady=5)
        
        # If the button wasn't pressed (window got too big), show "no you did not press it" message
        if not button_pressed:
            not_pressed_label = ctk.CTkLabel(
                response_window,
                text="no you did not press it",
                font=("Arial", 14, "bold"),
                text_color="white",
                fg_color="#D32F2F",
                corner_radius=8,
                width=250,
                height=30
            )
            not_pressed_label.pack(pady=(20, 5))
        
        messages = {
            "FUCK YOU": 10,
            "WHY?!": 9,
            "TRASH": 9,
            "NOPE": 8,
            "TERRIBLE": 8,
            "AWFUL": 8,
            "SERIOUSLY?": 7,
            "USELESS": 7,
            "GARBAGE": 7,
            "HELL NO": 7,
            "GO AWAY": 6,
            "PATHETIC": 6,
            "JOKE": 6,
            "BROKEN": 6,
            "SUCKS TO SUCK": 6,
            "IDIOT": 5,
            "FAIL": 5,
            "DUMB": 5,
            "CRAP": 5,
            "BULLSHIT": 5,
            "UGH": 5,
            "HORRIBLE": 4,
            "MORON": 4,
            "STUPID": 4,
            "NOT WORKING": 4,
            "WASTE": 4,
            "FOOL": 3,
            "ABSURD": 3,
            "REALLY?": 3,
            "BAD JOKE": 3,
            "NOT COOL": 3,
            "RIDICULOUS": 3,
            "LAME": 3,
            "DISASTER": 3,
            "WORTHLESS": 2,
            "HATE THIS": 2,
            "NEVER AGAIN": 2,
            "DISGUSTING": 2,
            "GTFO": 2,
            "MEH": 2,
            "SHAMEFUL": 2,
            "DESPICABLE": 1,
            "NONSENSE": 1,
            "IDIOTIC": 1,
            "SCAM": 1,
            "INFURIATING": 1,
            "ATROCIOUS": 1,
            "FRUSTRATING": 1,
            "DISAPPOINTING": 1,
            "UNACCEPTABLE": 1
        }
                
        # Choose the message text
        message_text = self.weighted_choice(messages)

        # Create a fitting label instead of fixed font size
        message = self.create_fitting_label(response_window, message_text)
        message.pack(pady=30, expand=True)
        
        # Add a loading indicator
        loading_frame = ctk.CTkFrame(
            response_window,
            fg_color="#333333",
            corner_radius=10
        )
        loading_frame.pack(pady=10, padx=20, fill="x")
        
        loading_label = ctk.CTkLabel(
            loading_frame,
            text="Preparing PERSONAL SURPRISE...",
            font=("Arial", 13, "bold"),
            text_color="#FFD700"  # Gold color for emphasis
        )
        loading_label.pack(pady=10, padx=5)
        
        logger.debug("'No' button clicked, scheduling explosion GIF download...")
        
        # Schedule download and explosion after 1 second
        # Use lambda to avoid passing arguments incorrectly
        self.root.after(1000, lambda: self.download_explosion_gif())
    
    def weighted_choice(self, messages_dict):
        total = sum(weight for weight in messages_dict.values())
        r = random.uniform(0, total)
        cumulative_weight = 0
        for message, weight in messages_dict.items():
            cumulative_weight += weight
            if r <= cumulative_weight:
                return message
        return list(messages_dict.keys())[0]  # Fallback
    
    def show_explosion(self):
        """Show explosion GIF and then destroy all windows"""
        logger.debug(f"Showing explosion from {self.explosion_path}")
        logger.debug(f"File exists: {os.path.exists(self.explosion_path) if self.explosion_path else 'N/A'}")
        
        if self.explosion_path and os.path.exists(self.explosion_path):
            # Create explosion window
            explosion_window = ctk.CTkToplevel()
            explosion_window.title("")
            
            # Make window borderless and full screen
            explosion_window.overrideredirect(True)  # Remove window borders/decorations
            fullscreen_geometry = f"{self.screen_width}x{self.screen_height}+0+0"
            explosion_window.geometry(fullscreen_geometry)
            logger.debug(f"Setting explosion window to fullscreen: {fullscreen_geometry}")
            
            # CRITICAL: Force the window to be on top of EVERYTHING
            # Different approaches for different platforms
            explosion_window.attributes('-topmost', 1)  # Set extreme topmost priority
            explosion_window.update()  # Force update to apply attributes
            
            # Additional platform-specific settings if needed
            if sys.platform == "darwin":  # macOS
                try:
                    # Try to use NSWindow's highest level if available
                    explosion_window.attributes('-fullscreen', True)
                    explosion_window.update()
                except:
                    pass
            
            try:
                # Load GIF with PIL
                logger.debug("Loading GIF with PIL")
                explosion_gif = Image.open(self.explosion_path)
                logger.debug(f"GIF format: {explosion_gif.format}, size: {explosion_gif.size}")
                
                # Extract all frames
                all_frames = []
                try:
                    # Get total frame count
                    if hasattr(explosion_gif, 'n_frames'):
                        total_frames = explosion_gif.n_frames
                        logger.debug(f"GIF has {total_frames} frames total")
                        
                        # Extract all frames first
                        for i in range(total_frames):
                            explosion_gif.seek(i)
                            frame = explosion_gif.copy()
                            all_frames.append(frame)
                        
                        # Rearrange frames: move first 8 frames to the end
                        rearranged_frames = []
                        
                        # If we have 17 frames total, take frames 9-17 first
                        if total_frames == 17:
                            logger.debug("Rearranging frames: moving first 8 frames to the end")
                            # Add frames 9-17 first (indices 8-16)
                            for i in range(8, 17):
                                rearranged_frames.append(all_frames[i])
                            
                            # Then add frames 1-8 (indices 0-7)
                            for i in range(8):
                                rearranged_frames.append(all_frames[i])
                        else:
                            # If we don't have exactly 17 frames, just use the original order
                            logger.debug(f"Not exactly 17 frames, using original order ({total_frames} frames)")
                            rearranged_frames = all_frames
                        
                        # Convert to CTkImage
                        frames = []
                        image_size = (self.screen_width - 100, self.screen_height - 100)
                        for frame in rearranged_frames:
                            ctk_frame = ctk.CTkImage(light_image=frame, size=image_size)
                            frames.append(ctk_frame)
                    else:
                        # Not an animated GIF, use as single frame
                        logger.debug("Not an animated GIF, using single frame")
                        image_size = (self.screen_width - 100, self.screen_height - 100)
                        frame = ctk.CTkImage(light_image=explosion_gif, size=image_size)
                        frames = [frame]
                    
                    # Create label for animation with black background
                    explosion_window.configure(fg_color="black")
                    explosion_label = ctk.CTkLabel(explosion_window, text="", fg_color="black")
                    explosion_label.pack(expand=True, fill="both")
                    
                    # Display frames with delay - NO REPEATING
                    def animate_explosion(frame_index=0):
                        if frame_index < len(frames):
                            # Ensure window stays on top
                            explosion_window.attributes('-topmost', 1)
                            explosion_window.update()
                            
                            # Update image
                            logger.debug(f"Showing frame {frame_index}/{len(frames)}")
                            explosion_label.configure(image=frames[frame_index])
                            explosion_window.after(40, animate_explosion, frame_index + 1)
                        else:
                            # Reached the end of the animation - only play once
                            logger.debug("Animation complete, destroying windows")
                            # Destroy all windows after animation completes
                            self.root.after(500, lambda: self.delete_gif_and_destroy())
                    
                    # Start animation
                    logger.debug("Starting animation")
                    # Force window to top one more time before starting animation
                    explosion_window.lift()
                    explosion_window.attributes('-topmost', 1)
                    explosion_window.update()
                    
                    animate_explosion()
                    
                except Exception as e:
                    logger.error(f"Error animating GIF: {e}")
                    # Fallback to static image
                    static_frame = explosion_gif.copy()
                    image_size = (self.screen_width - 100, self.screen_height - 100)
                    static_frame = ctk.CTkImage(light_image=static_frame, size=image_size)
                    explosion_label = ctk.CTkLabel(explosion_window, image=static_frame, text="")
                    explosion_label.pack(expand=True, fill="both")
                    
                    # Destroy all windows after 2 seconds
                    logger.debug("Using static image fallback, destroying in 2 seconds")
                    self.root.after(2000, lambda: self.delete_gif_and_destroy())
            
            except Exception as e:
                logger.error(f"Error showing explosion: {e}")
                self.delete_gif_and_destroy()
        else:
            # No GIF available, destroy windows directly
            logger.debug("GIF not available, destroying windows directly")
            self.root.after(1000, self.destroy_all_windows)
    
    def delete_gif_and_destroy(self):
        """Delete the explosion GIF file and then destroy all windows"""
        # Try to delete the GIF file
        if self.explosion_path and os.path.exists(self.explosion_path):
            try:
                logger.debug(f"Attempting to delete GIF file: {self.explosion_path}")
                os.remove(self.explosion_path)
                logger.debug("GIF file deleted successfully")
            except Exception as e:
                logger.error(f"Error deleting GIF file: {e}")
        
        # Destroy all windows
        self.destroy_all_windows()
    
    def destroy_all_windows(self):
        """Destroy all application windows"""
        logger.debug("Destroying all windows")
        # Reset explosion flag
        self.explosion_in_progress = False
        self.no_button_clicked = False
        
        for window in self.root.winfo_children():
            if isinstance(window, Toplevel):
                window.destroy()
        self.root.destroy()
    
    def center_window(self, window):
        """Center a window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_fitting_label(self, parent, text, max_font_size=100, min_font_size=12):
        # Create a temporary label to measure text
        temp_label = ctk.CTkLabel(parent, text=text, font=("Arial", max_font_size, "bold"))
        
        # Start with maximum font size
        font_size = max_font_size
        
        # Get parent width with some padding
        available_width = parent.winfo_width() - 40  # 20px padding on each side
        
        # If parent width isn't available yet, estimate based on geometry
        if available_width <= 0:
            width_str = parent.geometry().split('+')[0].split('x')[0]
            available_width = int(width_str) - 40 if width_str else 300
        
        # Reduce font size until it fits
        while font_size > min_font_size:
            temp_label.configure(font=("Arial", font_size, "bold"))
            temp_label.update_idletasks()
            text_width = temp_label.winfo_reqwidth()
            
            if text_width <= available_width:
                break
            
            font_size -= 2
        
        # Create a stylish frame with gradient-like appearance
        frame = ctk.CTkFrame(
            parent,
            fg_color="#2D2D2D",  # Dark background
            corner_radius=15,
            border_width=2,
            border_color="#FF3B30"  # Red border
        )
        
        # Create the actual label with the calculated font size and modern styling
        actual_label = ctk.CTkLabel(
            frame,
            text=text,
            font=("Arial", font_size, "bold"),
            text_color="#FF3B30",  # Vibrant red color for text
            padx=20,
            pady=15
        )
        actual_label.pack(padx=10, pady=10)
        
        # Destroy the temporary label
        temp_label.destroy()
        
        # Return the frame containing the label
        return frame

if __name__ == "__main__":
    logger.debug(f"Starting application from {os.path.abspath(__file__)}")
    app = SurveyApp()
    app.root.mainloop()
