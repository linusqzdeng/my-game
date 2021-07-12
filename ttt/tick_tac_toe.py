# This is the "Tick Tac Toe" game page! The game will start from
# asking the player which size of the game board they would like to
# have (classic sqaure board is 3 x 3)

#  --- --- ---
# |   |   |   |
#  --- --- ---
# |   |   |   |
#  --- --- ---
# |   |   |   |
#  --- --- ---

import numpy as np

instruction = """
Welcome to the Tick-Tac-Toe game! This game does not have a
graphical user interface therefore all movement is done by using
comman line. As a simple game, players would win the game once their
noughts "O" or crosses "X" are placed 3 in a row, a column or a diagonal.
To place your "O" or "X", simply input coordinate of the grid you intend
to move. E.g. if player 1 wants to put a cross on the right corner, a
a correct input ought to be "1 3", which represents "row 1 column 3" and
needs to be separated by a space.
"""

rows = " ---"
columns = "| "  # define the shape of row and column

player1_symbol = "X"
player2_symbol = "O"  # define the each player's symbol


def game_start():
    game_board = np.array([[" " for _ in range(3)]] * 3)
    draw_board(game_board)

    return game_board


def draw_board(board, n=3):
    """Print out a game board in terms
    of the given integer n, which represent
    the width and length of the board
    """
    for i in range(n):
        print(rows * n)
        print(columns + board[i][0] + " " + columns + board[i][1] + " " + columns + board[i][2] + " " + columns)

    print(rows * n)


def move(board, player):
    """Receiving the coordinate of player's intended
    placement and detect if the grid is available at 
    the same time. Return the new game board with play's 
    move.
    """
    if player == 1:
        symbol = player1_symbol
    if player == 2:
        symbol = player2_symbol

    while True:

        coor = list(map(int, input("Which row and which column: ").strip().split()))

        if board[coor[0] - 1][coor[1] - 1] == " ":
            board[coor[0] - 1][coor[1] - 1] = symbol
            break
        else:
            print("Sorry! The spot has been taken please choose another one")
            continue

    return board


def all_same(items):
    """Detect if all items are the same object"""
    return len(set(items)) == 1


def is_won(board):
    """Separately detect if players have won the game
    by row, column or diagonal
    """
    for i in board:  # detect row matched
        if all_same(i) and i[0] != " ":
            return i[0]

    for i in np.transpose(board):  # detect column matched
        if all_same(i) and i[0] != " ":
            return i[0]

    if board[1][1] != " ":  # detect diagonal matched
        if board[1][1] == board[0][0] == board[2][2]:
            return board[1][1]
        elif board[1][1] == board[0][2] == board[2][0]:
            return board[1][1]

    return 0


def switch_player(n=2):

    if n == 1:
        return 2
    if n == 2:
        return 1


def game_over(board, game_round):
    """Check if the there is a winner and printout the
    congratulation messasge
    """

    if game_round == 1:
        print("Game Start! Player 1 takes the first move!")

    if game_round > 1:
        if is_won(board) == player1_symbol:
            print("Game over! Player 1 won!")
            winner = 1
            return True

        elif is_won(board) == player2_symbol:
            print("Game over! Player 2 won!")
            winner = 1
            return True

        else:
            return False


player = 1
winner = 0
game_round = 1

while True:  # start the game loop

    if game_round == 1:
        print(instruction)
        board = game_start()

    if (10 > game_round >= 1) and (not game_over(board, game_round)):
        print(f"It's player {player}'s move")
        board = move(board, player)
        draw_board(board)
        player = switch_player(player)
        game_round += 1

    elif (game_round == 10) and winner == 0:  # check if it's draw
        print("Game over! Draw!")
        break

    else:
        break
