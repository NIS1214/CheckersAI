from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

def minimax(position, depth, max_player, game):#position passes different boards, depth is describing how far the tree goes (its recursivly called decrease by1), max player-boolean variable T max the player F min the player,
    if depth == 0 or position.winner() != None:#only evaluates if our depth is at 0
        return position.evaluate(), position
    
    if max_player:#maximizing the score
        maxEval = float('-inf')##max evaluation is negative infinity , this helps check the best position, if there is none the best is - inf
        best_move = None #storing the best move
        for move in get_all_moves(position, WHITE, game):#getting all posible moves for white
            evaluation = minimax(move, depth-1, False, game)[0]#minmax return to us the position or board (recursive)
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):#getting all posible moves for red
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []#list holds new board if peices are moved

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):# drawing green circles for valid moves
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

