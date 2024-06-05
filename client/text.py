import pygame

class Text:
    def __init__(self, y:int, x:int, font:pygame.font.Font, text:str, color:pygame.color.Color):
        """
        Initialize a Text object.

        Parameters:
        y (int): The y-coordinate of the text on the screen.
        x (int): The x-coordinate of the text on the screen.
        font (pygame.font.Font): The font object to use for rendering the text.
        text (str): The text to be displayed.
        color (pygame.color.Color): The color of the text.

        Returns:
        None
        """
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.color = color
    
    def set_text(self, text:str) -> None:
        """
        Set the text of the Text object.

        Parameters:
        text (str): The new text to be displayed.

        Returns:
        None
        """
        self.text = text
    
    def set_color(self, color:pygame.color.Color) -> None:
        """
        Set the color of the Text object.
        
        Parameters:
        color (pygame.color.Color): The new color of the text.
        
        Returns:
        None
        """
        self.color = color
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the text onto the given surface.

        Parameters:
        surface (pygame.Surface): The surface on which to draw the text.

        Returns:
        None

        This method renders the text into a surface and blits it onto the given surface.
        The text is centered at the coordinates (self.x, self.y) on the surface.
        """
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)