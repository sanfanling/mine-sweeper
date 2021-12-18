#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: mainGui.py
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class mineGrid(QPushButton):
    touched = pyqtSignal()
    def __init__(self, source): # source理论上为0-9,0意味着周边没有雷，表象上应该是灰色不可按；如source == -1,定义为“雷”
        super().__init__()
        self.source = source
        self.leftRight = False
        self.blankState()
        
    
    # under blankState, accept left click (check the blank) and right click (change to markState), ignore mid click
    def blankState(self):
        self.state = "blankState"
        self.setDown(False)
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon(""))
    
    # under markState, accept right click (change to questionState), ignore left click and mid click 
    def markState(self):
        self.state = "markState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/mark.png"))
    
    # under questionState, accept right click (change to blankState), ignore left click and mid click
    def questionState(self):
        self.state = "questionState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/question.png"))
    
    # under numberState, only accept mid click
    def numberState(self):
        self.state = "numberState"
        self.setFlat(True)
        self.setText(str(self.source))
        self.setIcon(QIcon(""))
    
    # under explodeState, game over
    def explodeState(self):
        self.state = "explodeState"
        self.setFlat(False)
        self.setText("")
        self.setIcon(QIcon("sources/explode.png"))
    
    # under zeroState, ignore all mouse mouse event
    def zeroState(self):
        self.state = "zeroState"
        self.setFlat(True)
        self.setText("")
        self.setIcon(QIcon(""))
    
    def checkAround(self): # if mines around, show a down-up state changing in around grids, otherwise change to numberState or zeroState
        print("探索周边")
        self.touched.emit()
    
    
    def mouseReleaseEvent(self, e):
        if not self.rect().contains(e.pos()):
            self.setDown(False)
            self.leftRight = False
            return
        
        if self.state == "blankState":
            self.setDown(False)
            if e.button() == Qt.LeftButton and not self.leftRight:
                if 1 <= self.source <= 9:
                    self.numberState()
                elif self.source == 0:
                    self.zeroState()
                elif self.source == -1:
                    self.explodeState()
            elif e.button() == Qt.RightButton and not self.leftRight:
                self.markState()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "markState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                self.questionState()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "questionState":
            self.setDown(False)
            if e.button() == Qt.RightButton and not self.leftRight:
                self.blankState()
            elif e.buttons() == Qt.NoButton and self.leftRight:
                self.leftRight = False
        
        elif self.state == "numberState":
            if (e.button() == Qt.LeftButton and self.leftRight and e.buttons() == Qt.NoButton) or (e.button() == Qt.RightButton and self.leftRight and e.buttons() == Qt.NoButton) or e.button() == Qt.MidButton:
                print("左右键同时释放")
                self.leftRight = False
                self.checkAround()
        
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
        
        elif self.state == "explodeState":
            pass
        
        elif self.state == "zeroState":
            pass
        
    
    def sizeHint(self):
        return QSize(25, 25)
