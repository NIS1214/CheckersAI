import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60 #rendering the game

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #displasy the playing board     
pygame.display.set_caption('Checkers') 

def get_row_col_from_mouse(pos):#take the pos of the mouse and tell us what row and col we're in
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main(): 
    run = True
    clock = pygame.time.Clock()#makes sure our loop doesn't run too fast or too slow
    game = Game(WIN)

    while run:#game loop
        clock.tick(FPS) 
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)#calls the function for minmax white
            game.ai_move(new_board)
        if game.winner() != None:#check for winner
            print(game.winner())
            run = False

        for event in pygame.event.get(): #check to see if any event happend at the current time
            if event.type == pygame.QUIT: #if we hit the red x button then we quit the game
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: #check to see if we clicked anything on our mouse
                pos = pygame.mouse.get_pos() #get the mouse pos
                row, col = get_row_col_from_mouse(pos) #get the row and col associated with it
                game.select(row, col)

        game.update()
    
    pygame.quit()

main() #calls the main function defined above