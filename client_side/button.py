import pygame
from typing import Callable, Any, Optional
class Button:
    # Init Button object: x - Horizontal position, y - Vertical position, width - Button width, height - Button height,
    # font - text font, text - Button text, active_c - color when active, inactive_c - color when inactive,
    # action - function to preform when pressed, *args - action arguments, **kwargs - action keywords arguments
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, text: str, active_c: pygame.color.Color, inactive_c: pygame.color.Color , action: Callable = None, args: Any = None, kwargs: dict = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = inactive_c
        self.color_active = active_c
        self.color = self.color_inactive # Button color 
        self.font = font
        self.text = text
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.active = False # Button activation
    
    # Input: event - pygame event
    # Preform: Handeling event of the Button object
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN: # If mouse pressed 
            if self.rect.collidepoint(event.pos): # If pressed on Button
                self.color = self.color_active
                if self.action is not None: # If there is action to preform
                    if self.args is not None and self.kwargs is not None: # If both args and kwargs
                        return self.action(*self.args, **self.kwargs)
                    elif self.args is not None: # If only args
                        return self.action(*self.args)
                    elif self.kwargs is not None: # If only kwargs
                        return self.action(**self.kwargs)
                    else:
                        return self.action() # If no args and no kwargs
            else: # If pressed not on button
                self.color = self.color_inactive 
        return None
    
    # Input: Surface to show the Buttom on
    # Preform: Adding the Button on the surface
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect) # Drawing Button rect
        text_surface = self.font.render(self.text, True, pygame.Color('black')) # Render the text to a surface in black
        text_rect = text_surface.get_rect(center=self.rect.center) # Calculate the rect the text will be presented on
        surface.blit(text_surface, text_rect) # Adds the Button's text surface in the text rect on the original surface
