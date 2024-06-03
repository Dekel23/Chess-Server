import pygame

class Text:
    # Init Text object: x - Horizontal position, y - Vertical position, font - text font, 
    # text - text to present, color - text color
    def __init__(self, x: int, y: int, font: pygame.font.Font, text: str, color: pygame.color.Color):
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.text = text

    def set_text(self, text:str):
        self.text = text
    
    # Input: Surface to show the text on
    # Preform: Adding the text on the surface
    def draw(self, surface: pygame.Surface):
        text_surface = self.font.render(self.text, True, self.color) # Render the text to a surface
        text_rect = text_surface.get_rect(center=(self.x, self.y)) # Calculate the rect the text will be presented on
        surface.blit(text_surface, text_rect) # Adds the text surface in the text rect on the original surface
