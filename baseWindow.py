#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: baseWindow.py
#Author: sanfanling
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
        
        self.aboutGameAction.triggered.connect(self.aboutGameAction_)
        self.aboutQtAction.triggered.connect(self.aboutQtAction_)

    def initMenubar(self):
        gameMenu = self.menuBar().addMenu("Game")
        self.newAction = QAction("New game", self)
        self.replayAction = QAction("Re-play", self)
        self.statisticsAction = QAction("Statistics...", self)
        self.quitAction = QAction("Quit", self)
        gameMenu.addAction(self.newAction)
        gameMenu.addAction(self.replayAction)
        gameMenu.addSeparator()
        gameMenu.addAction(self.statisticsAction)
        gameMenu.addSeparator()
        gameMenu.addAction(self.quitAction)
        
        optionMenu = self.menuBar().addMenu("Option")
        modeMenu = optionMenu.addMenu("mode")
        modeGroup = QActionGroup(self)
        self.easyAction = QAction("Easy", self)
        self.easyAction.setCheckable(True)
        self.mediumAction = QAction("Medium", self)
        self.mediumAction.setCheckable(True)
        self.difficultAction = QAction("Difficult", self)
        self.difficultAction.setCheckable(True)
        self.customAction = QAction("Custom", self)
        self.customAction.setCheckable(True)
        modeGroup.addAction(self.easyAction)
        modeGroup.addAction(self.mediumAction)
        modeGroup.addAction(self.difficultAction)
        modeGroup.addAction(self.customAction)
        modeMenu.addAction(self.easyAction)
        modeMenu.addAction(self.mediumAction)
        modeMenu.addAction(self.difficultAction)
        modeMenu.addAction(self.customAction)
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
        self.newGameButton = QPushButton("New", self)
        #self.replayButton = QPushButton("Re-play", self)
        self.timeUsageLcd = QLCDNumber(self)
    
    def aboutQtAction_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutGameAction_(self):
        QMessageBox.about(self, "About mine sweeper", "It is a PyQt5 version of classic windows mine sweeper game. The final purpose of this application is no difference between clone version and windows classic version.\n\nAuthor: sanfanling (xujia19@outlook.con)")
