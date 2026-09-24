"""
Handling AI moves.
"""
from multiprocessing import Process, Queue
import random

from games.chess.game_state import GameState
from games.chess.move import Move
from .scoring_consts import *

class Ai:
    def __init__(self):
        self.nextMove:Move
        self.cache = {}
        
    def find_move(self, gs: GameState, ai_valid_moves: list[Move]):
        return_queue = Queue()
        move_finder_process = Process(target=self.find_best_move, args=(gs, ai_valid_moves, return_queue))
        move_finder_process.start()
        if not move_finder_process.is_alive():
            print('Done thinking!!!')
            if return_queue.empty():
                ai_move = return_queue.get()
            else:
                ai_move = self.find_random_move(ai_valid_moves)
                print("no moves were found, returning a random move")
            return ai_move
        
    '''
    A positive score means that the white player is winning. A negative score means that the black player is winning.
    '''
    def scoreBoard(self, gs: GameState) -> float:
        if gs.checkmate:
            if gs.white_to_move:
                return -CHECKMATE
            else:
                return CHECKMATE
        elif gs.stalemate:
            return STALEMATE

        score = 0.0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                piece = gs.board[row][col]
                if piece != "--":
                    piecePositionScore = 0.0
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
        whitePieces, blackPieces,endgame_phase = self.isEndgame(gs)

        if endgame_phase:
            #calculate distance to the closest edge
            min_dist = min(abs(opponentKingRow - 0), abs(opponentKingRow - 7), abs(opponentKingCol - 0), abs(opponentKingCol - 7))
            score += min_dist * 0.1

            if whitePieces <= 7:
                score -= 50
            if blackPieces <= 7:
                score += 50
        return score


    def isEndgame(self, gs: GameState) -> bool:
        """Checks if the game is in EndGame"""
        whitePieces = sum(piece != "--" for row in gs.board for piece in row if piece[0] == "w")
        blackPieces = sum(piece != "--" for row in gs.board for piece in row if piece[0] == "b")

        if whitePieces <= 7 or blackPieces <= 7 or (whitePieces + blackPieces <= 14):
            return whitePieces, blackPieces, True
        else:
            return whitePieces, blackPieces, False

    def find_best_move(
        self,
        gs: GameState,
        validMoves: list[Move],
        returnQueue: Queue
    ):
        self.nextMove = validMoves[0]
        random.shuffle(validMoves)
        turnMultiplier = 1 if gs.white_to_move else -1
        self.findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, turnMultiplier)
        returnQueue.put(self.nextMove)

    def findMoveNegaMaxAlphaBeta(
        self, 
        gs:GameState, 
        validMoves: list[Move], 
        depth: int, 
        alpha, 
        beta, 
        turnMultiplier
    ):
        if depth == 0:
            return turnMultiplier * self.scoreBoard(gs)
        
        # Check if the current position is in the self.cache
        position_key = str(gs.board) + str(gs.white_to_move)
        if position_key in self.cache:
            return self.cache[position_key]
        
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.make_move(move)
            nextMoves = gs.get_valid_moves()
            score = -self.findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    self.nextMove = move
            gs.undo_move()
            if maxScore > alpha: #pruning happens
                alpha = maxScore
            
            if alpha >= beta:
                break
        # self.cache the result for future use
        self.cache[position_key] = maxScore
        return maxScore

    def find_random_move(self, validMoves):
        return random.choice(validMoves)