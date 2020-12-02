import math
import random
from timeit import default_timer as timer

import minmax
import utils

print("Chcesz zmienić rozmiar planszy? y/n")
response = input()
while not (response == 'y' or response == 'n'):
    response = input("y/n: ")

if response == 'y':
    while True:
        utils.WIDTH = int(input("Szerokość: "))
        utils.HEIGHT = int(input("Wysokość: "))

        if utils.WIDTH > 4 and utils.HEIGHT > 4:
            break

        print("Wysokość oraz szerokość muszą być większe od 4.")

print("Czy chcesz zapisywać czasy ospowiedzi? y/n")
response = input()
while not (response == 'y' or response == 'n'):
    response = input("y/n: ")

if response == 'y':
    utils.TESTIMG_MODE = True
    utils.DEPTH = int(input("Podaj głębokość przeszukiwania [4]: "))


#tworznie tablicy i ustawianie potrzebnych rzeczy
board = utils.CreateBoard()
utils.DisplayBoard(board)
gameOver = False
turn = random.randint(utils.PLAYER, utils.AI)

if utils.TESTIMG_MODE:
    time_sheet = open("Times.txt", 'a')
    message = "Depth " + str(utils.DEPTH) + '\n'
    time_sheet.write(message)

    if turn == utils.AI:
        start = timer()

while not gameOver:

#ruch gracza
    if turn == utils.PLAYER:
        move = int(input("Your move: "))
        print("\n")
        while move < 1 or move > utils.WIDTH:
            move = int(input("Invalid move, try again: "))
            print("\n")

        move -= 1
        if utils.CheckMovePossibility(board, move):
            row = utils.FindRow(board, move)
            utils.Move(board, row, move, utils.PLAYER_SYMBOL)

            if utils.CheckWin(board, utils.PLAYER_SYMBOL):
                print("YOU WIN!!!")
                gameOver = True

            turn += 1
            utils.DisplayBoard(board)

            if utils.TESTIMG_MODE:
                start = timer()

#ruch sztucznej inteligencji
    if turn == utils.AI and not gameOver:

        col, minmaxValue = minmax.Minmax(board, utils.DEPTH, -math.inf, math.inf, True)

        if utils.CheckMovePossibility(board, col):
            row = utils.FindRow(board, col)
            utils.Move(board, row, col, utils.AI_SYMBOL)

            if utils.CheckWin(board, utils.AI_SYMBOL):
                print("AI WINS!!!")
                gameOver = True

            print("AI move: ", col+1, "\n")
            utils.DisplayBoard(board)

            turn -= 1

            if utils.TESTIMG_MODE:
                end = timer()
                time_sheet.write(str(end - start))
                time_sheet.write("\n")

if utils.TESTIMG_MODE:
    time_sheet.write("\n\n")
    time_sheet.close()
