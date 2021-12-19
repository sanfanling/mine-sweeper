#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename: baseWindow.py
#licence: GPL-V3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys 


class baseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initMenubar()
        self.initPanelWidget()
        

    def initMenubar(self):
        gameMenu = self.menuBar().addMenu("Game")
        self.startAction = QAction("Start", self)
        self.checkRecordsAction = QAction("Check records...", self)
        self.quitAction = QAction("Quit", self)
        gameMenu.addAction(self.startAction)
        gameMenu.addAction(self.checkRecordsAction)
        gameMenu.addSeparator()
        gameMenu.addAction(self.quitAction)
        
        optionMenu = self.menuBar().addMenu("Option")
        modeMenu = optionMenu.addMenu("mode")
        modeGroup = QActionGroup(self)
        self.easyAction = QAction("Easy", self)
        self.easyAction.setCheckable(True)
        self.mediumAction = QAction("Medium", self)
        self.mediumAction.setCheckable(True)
        self.mediumAction.setChecked(True)
        self.difficultAction = QAction("Difficult", self)
        self.difficultAction.setCheckable(True)
        modeGroup.addAction(self.easyAction)
        modeGroup.addAction(self.mediumAction)
        modeGroup.addAction(self.difficultAction)
        modeMenu.addAction(self.easyAction)
        modeMenu.addAction(self.mediumAction)
        modeMenu.addAction(self.difficultAction)
        optionMenu.addSeparator()
        optionMenu.addSeparator()
        self.settingAction = QAction("Settings...", self)
        optionMenu.addAction(self.settingAction)
        
        helpMenu = self.menuBar().addMenu("Help")
        self.aboutGameAction = QAction("About mine sweeper...", self)
        self.aboutQtAction = QAction("About Qt...", self)
        helpMenu.addAction(self.aboutGameAction)
        helpMenu.addAction(self.aboutQtAction)
    
    def initPanelWidget(self):
        self.minesLeftLcd = QLCDNumber(self)
        self.newGameButton = QPushButton("Restart", self)
        self.timeUsageLcd = QLCDNumber(self)
