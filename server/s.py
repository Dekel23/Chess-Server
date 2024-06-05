from global_vars import *

from data_base.user_DB_manager import Database_User_Manager
import threading
import socket
import sqlite3

# Socket communication's constants
HOST = '192.168.1.214'
PORT = 5000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_LENGTH = 1024
SEPERATOR = "|"

# Start the server and listen to clients
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
print(f"[LISTENING] server is listening on {ADDR}")
SERVER.listen()

def send(conn:socket.socket, *data: str) -> str:
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
        conn.sendall(message.encode(FORMAT))  # Encode the message and send it to the server
    except socket.error as e:
        return str(e)  # Return the error message if any occurred

def recieve(conn: socket.socket) -> str:
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
        return message.strip(SEPERATOR + " ").split(SEPERATOR)  # Return the message as a list of strings separated by seperator
    except socket.error as e:
        return str(e)  # Return the error message if any occurred

def create_client_handler(*args):
    Client_Handler(*args)

class Client_Handler():
    def __init__(self, conn):
        self.conn = conn
        self.conn.sendall(SEPERATOR.encode(FORMAT))
        send(self.conn, EXIST_ERROR, NOT_EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_MESSAGE,
            SIGNUP_MESSAGE, str(GRID_ROWS), str(GRID_COLS), str(BLOCK_SIZE), str(WHITE_SQUARE),
            str(BLACK_SQUARE), str(PICKED_SQUARE), str(EATING_SQUARE), str(MOVING_SQUARE))
        self.user_manager = Database_User_Manager("Users")
        self.page = "signin"
        self.run_client = True
        self.handle_client()

    def handle_client(self):
        while self.run_client:
            match self.page:
                case "signin":
                    self.handle_signin()
                case "signup":
                    self.handle_signup()
                case "offline":
                    self.handle_offline()
                case "online":
                    self.handle_online()
                case "stat":
                    self.handle_stat()
                case _:
                    self.run_client = False
    
    def handle_signin(self):
        while True:
            request = recieve(self.conn)
            match request[0]:
                case "Signin":
                    if self.user_manager.user_exist(request[1], request[2]):
                        self.name = request[1]
                        send(self.conn, SIGNIN_MESSAGE)
                        self.page = "menu"
                    else:
                        send(self.conn, NOT_EXIST_ERROR)
                case "Signup":
                    self.page = "signup"
                    send(self.conn, "signup")
                case "close connection":
                        self.run_client = False


if __name__ == "__main__":
    while True:
        conn, addr = SERVER.accept()
        print(f"Got a connection on {conn}, {addr}")
        client_thread = threading.Thread(target=create_client_handler, args=(conn,))
        client_thread.start()