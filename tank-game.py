import pygame
import random
import time

# Define the size of the window
WINDOW_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 1050, 700

# Define the fps
FPS = 60

#Define some colors
WHITE = (255,255,255)
BLACK = (0,0,0)

class OtherTank:
    # Image for rendering Tank
    shape = [
            pygame.image.load('./images/tank-move-right.png'),
        ]
    fire = (
        pygame.image.load('./images/tank-fire-0.png'),
        pygame.image.load('./images/tank-fire-1.png'),
        pygame.image.load('./images/tank-fire-2.png'),
        pygame.image.load('./images/tank-fire-3.png'),
        pygame.image.load('./images/tank-fire-4.png'),
    )

    shapeWidth,shapeHeight = shape[0].get_rect().size
    fireWidth,fireHeight = fire[0].get_rect().size
    
    # After the ``run`` function was called ``default_amination_speed`` times
    # the image source will be changed
    default_amination_speed = 1

    def __init__(self,gameDisplay,x,y):
        self.gameDisplay = gameDisplay
        self.x = x
        self.y = y
        self.deltaX = 2
        self.deltaY = 0
        self.isBug = False
        self.isCompleteMission = False
        self.isFailureMission = False
        self.fireShapeIndex = 0
        self.frameCount = 1
        self.animation_speed = OtherTank.default_amination_speed

    # Set speed for object
    def set_speed(self,deltaX, deltaY):
        self.deltaX = deltaX
        self.deltaY = deltaY

    # 1 loop, call 1 time
    def draw(self):
        if self.isBug: 
            self.drawFire()
        if self.isCompleteMission or self.isFailureMission:
            return

        self.x += self.deltaX

        self.gameDisplay.blit(OtherTank.shape[0],(self.x,self.y))


        sw, sh = OtherTank.shape[0].get_rect().size
        w, h = pygame.display.get_surface().get_size()
        if self.x + sw > w - 50:
            self.finishMission()

    def drawFire(self):
        if self.fireShapeIndex < 5:
            x = self.x + OtherTank.shapeWidth/2 - OtherTank.fireWidth/2
            y = self.y + OtherTank.shapeHeight/2 - OtherTank.fireHeight/2
            if self.frameCount < self.animation_speed:
                self.frameCount += 1
                self.gameDisplay.blit(OtherTank.fire[self.fireShapeIndex],(x,y))
            else:
                self.gameDisplay.blit(OtherTank.fire[self.fireShapeIndex],(x,y))
                self.fireShapeIndex += 1
                self.frameCount = 1
        else:
            self.isBug = False
    
    def finishMission(self):
        self.isBug = True
        self.isCompleteMission = True
        pygame.mixer.Sound('./sounds/failure.wav').play()

    def failureMission(self):
        self.isFailureMission = True
        self.isBug = True
        pygame.mixer.Sound('./sounds/fire.wav').play()

    def otherShotAt(self,position):
        if not self.isCompleteMission and not self.isFailureMission:
            x = position[0]
            y = position[1]
            if x > self.x and x < self.x + OtherTank.shapeWidth \
            and y > self.y and y < self.y + OtherTank.shapeHeight:
                self.failureMission()

    def isDestroy(self):
        if self.isBug:
            return False
        return self.isCompleteMission or self.isFailureMission
    
    def getMissionResult(self):
        return self.isCompleteMission
        


    # param ``fps``: the fps of the game
    # param ``speed``: the number shape frame was changed per second
    def set_animation_speed(self,fps, speed):
        if speed > 0 and fps > 0:
            self.animation_speed = fps/speed
            if self.animation_speed < OtherTank.default_amination_speed: 
                self.animation_speed = OtherTank.default_amination_speed
        else:
            self.animation_speed = OtherTank.default_amination_speed

class MyTank:
    # Image for rendering Jerry
    shape = [
            pygame.image.load('./images/my-tank.png'),
        ]
    notReadyIcon = pygame.image.load('./images/not-ready.png')
    shotIcon = pygame.image.load('./images/cursor-shot.png')
  
    def __init__(self,gameDisplay,x,y):
        self.gameDisplay = gameDisplay
        self.x = x
        self.y = y
        self.deltaX = 2
        self.deltaY = 2
        self.isMovedToMouse = False

    # Set speed for object
    def set_speed(self,deltaX, deltaY):
        self.deltaX = deltaX
        self.deltaY = deltaY

    # 1 loop, call 1 time
    def draw(self, position):
        # Get the size of the shape
        shapeWidth, shapeHeight = MyTank.shape[0].get_rect().size

        # Get the middle point of the shape
        middleY = self.y + shapeHeight/2

        # new position
        if middleY < position[1]:
            middleY += self.deltaY
            if middleY >= position[1]:
                middleY = position[1]
                self.isMovedToMouse = True
            else:
                self.isMovedToMouse = False

        elif middleY > position[1]:
            middleY -= self.deltaY
            if middleY <= position[1]:
                middleY = position[1]
                self.isMovedToMouse = True
            else:
                self.isMovedToMouse = False
        
        
        # Detemine weather the tank is at the edge or not 
        # w, h = pygame.display.get_surface().get_size()
        self.y = middleY - shapeHeight/2
        # if self.y < 0:
        #     self.y = 0
        # elif self.y > h - shapeHeight:
        #     self.y = h - shapeHeight

        # draw Tank into game display
        self.gameDisplay.blit(MyTank.shape[0],(self.x,self.y))

        cursorX = position[0] -12
        cursorY = position[1] - 12
        if cursorX < 0: 
            cursorX = 0
        if cursorY < 0:
            cursorY = 0

        if self.isMovedToMouse:
            self.gameDisplay.blit(MyTank.shotIcon,(cursorX,cursorY))
        else:
            self.gameDisplay.blit(MyTank.notReadyIcon,(cursorX,cursorY))
    def isReadyToShot(self):
        return self.isMovedToMouse

def shotAt(tanks,position):
    for tank in tanks:
        tank.otherShotAt(position)

def removeDestroyTank(tanks):
    i = 0
    while i < len(tanks):
        if tanks[i].isDestroy():
            print('Destroy a tank')
            del tanks[i]
            i -= 1
        i += 1

def createNewTank(tanks, gameDisplay):
    if len(tanks) < 5:
        y = random.randint(50,DISPLAY_HEIGHT-50)
        tank = OtherTank(gameDisplay,0,y)
        tank.set_animation_speed(FPS,30)
        tank.set_speed(random.randint(1,5),0)

        tanks.append(tank)

# Initilize python
pygame.init()

# Set the size for the window
gameDisplay = pygame.display.set_mode(WINDOW_SIZE)

# Set caption for the window
pygame.display.set_caption('Tom And Jerry')

# Load background
background = pygame.image.load('./images/background.png')

# Hide cursor
pygame.mouse.set_visible(False)

# Play background sound
pygame.mixer.Sound('./sounds/background.wav').play(-1)

# Init Jerry object
tanks = [
    OtherTank(gameDisplay,0,0),
    OtherTank(gameDisplay,200,200),
    OtherTank(gameDisplay,0,200),
    OtherTank(gameDisplay,0,400),
    OtherTank(gameDisplay,10,300)
]
for tank in tanks:
    tank.set_animation_speed(FPS,30)
    tank.set_speed(3,0)

# Init my tank
myTank = MyTank(gameDisplay,DISPLAY_WIDTH-100,0)
myTank.set_speed(4,8)

# This is used for defining fps for game.
# Ex: clock.tick(60) indicates that this game has fps is 60
clock = pygame.time.Clock()

finishedGame = False

while not finishedGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finishedGame = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if myTank.isReadyToShot():
                shotAt(tanks,pygame.mouse.get_pos())

    removeDestroyTank(tanks)
    createNewTank(tanks,gameDisplay)

    gameDisplay.blit(background,(0,0))
    # pygame.draw.rect(gameDisplay,BLACK,pygame.Rect(0,300,DISPLAY_WIDTH,305))

    for tank in tanks:
        tank.draw()

    myTank.draw(pygame.mouse.get_pos())
    pygame.display.flip()

    # This will block execution until 1/60 seconds have passed 
    # since the previous time clock.tick was called.
    clock.tick(FPS)

pygame.quit()
quit()
