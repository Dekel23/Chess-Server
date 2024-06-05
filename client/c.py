import time
from button import Button
from input_box import InputBox
from text import Text

import pygame
import socket
import os

def send(*data: str) -> str:
    """
    This function sends a message to the server using the established socket connection.

    Parameters:
    *data (str): Variable length argument list of strings to be sent as a single message.

    Returns:
    str: Returns a string representation of the error if any occurred during the sending process.
         Returns an empty string if the message was sent successfully.

    Raises:
    socket.error: If there is an error while sending the message.
    """
    try:
        message = SEPERATOR.join(data)  # Join the data into a single string separated by seperator
        CONN.sendall(message.encode(FORMAT))  # Encode the message and send it to the server
    except socket.error as e:
        return str(e)  # Return the error message if any occurred

def recieve() -> str:
    """
    This function receives a message from the server using the established socket connection.

    Parameters:
    None

    Returns:
    str: Returns a list of strings separated by the seperator if the message was received successfully.
         Returns a string representation of the error if any occurred during the receiving process.

    Raises:
    socket.error: If there is an error while receiving the message.

    Note:
    The received message is stripped of leading and trailing seperators and split into a list of strings.
    """
    try:
        message = CONN.recv(MAX_LENGTH).decode(FORMAT)  # Receive the message from the server
        return message.strip(SEPERATOR + " ").split(SEPERATOR)  # Return the message as a list of strings separated by seperator
    except socket.error as e:
        return str(e)  # Return the error message if any occurred

def create_image_dictionary(directory: str) -> dict:
    """
    This function creates a dictionary of images from a given directory.

    Parameters:
    directory (str): The path to the directory containing the image files.

    Returns:
    dict: A dictionary where the keys are the filenames (without extensions) and the values are the corresponding pygame.Surface objects.

    Note:
    The function only loads.png files from the directory and its subdirectories.
    The images are scaled to the specified block size.
    If there is an error loading an image, the function logs the error and continues with the next image.
    """
    dict = {}  # Initialize an empty dictionary to store the images

    if not os.path.exists(directory): # If the directory does not exist
        print(f"Error: Directory '{directory}' does not exist.")
        return dict

    for dir in os.listdir(directory):  # Iterate over the files in the directory
        dir_path = os.path.join(directory, dir)  # Get the full path of the current directory

        if not os.path.isdir(dir_path):  # Skip if the current item is not a directory
            continue

        for file in os.listdir(dir_path):  # Iterate over the files in the current directory
            file_path = os.path.join(dir_path, file)  # Get the full path of the current file

            if not (os.path.isfile(file_path) and file.endswith(".png")):  # Skip if the current file is not a.png file
                continue

            try:
                dict[file.split('.')[0]] = pygame.image.load(os.path.join(dir_path, file))  # Load the image
                dict[file.split('.')[0]] = pygame.transform.scale(dict[file.split('.')[0]], (BLOCK_SIZE, BLOCK_SIZE))  # Scale the image
            except pygame.error:
                print(f"Error loading image: {file_path}")  # Log the error and continue with the next image

    return dict  # Return the dictionary of images

# def out_of_bounds(x: int, y: int) -> bool:   
#     """
#     This function checks if a given position is out of bounds of the grid.

#     Parameters:
#     x (int): The x-coordinate of the position to check.
#     y (int): The y-coordinate of the position to check.

#     Returns:
#     bool: True if the position is out of bounds, False otherwise.

#     Note:
#     The grid is defined by the constants GRID_COLS and GRID_ROWS.
#     """
#     return x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS

# Socket communication's constants
HOST = '192.168.1.214'
PORT = 5000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_LENGTH = 1024

# Start connection to the server
CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONN.connect(ADDR)
SEPERATOR = CONN.recv(MAX_LENGTH).decode(FORMAT)

# Reciving application's constants
[EXIST_ERROR, NOT_EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_MESSAGE,
SIGNUP_MESSAGE, GRID_ROWS, GRID_COLS, BLOCK_SIZE, WHITE_SQUARE,
BLACK_SQUARE, PICKED_SQUARE, EATING_SQUARE, MOVING_SQUARE] = recieve()
GRID_ROWS = eval(GRID_ROWS)
GRID_COLS = eval(GRID_COLS)
BLOCK_SIZE = eval(BLOCK_SIZE)
WHITE_SQUARE = eval(WHITE_SQUARE)
BLACK_SQUARE = eval(BLACK_SQUARE)
PICKED_SQUARE = eval(PICKED_SQUARE)
EATING_SQUARE = eval(EATING_SQUARE)
MOVING_SQUARE = eval(MOVING_SQUARE)

# Other application's constants
GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE
GRID_WIDTH = GRID_COLS * BLOCK_SIZE
PLAYES_HEIGHT = 100
EXTRA_WIDTH = 200
SURFACE_WIDTH = GRID_WIDTH + EXTRA_WIDTH
SURFACE_HEIGHT = GRID_HEIGHT + 2 * PLAYES_HEIGHT

# Initialize the pygame library and application objects
pygame.init()
FONT = pygame.font.Font(None, 24)

# Initialize the image dictionary
IMAGE_DICT = create_image_dictionary("./client/images")

class Client:
    def __init__(self) -> None:
        """
        Initializes a new instance of the Client class.

        Parameters:
        None

        Returns:
        None

        Attributes:
        page (str): The current page of the application. Default is "signin".
        run_app (bool): A flag indicating whether the application should continue running. Default is True.
        surface (pygame.Surface): The surface object used for rendering the application.
        """
        self.page = "signin"
        self.run_app = True
        self.surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    
    def close_conn(self) -> None:
        """
        This function sends a "close connection" message to the server and quits the pygame library.

        Parameters:
        None

        Returns:
        None: This function does not return any value. It modifies the attributes of the Client class instance.

        Note:
        This function is called when the user wants to close the connection and quit the application.
        It sends a "close connection" message to the server using the send() function and then quits the pygame library.
        After calling this function, the 'run_app' attribute of the Client class instance is set to False, indicating that the application should be closed.

        Raises:
        pygame.error: If there is an error while quitting the pygame library.
        """
        send("close connection")  # Send a "close connection" message to the server
        pygame.quit()  # Quit the pygame library
        self.run_app = False  # Set 'run_app' to False to indicate that the application should be closed

    def signin_page(self) -> None:
        """
        This function handles the signin page of the application.
        It displays the signin form, handles user input, and communicates with the server.

        Parameters:
        self (Client): The instance of the Client class.

        Returns:
        None: This function does not return any value. It modifies the attributes of the Client class instance.
        """

        def try_signin(name: str, password: str, message: Text) -> bool:
            """
            This function attempts to sign in the user with the given name and password.
            It sends a "Sign in" message to the server along with the user's credentials.
            It handles the server's response and updates the signin page accordingly.

            Parameters:
            name (str): The name of the user trying to sign in.
            password (str): The password of the user trying to sign in.
            message (Text): The Text object used to display error messages.

            Returns:
            bool: True if the signin was successful, False otherwise.
            """
            # Check if either name or password is empty
            if name == "" or password == "":
                # Set error message and color if any field is empty
                message.set_text(MISSING_ERROR)
                message.set_color(pygame.Color('red'))
                return False
            
            # Check if password is shorter than 8 characters
            if len(password) < 8:
                # Set error message and color if password is too short
                message.set_text(SHORT_ERROR)
                message.set_color(pygame.Color('red'))
                return False
            
            # Send signin request to the server
            send("Sign in", name, password)
            # Receive server response
            result = recieve()[0]
            
            # If signin is successful
            if result == SIGNIN_MESSAGE:
                # Change page to menu and set success message and color
                self.page = "menu"
                message.set_text(SIGNIN_MESSAGE)
                message.set_color(pygame.Color('green'))
                return True
            
            # If user does not exist
            if result == NOT_EXIST_ERROR:
                # Set error message and color
                message.set_text(NOT_EXIST_ERROR)
                message.set_color(pygame.Color('red'))
                return False

        def signin_to_signup() -> bool:
            """
            This function changes the current page to the signup page.
            It sends a "Sign up" message to the server.

            Parameters:
            None

            Returns:
            None: This function does not return any value. It modifies the attributes of the Client class instance.
            """
            # Change page to signup
            self.page = "signup"
            # Send signup request to the server
            send("Sign up")
            return True

        # Create input boxes for username and password
        name_box = InputBox(SURFACE_WIDTH/2, SURFACE_HEIGHT/2-100, 200, 25, FONT, "Name")
        password_box = InputBox(SURFACE_WIDTH/2, SURFACE_HEIGHT/2-50, 200, 25, FONT, "Password")
        # Create a Text object for displaying messages
        message = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, FONT, "", pygame.Color('red'))
        # Create buttons for signin and signup
        signin_button = Button(SURFACE_WIDTH/2-100, SURFACE_HEIGHT/2, 100, 25, FONT, "Sign In", try_signin, name_box.text, password_box.text, message)
        signup_button = Button(SURFACE_WIDTH/2+100, SURFACE_HEIGHT/2, 100, 25, FONT, "Sign Up", signin_to_signup)

        # Main loop for the signin page
        while True:
            for event in pygame.event.get():
                # If event is neither KEYDOWN nor QUIT, exit the loop
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    # Handle escape key and quit event
                    if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        self.close_conn()
                        return
                    
                    # Attempt signin when Enter key is pressed
                    if event.key == pygame.K_RETURN:
                        try_signin(name_box.text, password_box.text, message)
                 
                # Handle events for input boxes and buttons
                name_box.handle_event(event)
                password_box.handle_event(event)
                succesful = signin_button.handle_event(event)
                if signup_button.handle_event(event):
                    return
                
            # Clear the surface
            self.surface.fill("white")
            # Draw input boxes, buttons, and message on the surface
            name_box.draw(self.surface)
            password_box.draw(self.surface)
            signin_button.draw(self.surface)
            signup_button.draw(self.surface)
            message.draw(self.surface)
            # Update the display
            pygame.display.flip()

            # Pause briefly and exit loop if signin was successful
            if succesful:
                time.sleep(0.5)
                return


    def signup_page(self):
        # Implement the signup page logic here
        pass

    def menu_page(self):
        # Implement the menu page logic here
        pass

    def offline_page(self):
        # Implement the offline page logic here
        pass

    def run(self):   
        """
        The main function of the application. It runs the game loop and manages the different pages of the application.

        Parameters:
        None

        Returns:
        None

        Note:
        The function uses a while loop to continuously run the game until the application is closed.
        It uses a match-case statement to determine which page to display based on the value of the 'page' variable.
        If the 'page' variable does not match any of the defined cases, the function sets 'run_app' to False, indicating that the application should be closed.
        """
        while self.run_app:
            match self.page:
                case "signin":
                    self.signin_page()  # Display the signin page
                case "singup":
                    self.signup_page()  # Display the signup page
                case "menu":
                    self.menu_page()  # Display the menu page
                case "offline":
                    self.offline_page()  # Display the offline page
                case _:
                    self.run_app = False  # Close the application if the page does not match any of the defined cases

if __name__ == "__main__":
    c = Client()
    c.run()