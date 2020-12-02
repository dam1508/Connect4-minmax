import math
import random

import utils




def Minmax(board, depth, alpha, beta, maxPlayer):
    freeSlots = utils.FreeSlots(board)
    endGame = utils.EndGame(board)
    if depth == 0 or endGame:
        if endGame:
            if utils.CheckWin(board, utils.AI_SYMBOL):
                return (None, 999999999)
            elif utils.CheckWin(board, utils.PLAYER_SYMBOL):
                return (None, -999999999)
            else:
                return(None, 0)

        else:
            return (None, utils.PositionScore(board, utils.AI_SYMBOL))

    if maxPlayer:
        value = -math.inf
        column = random.choice(freeSlots)
        for col in freeSlots:
            row = utils.FindRow(board, col)
            help = board.copy()
            utils.Move(help, row, col, utils.AI_SYMBOL)
            newScore = Minmax(help, depth - 1, alpha, beta, False)[1]
            if newScore > value:
                value = newScore
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return [column, value]

    else:
        value = math.inf
        column = random.choice(freeSlots)
        for col in freeSlots:
            row = utils.FindRow(board, col)
            help = board.copy()
            utils.Move(help, row, col, utils.PLAYER_SYMBOL)
            newScore = Minmax(help, depth-1, alpha, beta, True)[1]
            if newScore < value:
                value = newScore
                column = col
            beta = min(beta, value)
            if(alpha >= beta):
                break
        return [column, value]
