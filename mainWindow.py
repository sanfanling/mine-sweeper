#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: mainGui.py
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baseWindow import baseWindow
from mineGrid import mineGrid
from libms import mineSweeper
import sys


class mainWindow(baseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mine sweeper")
        self.mode = "Easy"
        self.modeDict = {"Easy": (9, 9, 10), "Medium": (16, 16, 40), "Difficult": (16, 30, 99), "Custom": (20, 50, 200)}
        self.row, self.column, self.mines = self.modeDict[self.mode]
        eval("self.{}Action.setChecked(True)".format(self.mode.lower()))
        
        #self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        
        self.initBoard()
        self.initGame()
        
        self.newAction.triggered.connect(self.newGame)
        self.newGameButton.clicked.connect(self.newGame)
        self.replayAction.triggered.connect(self.restoreBoard)
        self.aboutGameAction.triggered.connect(self.aboutGameAction_)
        self.aboutQtAction.triggered.connect(self.aboutQtAction_)
        self.quitAction.triggered.connect(self.close)
        self.easyAction.triggered.connect(self.changeMode_)
        self.mediumAction.triggered.connect(self.changeMode_)
        self.difficultAction.triggered.connect(self.changeMode_)
        self.customAction.triggered.connect(self.changeMode_)
    
    def initBoard(self):
        gridLayout = QGridLayout(None)
        gridLayout.setSpacing(0)
        for i in range(self.row):
            for j in range(self.column):
                exec("self.grid{}_{} = mineGrid()".format(i, j))
                eval("gridLayout.addWidget(self.grid{}_{}, {}, {})".format(i, j, i, j))
                eval("self.grid{}_{}.touchPress.connect(self.touchPress_)".format(i, j))
                eval("self.grid{}_{}.touchRelease.connect(self.touchRelease_)".format(i, j))
                eval("self.grid{}_{}.zeroTouched.connect(self.zeroTouched_)".format(i, j))
                eval("self.grid{}_{}.mineTouched.connect(self.gameFailed)".format(i, j))
                eval("self.grid{}_{}.mineMarked.connect(self.reduceMines)".format(i, j))
        
        wid = QWidget()
        mainLayout = QVBoxLayout(None)
        mainLayout.setSizeConstraint(3)
        
        layout = QHBoxLayout(None)
        layout.setContentsMargins(0, 0, 0, 30)
        layout.addWidget(self.minesLeftLcd)
        layout.addStretch(15)
        layout.addWidget(self.newGameButton)
        layout.addStretch(15)
        layout.addWidget(self.timeUsageLcd)
        layout.setStretch(0, 15)
        layout.setStretch(2, 1)
        layout.setStretch(4, 15)
        
        mainLayout.addLayout(layout)
        mainLayout.addLayout(gridLayout)
        wid.setLayout(mainLayout)
        
        self.setCentralWidget(wid)
        self.adjustSize()
    
    def initGame(self):
        game = mineSweeper(self.row, self.column, self.mines)
        self.sourcesMap, self.minesMap = game.generate()
        print(self.sourcesMap)
        for i in range(self.row):
            for j in range(self.column):
                eval("self.grid{}_{}.setValue(self.sourcesMap[{}][{}])".format(i, j, i, j))
                exec("self.grid{}_{}.row = {}".format(i, j, i))
                exec("self.grid{}_{}.col = {}".format(i, j, j))
        self.minesLeftLcd.display(self.mines)
    
    def newGame(self):
        self.restoreBoard()
        self.initGame()
    
    def restoreBoard(self):
        for i in range(self.row):
            for j in range(self.column):
                eval("self.grid{}_{}.setBlankState()".format(i, j))
    
    def changeMode_(self):
        if self.mode != self.sender().text():
            self.mode = self.sender().text()
            self.row, self.column, self.mines = self.modeDict[self.mode]
            self.initBoard()
            self.initGame()
            
        
    def getNearPos(self, row, col, key):
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        posList = []
        for r, c in direction:
            newRow = row + r
            newCol = col + c
            if newRow not in range(0, self.row) or newCol not in range(0, self.column):
                continue
            else:
                t = eval("self.grid{}_{}.state in key".format(newRow, newCol))
                if t:
                    posList.append((newRow, newCol))
                else:
                    continue
        return posList
    
    def checkMark(self, markList):
        wrongList = []
        for r, c in markList:
            logic = eval("self.grid{}_{}.value == -1".format(r, c))
            if not logic:
                wrongList.append((r, c))
        return wrongList
    
    def zeroTouched_(self):
        b = self.autoZeroState((self.sender().row, self.sender().col), [])
        for r, c in b:
            eval("self.grid{}_{}.setZeroState()".format(r, c))
    
    def autoZeroState(self, zp, blockList = []):
        row, col = zp
        blockList.append(zp)
        for offsetRow, offsetCol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            newRow = row + offsetRow
            newCol = col + offsetCol
            if newRow in range(0, self.row) and newCol in range(0, self.column):
                if eval("self.grid{}_{}.value == 0".format(newRow, newCol)) and (newRow, newCol) not in blockList:
                    self.autoZeroState((newRow, newCol), blockList)
                else:
                    eval("self.grid{}_{}.setNumberState()".format(newRow, newCol))
        return blockList
        
    def operateGridTogether(self, expression, tmpList):
        for r, c in tmpList:
            eval("self.grid{}_{}.{}".format(r, c, expression))
    
    def touchRelease_(self):
        minePoslist = self.getNearPos(self.sender().row, self.sender().col, "markState")
        blankPoslist = self.getNearPos(self.sender().row, self.sender().col, "blankState")
        mineNum = len(minePoslist)
        if mineNum != self.sender().value:
            self.operateGridTogether("setDown(False)", blankPoslist)
        else:
            wrongMark = self.checkMark(minePoslist)
            if wrongMark == []:
                self.operateGridTogether("setDown(False)", blankPoslist)
                z = []
                for r1, c1 in blankPoslist:
                    eval("z.append(self.grid{}_{}.value)".format(r1, c1))
                
                if 0 not in z:
                    self.operateGridTogether("setNumberState()", blankPoslist)
                else:
                    zeroPos = blankPoslist[z.index(0)]
                    blockList = self.autoZeroState(zeroPos, [])
                    self.operateGridTogether("setZeroState()", blockList)
            else:
                self.operateGridTogether("setExplodeState()", wrongMark)
                self.operateGridTogether("setDown(False)", blankPoslist)
                self.gameFailed(wrongMark)
                
    
    def touchPress_(self):
        self.operateGridTogether("setDown(True)", self.getNearPos(self.sender().row, self.sender().col, "blankState"))
    
    def gameFailed(self, ex = []):
        if ex == []:
            ex = [(self.sender().row, self.sender().col)]
        c = list(set(self.minesMap) - set(ex))
        self.operateGridTogether("setMineState()", c)
        for i in range(0, self.row):
            for j in range(0, self.column):
                eval("self.grid{}_{}.setDisableState()".format(i, j))
    
    def reduceMines(self):
        self.minesLeftLcd.display(self.minesLeftLcd.intValue() - 1)
    
    def aboutQtAction_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutGameAction_(self):
        QMessageBox.about(self, "About mine sweeper", "It's a Linux game cloned from classic windows game, written with PyQt.\n\nAuthor: sanfanling (xujia19@outlook.con)")
    
    def closeEvent(self, e):
        e.accept()
 
