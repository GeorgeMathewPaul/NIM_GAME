import PIL  # Python image library
from tkinter import *  # Python Tk GUI toolkit
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import ImageTk, Image
from NIMGAMEpcbrain import Nim
from NIMGAMEsqlcon import User
import winsound
import mysql.connector

nim = Nim()  # nim-object and Nim()-class
user = User()  # Same as above


def redisplay(mybutton):
    global nim
    global mymatchimage
    global gamestatus
    for i in range(5):
        for m in range(5):
            if nim.matrix[i][m] == 1:
                mybutton[i][m]["state"] = NORMAL
            else:
                mybutton[i][m]["state"] = DISABLED
    if nim.totalcount == 0 or (nim.IsUserMove == False and nim.usermoved == False and nim.firstmove == False):
        pc_move["state"] = DISABLED
    else:
        pc_move["state"] = NORMAL
    gamestatus["text"] = nim.gamestatus


def btn_remove(row, column):
    global mybutton
    global nim
    if nim.IsUserMove == True and (nim.selectedrow == -1 or nim.selectedrow == row):
        mybutton[row][column]["state"] = DISABLED
        nim.selectedrow = row
        nim.rowcount[row] -= 1
        nim.totalcount -= 1
        nim.usermoved = True
        nim.firstmove = False
        nim.matrix[row][column] = 0
    if nim.totalcount == 0:
        nim.gamestatus = "User Won"


def newuser_click():
    new_user = simpledialog.askstring("Input", "What is your first name?",
                                      parent=window)
    new_user = new_user.upper()
    if new_user is not None:
        userlist = user.add_user(new_user)
        mycombobox['values'] = userlist
    else:
        print("You don't have a first name?")


def pcmove_click():
    global mybutton
    global currentusername
    currentusername = mycombobox.get()
    nim.pcmove(currentusername)
    redisplay(mybutton)
    winsound.PlaySound("buttonclicksound.wav", winsound.SND_ASYNC)


def newgame_click():
    global nim
    global mybutton
    nim.initialize()
    redisplay(mybutton)
    winsound.PlaySound("buttonclicksound.wav", winsound.SND_ASYNC)


def stats_click():
    currentusername = mycombobox.get()
    overalluserstat = user.get_stats(currentusername)

    messagebox.showinfo(title=currentusername + " STAT",
                        message="Total Games Won: " + str(overalluserstat[0][1]) + "/" + str(overalluserstat[0][2]))


def callbackFunc(event):
    currentusername = mycombobox.get()
    messagebox.showinfo(title="currentuser", message=currentusername)


window = Tk()
window.title("NIM GAME")
window.iconbitmap('MatchStick.ico')
window.geometry("600x620")  # Width and Height
# To make window non-resizable user can pass 0 or False.
window.resizable(0, 0)

nimframe_intro = LabelFrame(window, bd=0, highlightbackground="white", highlightcolor="white", highlightthickness=0,
                            height=100, width=600)
nimframe_intro.grid()
nimframe_user = LabelFrame(window, bd=0, highlightbackground="white", highlightcolor="white", highlightthickness=0,
                           height=20, width=600)
nimframe_user.grid()
nimframe_game = LabelFrame(window, bd=0, highlightbackground="white",
                           highlightcolor="white", highlightthickness=0, height=500, width=600)
nimframe_game.grid()

# Button is array used to store button object(matchstick). We're fixing size to 5x5
mybutton = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
    0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

matchimage = Image.open("matchstickbutton.jpg")  # Open image
matchimage = matchimage.resize((20, 55), Image.ANTIALIAS)  # resize image
mymatchimage = ImageTk.PhotoImage(matchimage)  # to display an icon

title = Label(nimframe_intro, text="NIM GAME", fg="brown",
              font=("Helvetica", 14, 'bold'), justify=CENTER)
title.grid()

instructions = Label(nimframe_intro, text="""How to play NIM game:
    1.Players take turns taking any number of matchsticks from one of the rows.
    2.Player can choose only from one row at a time.
    3.Whoever takes the last of the matchsticks wins!
    4.Click MOVEOVER for PC to start.""", fg="black", font=("Helvetica", 12, 'bold'), justify=LEFT)
instructions.grid()


userlist = user.get_users()
mycombobox = ttk.Combobox(nimframe_user, value=userlist)
mycombobox.grid(row=0, column=1)
mycombobox.current(0)
currentusername = mycombobox.get()
mycombobox.bind("<<ComboboxSelected>>", callbackFunc)


new_user_btn = Button(nimframe_user, text="New User", command=newuser_click, height=1, width=10,
                      borderwidth=0.5, font=("Helvetica", 10, 'bold'))
new_user_btn.grid(row=0, column=0)

stats_btn = Button(nimframe_user, text="STAT", command=stats_click, height=1, width=5,
                   borderwidth=0.5, font=("Helvetica", 10, 'bold'))
stats_btn.grid(row=0, column=2)

for i in range(5):
    for j in range(5):
        mybutton[i][j] = Button(
            nimframe_game, image=mymatchimage, height=65, width=80, borderwidth=5, state=DISABLED, command=lambda arg1=i, arg2=j: btn_remove(arg1, arg2))
        mybutton[i][j].grid(row=i+2, column=j)
pc_move = Button(nimframe_game, text="Move Over",
                 height=2, width=10, borderwidth=2, command=pcmove_click, font=("Helvetica", 12, 'bold'))
pc_move.grid(row=7, column=1)
new_game = Button(nimframe_game, text="New Game", command=newgame_click,
                  height=2, width=10, borderwidth=2, font=("Helvetica", 12, 'bold'))
new_game.grid(row=7, column=3)

gamestatus = Label(nimframe_game, text=nim.gamestatus, fg="white", bg="brown", relief=SUNKEN,
                   font=("Helvetica", 10, 'bold'), padx=10, pady=10)
gamestatus.grid(row=7, column=2)


window.mainloop()
