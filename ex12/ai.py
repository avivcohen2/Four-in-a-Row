import random

COLUMNS=[0,1,2,3,4,5,6]

class AI:
    """class for ai type objects, generates valid moves for the game 'four
    in a row' """

    def __init__(self, game, player):
        self.__game = game
        self.__player = player

    def find_legal_move(self, timeout=None):
        """finds a legal move in the game and returns it, raises and
        exception if the are no valid moves"""
        if self.__game.get_winner() is not None:
            raise Exception("No possible AI moves.")
        ai_move = random.choice(COLUMNS)
        while self.__game.get_player_at(0,ai_move):
            ai_move = random.choice(COLUMNS)
        return ai_move

    def get_player(self):
        return self.__player

    def get_last_found_move(self):
        pass
