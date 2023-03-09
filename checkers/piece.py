from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color): #when we make a new piece we have to pass in what row, collumn and color its in
        self.row = row
        self.col = col
        self.color = color
        self.king = False 
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self): #calculate the x and y position based on the row and col we're in
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self): #make this piece a king
        self.king = True
    
    def draw(self, win): #draw the actual pieces 
        radius = SQUARE_SIZE//2 - self.PADDING #need to put in the center of the
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)#larger circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)#smaller circle
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):#to move a piece we have to recalculate our position
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):#internal representation of the object, added this because it was giving errors
        return str(self.color)