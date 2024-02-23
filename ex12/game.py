from .disc import Disc
from .board import Board
COLUMNS = [0, 1, 2, 3, 4, 5, 6]
PLAYER1=1
PLAYER2=2

class Game:
    """this class is responsible for all the game rules and holds the
    current board, makes sure that only valid moves are being made and
    updates the board accordingly"""

    def __init__(self):
        self.__board = Board()
        self.__current_player = PLAYER1


    def make_move(self, column):
        """if possible puts a disc in the given column and returns the
        disc's location after the move,
        else raises an exception"""
        disc = Disc(self.__current_player, (column, 0))
        if not self.__board.add_disc(disc, column) or self.__board \
                .move_disc(disc, column) is False or column not in COLUMNS:
            raise Exception("Illegal move.")
        if self.__current_player == PLAYER1:
            self.__current_player = PLAYER2
        else:
            self.__current_player = PLAYER1
        return disc.get_location()


    def get_winner(self):
        """returns 0 upon a draw, or the number of the winning player when
        the game is won"""
        win_status=self.__board.is_win()
        if len(self.__board.all_board_cells()) == len(
                self.__board.all_disc_cells())and not win_status:
            return 0
        else:
            return win_status

    def get_player_at(self, row, col):
        """returns the 'color' of the disc in the current location. if the
        location is empty raises an exception"""
        if (col, row) not in self.__board.all_board_cells():
            raise Exception("Illegal location")
        return self.__board.cell_content((col, row))

    def get_current_player(self):
        """returns the current player"""
        return self.__current_player

    def get_board(self):
        """returns the board"""
        return self.__board

    def reset_game(self):
        """resets the game board to an empty board"""
        self.__board.reset_board()


