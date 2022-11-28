import pygame as pg
import colors
from data import bloons, bloonColors
WHITE = colors.white 

class Bloon(pg.sprite.Sprite):
    """
    Class representing the bloons created
    Inherits from the "Sprite" class in pygame
    """
    def __init__(self, color, widht, height, speed, path_list):
        #Calls the constructor of the inherited class
        super().__init__()

        # Attributes
        self.image = pg.Surface([widht, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.speed = bloons[bloonColors[color]]['speed']
        self.path = path_list
        self.i = 0

        # Draws the bloon
        pg.draw.rect(self.image, color, [0, 0, widht, height])
        
        # Gets the rect attribute from the "Sprite" class
        self.rect = self.image.get_rect()

        # Creates an atribute that returns x and y coordinates of the bloon
        self.pos = (self.rect.x, self.rect.y)

    def __refresh_pos(self):
        """
        A private method that actualizes the pos attribute everytime the rect attribute is changed
        """
        self.pos = (self.rect.x, self.rect.y)
    
    def set_pos(self, x, y):
        """
        Sets the position of the bloon
        """
        self.rect.x = x
        self.rect.y = y
        self.__refresh_pos()    

    def move_bloon(self):
        """
        Moves the bloon according to the path coordinates
        """

        pos, direction = self.path[self.i] # Gets the position and direction of the current path segment
        match(direction):
            case 'e':
                self.rect.x += self.speed
                if self.rect.x > pos[0]:
                    self.rect.x = pos[0]
            case 'w':
                self.rect.x -= self.speed
                if self.rect.x < pos[0]:
                    self.rect.x = pos[0]
            case 'n':
                self.rect.y -= self.speed
                if self.rect.y < pos[1]:
                    self.rect.y = pos[1]
            case 's':
                self.rect.y += self.speed
                if self.rect.y > pos[1]:
                    self.rect.y = pos[1]
        
        self.__refresh_pos()
        if self.pos == pos: # If the bloon has reached the end of the path segment, it moves to the next one
            self.i += 1
