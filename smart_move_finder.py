"""
Handling AI moves.
"""
import random


pieceScore = {"k": 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}

knightScores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishopScores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rookScores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queenScores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawnScores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piecePositionScores = {  "wn": knightScores,
                         "bn": knightScores[::-1],
                         "wb": bishopScores,
                         "bb": bishopScores[::-1],
                         "wq": queenScores,
                         "bq": queenScores[::-1],
                         "wr": rookScores,
                         "br": rookScores[::-1],
                         "wp": pawnScores,
                         "bp": pawnScores[::-1]}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

cache = {}

'''
A positive score means that the white player is winning. A negative score means that the black player is winning.
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                piecePositionScore = 0
                if piece[1] != "k":
                    piecePositionScore = piecePositionScores[piece][row][col]
                if piece[0] == "w":
                    score += pieceScore[piece[1]] + piecePositionScore
                if piece[0] == "b":
                    score -= pieceScore[piece[1]] + piecePositionScore
    
    if gs.white_to_move:
        opponentKingRow, opponentKingCol = gs.white_king_location
    else:
        opponentKingRow, opponentKingCol = gs.black_king_location
    
    #Check if game is in endgame
    whitePieces, blackPieces,endgame_phase = isEndgame(gs)

    if endgame_phase:
        #calculate distance to the closest edge
        min_dist = min(abs(opponentKingRow - 0), abs(opponentKingRow - 7), abs(opponentKingCol - 0), abs(opponentKingCol - 7))
        score += min_dist * 0.1

        if whitePieces <= 7:
            score -= 50
        if blackPieces <= 7:
            score += 50
    return score


def isEndgame(gs):
    """Checks if the game is in EndGame"""
    whitePieces = sum(piece != "--" for row in gs.board for piece in row if piece[0] == "w")
    blackPieces = sum(piece != "--" for row in gs.board for piece in row if piece[0] == "b")

    if whitePieces <= 7 or blackPieces <= 7 or (whitePieces + blackPieces <= 14):
        return whitePieces, blackPieces, True
    else:
        return whitePieces, blackPieces, False

def find_best_move(gs, validMoves, returnQueue):
    global nextMove
    nextMove = validMoves[0]
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, depth=DEPTH, alpha=-CHECKMATE, beta=CHECKMATE, turnMultiplier = 1 if gs.white_to_move else -1)
    returnQueue.put(nextMove)



def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # Check if the current position is in the cache
    position_key = str(gs.board) + str(gs.white_to_move)
    if position_key in cache:
        return cache[position_key]
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.make_move(move)
        nextMoves = gs.get_valid_moves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undo_move()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        
        if alpha >= beta:
            break
    # Cache the result for future use
    cache[position_key] = maxScore
    return maxScore

def find_random_move(validMoves):
    return random.choice(validMoves)