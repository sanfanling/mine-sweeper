#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: mineGrid.py
#Author: sanfanling
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mineGrid(QPushButton):
    
    touchPress = pyqtSignal()
    touchRelease = pyqtSignal()
    zeroTouched = pyqtSignal()
    mineTouched = pyqtSignal()
    mineMarked = pyqtSignal()
    cancelMineMarked = pyqtSignal()
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
        self.setText("")
        self.setIcon(QIcon(""))
    
    # under markState, accept right click (change to questionState), ignore left click and mid click 
    def setMarkState(self):
        self.state = "markState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/mark.png"))
    
    # under questionState, accept right click (change to blankState), ignore left click and mid click
    def setQuestionState(self):
        self.state = "questionState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/question.png"))
    
    # under numberState, only accept mid click
    def setNumberState(self):
        self.state = "numberState"
        self.setFlat(True)
        pal = self.palette()
        colorDict = {1: QColor(0, 0, 254), 2: QColor(0, 128, 0), 3: QColor(254, 0, 0), 4: QColor(0, 0, 128), 5: QColor(128, 0, 0), 6: QColor(128, 128, 0), 7: QColor(0, 0, 0), 8: QColor(128, 128, 128)}
        pal.setColor(QPalette.WindowText, colorDict[self.value])
        self.setPalette(pal)
        self.setText(str(self.value))
        self.setIcon(QIcon(""))
    
    # under explodeState, game over
    def setExplodeState(self):
        self.state = "explodeState"
        self.setFlat(False)
        self.setText("")
        pal = self.palette()
        pal.setColor(QPalette.Button, Qt.red)
        self.setPalette(pal)
        self.setIcon(QIcon("sources/mine.png"))
    
    def setMarkWrongState(self):
        self.state = "markWrongState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/wrong.png"))
        
    # under zeroState, ignore all mouse mouse event
    def setZeroState(self):
        self.state = "zeroState"
        self.setFlat(True)
        self.setText("")
        self.setIcon(QIcon(""))
    
    def setMineState(self):
        self.state = "mineState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/mine.png"))
    
    def setDisableState(self):
        self.state = "disableState"
    
    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.touchRelease.emit()
        
    def mouseReleaseEvent(self, e):
        if not self.rect().contains(e.pos()):
            if self.state == 'numberState' and self.leftRight:
                self.touchRelease.emit()
            else:
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
                    self.zeroTouched.emit()
                elif self.value == -1:
                    self.setExplodeState()
                    self.mineTouched.emit()
            elif e.button() == Qt.RightButton and not self.leftRight:
                self.setMarkState()
                self.mineMarked.emit()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "markState":
            self.setDown(False)
            if e.button() == Qt.RightButton and self.acceptQuestionMark and not self.leftRight:
                self.setQuestionState()
                self.cancelMineMarked.emit()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "questionState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                self.setBlankState()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "numberState":
            if (e.button() == Qt.LeftButton and self.leftRight and e.buttons() == Qt.NoButton) or (e.button() == Qt.RightButton and self.leftRight and e.buttons() == Qt.NoButton) or e.button() == Qt.MidButton:
                #print("左右键同时释放")
                self.leftRight = False
                self.touchRelease.emit()
        
    def mouseMoveEvent(self, e):
        self.setDown(False)
    
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
                print("左右键同时按下，但被屏蔽")
                self.setDown(True)
                self.leftRight = True
        
        elif self.state == "questionState":
            if e.button() == Qt.RightButton:
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
                self.touchPress.emit()
    
    def sizeHint(self):
       return QSize(25, 25)
