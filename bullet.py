import pygame

class Bullet:

    bullet = [
            pygame.image.load("./images/bullet-left.png"),
            pygame.image.load("./images/bullet-right.png"),
            pygame.image.load("./images/bullet-up.png"),
            pygame.image.load("./images/bullet-down.png")
    ]

    def __init__(self,gameDisplay,id_tank,id_group,speed,x_start,y_start,x_end,y_end):
        self.gameDisplay = gameDisplay
        self.id = id_tank
        self.id_group = id_group
        self.speed = speed
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end

    def draw(self,positionBullet):
        self.gameDisplay.blit(positionBullet,(self.x_start,self.y_start))

    def shot(self):
        print("This is a bullet object ")

    def colision_Bullet(self):
        pass






















