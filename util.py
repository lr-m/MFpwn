def good(text):
    print(f"[\033[32m+\033[0m] {text}")

def bad(text):
    print(f"[\033[31m-\033[0m] {text}")

def info(text):
    print(f"[\033[36m*\033[0m] {text}")

def print_ascii_art():
    # ANSI escape code for magenta (pink) color
    pink = '\033[95m'
    purple = '\033[34m'
    white = '\033[37m'
    green = '\033[31m'
    light_blue = '\033[32m'
    # ANSI escape code to reset to default color
    reset = '\033[0m'

    print(f"""    {light_blue} _______ _______ {green}______ ________ _______ 
    {light_blue}|   |   |    ___{green}|   __ \\  |  |  |    |  |
    {light_blue}|       |    ___{green}|    __/  |  |  |       |
    {light_blue}|__|_|__|___|   {green}|___|  |________|__|____|{reset}
                                         
    {reset}{light_blue}Tool Suite for Android-based ZTE Routers 
                  (MF904/MF931){reset}
""")