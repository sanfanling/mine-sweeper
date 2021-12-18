#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: mainGui.py
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from mineGrid import mineGrid
from libms import mineSweeper
import sys


class mainGui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.row = 5
        self.column = 10
        self.mines = 10
        game = mineSweeper(self.row, self.column, self.mines)
        sources = game.generate()
        print(sources)
        gridLayout = QGridLayout(None)
        
        gridLayout.setSpacing(0)
        for i in range(self.row):
            for j in range(self.column):
                exec("self.grid{}_{} = mineGrid(sources[{}][{}])".format(i, j, i, j))
                eval("gridLayout.addWidget(self.grid{}_{}, {}, {})".format(i, j, i, j))
                eval("self.grid{}_{}.setObjectName('{}-{}')".format(i, j, i, j))
                eval("self.grid{}_{}.touched.connect(self.touched_)".format(i, j))
        self.res = QPushButton("Restore", self)
        mainLayout = QVBoxLayout(None)
        mainLayout.setSizeConstraint(3)
        mainLayout.addLayout(gridLayout)
        mainLayout.addWidget(self.res)
        self.setLayout(mainLayout)
        
        self.res.clicked.connect(self.restore)
    
    def touched_(self):
        print(self.sender().objectName())
        
    
    def restore(self):
        for i in range(self.row):
            for j in range(self.column):
                eval("self.grid{}_{}.blankState()".format(i, j))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = mainGui()
    w.show()
    sys.exit(app.exec_()) 
