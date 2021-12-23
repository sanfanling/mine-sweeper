#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: mainWindow.py
#Author: sanfanling
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
        self.setWindowIcon(QIcon("sources/mine.png"))
        
        self.mode = "Easy"
        self.modeDict = {"Easy": (9, 9, 10), "Medium": (16, 16, 40), "Difficult": (16, 30, 99), "Custom": (20, 50, 200)}
        self.row, self.column, self.mines = self.modeDict[self.mode]
        eval("self.{}Action.setChecked(True)".format(self.mode.lower()))
        self.myTimer = QTimer()
        self.timeUsage = 0
        self.originalGridPal = mineGrid.palette(self)
        
        self.virtualNewWorld()
        
        self.myTimer.timeout.connect(self.timeDisplay)
        self.newAction.triggered.connect(self.virtualNewGame)
        self.newGameButton.clicked.connect(self.virtualNewGame)
        self.replayAction.triggered.connect(self.virtualReplay)
        self.aboutGameAction.triggered.connect(self.aboutGameAction_)
        self.aboutQtAction.triggered.connect(self.aboutQtAction_)
        self.quitAction.triggered.connect(self.close)
        self.easyAction.triggered.connect(self.changeMode_)
        self.mediumAction.triggered.connect(self.changeMode_)
        self.difficultAction.triggered.connect(self.changeMode_)
        self.customAction.triggered.connect(self.changeMode_)
    
    def initBoard(self):
        self.gridLayout = QGridLayout(None)
        self.gridLayout.setSpacing(0)
        for i in range(self.row):
            for j in range(self.column):
                m = mineGrid(i, j)
                self.gridLayout.addWidget(m, i, j)
                m.touchPress.connect(self.touchPress_)
                m.touchRelease.connect(self.touchRelease_)
                m.zeroTouched.connect(self.zeroTouched_)
                m.mineTouched.connect(self.gameFailed)
                m.mineMarked.connect(self.mineMarked_)
                m.cancelMineMarked.connect(self.cancelMineMarked_)
                m.numberMarked.connect(self.checkWin)                
        
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
        layout.setStretch(0, 10)
        layout.setStretch(2, 6)
        layout.setStretch(4, 10)
        
        mainLayout.addLayout(layout)
        mainLayout.addLayout(self.gridLayout)
        mainLayout.setStretch(0, 1)
        mainLayout.setStretch(1, 5)
        wid.setLayout(mainLayout)
        
        self.setCentralWidget(wid)
        self.adjustSize()
        w = int(QApplication.desktop().availableGeometry(self).width() / 2 - self.width())
        self.move(w, 200)
    
    def initGame(self):
        game = mineSweeper(self.row, self.column, self.mines)
        game.generate()
        self.sourcesMap = game.base
        self.minesMap = game.minesMap
        self.markedMinesMap = []
        #print(self.sourcesMap)
        for i in range(self.row):
            for j in range(self.column):
                wid = self.gridLayout.itemAtPosition(i, j).widget()
                wid.setValue(self.sourcesMap[i][j])
                wid.setPalette(self.originalGridPal)
                
    def virtualNewGame(self):
        self.restoreGrids()
        self.initGame()
        self.initExtra()
    
    def virtualReplay(self):
        self.restoreGrids()
        self.initExtra()
    
    def virtualNewWorld(self):
        self.initBoard()
        self.initGame()
        self.initExtra()
    
    def initExtra(self):
        self.markedMinesMap = []
        self.timeUsage = 0
        self.minesLeftLcd.display(self.mines)
        self.timeUsageLcd.display(0)
        self.myTimer.start(1000)
    
    def restoreGrids(self):
        for i in range(self.row):
            for j in range(self.column):
                wid = self.gridLayout.itemAtPosition(i, j).widget()
                wid.setBlankState()
                wid.setPalette(self.originalGridPal)
    
    def changeMode_(self):
        if self.mode != self.sender().text():
            self.mode = self.sender().text()
            self.row, self.column, self.mines = self.modeDict[self.mode]
            self.virtualNewWorld()
            
            
        
    def getNearPos(self, row, col, key):
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        posList = []
        for r, c in direction:
            newRow = row + r
            newCol = col + c
            if newRow not in range(0, self.row) or newCol not in range(0, self.column):
                continue
            else:
                if self.gridLayout.itemAtPosition(newRow, newCol).widget().state in key:
                    posList.append((newRow, newCol))
                else:
                    continue
        return posList
    
    def checkMark(self, markList):
        wrongList = []
        for r, c in markList:
            if self.gridLayout.itemAtPosition(r, c).widget().value != -1:
                wrongList.append((r, c))
        return wrongList
    
    def zeroTouched_(self):
        b, n = self.autoZeroState((self.sender().row, self.sender().column), [], [])
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
                wid = self.gridLayout.itemAtPosition(newRow, newCol).widget()
                if wid.value == 0 and (newRow, newCol) not in blockList:
                    self.autoZeroState((newRow, newCol), blockList, numberList)
                elif (newRow, newCol) not in numberList and 1 <= wid.value <= 8:
                    numberList.append((newRow, newCol))
        return blockList, numberList
        
    def operateGridTogether(self, expression, tmpList):
        for r, c in tmpList:
            eval("self.gridLayout.itemAtPosition({}, {}).widget().{}".format(r, c, expression))
    
    def touchRelease_(self):
        minePoslist = self.getNearPos(self.sender().row, self.sender().column, "markState")  #邻居雷位置
        blankAndQuestionPosList = self.getNearPos(self.sender().row, self.sender().column, "blankState questionState") #邻居空白+问号位置
        
        mineNum = len(minePoslist)
        if mineNum != self.sender().value:
            self.operateGridTogether("setDown(False)", blankAndQuestionPosList)
        else:
            wrongMark = self.checkMark(minePoslist)
            if wrongMark == []:
                self.operateGridTogether("setDown(False)", blankAndQuestionPosList)
                z = []
                for r1, c1 in blankAndQuestionPosList:
                    z.append(self.gridLayout.itemAtPosition(r1, c1).widget().value)
                
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
        self.operateGridTogether("setDown(True)", self.getNearPos(self.sender().row, self.sender().column, "blankState questionState"))
    
    def gameFailed(self, clickFailed = True):
        t1 = list(set(self.markedMinesMap) - set(self.minesMap))
        self.operateGridTogether("setMarkWrongState()", t1)
        if clickFailed:
            self.markedMinesMap.append((self.sender().row, self.sender().column))
        t2 = list(set(self.minesMap) - set(self.markedMinesMap))
        self.operateGridTogether("setMineState()", t2)
        self.myTimer.stop()
        print("Fail!")
        
        for i in range(0, self.row):
            for j in range(0, self.column):
                self.gridLayout.itemAtPosition(i, j).widget().setDisableState()
    
    def mineMarked_(self):
        self.markedMinesMap.append((self.sender().row, self.sender().column))
        self.minesLeftLcd.display(self.mines - len(self.markedMinesMap))
    
    def cancelMineMarked_(self):
        self.markedMinesMap.remove((self.sender().row, self.sender().column))
        self.minesLeftLcd.display(self.mines - len(self.markedMinesMap))
    
    def timeDisplay(self):
        self.timeUsage += 1
        self.timeUsageLcd.display(self.timeUsage)
    
    def checkWin(self):
        tmpList = []
        for i in range(0, self.row):
            for j in range(0, self.column):
                if self.gridLayout.itemAtPosition(i, j).widget().state == "blankState" or self.gridLayout.itemAtPosition(i, j).widget().state == "questionState":
                    tmpList.append((i, j))
        if set(tmpList) == set(self.minesMap) - set(self.markedMinesMap):
            self.operateGridTogether("setMarkState()", tmpList)
            self.minesLeftLcd.display(0)
            self.myTimer.stop()
            print("Win! time: {} seconds".format(self.timeUsage))
            
            for i in range(0, self.row):
                for j in range(0, self.column):
                    self.gridLayout.itemAtPosition(i, j).widget().setDisableState()
    
    def aboutQtAction_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutGameAction_(self):
        QMessageBox.about(self, "About mine sweeper", "It's a Linux game cloned from classic windows game, written with PyQt.\n\nAuthor: sanfanling (xujia19@outlook.con)")
    
    def closeEvent(self, e):
        e.accept()
 
