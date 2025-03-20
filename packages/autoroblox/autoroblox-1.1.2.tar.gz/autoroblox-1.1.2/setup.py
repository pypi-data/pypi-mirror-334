from setuptools import setup, find_packages

setup(
    name="autoroblox",
    version="1.1.2",
    author="AutoRoblox Project",
    author_email="contact.autoroblox@gmail.com",
    description="AutoRoblox is a library offering tools for automating Roblox-related gameplay.",
    long_description="""# AutoRoblox.
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

**Good luck.**""",
    url="https://github.com/autoRobloxProject/AutoRoblox",
    packages=find_packages(),
    install_requires=[
        "pynput",
        "keyboard",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
