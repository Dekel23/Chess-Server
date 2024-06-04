import pygame

class InputBox:
    def __init__(self, y:int, x:int, height:int, width:int, font:pygame.font.Font, title:str) -> None:
        """
        Initialize an instance of InputBox class.

        Parameters:
        y (int): The y-coordinate of the top-left corner of the input box.
        x (int): The x-coordinate of the top-left corner of the input box.
        height (int): The height of the input box.
        width (int): The width of the input box.
        font (pygame.font.Font): The font to be used for rendering the text in the input box.
        title (str): The title of the input box.

        Returns:
        None
        """
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = font
        self.title = title
        self.text = ''
        self.color_inactive = (100, 100, 100)
        self.action_active = (200, 200, 200)
        self.active = False
        self.color = self.color_inactive
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handles mouse and keyboard events for the input box.

        Parameters:
        event (pygame.event.Event): The event to be handled.

        Returns:
        None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the input box's boundaries
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change the color of the input box based on its active state
            self.color = self.color_inactive if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN:
            # Check if the input box is active
            if self.active:
                # Handle backspace key
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Handle other keys, excluding return and question mark
                elif event.key!= pygame.K_RETURN and event.key!= pygame.K_QUESTION:
                    # Calculate the width of the new text
                    new_text_width = self.font.size(self.title + ':'+ self.text + event.unicode)[0]
                    # Check if the new text will fit within the input box
                    if new_text_width <= self.width - 10:
                        self.text += event.unicode
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the input box on the given surface.

        Parameters:
        surface (pygame.Surface): The surface on which to draw the input box.

        Returns:
        None
        """
        pygame.draw.rect(surface, self.color, self.rect, 2)
        box_surface = self.font.render(self.title + ':'+ self.text, True, self.color)
        surface.blit(box_surface, (self.rect.x + 5, self.rect.y + 5))
