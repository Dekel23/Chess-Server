import pygame
from typing import Callable

class Button:
    
    def __init__(self, x:int, y:int, width:int, height:int, font:pygame.font.Font, text:str,
                action:Callable = None, *args:object, **kwargs:dict) -> None:
        """
        Initialize a Button object.

        Parameters:
        y (int): The y-coordinate of the top-left corner of the button.
        x (int): The x-coordinate of the top-left corner of the button.
        height (int): The height of the button.
        width (int): The width of the button.
        font (pygame.font.Font): The font object to use for rendering the button text.
        text (str): The text to display on the button.
        action (Callable, optional): A function to call when the button is clicked. Defaults to None.
        *args: Additional positional arguments to pass to the action function.
        **kwargs: Additional keyword arguments to pass to the action function.

        Returns:
        None
        """
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        # Create the rect with the center at (x, y)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.font = font
        self.text = text
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.color_inactive = (100, 100, 100)
        self.action_active = (200, 200, 200)
        self.color = self.color_inactive
    
    def draw(self, surface:pygame.Surface) -> None:
        """
        Draw the button on the given surface.

        Parameters:
        surface (pygame.Surface): The surface on which to draw the button.

        Returns:
        None

        This method uses the Pygame library to draw a rectangle representing the button
        on the given surface. The button's color is determined by the 'color' attribute,
        and the text is rendered and centered within the button's boundaries.
        """
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event:pygame.event.Event) -> object:
        """
        Handle mouse events for the button.

        Parameters:
        event (pygame.event.Event): The event to handle.

        Returns:
        object: The result of the action function if the event is a mouse button down event and
        the mouse position is within the button's boundaries.

        This method checks if the given event is a mouse button down event.
        If it is, it checks if the mouse position is within the button's boundaries.
        If the mouse position is within the button's boundaries,it changes the button's color
        to indicate that it is active and calls the action function, if it exists.
        If the mouse position is not within the button's boundaries,
        it changes the button's color to indicate that it is inactive.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the button's boundaries
            if self.rect.collidepoint(event.pos):
                self.color = self.action_active
                # Call the action function if it exists with the appropriate argument
                if self.action is not None:
                    return self.action(*self.args, **self.kwargs)
            else:
                self.color = self.color_inactive        