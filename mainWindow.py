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
        
        self.originalGridPal = mineGrid.palette(self)
        
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
                exec("self.grid{}_{}.row = {}".format(i, j, i))
                exec("self.grid{}_{}.col = {}".format(i, j, j))
                eval("gridLayout.addWidget(self.grid{}_{}, {}, {})".format(i, j, i, j))
                eval("self.grid{}_{}.touchPress.connect(self.touchPress_)".format(i, j))
                eval("self.grid{}_{}.touchRelease.connect(self.touchRelease_)".format(i, j))
                eval("self.grid{}_{}.zeroTouched.connect(self.zeroTouched_)".format(i, j))
                eval("self.grid{}_{}.mineTouched.connect(self.gameFailed)".format(i, j))
                eval("self.grid{}_{}.mineMarked.connect(self.mineMarked_)".format(i, j))
                eval("self.grid{}_{}.cancelMineMarked.connect(self.cancelMineMarked_)".format(i, j))
                eval("self.grid{}_{}.numberMarked.connect(self.checkWin)".format(i, j))
                
        
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
        game.generate()
        self.sourcesMap = game.base
        self.minesMap = game.minesMap
        self.markedMinesMap = []
        print(self.sourcesMap)
        for i in range(self.row):
            for j in range(self.column):
                eval("self.grid{}_{}.setValue(self.sourcesMap[{}][{}])".format(i, j, i, j))
                eval("self.grid{}_{}.setPalette(self.originalGridPal)".format(i, j))
                
        self.minesLeftLcd.display(self.mines)
    
    def newGame(self):
        self.restoreBoard()
        self.initGame()
    
    def restoreBoard(self):
        self.markedMinesMap = []
        for i in range(self.row):
            for j in range(self.column):
                eval("self.grid{}_{}.setBlankState()".format(i, j))
                eval("self.grid{}_{}.setPalette(self.originalGridPal)".format(i, j))
    
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
        b, n = self.autoZeroState((self.sender().row, self.sender().col), [], [])
        self.operateGridTogether("setZeroState()", b)
        self.operateGridTogether("setNumberState()", n)
        self.checkWin()
            
    
    def autoZeroState(self, zp, blockList = [], numberList = []):
        row, col = zp
        blockList.append(zp)
        for offsetRow, offsetCol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            newRow = row + offsetRow
            newCol = col + offsetCol
            if newRow in range(0, self.row) and newCol in range(0, self.column):
                if eval("self.grid{}_{}.value == 0".format(newRow, newCol)) and (newRow, newCol) not in blockList:
                    self.autoZeroState((newRow, newCol), blockList, numberList)
                elif (newRow, newCol) not in numberList and eval("1 <= self.grid{}_{}.value <= 8".format(newRow, newCol)):
                    numberList.append((newRow, newCol))
        return blockList, numberList
        
    def operateGridTogether(self, expression, tmpList):
        for r, c in tmpList:
            eval("self.grid{}_{}.{}".format(r, c, expression))
    
    def touchRelease_(self):
        minePoslist = self.getNearPos(self.sender().row, self.sender().col, "markState")  #邻居雷位置
        blankPoslist = self.getNearPos(self.sender().row, self.sender().col, "blankState") #邻居空白位置
        questionPosList = self.getNearPos(self.sender().row, self.sender().col, "questionState") #邻居问号位置
        blankAndQuestionPosList = blankPoslist + questionPosList #邻居空白+问号位置
        
        mineNum = len(minePoslist)
        if mineNum != self.sender().value:
            self.operateGridTogether("setDown(False)", blankAndQuestionPosList)
        else:
            wrongMark = self.checkMark(minePoslist)
            if wrongMark == []:
                self.operateGridTogether("setDown(False)", blankAndQuestionPosList)
                z = []
                for r1, c1 in blankAndQuestionPosList:
                    eval("z.append(self.grid{}_{}.value)".format(r1, c1))
                
                if 0 not in z:
                    self.operateGridTogether("setNumberState()", blankAndQuestionPosList)
                else:
                    zeroPos = blankAndQuestionPosList[z.index(0)]
                    blockList, numberList = self.autoZeroState(zeroPos, [], [])
                    self.operateGridTogether("setZeroState()", blockList)
                    self.operateGridTogether("setNumberState()", numberList)
                self.checkWin()
            else:
                self.operateGridTogether("setDown(False)", blankAndQuestionPosList)
                self.gameFailed(False)
                
    
    def touchPress_(self):
        self.operateGridTogether("setDown(True)", self.getNearPos(self.sender().row, self.sender().col, "blankState questionState"))
    
    def gameFailed(self, clickFailed = True):
        t1 = list(set(self.markedMinesMap) - set(self.minesMap))
        self.operateGridTogether("setMarkWrongState()", t1)
        if clickFailed:
            self.markedMinesMap.append((self.sender().row, self.sender().col))
        t2 = list(set(self.minesMap) - set(self.markedMinesMap))
        self.operateGridTogether("setMineState()", t2)
        
        for i in range(0, self.row):
            for j in range(0, self.column):
                eval("self.grid{}_{}.setDisableState()".format(i, j))
    
    def mineMarked_(self):
        self.markedMinesMap.append((self.sender().row, self.sender().col))
        self.minesLeftLcd.display(self.mines - len(self.markedMinesMap))
    
    def cancelMineMarked_(self):
        self.markedMinesMap.remove((self.sender().row, self.sender().col))
        self.minesLeftLcd.display(self.mines - len(self.markedMinesMap))
    
    def checkWin(self):
        tmpList = []
        for i in range(0, self.row):
            for j in range(0, self.column):
                if eval("self.grid{}_{}.state == 'blankState' or self.grid{}_{}.state == 'questionState'".format(i, j, i, j)):
                    tmpList.append((i, j))
        if set(tmpList) == set(self.minesMap) - set(self.markedMinesMap):
            self.operateGridTogether("setMarkState()", tmpList)
            self.minesLeftLcd.display(0)
            print("Win")
    
    def aboutQtAction_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutGameAction_(self):
        QMessageBox.about(self, "About mine sweeper", "It's a Linux game cloned from classic windows game, written with PyQt.\n\nAuthor: sanfanling (xujia19@outlook.con)")
    
    def closeEvent(self, e):
        e.accept()
 
