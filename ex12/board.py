WIDTH = 7
HEIGHT = 6
PLAYER1=1
PLAYER2=2

class Board:
    """ class for board type objects, has height,width and list of discs as
    attributes. the purpose of board is to contain discs and obtain the
    order of the discs within it"""

    def __init__(self):
        self.__height = HEIGHT
        self.__width = WIDTH
        self.__discs = []

    def __str__(self):
        """prints the board"""
        board = ""
        for row in range(self.__height):
            for col in range(self.__width):
                disc_col = self.cell_content((col, row))
                if disc_col:
                    board += str(disc_col) + "# "
                else:
                    board += "__ "
            if row < self.__height - 1:
                board += "\n"
        return board

    def reset_board(self):
        """resets the board to be empty"""
        self.__discs=list()

    def cell_content(self, coordinate):
        """
        :param coordinate:
        :return: disc color if a disc is found in coordinate else return None
        """
        for disc in self.__discs:
            if disc.get_location() == coordinate:
                return disc.get_color()

    def all_board_cells(self):
        """returns a list of all the cells in board."""
        all_b_cells = []
        for i in range(self.__height):
            for j in range(self.__width):
                all_b_cells.append((j, i))
        return all_b_cells

    def is_col_full(self, col):
        """returns True if the given column is full, False otherwise"""
        c = 0
        for row in range(self.__height):
            cur_cell = self.cell_content((col, row))
            if cur_cell:
                c += 1
        if c == self.__height:
            return True
        return False

    def all_disc_cells(self):
        """returns a list of all the discs locations in board"""
        all_discs = []
        for disc in self.__discs:
            all_discs.append(disc.get_location())
        return all_discs

    def add_disc(self, disc, col):
        """add a new disc to the board if possible.returns True upon success,
         False otherwise"""
        if not self.is_col_full(col) and disc.get_location() in \
                self.all_board_cells():
            self.__discs.append(disc)
            self.move_disc(disc, col)
            return True
        return False

    def move_disc(self, disc, col):
        """moves a disc to the lower position available in board in the
        given column. returns True upon success, False otherwise"""
        for row in range(self.__height, -1, -1):
            if not self.cell_content((col, row)):
                disc.move_disc((col, row))
                return True
        return False

    def create_board(self):
        """creates a list of lists representing the board and all it's disc
        in their location. returns the board"""
        one_row = []
        board = []
        for row in range(self.__height):
            for col in range(self.__width):
                cell_disc = self.cell_content((col, row))
                if cell_disc:
                    one_row.append(str(cell_disc))
                else:
                    one_row.append("_")
            board.append(one_row[:])
            one_row = []
        return board

    def is_win(self):
        """returns the number of the winning player, if theres is no winner
        returns None"""
        board = self.create_board()
        win1 = self.check_win_up_right(board,str(PLAYER1)) \
               or self.check_win_down_right(board,str(PLAYER1))\
               or self.check_win_col(board,str(PLAYER1))\
               or self.check_win_row(board, str(PLAYER1))
        win2 = self.check_win_up_right(board,str(PLAYER2))\
               or self.check_win_down_right(board, str(PLAYER2)) or \
               self.check_win_col(board,str(PLAYER2)) \
               or self.check_win_row(board, str(PLAYER2))
        if win1:
            return PLAYER1
        elif win2:
            return PLAYER2

    def win_streak(self):
        """returns the locations of the 4 winning discs"""
        board = self.create_board()
        winner = str(self.is_win())
        if winner:
            return self.check_win_row(board, winner) or self.check_win_col(
                board, winner) or self.check_win_down_right(board, winner) \
                   or self.check_win_up_right(board, winner)

    def check_win_row(self, board, winner):
        """checks for a victory in a row if exists returns the locations of
        the 4 winning discs"""
        for y in range(self.__height):
            for x in range(self.__width - 3):
                if board[y][x] == winner and board[y][x + 1] == winner \
                        and board[y][x + 2] == winner \
                        and board[y][x + 3] == winner:
                    return [(y, x), (y, x + 1), (y, x + 2), (y, x + 3)]

    def check_win_col(self, board, winner):
        """checks for a victory in a column if exists returns the locations of
                the 4 winning discs"""
        for y in range(self.__height - 3):
            for x in range(self.__width):
                if board[y][x] == winner and board[y + 1][x] == winner \
                        and board[y + 2][x] == winner \
                        and board[y + 3][x] == winner:
                    return [(y, x), (y + 1, x), (y + 2, x), (y + 3, x)]

    def check_win_down_right(self, board, winner):
        """checks for a victory in a down right diagonal if exists returns
        the locations of the 4 winning discs"""
        for y in range(self.__height - 3, ):
            for x in range(self.__width - 3):
                if board[y][x] == winner and board[y + 1][x + 1] == winner \
                        and board[y + 2][x + 2] == winner \
                        and board[y + 3][x + 3] == winner:
                    return [(y, x), (y + 1, x + 1), (y + 2, x + 2),
                            (y + 3, x + 3)]

    def check_win_up_right(self, board, winner):
        """checks for a victory in an up right diagonal if exists returns
        the locations of the 4 winning discs"""
        for y in range(3, self.__height):
            for x in range(self.__width - 3):
                if board[y][x] == winner and board[y - 1][x + 1] == winner \
                        and board[y - 2][x + 2] == winner \
                        and board[y - 3][x + 3] == winner:
                    return [(y, x), (y - 1, x + 1), (y - 2, x + 2), (y - 3,
                                                                     x + 3)]
