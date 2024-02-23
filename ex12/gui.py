import time
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk

from .ai import AI
from .game import Game


class Screen:
    """this class is responsible for all the graphical interface of the
    game, displays the game board and every move made in the game."""

    def __init__(self):
        self.__root = tk.Tk()
        self.__game = Game()
        self.__player = self.__game.get_current_player()
        self.blank = ImageTk.PhotoImage(Image.open("ex12//blank.png"))
        self.boardimage = ImageTk.PhotoImage(Image.open("ex12//b.png"))
        self.blueball = ImageTk.PhotoImage(Image.open("ex12//blueball.png"))
        self.redball = ImageTk.PhotoImage(Image.open("ex12//redball.png"))
        self.menuimage = ImageTk.PhotoImage(Image.open('ex12//main_menu.png'))
        self.exit = ImageTk.PhotoImage(Image.open('ex12//exit.png'))
        self.pvpimage = ImageTk.PhotoImage(Image.open('ex12//pp.png'))
        self.cpcimage = ImageTk.PhotoImage(Image.open('ex12//cpc.png'))
        self.pvcimage = ImageTk.PhotoImage(Image.open('ex12//pcp.png'))
        self.cvpimage = ImageTk.PhotoImage(Image.open('ex12//pcvsplayer.png'))
        self.__color_match = {1: self.redball, 2: self.blueball}
        self.__red_blue_match = {1: "#910c00", 2: "#002f7c"}
        self.main_menu = tk.Label(self.__root, image=self.menuimage)
        self.__endGame = False
        self.__ai_1 = AI(self.__game, 1)
        self.__ai_2 = AI(self.__game, 2)
        self.__game_mode = None
        self.__mode_dict = {1: self.player_vs_player, 2: lambda
            x=self.__ai_1: self.player_vs_pc(x),
                            3: lambda x=self.__ai_2: self.player_vs_pc(x),
                            4: self.pc_vs_pc}

    def init_graphics(self):
        """initiates the main menu graphics"""
        self.__root.title("Four in a Row!")
        self.main_menu.grid(row=0, column=0, columnspan=3, rowspan=6)
        pvpbutton = tk.Button(self.__root, image=self.pvpimage,
                              command=self.player_vs_player, bg="#84d0ff")
        pvpbutton.grid(row=4, column=0)
        cvcbutton = tk.Button(self.__root, image=self.cpcimage,
                              command=self.pc_vs_pc, bg="#84d0ff")
        cvcbutton.grid(row=4, column=1)
        pvcbutton = tk.Button(self.__root, image=self.cvpimage,
                              command=lambda ai=self.__ai_1: self.player_vs_pc(
                                  ai), bg="#84d0ff")
        pvcbutton.grid(row=5, column=0)
        cvpbutton = tk.Button(self.__root, image=self.pvcimage,
                              command=lambda ai=self.__ai_2: self.player_vs_pc(
                                  ai), bg="#84d0ff")
        cvpbutton.grid(row=5, column=1)
        quit_button = tk.Button(self.__root, image=self.exit,
                               command=self._handle_exit, bg="#84d0ff")
        quit_button.grid(row=5, column=2)

    def start_screen(self):
        """starts the main menu"""
        self.__root.mainloop()

    def make_board(self):
        """creates the graphical interface of the game board"""
        self.__endGame = False
        self.game_root = tk.Toplevel(self.__root, bg="#84d0ff")
        self.game_root.protocol("WM_DELETE_WINDOW", self._close_game)
        exit_game = tk.Button(self.game_root, image=self.exit,
                               command=self._close_game)
        exit_game.grid(row=4, column=8,rowspan=2)
        self.player_mark = tk.Label(self.game_root,
                                    text="Player" + str(self.__player),
                                    bg=self.__red_blue_match[self.__player],
                                    fg="white",font=("impact",15))
        self.player_mark.grid(row=2, column=8)
        for i in range(7):
            for j in range(6):
                blanc = tk.Label(self.game_root, image=self.blank,
                                 bg="#42210B")
                blanc.grid(row=j, column=i, sticky="ew")
        self.background = tk.Label(self.game_root, image=self.boardimage)
        self.background.grid(row=0, column=0, rowspan=6, columnspan=7)
        self.frame = tk.Frame(self.game_root, height=20, width=80)
        self.background.bind("<Motion>", self.mark_column)
        self.__root.withdraw()

    def player_vs_player(self):
        """starts a game of players versus player"""
        self.__game_mode = 1
        self.make_board()
        self.background.bind("<Button-1>", self.mouse_callback)
        self.game_root.mainloop()

    def player_vs_pc(self, ai):
        """starts a game of player versus the ai"""
        if ai == self.__ai_1:
            self.__game_mode = 2
        else:
            self.__game_mode = 3
        self.make_board()
        if self.__player != ai.get_player():
            self.background.bind("<Button-1>", lambda event, ai=ai:
            self.mouse_callback(event, ai))
        else:
            self.background.unbind("<Button-1>")
            self.make_ai_move(ai)
        self.game_root.mainloop()

    def pc_vs_pc(self):
        """starts a game of ai versus the ai"""
        self.__game_mode = 4
        self.make_board()
        while self.__endGame is False:
            if self.__player == 1:
                self.make_ai_move(self.__ai_1)
            else:
                self.make_ai_move(self.__ai_2)
        self.game_root.mainloop()

    def make_ai_move(self, ai):
        """makes an ai move"""
        if self.__endGame is False:
            ai_loc = ai.find_legal_move()
            disc = tk.Label(self.game_root,
                            image=self.__color_match[
                                self.__game.get_current_player()],
                            bg="#42210B")
            self.background.unbind("<Button-1>")
            self.background.unbind("<Motion>")
            self.game_root.update()
            time.sleep(0.5)
            try:
                loc = self.__game.make_move(ai_loc)
                self.__player = self.__game.get_current_player()
                self.player_mark.config(bg=self.__red_blue_match[self.__player],
                                        text="Player" + str(self.__player))
                disc.grid(row=loc[1], column=loc[0])
                self.game_root.update()
            except:
                tk.messagebox.showerror("Error", "column is full")
            self.win_status()

            if self.__game_mode in [2, 3] and self.__endGame is False:
                self.background.bind("<Button-1>", lambda event, ai=ai:
                            self.mouse_callback(event, ai))
                self.background.bind("<Motion>", self.mark_column)

    def mouse_callback(self, event, ai=None):
        """makes a move according to the users press location on the board"""
        disc = tk.Label(self.game_root,
                        image=self.__color_match[self.__game.get_current_player()],
                        bg="#42210B")

        try:
            column=event.x//100
            if column<7 and column>=0:
                loc = self.__game.make_move(column)
                self.__player = self.__game.get_current_player()
                self.player_mark.config(bg=self.__red_blue_match[self.__player],
                                        text="Player" + str(self.__player))
                self.frame.config(bg=self.__red_blue_match[self.__player])
                disc.grid(row=loc[1], column=loc[0])
        except:
            tk.messagebox.showerror("Error", "column is full")
        self.game_root.update()
        self.win_status()

        if self.__game_mode != 1 and self.__endGame is False:
            self.make_ai_move(ai)

    def mark_column(self, event):
        """marks the column that the players is 'standing' on"""
        col = event.x // 100
        self.frame.config(bg=self.__red_blue_match[self.__player])
        if col <= 6:
            self.frame.grid(row=6, column=col, sticky="s")

    def mark_winner(self, winner):
        """marks the 4 winning disc on the board"""
        self.background.unbind("<Button-1>")
        self.player_mark.config(bg=self.__red_blue_match[winner],
                                text="Player" + str(winner), fg="white",
                                font=("impact", 25))
        for loc in self.__game.get_board().win_streak():
            win = tk.Label(self.game_root, image=self.__color_match[winner],
                           bg="yellow")
            win.grid(row=loc[0], column=loc[1])

    def run_new_game(self):
        """runs a new game of the same type"""
        self.__endGame = False
        play = self.__mode_dict[self.__game_mode]
        self._close_game()
        play()

    def win_status(self):
        """when a game is finished asks if the user wants to
         play another of the same type"""
        winner = self.__game.get_winner()
        if winner == 0:
            self.__endGame = True
            self.player_mark.config(bg="grey", text="Tie", fg="white",
                                    font=("impact", 25))
            self.background.unbind("<Button-1>")
            answer = tk.messagebox.askquestion("It's a tie", "would you like"
                                                             " to play again?", )
            self._close_game()
            if answer == "yes":
                self.run_new_game()
            else:
                self._close_game()
        if winner:
            self.__endGame = True
            self.mark_winner(winner)
            answer = tk.messagebox.askquestion("player " + str(winner)
                                               + " has won",
                                               "would you like to  play again?")
            self._close_game()
            if answer == "yes":
                self.run_new_game()
            else:
                self._close_game()

    def _close_game(self):
        """closes the current game(top level) and returns to main_menu"""
        self.__endGame=True
        self.__game.reset_game()
        self.game_root.destroy()
        self.game_root.quit()
        self.__root.update()
        self.__root.deiconify()

    def _handle_exit(self):
        """exits the entire game"""
        self.__root.destroy()
        self.__root.quit()

