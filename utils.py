import math
import random
import numpy as np

#Czy chcemy uruchomić program z zapisywaniem czasu odpowiedzi
TESTIMG_MODE = False

#wielkosc planszy
HEIGHT = 6
WIDTH = 7

#stale opisujace gracza i sztuczna inteligencje
PLAYER = 0
AI = 1
PLAYER_SYMBOL = 1
AI_SYMBOL = 2
#Stała określająca głębokość rekurencji
DEPTH = 4

#stale mowiace jaki symbol oznacza puste miejsce i ile pol nalezy sprawdzic w przypadku szukania connect 4
EMPTY = 0
CHECK = 4

#funkcja tworzaca plansze
def CreateBoard():
    board = np.zeros((HEIGHT, WIDTH), dtype=int)
    return board

#funkcja wykonujaca ruch
def Move(board, row, col, symbol):
    board[row][col] = symbol

#funkcja sprawdzajaca czy mozna dokonac ruchu w tej kolumnie
def CheckMovePossibility(board, col):
    return board[HEIGHT -1][col] == 0

#funkcja znajdujaca pierwszy wolny rzad w danej kolumnie
def FindRow(board, col):
    for r in range(HEIGHT):
        if board[r][col] == 0:
            return r

#funkcja wyswietlajaca plansze
def DisplayBoard(board):
    for row in range(HEIGHT):
        for column in range(WIDTH):
            print(board[HEIGHT - row - 1][column], "  ", end="")

        print("\n")

#funkcja sprawdzajaca czy zostalo dokonane connect 4
def CheckWin(board, symbol):

    #w poziomie
    for c in range(WIDTH - 3):
        for r in range(HEIGHT):
            if board[r][c] == symbol and board[r][c+1] == symbol and board[r][c+2] == symbol and board[r][c+3] == symbol:
                return True

    #pionie
    for c in range(WIDTH):
        for r in range(HEIGHT - 3):
            if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
                return True

    #ukosnie w prawo do gory
    for c in range(WIDTH - 3):
        for r in range(HEIGHT - 3):
            if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
                return True

    #ukosnie w prawo w dol
    for c in range(WIDTH - 3):
        for r in range(3, HEIGHT):
            if board[r][c] == symbol and board[r-1][c+1] == symbol and board[r-2][c+2] == symbol and board[r-3][c+3] == symbol:
                return True

#funkcja oceniajaca sytuacje w tablicy
def CalculateScore(array, symbol):
    score = 0
    opponent = PLAYER_SYMBOL
    if symbol == PLAYER_SYMBOL:
        opponent = AI_SYMBOL

    if array.count(symbol) == 4:
        score += 500

    elif array.count(symbol) == 3 and array.count(EMPTY) == 1:
        score += 4

    elif array.count(symbol) == 2 and array.count(EMPTY) == 2:
        score += 1

    if array.count(opponent) == 3 and array.count(EMPTY) == 1:
        score -= 4


    return score

#funkcja oceniajaca pozycje
def PositionScore(board, symbol):
    score = 0

    array_center = [board[i][WIDTH//2] for i in range(HEIGHT)]
    count_center = array_center.count(symbol)
    score += count_center * 2

    for r in range(HEIGHT):
        help = [[board[r][i] for i in range(WIDTH)]]
        for c in range(WIDTH-3):
            check = [help[0][i] for i in range(c, c+CHECK)]
            score += CalculateScore(check, symbol)

    for c in range(WIDTH):
        help = [[board[i][c] for i in range(HEIGHT)]]
        for r in range(HEIGHT-3):
            check = [help[0][i] for i in range(r, r+CHECK)]
            score += CalculateScore(check, symbol)

    for r in range(HEIGHT-3):
        for c in range(WIDTH-3):
            check = [board[r+i][c+i] for i in range(CHECK)]
            score += CalculateScore(check, symbol)

    for r in range(HEIGHT-3):
        for c in range(WIDTH-3):
            check = [board[r+3-i][c-i] for i in range(CHECK)]
            score += CalculateScore(check, symbol)
    return score

#funkcja informujaca o wolnych polach
def FreeSlots(board):
    freeSlots = []
    for c in range(WIDTH):
        if CheckMovePossibility(board, c):
            freeSlots.append(c)
    return freeSlots

#funkcja sprawdzajaca czy nastapil koniec gry
def EndGame(board):
    return CheckWin(board, PLAYER_SYMBOL) or CheckWin(board, AI_SYMBOL) or len(FreeSlots(board)) == 0

#funkcja znajdujaca optynamalny ruch
def OptimalMove(board, symbol):
    freeSlots = FreeSlots(board)
    bestScore = -99999
    bestColumn = random.choice(freeSlots)
    for col in freeSlots:
        row = FindRow(board, col)
        help = board.copy()
        Move(help, row, col, symbol)
        score = PositionScore(help, symbol)
        if score > bestScore:
            bestScore = score
            bestColumn = col

    return bestColumn
