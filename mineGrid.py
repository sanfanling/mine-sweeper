#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: mainGui.py
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mineGrid(QPushButton):
    touchPress = pyqtSignal()
    touchRelease = pyqtSignal()
    zeroTouched = pyqtSignal()
    def __init__(self, value): # value理论上为0-9,0意味着周边没有雷，表象上应该是灰色不可按；如value == -1,定义为“雷”
        super().__init__()
        self.value = value
        self.leftRight = False
        self.setBlankState()
        
    
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
        self.setText(str(self.value))
        self.setIcon(QIcon(""))
    
    # under explodeState, game over
    def setExplodeState(self):
        self.state = "explodeState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/explode.png"))
    
    # under zeroState, ignore all mouse mouse event
    def setZeroState(self):
        self.state = "zeroState"
        self.setFlat(True)
        self.setText("")
        self.setIcon(QIcon(""))
    
    
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
                if 1 <= self.value <= 9:
                    self.setNumberState()
                elif self.value == 0:
                    self.zeroTouched.emit()
                elif self.value == -1:
                    self.setExplodeState()
            elif e.button() == Qt.RightButton and not self.leftRight:
                self.setMarkState()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "markState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                self.setQuestionState()
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
                print("左右键同时释放")
                self.leftRight = False
                self.touchRelease.emit()
        
        elif self.state == "explodeState":
            pass
        
        elif self.state == "zeroState":
            pass
        
    def mouseMoveEvent(self, e):
        self.setDown(False)
    
    def mousePressEvent(self, e):
        if self.state == "blankState":
            if e.button() == Qt.LeftButton or e.button() == Qt.RightButton:
                self.setDown(True)
                self.leftRight = False
            if (e.buttons() == Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                print("左右键同时按下，但被屏蔽")
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
                print("左右键同时按下，但被屏蔽")
                self.setDown(True)
                self.leftRight = True
        
        elif self.state == "numberState":
            if e.buttons() == (Qt.LeftButton | Qt.RightButton) or e.button() == Qt.MidButton:
                print("左右键同时按下，有效")
                self.leftRight = True
                self.touchPress.emit()
                
        
        elif self.state == "explodeState":
            pass
        
        elif self.state == "zeroState":
            pass
        
    
    def sizeHint(self):
        return QSize(25, 25)
