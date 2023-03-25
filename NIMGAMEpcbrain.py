import random
import winsound
from NIMGAMEsqlcon import User
from tkinter import messagebox

user = User()


class Nim:
    currentusername = ""
    rowcount = [0, 0, 0, 0, 0]
    firstmove = True
    usermoved = False
    selectedrow = -1
    IsUserMove = True
    totalcount = 0
    gamestatus = ""
    matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    def initialize(self):
        for i in range(5):
            self.rowcount[i] = random.randint(1, 5)
            self.totalcount += self.rowcount[i]
            for m in range(5):
                if m < self.rowcount[i]:
                    self.matrix[i][m] = 1
                else:
                    self.matrix[i][m] = 0
        self.firstmove = True
        self.usermoved = False
        self.selectedrow = -1
        self.IsUserMove = True
        self.gamestatus = "PC/USER MOVE"

    def pcmove(self, currentusername):

        if self.firstmove == False and self.IsUserMove == True and self.usermoved == False:
            self.gamestatus = currentusername + " MOVE"
            return False

        if self.totalcount == 0 and self.IsUserMove == True and self.usermoved == True:
            self.gamestatus = currentusername + " WON"
            messagebox.showinfo(title="GAME OVER",
                                message=currentusername+" WON")
            user.update_game_status(currentusername, True)
            return False
        if self.firstmove == True and self.IsUserMove == True and self.usermoved == False:
            self.IsUserMove = False
            self.gamestatus = "PC MOVE"

        newrowcount = [0, 0, 0, 0, 0]
        removecount = 0
        for i in range(5):
            if self.rowcount[i] == 0: # Check whether all matchstick are removed
                continue 
            # Find xor of all other rows excluding ith row. 
            #To calculate balance match stick we have to keep after the move
            for n in range(5):
                if i != n: 
                    newrowcount[i] ^= self.rowcount[n]
            if newrowcount[i] < self.rowcount[i]:
                removecount = self.rowcount[i]-newrowcount[i]
                self.rowcount[i] = newrowcount[i]
                removed = 0
                while removed < removecount:
                    for j in range(5):
                        if self.matrix[i][j] == 1 and removed < removecount:
                            self.matrix[i][j] = 0
                            removed += 1
                break
        #No good move possible. Remove one matchstick from uppermost row
        else:
            for i in range(5):
                if self.rowcount[i] > 0:
                    self.rowcount[i] = self.rowcount[i] - 1
                    for j in range(5):
                        if self.matrix[i][j] == 1:
                            self.matrix[i][j] = 0
                            break
                    break
        #Recalculate the totalcount value
        self.totalcount = 0
        for i in range(5):
            self.totalcount += self.rowcount[i]
        if self.totalcount == 0:
            self.gamestatus = "PC WON"
            messagebox.showinfo(title="GAME OVER", message="PC WON")
            user.update_game_status(currentusername, False)
            return True
        else:
            self.firstmove = False
            self.usermoved = False
            self.selectedrow = -1
            self.IsUserMove = True
            self.gamestatus = currentusername + " MOVE"
            return True
