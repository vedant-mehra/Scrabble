import sys
from PyQt4 import QtGui, QtCore
from ui_scrabble import Ui_Scrabble
from graph import Graph
from wordchecker import WordBank
import random
import webbrowser


class Scrabble(QtGui.QMainWindow, Ui_Scrabble, Graph, WordBank):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.g = Graph()
        self.w = WordBank()
        self.retrace = []
        self.doneword = {}

        self.scrabbleboard = [[""]*15 for i in range(15)]
        self.p1score = 0
        self.p2score = 0
        self.tiles2.hide()
        self.done2.hide()
        self.board.setEnabled(False)
        self.done.setEnabled(False)
        self.done2.setEnabled(False)
        self.first = True
        self.r1 = 16
        self.c1 = 16
        self.second = True
        self.row = False
        self.colom = False

        self.home()
        self.fill()
        self.fill2()

    def home(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.board.cellClicked.connect(self.boardclicked)
        self.tiles.itemClicked.connect(self.tileclicked)
        self.done.clicked.connect(self.doneclicked)
        self.tiles2.itemClicked.connect(self.tile2clicked)
        self.done2.clicked.connect(self.done2clicked)
        self.actionNew_Game.triggered.connect(self.newgame)
        self.actionQuit.triggered.connect(self.closeapp)
        self.actionRules.triggered.connect(lambda: webbrowser.open('https://scrabble.hasbro.com/en-us/rules'))
        self.actionNo_Of_Tiles_Left.triggered.connect(self.tilecount)
        self.actionScore_Card.triggered.connect(self.scoreboard)
        self.actionWord_Check.triggered.connect(self.wordchecker)
        self.actionWord_Hint.triggered.connect(self.hint)

    def doneclicked(self):
        s = self.checkword()
        self.first = True
        self.r1 = 16
        self.c1 = 16
        self.second = True
        self.row = False
        self.colom = False
        if s == 0:
            self.revert()
            self.fill()
        else:
            self.p1score += s
            self.scorecard.setText("SCORE = " + str(self.p1score))
            self.retrace = []
            self.tiles.hide()
            self.done2.setEnabled(False)
            self.done.hide()
            self.tiles2.show()
            self.done2.show()
            refill()
            self.fill()

    def tileclicked(self, item):
        cr = item.text()
        if cr.isalpha():
            self.char = item.text()
            player1.remove(self.char.lower())
            item.setText("")
            self.tiles.setEnabled(False)
            self.board.setEnabled(True)
            self.done.setEnabled(False)
            self.ques.setText("PLACE YOUR LETTER")

    def done2clicked(self):
        s = self.checkword()
        self.first = True
        self.r1 = 16
        self.c1 = 16
        self.second = True
        self.row = False
        self.colom = False
        if s == 0:
            self.revert2()
            self.fill2()
        else:
            self.p2score += s
            self.scorecard2.setText("SCORE = " + str(self.p2score))
            self.retrace = []
            self.tiles2.hide()
            self.done.setEnabled(False)
            self.done2.hide()
            self.tiles.show()
            self.done.show()
            refill2()
            self.fill2()

    def tile2clicked(self, item):
        cr = item.text()
        if cr.isalpha():
            self.char = item.text()
            player2.remove(self.char.lower())
            item.setText("")
            self.tiles2.setEnabled(False)
            self.board.setEnabled(True)
            self.done2.setEnabled(False)
            self.ques.setText("PLACE YOUR LETTER")

    def boardclicked(self, r, c):
        item = self.board.item(r, c)
        if self.scrabbleboard[r][c] == "":
            flag = False
            if r == 7 and c == 7:
                flag = True

            if 0 <= r - 1 < 15:
                item2 = self.board.item(r - 1, c)
                if not item2.text() == "" and self.g.dfs(15 * (r - 1) + c):
                    flag = True
                    self.g.addedge(15*r+c, 15*(r-1)+c)
            if 0 <= r+1 < 15:
                item2 = self.board.item(r + 1, c)
                if not item2.text() == "" and self.g.dfs(15 * (r + 1) + c):
                    flag = True
                    self.g.addedge(15*r+c, 15*(r+1)+c)
            if 0 <= c-1 < 15:
                item2 = self.board.item(r, c - 1)
                if not item2.text() == "" and self.g.dfs(15 * r + (c - 1)):
                    flag = True
                    self.g.addedge(15*r+c, 15*r+(c-1))
            if 0 <= c+1 < 15:
                item2 = self.board.item(r, c + 1)
                if not item2.text() == "" and self.g.dfs(15 * r + (c + 1)):
                    flag = True
                    self.g.addedge(15*r+c, 15*r+(c+1))

            if flag:
                if not self.first:
                    if self.second:
                        if r == self.r1:
                            self.row = True
                            self.second = False
                        if c == self.c1:
                            self.colom = True
                            self.second = False
                    else:
                        y = False
                        x = False
                        if self.row:
                            if not r == self.r1:
                                x = True
                        if self.colom:
                            if not c == self.c1:
                                y = True
                        if x or y:
                            return
                if self.row or self.colom or self.first:
                    self.board.setEnabled(False)
                    self.tiles.setEnabled(True)
                    self.done.setEnabled(True)
                    self.tiles2.setEnabled(True)
                    self.done2.setEnabled(True)
                    self.ques.setText("CHOOSE YOUR LETTER")
                    clr = item.backgroundColor()
                    item.setText(self.char)
                    self.tiles.setItem(r, c, item)
                    self.scrabbleboard[r][c] = self.char
                    if clr.red() == 0:
                        self.retrace.append(str(r) + " " + str(c) + " " + self.char + " " + "n")
                    if clr.green() == 255:
                        self.retrace.append(str(r) + " " + str(c) + " " + self.char + " " + "dw")
                    if clr.red() == 75:
                        self.retrace.append(str(r) + " " + str(c) + " " + self.char + " " + "dl")
                    if clr.red() == 50:
                        self.retrace.append(str(r) + " " + str(c) + " " + self.char + " " + "tl")
                    if clr.green() == 170:
                        self.retrace.append(str(r) + " " + str(c) + " " + self.char + " " + "tw")
                    if self.first:
                        self.r1 = r
                        self.c1 = c
                        self.first = False

    def fill(self):
        K = 0
        for i in player1:
            item = QtGui.QTableWidgetItem()
            item.setText(i.upper())
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tiles.setItem(0, K, item)
            item = QtGui.QTableWidgetItem()
            item.setText(points(i.upper()))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tiles.setItem(1, K, item)
            K += 1

    def fill2(self):
        K = 0
        for i in player2:
            item = QtGui.QTableWidgetItem()
            item.setText(i.upper())
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tiles2.setItem(0, K, item)
            item = QtGui.QTableWidgetItem()
            item.setText(points(i.upper()))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tiles2.setItem(1, K, item)
            K += 1

    def revert(self):
        for i in self.retrace:
            j = i.split()
            e = j[2].lower()
            player1.append(e)
            self.scrabbleboard[int(j[0])][int(j[1])] = ""
            item = self.board.item(int(j[0]), int(j[1]))
            item.setText("")
            self.board.setItem(int(j[0]), int(j[1]), item)
        self.retrace = []

    def revert2(self):
        for i in self.retrace:
            j = i.split()
            e = j[2].lower()
            player2.append(e)
            self.scrabbleboard[int(j[0])][int(j[1])] = ""
            item = self.board.item(int(j[0]), int(j[1]))
            item.setText("")
            self.board.setItem(int(j[0]), int(j[1]), item)
        self.retrace = []

    def checkword(self):
        self.scnet = 0
        self.mnet = 1
        if self.row:
            flag = True
            line = ""
            score = 0
            for k in self.retrace:
                j = k.split()
                b = int(j[0])
                if j[3] == "n":
                    sc = 0
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "dl":
                    sc = int(points(j[2]))
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "dw":
                    sc = 0
                    m = 2
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "tw":
                    sc = 0
                    m = 3
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "tl":
                    sc = int(points(j[2])) * 2
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                for i in range(0, 15):
                    if self.scrabbleboard[i][int(j[1])] == "" and len(line):
                        if len(line) >= 2 and self.check(line.lower()) and line not in self.doneword:
                            scor = 0
                            for a in line:
                                scor += int(points(a))
                            scor += sc
                            scor *= m
                            if self.done.isHidden():
                                self.doneword[line] = j[1] + " " + "c" + " " + str(scor) + " " + "2"
                            else:
                                self.doneword[line] = j[1] + " " + "c" + " " + str(scor) + " " + "1"
                            score += scor
                        if len(line) >= 2 and not self.check(line.lower()):
                            flag = False
                        line = ""
                    if not self.scrabbleboard[i][int(j[1])] == "":
                        line += self.scrabbleboard[i][int(j[1])]
            for i in range(0, 15):
                if self.scrabbleboard[b][i] == "" and len(line):
                    if len(line) >= 2 and self.check(line.lower()) and line not in self.doneword:
                        scor = 0
                        for a in line:
                            scor += int(points(a))
                        scor += self.scnet
                        scor *= self.mnet
                        if self.done.isHidden():
                            self.doneword[line] = str(b) + " " + "r" + " " + str(scor) + " " + "2"
                        else:
                            self.doneword[line] = str(b) + " " + "r" + " " + str(scor) + " " + "1"
                        score += scor
                    if len(line) >= 2 and not self.check(line.lower()):
                        flag = False
                    line = ""
                if not self.scrabbleboard[b][i] == "":
                    line += self.scrabbleboard[b][i]
            if not flag:
                score = 0
        else:
            flag = True
            line = ""
            score = 0
            for k in self.retrace:
                j = k.split()
                b = int(j[1])
                if j[3] == "n":
                    sc = 0
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "dl":
                    sc = int(points(j[2]))
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "dw":
                    sc = 0
                    m = 2
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "tw":
                    sc = 0
                    m = 3
                    self.scnet += sc
                    self.mnet *= m
                if j[3] == "tl":
                    sc = int(points(j[2])) *2
                    m = 1
                    self.scnet += sc
                    self.mnet *= m
                for i in range(0, 15):
                    if self.scrabbleboard[int(j[0])][i] == "" and len(line):
                        if len(line) >= 2 and self.check(line.lower()) and line not in self.doneword:
                            scor = 0
                            for a in line:
                                scor += int(points(a))
                            scor += sc
                            scor *= m
                            if self.done.isHidden():
                                self.doneword[line] = j[0] + " " + "r" + " " + str(scor) + " " + "2"
                            else:
                                self.doneword[line] = j[0] + " " + "r" + " " + str(scor) + " " + "1"
                            score += scor
                        if len(line) >= 2 and not self.check(line.lower()):
                            flag = False
                        line = ""
                    if not self.scrabbleboard[int(j[0])][i] == "":
                        line += self.scrabbleboard[int(j[0])][i]
            for i in range(0, 15):
                if self.scrabbleboard[i][b] == "" and len(line):
                    if len(line) >= 2 and self.check(line.lower()) and line not in self.doneword:
                        scor = 0
                        for a in line:
                            scor += int(points(a))
                        scor += self.scnet
                        scor *= self.mnet
                        if self.done.isHidden():
                            self.doneword[line] = str(b) + " " + "c" + " " + str(scor) + " " + "2"
                        else:
                            self.doneword[line] = str(b) + " " + "c" + " " + str(scor) + " " + "1"
                        score += scor
                    if len(line) >= 2 and not self.check(line.lower()):
                        flag = False
                    line = ""
                if not self.scrabbleboard[i][b] == "":
                    line += self.scrabbleboard[i][b]
            if not flag:
                score = 0

        return score

    def newgame(self):
        choice = QtGui.QMessageBox.question(self, 'Scrabble', "Are you sure you want to start a New Game", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            tilepool = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                        'a', 'a', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
                        'n', 'n', 'n', 'n', 'n', 'n', 'r', 'r', 'r', 'r', 'r', 'r', 't', 't', 't', 't', 't', 't', 'l',
                        'l', 'l', 'l', 's', 's', 's', 's', 'u', 'u', 'u', 'u', 'd', 'd', 'd', 'd', 'g', 'g', 'g', 'b',
                        'b', 'c', 'c', 'm', 'm', 'p', 'p', 'f', 'f', 'h', 'h', 'v', 'v', 'w', 'w', 'y', 'y', 'k', 'j',
                        'x', 'q', 'z']

            self.setupUi(self)
            player1.clear()
            player2.clear()
            refill()
            refill2()
            self.g = Graph()
            self.w = WordBank()
            self.retrace = []
            self.doneword = {}

            self.scrabbleboard = [[""] * 15 for i in range(15)]
            self.p1score = 0
            self.p2score = 0

            self.tiles2.hide()
            self.done2.hide()
            self.tiles.show()
            self.done.show()
            self.board.setEnabled(False)
            self.done.setEnabled(False)
            self.done2.setEnabled(False)
            self.first = True
            self.r1 = 16
            self.c1 = 16
            self.second = True
            self.row = False
            self.colom = False
            self.home()
            self.fill()
            self.fill2()
        else:
            pass

    def closeapp(self):
        choice = QtGui.QMessageBox.question(self, 'Scrabble', "Are you sure you want to exit SCRABBLE", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def tilecount(self):
        QtGui.QMessageBox.information(self, 'Scrabble', str(len(tilepool)))

    def scoreboard(self):
        msg = QtGui.QMessageBox()
        msg.setInformativeText("Player 1" + "   " + str(self.p1score) + "\n" + "Player 2" + "   " + str(self.p2score))
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("Score Card")
        msg.setWindowTitle("Scrabble")
        card1 = "Player 1" + "\n"
        card2 = "Player 2" + "\n"
        for i in self.doneword.keys():
            j = self.doneword[i].split()
            if j[3] == "1":
                card1 = card1 + i + "   " + "Score = " + j[2] + "\n"
            else:
                card2 = card2 + i + "   " + "Score = " + j[2] + "\n"
        msg.setDetailedText(card1 + card2)
        msg.exec_()

    def hint(self):
        msg = QtGui.QMessageBox()
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        hints = self.wordhint()
        if hints:
            msg.setInformativeText(hints)
        else:
            msg.setInformativeText("Sorry no hints available at this time")
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText("TRY")
        msg.setWindowTitle("Scrabble")
        msg.exec_()

    def wordchecker(self):
        Dialog = QtGui.QDialog()
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        Dialog.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.truefalse = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.truefalse.setFont(font)
        self.truefalse.setStyleSheet("color: rgb(255, 255, 0);")
        self.truefalse.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.truefalse)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.recheck = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.recheck.setFont(font)
        self.recheck.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.horizontalLayout_2.addWidget(self.recheck)
        self.exit = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.exit.setFont(font)
        self.exit.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.horizontalLayout_2.addWidget(self.exit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.checkbutton = QtGui.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkbutton.setFont(font)
        self.checkbutton.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.horizontalLayout_3.addWidget(self.checkbutton)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        Dialog.setWindowTitle("Word Checker")
        self.truefalse.setText("Enter your word")
        self.recheck.setText("RECHECK")
        self.exit.setText("EXIT")
        self.checkbutton.setText("CHECK")
        self.exit.hide()
        self.recheck.hide()
        self.exit.clicked.connect(Dialog.close)
        self.recheck.clicked.connect(self.rcheck)
        self.checkbutton.clicked.connect(self.checkb)
        self.checkbutton.setDefault(True)
        Dialog.exec_()

    def rcheck(self):
        self.exit.hide()
        self.recheck.hide()
        self.checkbutton.show()
        self.lineEdit.show()
        self.truefalse.setText("Enter your word")

    def checkb(self):
        self.exit.show()
        self.recheck.show()
        self.checkbutton.hide()
        self.lineEdit.hide()
        s = self.lineEdit.text()
        if self.check(s.lower()):
            self.truefalse.setText("TRUE")
        else:
            self.truefalse.setText("FALSE")

    def wordhint(self):
        hints = ""
        for j in self.doneword.keys():
            for i in self.dictionary.keys():
                if j.lower() in i:
                    if 0 < len(i) - len(j) <= 7:
                        k = i.replace(j.lower(), "", 1)
                        flag = True
                        self.tile = player1.copy()
                        for s in k:
                            if s in self.tile:
                                self.tile.remove(s)
                            else:
                                flag = False
                        if flag:
                            hints = hints + i + "\n"
            hints += "\n"
        return hints


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Scrabble()
    sys.exit(app.exec_())


tilepool = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
            'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'n', 'n', 'n', 'n',
            'n', 'n', 'r', 'r', 'r', 'r', 'r', 'r', 't', 't', 't', 't', 't', 't', 'l', 'l', 'l', 'l', 's', 's', 's',
            's', 'u', 'u', 'u', 'u', 'd', 'd', 'd', 'd', 'g', 'g', 'g', 'b', 'b', 'c', 'c', 'm', 'm', 'p', 'p', 'f',
            'f', 'h', 'h', 'v', 'v', 'w', 'w', 'y', 'y', 'k', 'j', 'x', 'q', 'z']


def points(ch):
    if ch in ['E', 'A', 'I', 'O', 'N', 'R', 'T', 'L', 'S', 'U']:
        return '1'
    if ch in ['D', 'G']:
        return '2'
    if ch in ['B', 'C', 'M', 'P']:
        return '3'
    if ch in ['F', 'H', 'V', 'W', 'Y']:
        return '4'
    if ch in ['K']:
        return '5'
    if ch in ['J', 'X']:
        return '8'
    if ch in ['Q', 'Z']:
        return '10'


player1 = []
player2 = []
for i in range(0, 7):
    c = random.choice(tuple(tilepool))
    tilepool.remove(c)
    player1.append(c)

for i in range(0, 7):
    c = random.choice(tuple(tilepool))
    tilepool.remove(c)
    player2.append(c)


def refill():

    for i in range(len(player1), 7):
        if len(tilepool):
            c = random.choice(tuple(tilepool))
            tilepool.remove(c)
            player1.append(c)


def refill2():
    for i in range(len(player2), 7):
        if len(tilepool):
            c = random.choice(tuple(tilepool))
            tilepool.remove(c)
            player2.append(c)


run()
