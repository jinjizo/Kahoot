#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    May 03, 2019 05:47:25 PM +0300  platform: Windows NT

import sys
import Server
import time
import tkMessageBox

players = []
timer = None
correct = None
player = None
spinbox1 = None
spinbox2 = None
checkbox = None

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def login():
    global player, root, players
    x = len(players)
    if checkbox.get():
        players = Server.update_login(True)
    else:
        players = Server.update_login()
    if x != len(players):
        player = (players[len(players)-1], 0)
        w.log.config(state="normal")
        w.log.insert("end", player[0] + " has successfully joined the game.\n\n")
        w.log.config(state="disabled")
    root.after(100, login)


def set_Tk_var():
    global spinbox1, spinbox2, checkbox
    spinbox1 = tk.StringVar()
    spinbox2 = tk.StringVar()
    checkbox = tk.IntVar()


def new_question():
    global root, player, correct, timer, spinbox1, spinbox2
    if not timer:
        if player:
            try:
                correct = int(spinbox1.get())
                timer = int(time.time()) + int(spinbox2.get())
                Server.new_question(spinbox2.get())
                w.log.config(state="normal")
                w.log.insert("end", "Posted the question demonstration\nCorrect answer: %s              Timer: %s\n\n" % (correct, timer - int(time.time())))
                w.log.config(state="disabled")
                w.Button1.config(state="disable")
                root.after(150, receive)
                sys.stdout.flush()
            except Exception:
                tkMessageBox.showerror("Error!", "You must choose the correct answer and the duration of the question!")
        else:
            tkMessageBox.showerror("Error!", "You haven't successfully joined in yet!")
    else:
        tkMessageBox.showerror("Error!", "There is currently another question in progress!")


def finito():
    global root, player, correct, timer, spinbox1, spinbox2
    if not timer:
        if player:
                Server.end_game()
                Server.new_question(0)
                w.log.config(state="normal")
                w.log.insert("end", "Game is done.\n\n")
                w.log.config(state="disabled")
                sys.stdout.flush()
        else:
            tkMessageBox.showerror("Error!", "You haven't successfully joined in yet!")
    else:
        tkMessageBox.showerror("Error!", "There is currently a question in progress!")


def receive():
    global timer, correct, player
    if timer < int(time.time()):
        answer = Server.results(correct, 10)
        if answer[player[0]] != player[1]:
            was_correct = " has answered the correct answer."
            player = (player[0], answer[player[0]])
        else:
            was_correct = " either answered a wrong answer, or he didn't answer at all."

        w.log.config(state="normal")
        w.log.insert("end", player[0] + str(was_correct) + "\n\n")
        w.log.config(state="disabled")
        w.Button1.config(state="normal")
        timer = None
    else:
        Server.receive()
        time_change = log_timer(w.log.get("1.0", "end"))
        w.log.config(state="normal")
        w.log.delete('1.0', 'end')
        w.log.insert("end", time_change + "\n\n")
        w.log.config(state="disabled")
        root.after(100, receive)


def log_timer(current):
    messages = current.split("\n\n")
    messages.pop()
    before = messages[::-1][1:][::-1][:]
    self = messages[::-1][0][:]
    new_last = "Timer: ".join([self.split("Timer: ")[0]] + [str(timer - int(time.time()))])
    before.append(new_last)
    return '\n\n'.join(before)


def update():
    global root, w
    Server.receive()
    root.after(200, update)

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import unknown
    unknown.vp_start_gui()




