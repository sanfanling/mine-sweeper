#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: mainWindow.py
#Author: sanfanling
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from baseWindow import baseWindow
from mineGrid import mineGrid
from libms import mineSweeper
from settingDialog import settingDialog
from handleData import handleData
from statisticsDialog import statisticsDialog, displayBestDialog
import getpass
import time
import sys


class mainWindow(baseWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mine sweeper")
        self.setWindowIcon(QIcon("sources/mine.png"))
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        
        self.data = handleData()
        self.data.getAllData()
        
        
        self.mode = self.data.lastMode
        self.modeDict = {"Easy": (9, 9, 10), "Medium": (16, 16, 40), "Difficult": (16, 30, 99)}
        self.modeDict["Custom"] = self.data.customSize
        self.row, self.column, self.mines = self.modeDict[self.mode]
        eval("self.{}Action.setChecked(True)".format(self.mode.lower()))
        self.myTimer = QTimer()
        self.soundEffect = QSoundEffect(self)
        self.timeUsage = 0
        self.originalGridPal = self.palette()
        
        self.virtualNewWorld()
        
        self.statisticsAction.triggered.connect(self.statisticsAction_)
        self.myTimer.timeout.connect(self.timeDisplay)
        self.newAction.triggered.connect(self.virtualNewGame)
        self.newGameButton.clicked.connect(self.virtualNewGame)
        self.replayAction.triggered.connect(self.virtualReplay)
        self.quitAction.triggered.connect(self.close)
        self.easyAction.triggered.connect(self.changeMode_)
        self.mediumAction.triggered.connect(self.changeMode_)
        self.difficultAction.triggered.connect(self.changeMode_)
        self.customAction.triggered.connect(self.changeMode_)
        self.settingAction.triggered.connect(self.settingAction_)
        self.resizeTimer.timeout.connect(self.adjustSize)
    
    def initBoard(self):
        self.gridLayout = QGridLayout(None)
        self.gridLayout.setSpacing(0)
        for i in range(self.row):
            for j in range(self.column):
                m = mineGrid(i, j)
                m.setGridSize(self.data.gridSize)
                m.setNumberSize(self.data.numberSize)
                m.setQuestionMark(self.data.questionMark)
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
        #self.adjustSize()
        self.resizeTimer.start(100)
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
        self.data.updateTotalGame(self.mode)
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
        if self.data.sound:
            self.soundEffect.setSource(QUrl.fromLocalFile("sources/bomb.wav"))
            self.soundEffect.play()
        
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
            if self.data.sound:
                self.soundEffect.setSource(QUrl.fromLocalFile("sources/win.wav"))
                self.soundEffect.play()
            
            for i in range(0, self.row):
                for j in range(0, self.column):
                    self.gridLayout.itemAtPosition(i, j).widget().setDisableState()
            
            
            
            if self.mode != "Custom":
                self.data.updateWinGame(self.mode)
                add, ind = self.data.compareToBest(self.timeUsage, self.mode)
                if add:
                    # ask user name
                    user, ok = QInputDialog.getText(self, "Input player name", "Player name:", 0, getpass.getuser())
                    record = (self.timeUsage, user, time.strftime("%Y-%m-%d"))
                    self.data.updateBest(record, ind, self.mode)
                    if self.mode == "Easy":
                        r = self.data.easyRankList
                    elif self.mode == "Medium":
                        r = self.data.mediumRankList
                    else:
                        r = self.data.difficultRankList
                    bestDialog = displayBestDialog(self.mode, r)
                    bestDialog.highLightCurrentRecord(ind)
                    bestDialog.exec_()
                    
                    
    def statisticsAction_(self):
        dialog = statisticsDialog(self.data.easyRankList, self.data.easy_totalGame, self.data.easy_winGame, self.data.mediumRankList, self.data.medium_totalGame, self.data.medium_winGame, self.data.difficultRankList, self.data.difficult_totalGame, self.data.difficult_winGame)
        index = {"Easy": 0, "Medium": 1, "Difficult": 2, "Custom": 0}[self.mode]
        dialog.chooseItem.setCurrentIndex(index)
        dialog.stackedWidget.setCurrentIndex(index)
        dialog.dataReset.connect(self.data.resetRecords)
        dialog.exec_()
            

    def settingAction_(self):
        dialog = settingDialog()
        logicalDict1 = {True: 2, False: 0}
        dialog.generalBox.questionMark.setCheckState(logicalDict1[self.data.questionMark])
        dialog.generalBox.autoStart.setCheckState(logicalDict1[self.data.autoStart])
        dialog.generalBox.sound.setCheckState(logicalDict1[self.data.sound])
        dialog.interfaceBox.gridSize.setValue(self.data.gridSize)
        dialog.interfaceBox.numberSize.setValue(self.data.numberSize)
        h, w, m = self.data.customSize
        dialog.customBox.customHeight.setValue(h)
        dialog.customBox.customWidth.setValue(w)
        dialog.customBox.customMines.setValue(m)
        if dialog.exec_() == QDialog.Accepted:
            logicalDict2 = {2: True, 0: False}
            self.data.questionMark = logicalDict2[dialog.generalBox.questionMark.checkState()]
            self.data.autoStart = logicalDict2[dialog.generalBox.autoStart.checkState()]
            self.data.sound = logicalDict2[dialog.generalBox.sound.checkState()]
            self.data.gridSize = dialog.interfaceBox.gridSize.value()
            self.data.numberSize = dialog.interfaceBox.numberSize.value()
            self.data.customSize = (dialog.customBox.customHeight.value(), dialog.customBox.customWidth.value(), dialog.customBox.customMines.value())
            
            # proceed questionMark
            for x in range(self.row):
                for y in range(self.column):
                    w = self.gridLayout.itemAtPosition(x, y).widget()
                    w.setQuestionMark(self.data.questionMark)
                    if not self.data.questionMark and w.state == "questionState":
                        w.setBlankState()
            
            
            
            # proceed autoStart
            # proceed sound
            # procedd grid size
            # proceed number size
            for i in range(self.row):
                for j in range(self.column):
                    self.gridLayout.itemAtPosition(i, j).widget().setNumberSize(self.data.numberSize)
                    self.gridLayout.itemAtPosition(i, j).widget().setGridSize(self.data.gridSize)
            
            self.modeDict["Custom"] = self.data.customSize
            self.resizeTimer.start(100)

    
    def closeEvent(self, e):
        self.data.updateLastMode(self.mode)
        self.data.setAllData()
        self.data.writeToFile()
        e.accept()
 
