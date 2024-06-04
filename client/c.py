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
        message = seperator.join(data)  # Join the data into a single string separated by seperator
        conn.sendall(message.encode(FORMAT))  # Encode the message and send it to the server
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
        message = conn.recv(MAX_LENGTH).decode(FORMAT)  # Receive the message from the server
        return message.strip(seperator + " ").split(seperator)  # Return the message as a list of strings separated by seperator
    except socket.error as e:
        return str(e)  # Return the error message if any occurred

def close_conn():
    """
    This function sends a "close connection" message to the server and quits the pygame library.

    Parameters:
    None

    Returns:
    bool: Returns False to indicate that the connection should be closed.

    Note:
    This function is called when the user wants to close the connection and quit the application.
    It sends a "close connection" message to the server using the send() function and then quits the pygame library.
    """
    send("close connection")  # Send a "close connection" message to the server
    pygame.quit()  # Quit the pygame library
    return False  # Return False to indicate that the connection should be closed

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

def out_of_bounds(x: int, y: int) -> bool:   
    """
    This function checks if a given position is out of bounds of the grid.

    Parameters:
    x (int): The x-coordinate of the position to check.
    y (int): The y-coordinate of the position to check.

    Returns:
    bool: True if the position is out of bounds, False otherwise.

    Note:
    The grid is defined by the constants GRID_COLS and GRID_ROWS.
    """
    return x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS

def main():
    pass

# Socket communication's constants
HOST = '192.168.1.214'
PORT = 5000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_LENGTH = 1024

# Start connection to the server
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(ADDR)
seperator = conn.recv(MAX_LENGTH).decode(FORMAT)

# Reciving application's constants
[EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_ERROR, SIGNUP_ERROR,
GRID_ROWS, GRID_COLS, BLOCK_SIZE, BLACK_SQUARE, WHITE_SQUARE, BLACK_POSS_SQUARE, WHITE_POSS_SQUARE] = recieve()
GRID_ROWS = int(GRID_ROWS)
GRID_COLS = int(GRID_COLS)

# Other application's constants
GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE
GRID_WIDTH = GRID_COLS * BLOCK_SIZE
PLAYES_HEIGHT = 100
EXTRA_WIDTH = 200
SURFACE_WIDTH = GRID_WIDTH + EXTRA_WIDTH
SURFACE_HEIGHT = GRID_HEIGHT + 2 * PLAYES_HEIGHT

# Initialize the pygame library and application objects
pygame.init()
SURFACE = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
FONT = pygame.font.Font('freesansbold.ttf', 32)

# Initialize the image dictionary
IMAGE_DICT = create_image_dictionary("./images")

page = "signin"

if __name__ == "__main__":
    main()