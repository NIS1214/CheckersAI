import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

class Game:
    def __init__(self, win):#take the window we want to draw the game on
        self._init()
        self.win = win
    
    def update(self): #updating the pygame display
        self.board.draw(self.win)#draws the board
        self.draw_valid_moves(self.valid_moves)#draws the valid moves
        pygame.display.update()

    def _init(self): #intializes the game and also for convince sake b/c we're calling it in __init__ and reset
        self.selected = None #identifies what piece is selected
        self.board = Board()  #making a game that controls the board for us
        self.turn = RED #import constants needed
        self.valid_moves = {}#identifies valid moves for the player

    def winner(self):
        return self.board.winner()

    def reset(self): #resets the game
        self._init()#calls the init funtion

    def select(self, row, col):
        if self.selected:#if something is selected
            result = self._move(row, col)#try to move it to the row and col in this location
            if not result:# or else select a diff piece
                self.selected = None #reset the selection
                self.select(row, col) #reselect a row and col
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn: #if we're not selecting an empty piece and who's ever turn it currently is 
            self.selected = piece #then select that piece
            self.valid_moves = self.board.get_valid_moves(piece) #select a valid move
            return True
            
        return False

    def _move(self, row, col):#when selecting a move, this helps confirm the move you have selected
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #if we have something selected and the piece is 0 and the row and col we want to move to is in valid moves
            self.board.move(self.selected, row, col) #then we can move the piece
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped) #remove the piece
            self.change_turn()
        else:
            return False 

        return True #return true if it works

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):#if it's red we'll go to white and vice versa
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()