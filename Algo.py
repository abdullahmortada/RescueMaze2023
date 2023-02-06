import time

#from RPi.GPIO import GPIO


def mpuRead():
    return


DEF_angle = mpuRead()
currAngle = 0
lastDir = ""
start = (1, 1) # Default start position
imgNo = 0

def main():
    # Initialize all pins and sensors
    stack, maze = DFS()
    with open("maze.txt", 'w') as f: 
        for key, value in maze.items(): 
            f.writelines(str(key) + " : " + str(value) + "\n")
    BFS(stack[0], stack[-1], maze)


def BFS(currCell, goal, maze):
    start=(currCell)
    visited = []
    queue = [start]
    bfsPath = {}
    while currCell != goal:
        currCell = queue.pop(0)
        if currCell not in visited:
            visited.append(currCell)
            for childCell in maze[currCell]:
                if childCell not in visited:
                    queue.append(childCell)
                    bfsPath[childCell] = currCell
    
    fwdPath = {}
    cell = goal
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]

    path = dict(reversed(list(fwdPath.items())))
    for cell in path:
        traverse(cell, path[cell])


def DFS():
    time.sleep(10)
    maze = {} # Dictionary to store the maze
    not_visited = [start] 
    visited = []
    stack = [start] # DFS Path
    while True:
        currCell = stack[-1]
        if currCell not in visited:
            # Pics and analysis
            picLeft = PiCam(imgNo)
            picRight = Logi(imgNo)
            imgNo += 1
            Rcolors = ColorDetect(picRight)
            Lcolors = ColorDetect(picRight)
            if "red" in Rcolors:
                DropKits(2, "r")
            elif "yellow" in Rcolors:
                DropKits(1, "r")
            elif "green" in Rcolors:
                DropKits(0, "r")
            elif "black" in Rcolors:
                l = letterDetect(picRight)
                if l == "H":
                    DropKits(2, "r")
                elif l == "S":
                    DropKits(1, "r")
                elif l == "U":
                    DropKits(0)

            if "red" in Lcolors:
                DropKits(2, "l")
            elif "yellow" in Lcolors:
                DropKits(1, "l")
            elif "green" in Lcolors:
                DropKits(0)
            elif "black" in Lcolors:
                l = letterDetect(picLeft)
                if l == "H":
                    DropKits(2, "l")
                elif l == "S":
                    DropKits(1, "l")
                elif l == "U":
                    DropKits(0)
                

            # Navigation
            maze[currCell] = []
            visited.append(currCell)
            not_visited.remove(currCell)
            if currAngle == 90: # facing right
                n = US_Left()
                e = US_Up()
                s = US_Right()
                if lastDir == "E":
                    w = 1
                else:
                    w = 0
            elif currAngle == -90: # facing left
                n = US_Right()
                w = US_Up()
                s = US_Left()
                if lastDir == "W":
                    e = 1
                else:
                    e = 0
            elif abs(currAngle == 180): # upside down
                e = US_Left()
                s = US_Up()
                w = US_Right()
                if lastDir == "S":
                    n = 1
                else:
                    n = 0
            elif currAngle == 0: # default tilt
                n = US_Up()
                e = US_Right()
                w = US_Left()
                if lastDir == "N":
                    s = 1
                else:
                    s = 0
            for _ in range(4):
                if e:
                    childCell = (currCell[0], currCell[1] + 1)
                    maze[currCell].append(childCell)
                elif s:
                    childCell = (currCell[0], currCell[1] - 1)
                    maze[currCell].append(childCell)
                elif n:
                    childCell = (currCell[0] + 1, currCell[1])
                    maze[currCell].append(childCell)
                elif w:
                    childCell = (currCell[0] - 1, currCell[1])
                    maze[currCell].append(childCell)
                if childCell not in visited and childCell not in not_visited:
                        not_visited.append(childCell)
        if len(not_visited) == 0:
            break

        flag = False
        for childCell in maze[currCell]:
            if childCell in not_visited:
                stack.append(childCell)
                flag = True
                break

        if not flag:
            stack.pop()

        
        while True():
            goTo = stack[-1]
            # If it found a black/blue tile
            if not traverse(currCell, goTo, currAngle):
                maze[currCell].remove(stack[-1])
                not_visited.remove(childCell)
                stack.pop()
                continue
            break

    with open("maze.txt", 'w') as f: 
        for key, value in maze.items(): 
            f.writelines(str(key) + " : " + str(value) + "\n")

    return stack, maze



def traverse(pos, dest, tilt):
    # If destination is one cell up
    if dest[0] - pos[0] == 1 and tilt == 0:
        if not forward():
            return False
        lastDir = "N"
    elif dest[0] - pos[0] == 1 and tilt == 90:
        turnLeft()
        if not forward():
            return False
        lastDir = "N"
    elif dest[0] - pos[0] == 1 and tilt == -90:
        turnRight()
        if not forward():
            return False
        lastDir = "N"
    elif dest[0] - pos[0] == 1 and abs(tilt) == 180:
        turnRight()
        turnRight()
        if not forward():
            return False
        lastDir = "N"
    
    # If destination is one cell down
    elif dest[0] - pos[0] == -1 and tilt == 0:
        turnRight()
        turnRight()
        if not forward():
            return False
        lastDir = "S"
    elif dest[0] - pos[0] == -1 and tilt == 90:
        turnRight()
        if not forward():
            return False
        lastDir = "S"
    elif dest[0] - pos[0] == -1 and tilt == -90:
        turnLeft()
        if not forward():
            return False
        lastDir = "S"
    elif dest[0] - pos[0] == -1 and abs(tilt) == 180:
        if not forward():
            return False
        lastDir = "S"

    # If destination is one cell right
    if dest[1] - pos[1] == 1 and tilt == 0:
        turnRight()
        if not forward():
            return False
        lastDir = "E"
    elif dest[1] - pos[1] == 1 and tilt == 90:
        if not forward():
            return False
        lastDir = "E"
    elif dest[1] - pos[1] == 1 and tilt == -90:
        turnRight()
        turnRight()
        if not forward():
            return False
        lastDir = "E"
    elif dest[1] - pos[1] == 1 and abs(tilt) == 180:
        turnRight()
        if not forward():
            return False
        lastDir = "E"

    # If destination is one cell left
    if dest[1] - pos[1] == 1 and tilt == 0:
        turnLeft()
        if not forward():
            return False
        lastDir = "W"
    elif dest[1] - pos[1] == 1 and tilt == 90:
        turnRight()
        turnRight()
        if not forward():
            return False
        lastDir = "W"
    elif dest[1] - pos[1] == 1 and tilt == -90:
        if not forward():
            return False
        lastDir = "W"
    elif dest[1] - pos[1] == 1 and abs(tilt) == 180:
        turnLeft()
        if not forward():
            return False
        lastDir = "W"
    
    return True
        


def turnRight():
    # Turn right until mpu gives 90 degree difference from original mpu reading
    currAngle += 90
    if abs(currAngle) >= 360:
        currAngle -= 360
    return


def turnLeft():
    currAngle -= 90
    if abs(currAngle) > 360:
        currAngle -= 360
    return


def MPU_ANGLE():
    return 0


def forward():
    # Set motors to high
    # if encoder gives 30 cm stop
    # if color sensor reads blue/black stop
    # revers pins
    # move until reading prev encoder value then return
    return


def Logi():
    return


def PiCam():
    return


def stop():
    return


def US_Up():
    return


def US_Right():
    return


def US_Left():
    return


def ColorDetect():
    return


def DropKits(n, dir="none"):
    # Set LED and buzzer high 
    time.sleep(5)
    # Set LED and buzzed to low
    if dir == "none":
        return

    elif dir == "r":
        turnLeft()
        for _ in range(n):
            ...
            #set servo to high then low
        turnRight()

    elif dir == "l":
        turnRight()
        for _ in range(n):
            ...
            #set servo to high then low
        turnLeft()
    return


def letterDetect():
    return

