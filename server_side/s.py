from global_vars import EXIST_ERROR, NOT_EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_MESSAGE, SIGNUP_MESSAGE
from global_vars import GRID_COLS, GRID_ROWS, BLOCK_SIZE, out_of_boundes
from DB_user_manager import DB_User_Manager
from DB_manager import DB_Manager

import threading
import sqlite3
import socket

from stop_watch import stop_watch

# Socket communication constants
HOST = '192.168.1.214'
PORT = 5000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_LENGTH = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print(f"[LISTENING] server is listening on {ADDR}")
server.listen()

def send(conn: socket.socket, *data: str):
    try:
        message = ','.join(data)
        conn.sendall(message.encode(FORMAT))
    except socket.error as e:
        return str(e)

def recieve(conn: socket.socket):
    try:
        message = conn.recv(MAX_LENGTH).decode(FORMAT)
        return message.strip(', ').split(',')
    except socket.error as e:
        return str(e)

def main():
    while True:
        conn, addr = server.accept()
        print(f"Got a connection on {conn}, {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

def handle_client(conn: socket.socket):
    send(conn, str(GRID_ROWS), str(GRID_COLS), str(BLOCK_SIZE), EXIST_ERROR, NOT_EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_MESSAGE, SIGNUP_MESSAGE)
    send(conn, "black", "white", "light_gray", "dark_gray")
    conn_db = sqlite3.connect(".\\server_side\\data_bases\\users_info.db")
    c_db = conn_db.cursor()
    db_manager = DB_Manager(conn_db, c_db)
    user_manager = DB_User_Manager(db_manager, "Users")

    name:str = None
    page = "signin"

    run_client = True
    while run_client:
        match page:
            case "signin":
                if run_client:
                    run_client, page, name = handle_signin(conn, user_manager)
            case "signup":
                if run_client:
                    run_client, page = handle_signup(conn, user_manager)
            case "menu":
                if run_client:
                    run_client, page = handle_menu(conn)
            case "offline":
                if run_client:
                    run_client, page = handle_offline(conn, user_manager)
            case "online":
                if run_client:
                    run_client, page = handle_online(conn, user_manager)
            case "stat":
                if run_client:
                    run_client, page = handle_stat(conn, user_manager)
            case _:
                run_client = False

    conn_db.close()

def handle_signin(conn: socket.socket, user_manager: DB_User_Manager):
    while True:
        request = recieve(conn)
        match request[0]:
            case "Sign In":
                name, password = request[1], request[2]
                in_system = user_manager.user_exist(name, password)
                if in_system:
                    send(conn, SIGNIN_MESSAGE)
                    return True, "menu", name
                else:
                    send(conn, NOT_EXIST_ERROR)
            case "Sign Up":
                return True, "signup", None
            case "close connection":
                return False, "null", None

def handle_signup(conn: socket.socket, user_manager: DB_User_Manager):
    while True:
        request = recieve(conn)
        match request[0]:
            case "Sign Up":
                name, password = request[1], request[2]
                in_system = user_manager.user_exist(name, password)
                if in_system:
                    send(conn, EXIST_ERROR)
                else:
                    #user_manager.insert_user(name, password)
                    send(conn, SIGNUP_MESSAGE)
                    return True, "signin"
            case "Back":
                return True, "signin"
            case "close connection":
                return False, "null"

def handle_menu(conn: socket.socket):
    while True:
        request = recieve(conn)
        match request[0]:
            case "Offline":
                return True, "offline"
            case "Online":
                return True, "online"
            case "Stat":
                return True, "stat"
            case "Back":
                return True, "signin"
            case "close connection":
                return False, "null"

def handle_offline(conn: socket.socket, user_manager: DB_User_Manager, name: str):
    def recieve_thread(shared_vars):
        while shared_vars['run']:
            shared_vars['massage'] = recieve()
            shared_vars['update'] = True

    shared_vars = {'run': True, 'update': False, 'massage': list[str]}
    recieving_thread = threading.Thread(target=recieve_thread, args=(shared_vars, ))
    recieving_thread.start()
    start_time = 600
    player_timer = stop_watch(start_time)
    computer_timer = stop_watch(start_time)
    send(conn, name, "comupter", player_timer.get_time())
    turn = "player"

    while shared_vars["run"]:
        if turn == "player":
            

            
if __name__ == "__main__":
    main()