#from tetris.game_vars import GRID_COLS, GRID_ROWS

# Game vars
GRID_ROWS = 8
GRID_COLS = 8

# Graphics vars
BLOCK_SIZE = 50
WHITE_SQUARE = (235,236,208)
BLACK_SQUARE = (115,149,82)

# Errors
EXIST_ERROR = "User already exist"
NOT_EXIST_ERROR = "User doesn't exist"
MISSING_ERROR = "Missing name or password"
SHORT_ERROR = "Password too short"
SIGNIN_MESSAGE = "Signed In!"
SIGNUP_MESSAGE = "Signed Up!"

# Functions
def out_of_boundes(y, x):
    return not ((0 <= y < GRID_ROWS) and (0 <= x < GRID_COLS))