# AutoRoblox.
**AutoRoblox** is a library offering tools for automating Roblox gameplay.
Currently, it consists of 10 commands making to easier to automate Roblox gameplay.

## Commands.
### critical_error(text: str)
**Prints a red "Critical Error" message and shuts down the program.**
Example: `critical_error("Critical Error.")`
Output: 🚫 Critical Error. *and shuts down the program.*

### error(text: str) -> int
**Prints a red "Error" message and returns 1.**
Example: `error("Error.")`
Output: 🛑 Error. *and returns 1.*

### warn(text: str) -> int
**Prints a yellow "Warning" message and returns 0.**
Example: `warn("Warning.")`
Output: ⚠ Warning. *and returns 0.*

### info(text: str)
**Prints a blue "Info" message.**
Example: `info("Info.")`
Output: 🛈 Info.

### move(direction: str, studs: float)
**Moves the character in the specified direction for specified studs.**
Example 1: `move("forward", 10)`
Output: *Makes the character move forward by 10 studs if the walk speed is default(16).*
Example 2: `move("backward", 10)`
Output: *Makes the character move backward by 10 studs if the walk speed is default(16).*
Example 3: `move("left", 10)`
Output: *Makes the character move to the left by 10 studs if the walk speed is default(16).*
Example 4: `move("right", 10)`
Output: *Makes the character move to the right by 10 studs if the walk speed is default(16).*

### jump()
**Makes the character jump.** (Unless jumps are disabled)
Example: `jump()`
Output: *Jumps if jumps are enabled.*

### camera(rotation: int, sensivity: float = 1.6)
**Makes the camera rotate.**
Example: `camera(180, 1.6)`
Output: *Rotates camera by 180 if the camera sensivity at Roblox settings is 1.6.*

### chat(message: str)
**Sends a message at chat.**
Example: `chat(\"Hello!\")`
Output: *Sends \"Hello!\" at chat.*

### click(duration: float, x: int, y: int)
**Clicks on the specified coordinates if any. If none, clicks on the current mouse position.**
Example 1: `click()`
Output: *Clicks.*
Example 2: `click(1)`
Output: *Holds the click for 1 second.*
Example 3: `click(1, 1000, 100)`
Output: *Drags mouse to coordinates x:1000 and y:100 and holds the click for 1 second.*

### press(key: str, duration: float)
Example 1: `press("C")`
Output: *Presses [C].*
Example 2: `press("E", 1)`
Output: *Holds [E] for 1 second.*

**Good luck.**