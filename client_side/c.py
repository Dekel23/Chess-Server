from input_box import Input_Box
from button import Button
from text import Text

import time
import pygame
import socket
import threading

# Socket communication constants
HOST = '192.168.1.214'
PORT = 5000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
MAX_LENGTH = 1024
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
conn.connect(ADDR)

def send(*data: str):
    try:
        message = ','.join(data)
        conn.sendall(message.encode(FORMAT))
    except socket.error as e:
        return str(e)

def recieve():
    try:
        message = conn.recv(MAX_LENGTH).decode(FORMAT)
        return message.strip('& ').split('&')
    except socket.error as e:
        return str(e)

def close_conn():
    send("close connection") # Sending closing connection 
    pygame.quit() # Closing pygame
    return False # Return False to stop the main while loop

# Reciving from server all the game constants
[GRID_ROWS, GRID_COLS, BLOCK_SIZE, EXIST_ERROR, NOT_EXIST_ERROR, MISSING_ERROR, SHORT_ERROR, SIGNIN_MESSAGE, SIGNUP_MESSAGE] = recieve()
GRID_ROWS = int(GRID_ROWS)
GRID_COLS = int(GRID_COLS)
[WHITE_SQUARE, BLACK_SQUARE, WHITE_POS_SQUARE, BLACK_POS_SQUARE] = recieve()
WHITE_SQUARE = eval(WHITE_SQUARE)
BLACK_SQUARE = eval(BLACK_SQUARE)
WHITE_POS_SQUARE = eval(WHITE_POS_SQUARE)
BLACK__POS_SQUARE = eval(BLACK_POS_SQUARE)

# graphics contants
GRID_HEIGHT = GRID_ROWS * BLOCK_SIZE
GRID_WIDTH = GRID_COLS * BLOCK_SIZE
PLAYES_HEIGHT = 100
EXTRA_WIDTH = 200
SURFACE_WIDTH = GRID_WIDTH + EXTRA_WIDTH
SURFACE_HEIGHT = GRID_HEIGHT + 2 * PLAYES_HEIGHT

#pygame init
pygame.init()
surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
WHITE_PAWN_IMG = pygame.image.load('images/white/white_pawn.png')
WHITE_PAWN_IMG = pygame.transform.scale(WHITE_PAWN_IMG, (BLOCK_SIZE, BLOCK_SIZE))
WHITE_KNIGHT_IMG = pygame.image.load('images/white/white_knight.png')
WHITE_KNIGHT_IMG = pygame.transform.scale(WHITE_KNIGHT_IMG, (BLOCK_SIZE, BLOCK_SIZE))
WHITE_BISHOP_IMG = pygame.image.load('images/white/white_bishop.png')
WHITE_BISHOP_IMG = pygame.transform.scale(WHITE_BISHOP_IMG, (BLOCK_SIZE, BLOCK_SIZE))
WHITE_ROOK_IMG = pygame.image.load('images/white/white_rook.png')
WHITE_ROOK_IMG = pygame.transform.scale(WHITE_ROOK_IMG, (BLOCK_SIZE, BLOCK_SIZE))
WHITE_QUEEN_IMG = pygame.image.load('images/white/white_queen.png')
WHITE_QUEEN_IMG = pygame.transform.scale(WHITE_QUEEN_IMG, (BLOCK_SIZE, BLOCK_SIZE))
WHITE_KING_IMG = pygame.image.load('images/white/white_king.png')
WHITE_KING_IMG = pygame.transform.scale(WHITE_KING_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_PAWN_IMG = pygame.image.load('images/black/black_pawn.png')
BLACK_PAWN_IMG = pygame.transform.scale(BLACK_PAWN_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_KNIGHT_IMG = pygame.image.load('images/black/black_knight.png')
BLACK_KNIGHT_IMG = pygame.transform.scale(BLACK_KNIGHT_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_BISHOP_IMG = pygame.image.load('images/black/black_bishop.png')
BLACK_BISHOP_IMG = pygame.transform.scale(BLACK_BISHOP_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_ROOK_IMG = pygame.image.load('images/black/black_rook.png')
BLACK_ROOK_IMG = pygame.transform.scale(BLACK_ROOK_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_QUEEN_IMG = pygame.image.load('images/black/black_queen.png')
BLACK_QUEEN_IMG = pygame.transform.scale(BLACK_QUEEN_IMG, (BLOCK_SIZE, BLOCK_SIZE))
BLACK_KING_IMG = pygame.image.load('images/black/black_king.png')
BLACK_KING_IMG = pygame.transform.scale(BLACK_KING_IMG, (BLOCK_SIZE, BLOCK_SIZE))
troops_dict = {
    "w_qu": WHITE_QUEEN_IMG,
    "w_pa": WHITE_PAWN_IMG,
    "w_kn": WHITE_KNIGHT_IMG,
    "w_bi": WHITE_BISHOP_IMG,
    "w_ro": WHITE_ROOK_IMG,
    "w_ki": WHITE_KING_IMG,
    "b_qu": BLACK_QUEEN_IMG,
    "b_pa": BLACK_PAWN_IMG,
    "b_kn": BLACK_KNIGHT_IMG,
    "b_bi": BLACK_BISHOP_IMG,
    "b_ro": BLACK_ROOK_IMG,
    "b_ki": BLACK_KING_IMG
}

def synchronized(func):
    lock = threading.Lock()   
    def wrapper(*args, **kwargs):
        if not lock.locked():
            with lock:
                return func(*args, **kwargs)  
    return wrapper

def draw_board(game, possiable_pos):
    for y, row in enumerate(game):
        for x, value in enumerate(row):
            pygame.draw.rect(surface, BLACK_SQUARE if (x + y) % 2 else WHITE_SQUARE, pygame.Rect(x * BLOCK_SIZE, y*BLOCK_SIZE + PLAYES_HEIGHT, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, BLACK_SQUARE, pygame.Rect(x * BLOCK_SIZE, y*BLOCK_SIZE + PLAYES_HEIGHT, BLOCK_SIZE, BLOCK_SIZE), 2)
    for y, x in possiable_pos:
            pygame.draw.rect(surface, BLACK__POS_SQUARE if (x + y) % 2 else WHITE_POS_SQUARE, pygame.Rect(x * BLOCK_SIZE, y*BLOCK_SIZE + PLAYES_HEIGHT, BLOCK_SIZE, BLOCK_SIZE))
    for y, row in enumerate(game):
        for x, value in enumerate(row):
            surface.blit(troops_dict[value], (x * BLOCK_SIZE, y*BLOCK_SIZE + PLAYES_HEIGHT))

def draw_me(me_text:Text, timer_me:Text):
    me_text.draw(surface)
    timer_me.draw(surface)

def draw_enemy(enemy_text:Text, timer_enemy:Text):
    enemy_text.draw(surface)
    timer_enemy.draw(surface)

@synchronized
def draw_game_offline(game, timer_me, timer_enemy, me, enemy, possiable_pos):
    surface.fill(pygame.Color('white'))
    draw_board(game, possiable_pos)
    draw_me(me, timer_me)
    draw_enemy(enemy, timer_enemy)
    pygame.display.flip()


def out_of_boundes(y, x):
    return not ((0 <= y < GRID_ROWS) and (0 <= x < GRID_COLS))

page = "signin"

def main():
    run_main = True
    while run_main:
        match page:
            case "signin":
                if run_main:
                    run_main = signin_page()
            case "signup":
                if run_main:
                    run_main = signup_page()
            case "menu":
                if run_main:
                    run_main = menu_page()
            case "offline":
                if run_main:
                    run_main = offline_page()
            case "online":
                if run_main:
                    run_main = online_page()
            case "stat":
                if run_main:
                    run_main = stat_page()
            case _:
                run_main = False

def signin_page():
    def signin_correct():
        global page
        nonlocal name_box
        nonlocal password_box
        if name_box.text == '' or password_box.text == '': # If one text is empty
            return MISSING_ERROR
        if len(password_box.text) < 8: # If password is less than 8 characters
            return SHORT_ERROR
        send("Sign In", name_box.text, password_box.text)
        premission = recieve()[0]
        if premission == SIGNIN_MESSAGE: # If sign in was successful
            page = "menu" # New screen is menu
            return SIGNIN_MESSAGE
        elif premission == NOT_EXIST_ERROR:
            return NOT_EXIST_ERROR
        else:
            return "WHATTT?" # Special case
    
    def signin_signup():
        global page
        page = "signup" # New screen is signup
        send("Sign Up")
        return "signup" # Return indecation if function was called

    name_box = Input_Box(SURFACE_WIDTH/2 - 100, SURFACE_HEIGHT/2 - 125, 200, 24, font, "Name", pygame.Color('lightskyblue3'), pygame.Color('dodgerblue2'))
    password_box = Input_Box(SURFACE_WIDTH/2 - 100, SURFACE_HEIGHT/2 - 75, 200, 24, font, "Password", pygame.Color('lightskyblue3'), pygame.Color('dodgerblue2'))
    sign_in_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 - 25, 80, 24, font, "LOG IN", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), signin_correct)
    sign_up_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 + 75, 80, 24, font, "SIGN UP", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), signin_signup)
    signin_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, SIGNIN_MESSAGE, pygame.Color('green'))
    missing_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, MISSING_ERROR, pygame.Color('red'))
    short_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, SHORT_ERROR, pygame.Color('red'))
    not_exist_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, NOT_EXIST_ERROR, pygame.Color('red'))
    whattt_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, "WHATTT?", pygame.Color('yellow'))
    lasterror = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If quit, close connection
                return close_conn()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # If escape, close connection
                    return close_conn()
                elif event.key == pygame.K_RETURN: # If enter, check correctness
                    lasterror = signin_correct()
            name_box.handle_event(event)
            password_box.handle_event(event)
            error = sign_in_button.handle_event(event)
            if error is not None: # If new error, update last error
                lasterror = error
            sign_up = sign_up_button.handle_event(event)
            if (sign_up is not None) and (sign_up == "signup"): # If sign_up pressed
                return True # Stop while loop

            
            name_box.draw(surface)
            password_box.draw(surface)
            sign_in_button.draw(surface)
            sign_up_button.draw(surface)

            if lasterror != '': # Once lasterror got init value, show error text on screen
                if lasterror == SIGNIN_MESSAGE:
                    signin_text.draw(surface)
                elif lasterror == SHORT_ERROR:
                    short_text.draw(surface)
                elif lasterror == MISSING_ERROR:
                    missing_text.draw(surface)
                elif lasterror == NOT_EXIST_ERROR:
                    not_exist_text.draw(surface)
                else:
                    whattt_text.draw(surface)
            
            pygame.display.flip()

            if lasterror == SIGNIN_MESSAGE: # If sign in was successful
                time.sleep(1) # Wait 1 sec
                return True # Stop while loop

def signup_page():
    def signup_correct():
        global page
        nonlocal name_box
        nonlocal password_box
        if name_box.text == '' or password_box.text == '': # If one text is empty
            return MISSING_ERROR
        if len(password_box.text) < 8: # If password is less than 8 characters
            return SHORT_ERROR
        send("Sign Up", name_box.text, password_box.text)
        premission = recieve()[0]
        if premission == SIGNUP_MESSAGE: # If sign up was successful
            page = "signin" # New screen is signin
            return SIGNUP_MESSAGE
        elif premission == EXIST_ERROR:
            return EXIST_ERROR
        else:
            return "WHATTT?" # Special case
    
    def signup_signin():
        global page
        page = "signin" # New screen is signin
        send("Back")
        return "signin" # Return indecation if function was called

    name_box = Input_Box(SURFACE_WIDTH/2 - 100, SURFACE_HEIGHT/2 - 125, 200, 24, font, "Name", pygame.Color('lightskyblue3'), pygame.Color('dodgerblue2'))
    password_box = Input_Box(SURFACE_WIDTH/2 - 100, SURFACE_HEIGHT/2 - 75, 200, 24, font, "Password", pygame.Color('lightskyblue3'), pygame.Color('dodgerblue2'))
    sign_up_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 - 25, 80, 24, font, "SIGN UP", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), signup_correct)
    back_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 + 75, 80, 24, font, "BACK", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), signup_signin)
    signup_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, SIGNUP_MESSAGE, pygame.Color('green'))
    missing_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, MISSING_ERROR, pygame.Color('red'))
    short_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, SHORT_ERROR, pygame.Color('red'))
    exist_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, EXIST_ERROR, pygame.Color('red'))
    whattt_text = Text(SURFACE_WIDTH/2, SURFACE_HEIGHT/2 + 25, font, "WHATTT?", pygame.Color('yellow'))
    lasterror = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If quit, close connection
                return close_conn()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # If escape, go to sign in
                    signup_signin()
                    return True
                elif event.key == pygame.K_RETURN: # If enter, check correctness
                    lasterror = signup_correct()
            name_box.handle_event(event)
            password_box.handle_event(event)
            error = sign_up_button.handle_event(event)
            if error is not None: # If new error, update last error
                lasterror = error
            sign_in = back_button.handle_event(event)
            if (sign_in is not None) and (sign_in == "signin"):  # If back pressed
                return True # Stop while loop
            
            surface.fill(pygame.Color('white'))
            name_box.draw(surface)
            password_box.draw(surface)
            sign_up_button.draw(surface)
            back_button.draw(surface)

            if lasterror != '': # Once lasterror got init value, show error text on screen
                if lasterror == SIGNUP_MESSAGE:
                    signup_text.draw(surface)
                elif lasterror == SHORT_ERROR:
                    short_text.draw(surface)
                elif lasterror == MISSING_ERROR:
                    missing_text.draw(surface)
                elif lasterror == EXIST_ERROR:
                    exist_text.draw(surface)
                else:
                    whattt_text.draw(surface)
            
            pygame.display.flip()

            if lasterror == SIGNUP_MESSAGE: # If sign up was successful
                time.sleep(1) # Wait 1 sec
                return True # Stop while loop

def menu_page():
    def menu_offline():
        global page
        page = "offline"
        send("Offline")
        return "offline"

    def menu_online():
        global page
        page = "online"
        send("Online")
        return "online"

    def menu_stat():
        global page
        page = "stat"
        send("Stat")
        return "stat"

    def menu_signin():
        global page
        page = "signin"
        send("Back")
        return "signin"
    
    offline_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 - 100, 80, 24, font, "OFFLINE", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), menu_offline)
    online_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 - 50, 80, 24, font, "ONLINE", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), menu_online)
    stat_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2, 80, 24, font, "STATISTICS", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), menu_stat)
    back_button = Button(SURFACE_WIDTH/2 - 40, SURFACE_HEIGHT/2 + 50, 80, 24, font, "BACK", pygame.Color('dodgerblue2'), pygame.Color('lightskyblue3'), menu_signin)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return close_conn()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_signin()
                    return True
            if offline_button.handle_event(event) or online_button.handle_event(event) or stat_button.handle_event(event) or back_button.handle_event(event): # If one of the buttons was pressed
                return True
            
            surface.fill(pygame.Color('white'))
            offline_button.draw(surface)
            online_button.draw(surface)
            stat_button.draw(surface)
            back_button.draw(surface)

            pygame.display.flip()

def offline_page():
    def recieve_thread(shared_vars):
        while shared_vars['run']:
            shared_vars['massage'] = recieve()
            shared_vars['update'] = True

    players = recieve()
    me, enemy = players[0], players[1]
    me_text = Text(100, GRID_HEIGHT + 1/4 * PLAYES_HEIGHT, font, me, (0, 0, 0))
    enemy_text = Text(100, 1/4 * PLAYES_HEIGHT, font, enemy, (0, 0, 0))
    timer_me, timer_enemy = "10:00", "10:00"
    timer_me_text = Text(300, GRID_HEIGHT + 1/4 * PLAYES_HEIGHT, font, timer_me, (0, 0, 0))
    timer_enemy_text = Text(300, 1/4 * PLAYES_HEIGHT, font, timer_enemy, (0, 0, 0))
    shared_vars = {'run': True, 'update': False, 'massage': list[str]}
    recieving_thread = threading.Thread(target=recieve_thread, args=(shared_vars, ))
    recieving_thread.start()

    while shared_vars['run']:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return close_conn()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                x, y = int(pos_x / BLOCK_SIZE), int(pos_y / BLOCK_SIZE)
                if out_of_boundes(y, x):
                    break
                send(str(y), str(x))

        if shared_vars['update']:
            if shared_vars['massage'].startwith("win") or shared_vars['massage'].startwith("lose"):
                shared_vars['run'] = False
                print(shared_vars['massage'])
            else:
                [game, timer_me, timer_enemy, possiable_pos] = shared_vars['massage']
                timer_me_text.set_text(timer_me)
                timer_enemy_text.set_text(timer_enemy)
                draw_game_offline(game, timer_me, timer_enemy, me_text, enemy_text, possiable_pos)

    recieving_thread.join()
    return True


if __name__ == "__main__":
    main()