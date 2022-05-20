#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from __future__ import print_function
import numpy as np
import os, csv, sys, random, time, string
import shutil
import os, termios, tty
import argparse
from time import sleep

# I think plenty of things in here can be redone to be a bit simpler and more streamlined, but it all pretty much works atm, and that was the initial goal. Overall, it's a pretty good start. It is Python, after all.
# Comments should probably be put in eventually as a well. It gets a bit confusing in parts.

class Go(object):
    def __init__(self, cursor=[18,0], starter=1, board_size=19, board_bg=44, show_debug=False):
        self.starting_color, self.board_size, self.board_bg, self.show_debug = starter, board_size, board_bg, show_debug
        self.moves, self.current_move, self.current_turn = [[]], [], starter
        self.white_score, self.black_score, self.white_moves, self.black_moves = 0, 0, 0, 0
        self.state_count, self.cursor_item = 0, cursor
        self.current_cursor, self.previous_cursor = [], []
        # self.previous, self.color = [], color
        self.swap, self.winner = True, False
        self.board = self.new_board()

        self.grids = { 41:90, 42:37, 43:90, 44:37, 45:37, 46:37, 47:90 }
        self.grid_fg = self.grids[self.board_bg]

        self.colors = { -1:"\033[%dm{}\033[0m" % (self.grid_fg), 0:"\033[30m{}\033[0m", 1:"{}", 2: "\033[95m{}\033[0m" }
        self.pieces_letters = { -1:"\033[%dm·\033[0m" % (self.grid_fg), 0:"\033[31m0\033[0m", 1:"\033[34m1\033[0m" }

    def new_board(self):
        flat = [-1]*(self.board_size*self.board_size)
        return np.reshape(flat, (self.board_size, self.board_size))

    def move_piece(self, cursor, direction):
        self.current_cursor = self.check_next_col_row(cursor, direction)
        self.cursor_item = self.current_cursor

        return self.current_cursor

    def check_next_col_row(self, cursor, direction):
        if direction == "right": cursor[1] = 0 if cursor[1] == self.board_size-1 else cursor[1]+1
        elif direction == "left": cursor[1] = self.board_size-1 if cursor[1] == 0 else cursor[1]-1
        elif direction == "up": cursor[0] = self.board_size-1 if cursor[0] == 0 else cursor[0]-1
        elif direction == "down": cursor[0] = 0 if cursor[0] == self.board_size-1 else cursor[0]+1
        
        return cursor

    def move_action(self, cursor):
        selected_spot  = [cursor[0], cursor[1]]
        selected_piece = self.board[cursor[0]][cursor[1]]

        if self.valid_place(selected_piece):
            self.board[cursor[0]][cursor[1]] = 0 if self.current_turn == 0 else 1
            self.previous_cursor = [selected_spot, selected_piece]
            self.change_turn()

    def valid_place(self, spot):
        if self.board[cursor[0]][cursor[1]] == -1:
            return True
        return False

    def change_turn(self):
        self.current_turn = 0 if self.current_turn == 1 else 1

    def set_new_cursor(self):
        return self.current_cursor

    def draw_board(self, cursor):
        os.system('clear')
        col_idx, row_num, letters = 0, self.board_size, ""
        print()
        # if self.show_debug:
        #     print(" self.previous_cursor:   {}".format(self.previous_cursor))
        #     print(" self.moves:             {} , {} , {} ".format(self.colors[1].format(self.blue_moves), self.colors[2].format(self.red_moves), self.total_moves))
        #     print(" self.current_turn:     {}, {}".format(self.turns[self.current_turn], self.current_turn))
        #     if self.selected:
        #         print(" self.selected:          {} ,{}, {} ".format(self.return_board_cords(self.selected), self.pieces[self.board[self.selected[0]][self.selected[1]]], self.board[self.selected[0]][self.selected[1]]))
        #     else:
        #         print(" self.selected:          · ")
        #     print(" self.cursor_item:       {}{} ,{}, {} ".format(string.ascii_lowercase[self.cursor_item[1]], -(self.cursor_item[0]-8), self.pieces[self.board[self.cursor_item[0]][self.cursor_item[1]]], self.board[self.cursor_item[0]][self.cursor_item[1]]))
        #     print(" self.available_moves:   {}".format(', '.join([self.colors[5].format(x) if x in self.available_capture_piece_moves else self.colors[4].format(x) if not x in self.available_castle_rooks else self.colors[5].format(x) for x in self.available_moves])))
            
        #     # print(" self.blue_captures:    {}".format(self.colors[2].format(','.join([self.colors[2].format(x) for x in self.blue_captures]))))
        #     # print(" self.red_captures:     {}".format(self.colors[1].format(','.join([self.colors[2].format(x) for x in self.red_captures]))))

        # red captures top
        # print("\n    {} {} {} {} {} {}".format(
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 6]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 3]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 2]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 1]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 4]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.red_captures if x == 5]) 
        # ))

        for row_index, row in enumerate(self.board):
            if -(self.cursor_item[0]-self.board_size) == row_num:
                print(" \033[95m{}{}\033[0m ".format(row_num, " " if (self.board_size >= 13 and row_num <= 9) else ""), end="") # pink number
            else:
                # print(self.cursor_item[0], -(self.cursor_item[0]-self.board_size), row_num)
                print(" \033[90m{}{}\033[0m ".format(row_num, " " if (self.board_size >= 13 and row_num <= 9) else ""), end="") # grey number

            for col_index, item in enumerate(row):
                current = [row_index, col_index]
                
                if row_index == 0:                      # top row
                    if col_index == 0:                      self.print_cursor_item("○", "┌", "●", "", "─", current, cursor, item)
                    elif col_index == self.board_size-1:    self.print_cursor_item("○", "┐", "●", "", "─", current, cursor, item)
                    else:                                   self.print_cursor_item("○", "┬", "●", "", "─", current, cursor, item)
                elif row_index == self.board_size-1:    # bottom row
                    if col_index == 0:                      self.print_cursor_item("○", "└", "●", "", "─", current, cursor, item)
                    elif col_index == self.board_size-1:    self.print_cursor_item("○", "┘", "●", "", "─", current, cursor, item)
                    else:                                   self.print_cursor_item("○", "┴", "●", "", "─", current, cursor, item)
                else:                                   # middle rows
                    if col_index == 0:                      self.print_cursor_item("○", "├", "●", "", "─", current, cursor, item)
                    elif col_index == self.board_size-1:    self.print_cursor_item("○", "┤", "●", "", "─", current, cursor, item)
                    else:                                   self.print_cursor_item("○", "┼", "●", "", "─", current, cursor, item)

                col_idx += 1
            row_num -= 1

            #print raw board right
            if self.show_debug:
                print("  {}".format(''.join([ self.pieces_letters[self.board[-row_num-1][x]] for x in range(0, self.board_size) ])), end="")

            print()
        
        # letters
        for i in range(0,self.board_size):
            if self.cursor_item[1] == i:
                letters += "\033[95m {}\033[0m".format(string.ascii_lowercase[i]) # pink letter
            else:
                letters += "\033[90m {}\033[0m".format(string.ascii_lowercase[i]) # grey letter

        print("   {}{}\n".format("" if (self.board_size >= 13) else "", letters), end="")

        # blue captures bottom
        # print("\n    {} {} {} {} {} {}".format(
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 12]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 9]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 8]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 7]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 10]),
        #     ''.join([self.pieces[x].replace(' ', '') for x in self.blue_captures if x == 11]) 
        # ))

        print("\n ⭠ ⭡⭣ ⭢  to move.\n SPACE to select.\n ESC to exit.\n")

    def print_item(self, item):
        print("\033[{}m{}\033[0m".format(self.board_bg, item), end="")
    
    def print_cursor_item(self, cursor_t, blank_t, item_t, extra_left, extra_right, current, cursor, item):
        self.print_item(self.colors[-1].format(extra_left))
        if current == cursor:
            self.print_item(self.colors[self.current_turn if item == -1 else item].format(cursor_t))
        else:
            self.print_item(self.colors[-1 if item == -1 else item].format(blank_t if item == -1 else item_t))
        self.print_item(self.colors[-1].format((extra_right if item == -1 else " ") if current[1] != self.board_size-1 else ""))

def play_console():
    global cursor

    go.draw_board(cursor)
    try:
        while True:
            k = getkey()
            if k == 'up':
                cursor = go.check_next_col_row(cursor, "up")
                go.draw_board(cursor)
            elif k == 'right':
                cursor = go.check_next_col_row(cursor, "right")
                go.draw_board(cursor)
            elif k == 'down':
                cursor = go.check_next_col_row(cursor, "down")
                go.draw_board(cursor)
            elif k == 'left':
                cursor = go.check_next_col_row(cursor, "left")
                go.draw_board(cursor)
            elif k == 'space':
                go.move_action(cursor)
                go.draw_board(cursor)
            elif k in ['esc']:
                sys.exit()

    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')
        sys.exit()

def sim():
    global cursor,turn

    # while True:
    #     checkers.play_random(turn)
    #     turn = -1 if turn == 1 else 1
    #     checkers.change_turn(turn)
    #     checkers.draw_board(cursor, turn)
    #     sleep(delay)

def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3: k = ord(b[2])
            else: k = ord(b)

            key_mapping = { 27:'esc', 32:'space', 68:'left', 67:'right', 66:'down', 65:'up', 127:'backspace' }
            return key_mapping.get(k, chr(k))

    except Exception: sys.exit()
    finally: termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Play Go in the terminal. Written in Python.")
    opt = ap._action_groups.pop()
    req = ap.add_argument_group('required arguments')
    opt.add_argument("-V","--version",action="store_true",help="show script version")
    opt.add_argument("-e","--extra",action="store_true",help="show extra game info after win")
    opt.add_argument("-d","--debug",action="store_true",help="show debug info about the game while playing")
    opt.add_argument("-t","--turn",const=1,type=int,choices=range(0,2),nargs="?",help="set starting piece. Blue/Red (0, 1)")
    opt.add_argument("-s","--size",const=1,type=int,choices=[9, 13, 19],nargs="?",help="choose to select the board size, instead of the default 19x19")
    opt.add_argument("-c","--color",const=1,type=int,choices=[41, 42, 43, 44, 45, 46, 47],nargs="?",help="choose to select the color for board background color, instead of random on load")
    ap._action_groups.append(opt)
    args = vars(ap.parse_args())

    starter, board_size, board_bg, show_debug = 0, 13, 47, True
    if args["version"]: sys.exit("v1.0.0")
    if args["turn"]: starter = args["turn"]
    if args["size"]:    board_size = args["size"]
    if args["color"]:   board_bg = args["color"]
    if args["debug"]:   show_debug = True
    cursor = [board_size-1, 0]

    go = Go(cursor=cursor, starter=starter, board_size=board_size, board_bg=board_bg, show_debug=show_debug)
    play_console()