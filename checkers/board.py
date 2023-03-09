import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []#internal representation of the board
        self.red_left = self.white_left = 12 #board starts with 12 pieces from red and white 
        self.red_kings = self.white_kings = 0 #board starts with 0 kings
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)#fill entire window with black
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):#for loop for creating checker board pattern
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color): #loop through all the pieces returns the one that are the pieces
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col): #tell the piece what row and col u want to move to
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #we are swapping the values of the piece we want to move and the position we want to move it to
        piece.move(row, col)

        if row == ROWS - 1 or row == 0: #if the piece hits the last row or 1st row the piece becomes a king
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col): #give it row and col and it returns a piece back
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])#list to represent what each row has
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):#if the current col is divisble by 2 then we can draw red or white piece
                    if row < 3: # because 0, 1, 2 are the 1st 3 rows we want to draw the white pieces
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4: # row 5, 6, 7 draw the red piece
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0) # when we don't add a piece we add a zero instead so we can seperate the pieces and look at this list to figure out where the pieces are
                else:
                    self.board[row].append(0) 
        
    def draw(self, win): #draw all the pieces and the squares
        self.draw_squares(win) 
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col] 
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces): #loop through all the pieces remove the ones we need
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self): #whoever has more pieces wins
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {} #empty dictionary
        left = piece.col - 1 #left and right diagonals we're considering
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left)) #look up but not futher than 2 pieces from where the current piece is and look up to row 0
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right)) 
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))#look down but not futher than 2 pieces from where the current piece is and look down to row 0
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):#what row it's starting at, stopping at and stepping by
            if left < 0: #if the left is no longer in the range of col, break
                break
            
            current = self.board[r][left]
            if current == 0: #if there's an empty square
                if skipped and not last: #if we skipped over a piece and we don't have anything we can skip then we can't move there
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped #combine last checker with the skipped checker 
                else:
                    moves[(r, left)] = last #we can jump over the piece
                
                if last:#check to see if you can jump more than once
                    if step == -1: 
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last)) #update the pos to see if u can double or triple jump
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color: #otherwise if it has a color and is equal to our current color
                break
            else:
                last = [current] #if it wasn't our color then it's the other player's and we can move on top of it assuming there's an empty space

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves