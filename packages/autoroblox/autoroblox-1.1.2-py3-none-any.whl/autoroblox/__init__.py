"""
# AutoRoblox.
**AutoRoblox** is a library offering tools for automating Roblox gameplay.
\nCurrently, it consists of different commands making to easier to automate Roblox gameplay.

## Commands.
### critical_error(text: str)
**Prints a red "Critical Error" message and shuts down the program.**
\nExample: `critical_error("Critical Error.")`
\nOutput: 🚫 Critical Error. *and shuts down the program.*

### error(text: str) -> int
**Prints a red "Error" message and returns 1.**
\nExample: `error("Error.")`
\nOutput: 🛑 Error. *and returns 1.*

### warn(text: str) -> int
**Prints a yellow "Warning" message and returns 0.**
\nExample: `warn("Warning.")`
\nOutput: ⚠ Warning. *and returns 0.*

### info(text: str)
**Prints a blue "Info" message.**
\nExample: `info("Info.")`
\nOutput: 🛈 Info.

### info_by_username(information: str, username: str)
**Requests information about someone by his username.**
\nExample: `print(info_by_username("previousUsername", "AutoRobloxProject"))`
\nOutput: []
\nExample: `print(info_by_username("hasVerifiedBadge", "AutoRobloxProject"))`
\nOutput: False
\nExample: `print(info_by_username("id", "AutoRobloxProject"))`
\nOutput: 8166253857
\nExample: `print(info_by_username("name", "AutoRobloxProject"))`
\nOutput: AutoRobloxProject
\nExample: `print(info_by_username("displayName", "AutoRobloxProject"))`
\nOutput: AutoRobloxProject

### move(direction: str, studs: float)
**Moves the character in the specified direction for specified studs.**
\nExample 1: `move("forward", 10)`
\nOutput: *Makes the character move forward by 10 studs if the walk speed is default(16).*
\nExample 2: `move("backward", 10)`
\nOutput: *Makes the character move backward by 10 studs if the walk speed is default(16).*
\nExample 3: `move("left", 10)`
\nOutput: *Makes the character move to the left by 10 studs if the walk speed is default(16).*
\nExample 4: `move("right", 10)`
\nOutput: *Makes the character move to the right by 10 studs if the walk speed is default(16).*

### jump()
**Makes the character jump.** (Unless jumps are disabled)
\nExample: `jump()`
\nOutput: *Jumps if jumps are enabled.*

### camera(rotation: int, sensivity: float = 1.6)
**Makes the camera rotate.**
\nExample: `camera(180, 1.6)`
\nOutput: *Rotates camera by 180 if the camera sensivity at Roblox settings is 1.6.*

### chat(message: str)
**Sends a message at chat.**
\nExample: `chat(\"Hello!\")`
\nOutput: *Sends \"Hello!\" at chat.*

### click(duration: float, x: int, y: int)
**Clicks on the specified coordinates if any. If none, clicks on the current mouse position.**
\nExample 1: `click()`
\nOutput: *Clicks.*
\nExample 2: `click(1)`
\nOutput: *Holds the click for 1 second.*
\nExample 3: `click(1, 1000, 100)`
\nOutput: *Drags mouse to coordinates x:1000 and y:100 and holds the click for 1 second.*

### press(key: str, duration: float)
\nExample 1: `press("C")`
\nOutput: *Presses [C].*
\nExample 2: `press("E", 1)`
\nOutput: *Holds [E] for 1 second.*

**Good luck.**
"""

from pynput.mouse import Button, Controller
import keyboard
import requests
import time
import sys

# -------------------------------------- INFORMATION --------------------------------------- #

def critical_error(text: str):
    print(f"\033[31m🚫 {text}\033[0m")
    sys.exit(1)
def error(text: str) -> int:
    print(f"\033[31m🛑 {text}\033[0m")
    return 1
def warn(text: str) -> int:
    print(f"\033[33m⚠ {text}\033[0m")
    return 0
def info(text: str):
    print(f"\033[36m🛈 {text}\033[0m")
def info_by_username(information: str, username: str):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get('data'):
            warn("Username not found.")
        user_info = data['data'][0]
        if information in user_info:
            return user_info[information]
        else:
            error("Unknown information requested. Known fields are: previousUsernames, hasVerifiedBadge, id, name, displayName.")
    except requests.exceptions.RequestException as e:
        warn(e)

# --------------------------------------- ATTRIBUTES --------------------------------------- #

__version__ = "1.1.2"
__author__ = "AutoRoblox Project"
__email__ = "contact.autoroblox@gmail.com"

# ------------------------------------ CHARACTER CONTROL ----------------------------------- #

def move(direction: str, studs: float):
    if direction == "forward":
        keyboard.press('w')
    elif direction == "backward":
        keyboard.press('s')
    elif direction == "left":
        keyboard.press('a')
    elif direction == "right":
        keyboard.press("d")
    elif direction == "":
        error("Direction unspecified.")
    else:
        error("Unknown direction. Possible directions are: forward, backward, left, right.")
    time.sleep(studs*0.0625)
    if direction == "forward":
        keyboard.release('w')
    elif direction == "backward":
        keyboard.release('s')
    elif direction == "left":
        keyboard.release('a')
    elif direction == "right":
        keyboard.release("d")
    else:
        error("Unknown direction. Possible direction are: forward, backward, left, right.")
def jump():
    keyboard.press("Space")
    time.sleep(0.05)
    keyboard.release("Space")
def camera(rotation: int = 0, sensivity: float = 1.6):
    if rotation != 0:
        if rotation > 0:
            keyboard.press("right")
            time.sleep(sensivity / 180 * rotation)
            keyboard.release("right")
        else:
            keyboard.press("left")
            time.sleep(sensivity / 180 * (rotation + rotation + rotation))
            keyboard.release("left")
    else:
        error("Rotation degrees unspecified.")
def chat(message: str = ""):
    if message != "":
        keyboard.press("/")
        time.sleep(0.05)
        keyboard.release("/")
        keyboard.write(message, delay=0.02)
        keyboard.press("Enter")
        keyboard.release("Enter")
    else:
        error("Message unspecified.")
def click(duration: float = 0.05, x: int = None, y: int = None):
    mouse = Controller()
    if x != None and y != None:
        mouse.position = (x, y)
    mouse.press(Button.left)
    if duration < 0.05:
        time.sleep(0.05)
    else:
        time.sleep(duration)
    mouse.release(Button.left)
def press(key: str = "", duration: float = 0.05):
    if key != "":
        try:
            keyboard.press(key)
            if duration < 0.05:
                time.sleep(0.05)
            else:
                time.sleep(duration)
            keyboard.release(key)
        except Exception:
            error(f"An error occured: {Exception}")
    else:
        error("Key unspecified.")