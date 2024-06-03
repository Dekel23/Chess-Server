import pygame

class Input_Box:
    # Init Input_Box object: x - Horizontal position, y - Vertical position, width - Input_Box width, height - Input_Box height
    # font - text font, title - Input_Box title, active_c - color when active, inactive_c - color when inactive
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, title: str, inactice_c: pygame.color.Color, active_c: pygame.color.Color):
        self.init_width = width
        self.rect = pygame.Rect(x, y, width, height) # Creating Input_Box rect
        self.color_inactive = inactice_c
        self.color_active = active_c
        self.color = self.color_inactive # Input_Box color 
        self.font = font
        self.title = title
        self.text = '' # User text
        self.active = False # Input_Box activation
    
    # Input: event - pygame event
    # Preform: Handeling event of the Input_Box object
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN: # If mouse pressed 
            if self.rect.collidepoint(event.pos): # If pressed on Input_Box
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive # Color change based on activation
        elif event.type == pygame.KEYDOWN: # If key if pressed
            if self.active: # if the Input_Box is active
                if event.key == pygame.K_BACKSPACE: # if pressed backspace delete last char
                    self.text = self.text[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_QUESTION:
                    new_text_width = self.font.size(self.title + ': ' + self.text + event.unicode)[0] # calc new width based on the text in the Input_Box
                    if new_text_width <= self.init_width - 10: # if text width smaller than max_width
                        self.text += event.unicode # add to text the pressed key
    
    # Input: Surface to show the Input_Box on
    # Preform: Adding the Input_Box on the surface
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect, 2) # Drawing frame 
        box_surface = self.font.render(self.title + ': ' + self.text, True, self.color) # Render the text to a surface
        surface.blit(box_surface, (self.rect.x + 5, self.rect.y + 5)) # Adds the Input_Box surface in the rect's position on the original surface