import mysql.connector
from tkinter import messagebox


class User:
    def get_users(self):
        con = mysql.connector.connect(
            host="localhost", user="root", password="root")
        cusorc = con.cursor()
        cusorc.execute(
            "SELECT username FROM nimgame.user")
        r = cusorc.fetchall()
        # con.commit()
        con.close()
        userlist = []
        for i in range(len(r)):
            userlist.append(r[i][0])
        return userlist

    def get_stats(self, UserName):
        con = mysql.connector.connect(
            host="localhost", user="root", password="root")
        cusorc = con.cursor()
        sql = "SELECT * FROM nimgame.user where UserName='" + UserName + "'"
        cusorc.execute(sql)
        r = cusorc.fetchall()
        con.close()
        return r

    def add_user(self, UserName):
        con = mysql.connector.connect(
            host="localhost", user="root", password="root")
        cusorc = con.cursor()
        sql = "SELECT username FROM nimgame.user where UserName='" + UserName + "'"
        cusorc.execute(sql)
        r = cusorc.fetchall()
        if len(r) == 0:
            sql = "INSERT INTO nimgame.user (UserName, UserWonCount, TotalGamesCount) VALUES ('" + \
                UserName + "',0,0)"
            cusorc.execute(sql)
            con.commit()
        cusorc.execute(
            "SELECT username FROM nimgame.user")
        r = cusorc.fetchall()
        con.close()
        userlist = []
        for i in range(len(r)):
            userlist.append(r[i][0])
        return userlist

    def update_game_status(self, UserName, IsUserWon):
        con = mysql.connector.connect(
            host="localhost", user="root", password="root")
        cusorc = con.cursor()
        if IsUserWon == True:
            sql = "UPDATE nimgame.user SET UserWonCount = UserWonCount+1,TotalGamesCount = TotalGamesCount+1 WHERE UserName ="+"'" + UserName + "'"
        else:
            sql = "UPDATE nimgame.user SET TotalGamesCount = TotalGamesCount+1 WHERE UserName =" + \
                "'" + UserName + "'"
        cusorc.execute(sql)
        con.commit()
        con.close()
