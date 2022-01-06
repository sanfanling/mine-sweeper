#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: mineGrid.py
#Author: sanfanling
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mineGrid(QPushButton):
    
    touchPress = pyqtSignal(int, int)
    touchRelease = pyqtSignal(int, int)
    zeroTouched = pyqtSignal(int, int)
    mineTouched = pyqtSignal(int, int, bool)
    mineMarked = pyqtSignal(int, int)
    cancelMineMarked = pyqtSignal(int, int)
    touchCancel = pyqtSignal(int, int)
    numberMarked = pyqtSignal()
    
    def __init__(self, row, column, acceptQuestionMark = True, value = 0): # value理论上为0-8,0意味着周边没有雷，表象上应该是灰色不可按；如value == -1,定义为“雷”
        super().__init__()
        self.value = value
        self.row = row
        self.column = column
        self.acceptQuestionMark = acceptQuestionMark
        self.leftRight = False
        self.setBlankState()
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Minimum)
        policy.setVerticalPolicy(QSizePolicy.Minimum)
        self.setSizePolicy(policy)
    
    def setQuestionMark(self, b):
        self.acceptQuestionMark = b
    
    def setValue(self, v):
        self.value = v
    
    def setGridSize(self, s):
        self.setFixedSize(QSize(s, s))
        
    def setNumberSize(self, n):
        font = self.font()
        font.setPointSize(n)
        self.setFont(font)
        
    # under blankState, accept left click (check the blank) and right click (change to markState), ignore mid click
    def setBlankState(self):
        self.state = "blankState"
        self.setDown(False)
        self.setFlat(False)
        self.setEnabled(True)
        self.setText("")
        s = "QPushButton{background-color: rgb(98, 131, 204); border: 1px outset black} QPushButton:hover{background-color: rgb(119, 160, 248); border: 1px outset black} QPushButton:pressed{background-color: rgb(184, 229, 251); border-style:inset}"
        self.setStyleSheet(s)
    
    # under markState, accept right click (change to questionState), ignore left click and mid click 
    def setMarkState(self):
        self.state = "markState"
        self.setFlat(False)
        self.setText("")
        s = "QPushButton{border-image: url(./sources/pictures/mark.png); background-color: rgb(98, 131, 204); border: 1px outset black}"
        self.setStyleSheet(s)
        #self.setIcon(QIcon("sources/pictures/mark.png"))
    
    # under questionState, accept right click (change to blankState), ignore left click and mid click
    def setQuestionState(self):
        self.state = "questionState"
        self.setFlat(False)
        self.setText("")
        s = "QPushButton{border-image: url(./sources/pictures/question.png); background-color: rgb(98, 131, 204); border: 1px outset black}"
        self.setStyleSheet(s)
        #self.setIcon(QIcon("sources/pictures/question.png"))
    
    # under numberState, only accept mid click
    def setNumberState(self):
        self.state = "numberState"
        self.setFlat(True)
        colorDict = {1: "rgb(0, 0, 254)", 2: "rgb(0, 128, 0)", 3: "rgb(254, 0, 0)", 4: "rgb(0, 0, 128)", 5: "rgb(128, 0, 0)", 6: "rgb(128, 128, 0)", 7: "rgb(0, 0, 0)", 8: "rgb(128, 128, 128)"}
        s = "QPushButton{}color: {}; border: 1px solid black{}".format("{", colorDict[self.value], "}")
        self.setStyleSheet(s)
        self.setText(str(self.value))
    
    # under explodeState, game over
    def setExplodeState(self):
        self.state = "explodeState"
        self.setFlat(False)
        self.setText("")
        s = "QPushButton{background-color: red; border-image: url(./sources/pictures/mine.png); border: 1px solid black}"
        self.setStyleSheet(s)
        #self.setIcon(QIcon("sources/pictures/mine.png"))
    
    def setMarkWrongState(self):
        self.state = "markWrongState"
        self.setFlat(False)
        self.setText("")
        s = "QPushButton{background-color: rgb(98, 131, 204); border-image: url(./sources/pictures/wrong.png); border: 1px solid black}"
        self.setStyleSheet(s)
        #self.setIcon(QIcon("sources/pictures/wrong.png"))
        
    # under zeroState, ignore all mouse mouse event
    def setZeroState(self):
        self.state = "zeroState"
        #self.setFlat(True)
        self.setEnabled(False)
        s = "QPushButton{background-color: rgb(217, 217, 217); border: 1px dashed black}"
        self.setStyleSheet(s)
        self.setText("")
    
    def setMineState(self):
        self.state = "mineState"
        self.setFlat(False)
        self.setText("")
        s = "QPushButton{background-color: rgb(98, 131, 204); border-image: url(./sources/pictures/mine.png); border: 1px solid black}"
        self.setStyleSheet(s)
        #self.setIcon(QIcon("sources/pictures/mine.png"))
    
    def setDisableState(self):
        self.state = "disableState"
    
    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.touchRelease.emit(self.row, self.column)
        
    def mouseReleaseEvent(self, e):
        if not self.rect().contains(e.pos()):
            self.setDown(False)
            self.leftRight = False
            return
        
        if self.state == "blankState":
            self.setDown(False)
            if e.button() == Qt.LeftButton and not self.leftRight:
                if 1 <= self.value <= 8:
                    self.setNumberState()
                    self.numberMarked.emit()
                elif self.value == 0:
                    self.zeroTouched.emit(self.row, self.column)
                elif self.value == -1:
                    self.setExplodeState()
                    self.mineTouched.emit(self.row, self.column, True)
            elif e.button() == Qt.RightButton and not self.leftRight:
                self.setMarkState()
                self.mineMarked.emit(self.row, self.column)
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "markState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                if self.acceptQuestionMark: 
                    self.setQuestionState()
                else:
                    self.setBlankState()
                self.cancelMineMarked.emit(self.row, self.column)
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "questionState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                self.setBlankState()
            elif e.button() == Qt.LeftButton and not self.leftRight:
                self.setBlankState()
                self.mouseReleaseEvent(e)
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "numberState":
            if (e.button() == Qt.LeftButton and self.leftRight and e.buttons() == Qt.NoButton) or (e.button() == Qt.RightButton and self.leftRight and e.buttons() == Qt.NoButton) or e.button() == Qt.MidButton:
                #print("左右键同时释放")
                self.leftRight = False
                self.touchRelease.emit(self.row, self.column)
        
    def mouseMoveEvent(self, e):
        if not self.rect().contains(e.pos()):
            self.setDown(False)
            if self.state == 'numberState' and self.leftRight:
                self.touchCancel.emit(self.row, self.column)
    
    def mousePressEvent(self, e):
        if self.state == "blankState":
            if e.button() == Qt.LeftButton or e.button() == Qt.RightButton:
                self.setDown(True)
                self.leftRight = False
            if (e.buttons() == Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                #print("左右键同时按下，但被屏蔽")
                self.setDown(True)
                self.leftRight = True
        
        elif self.state == "markState":
            if e.button() == Qt.RightButton:
                self.setDown(True)
                self.leftRight = False
            if (e.buttons() == Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                #print("左右键同时按下，但被屏蔽")
                self.setDown(True)
                self.leftRight = True
        
        elif self.state == "questionState":
            if e.button() == Qt.RightButton or e.button() == Qt.LeftButton:
                self.setDown(True)
                self.leftRight = False
            if (e.buttons() == Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                #print("左右键同时按下，但被屏蔽")
                self.setDown(True)
                self.leftRight = True
        
        elif self.state == "numberState":
            if e.buttons() == (Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                #print("左右键同时按下，有效")
                self.leftRight = True
                self.touchPress.emit(self.row, self.column)
    
    def sizeHint(self):
       return QSize(25, 25)
