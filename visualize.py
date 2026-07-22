import pygame
import os
from typing import Tuple


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
BUTTON_FONT_SIZE = 18
TEAL = (0, 128, 128)
PYTHON_BLUE = (55,118, 171)

BACKGROUND_COLOR = PYTHON_BLUE

FONT_PATH = "resources/superstar_memesbruh03.ttf"



class PyGameVisualizer:
    def __init__(self, screen_width=1400, screen_height=900):
        # initialize pygame
        pygame.init()

        # window setup
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Fly-in: Let the drones fly")

        # clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.Font(FONT_PATH, 48) # Big titles
        self.font_label = pygame.font.Font(FONT_PATH, 32) # Category labels
        self.font_text = pygame.font.Font(FONT_PATH, 24) # Map names

        # Discover maps from directory
        self.maps_by_category = self.discover_maps()
    
    def discover_maps(self) -> dict:
        """
        Scan maps/ directory and organize maps by category.

        Returns:
            Dict like: {"Easy": ["maps/easy/01_linear_path.txt", ...], ...}
        """
        maps_dict = {}
        categories = ["easy", "medium", "hard", "challenger"]
        maps_dir = "maps"

        for category in categories:
            category_path = os.path.join(maps_dir, category)
            maps_dict[category.capitalize()] = []
            
            # check if directory exist
            if os.path.isdir(category_path):
                # List all .txt files in this directory
                files = os.listdir(category_path)
                for file in sorted(files):
                    if file.endswith(".txt"):
                        full_path = os.path.join(category_path, file)
                        maps_dict[category.capitalize()].append(full_path)
        
        return maps_dict


    def screen_map_selection(self) -> str:
        """
        Display map selection screen with categories.
        User clicks on a map to select it.

        Returns:
            Path to selected map file (e.g., "maps/easy/01_linear_path.txt")
        """
        selected_map = None
        running = True

        while running and selected_map is None:
            #handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # check which map was selected
                    selected_map = self._check_map_click(mouse_pos)
            
            # draw the screen
            self._draw_map_selection_screen()
            
            pygame.display.flip()
            self.clock.tick(60)

        return selected_map
    

    def _draw_map_selection_screen(self):
        """Draw the map selection UI"""
        # Clear screen (black background)
        self.screen.fill(BACKGROUND_COLOR)

        # Draw title
        title = self.font_title.render("SELECT A MAP", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw categories and maps
        y_offset = 100
        for category, maps in self.maps_by_category.items():
            # Draw category label (e.g., "Easy")
            category_text = self.font_label.render(category, True, GREEN)
            self.screen.blit(category_text, (50, y_offset))
            y_offset += 40

            # Draw maps under this category
            for map_file in maps:
                map_name = os.path.basename(map_file)
                map_name = map_name.replace(".txt", "")  # Remove .txt

                map_text = self.font_text.render(f"  → {map_name}", True, WHITE)
                self.screen.blit(map_text, (70, y_offset))
                y_offset += 30

            y_offset += 20  # Space between categories
    

    def _check_map_click(self, mouse_pos) -> str | None:
        """
        Check if user clicked on a map.
        Returns map file path if clicked, None otherwise.
        """
        y_offset = 100
        for category, maps in self.maps_by_category.items():
            y_offset += 40  # Category label height

            for map_file in maps:
                # Create a rectangle around the map name
                map_name = os.path.basename(map_file).replace(".txt", "")
                rect = pygame.Rect(70, y_offset, 500, 30)

                # Check if click is inside this rectangle
                if rect.collidepoint(mouse_pos):
                    return map_file

                y_offset += 30

            y_offset += 20

        return None


    def run(self) -> str:
        """
        Start the visualizer and return selected map.

        Returns:
            Path to the selected map file
        """
        selected_map = self.screen_map_selection()
        pygame.quit()
        return selected_map


class Button:
    """
    Button class, a blueprint for simulation controls.
    In Simulation window, we implement Play/Pause/Stop buttons.
    """
    def __init__(self, x: float, y: float, label: str):
        self.x = x
        self.y = y
        self.label = label
    
    def draw_stop(self, screen):
        """Draw STOP button: Red rectangle with label below"""
        
        width, height = 80, 60

        #Draw red recatngle
        pygame.draw.rect(screen, RED, (self.x, self.y, width, height))
        
        #Draw text centred on button
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_image = font.render(self.label, True, WHITE)
        text_rect = text_image.get_rect(
            center=(self.x + width // 2, self.y + height + 15)
        )
        screen.blit(text_image, text_rect)

        #Store rect for click detection
        self.rect = pygame.Rect(self.x, self.y, width, height)


    def draw_pause(self, screen):
        """Draw PAUSE button: Orange circle with two vertical lines + label below"""
        radius = 25
        
        # Draw orange circle
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), radius)
        
        # Draw two vertical white lines
        line_width = 4
        line_height = 30
        gap = 8
        
        # Left line
        pygame.draw.line(screen, WHITE, 
                        (self.x - gap - line_width, self.y - line_height // 2),
                        (self.x - gap - line_width, self.y + line_height // 2),
                        line_width)
        
        # Right line
        pygame.draw.line(screen, WHITE,
                        (self.x + gap + line_width, self.y - line_height // 2),
                        (self.x + gap + line_width, self.y + line_height // 2),
                        line_width)
        
        # Draw label BELOW button
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_image = font.render(self.label, True, WHITE)
        text_rect = text_image.get_rect(center=(self.x, self.y + radius + 15))
        screen.blit(text_image, text_rect)
        
        # Store circle center and radius for click detection
        self.circle_center = (self.x, self.y)
        self.circle_radius = radius
    

    def draw_play(self, screen):
        """Draw PLAY button: Green triangle with label below"""
        # Triangle points: base at bottom, point at right
        radius = 25
        points = [
            (self.x, self.y - radius),           # top
            (self.x, self.y + radius),           # bottom left
            (self.x + radius * 1.5, self.y)      # right (the point)
        ]
        
        # Draw green triangle
        pygame.draw.polygon(screen, GREEN, points)
        
        # Draw label BELOW button
        font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        text_image = font.render(self.label, True, WHITE)
        text_rect = text_image.get_rect(center=(self.x + radius * 0.75, self.y + radius + 15))
        screen.blit(text_image, text_rect)
        
        # Store circle rect for click detection
        self.circle_center = (self.x + radius * 0.75, self.y)
        self.circle_radius = radius


    def is_stop_clicked(self, mouse_pos) -> bool:
        """check if STOP (rectangle) button was clicked"""
        return self.rect.collidepoint(mouse_pos)
    
    def is_pause_clicked(self, mouse_pos) -> bool:
        dist = ((mouse_pos[0] - self.circle_center[0])**2 +
                (mouse_pos[1] - self.circle_center[1])**2)**0.5
        return dist < self.circle_radius
    
    def is_play_clicked(self, mouse_pos) -> bool:
        dist = ((mouse_pos[0] - self.circle_center[0])**2 +
                (mouse_pos[1] - self.circle_center[1])**2)**0.5
        return dist < self.circle_radius


