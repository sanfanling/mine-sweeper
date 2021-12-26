#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: statisticsDialog.py
#Author: sanfanling
#licence: GPL-V3 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class displayBestDialog(QDialog):
    
    def __init__(self, mode, rankList):
        super().__init__()
        self.setWindowTitle("Made a record!")
        self.setWindowIcon(QIcon("sources/mine.png"))
        self.setMinimumWidth(350)
        
        self.display = baseBestBox(mode, rankList)
        
        self.buttonBox = QDialogButtonBox(self)
        self.okButton = QPushButton("OK")
        self.buttonBox.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.display)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        
        self.buttonBox.accepted.connect(self.accept)
    
    def highLightCurrentRecord(self, ind):
        font = self.display.gridLayout.itemAtPosition(ind + 1, 0).widget().font()
        font.setItalic(True)
        font.setBold(True)
        for i in range(4):
            self.display.gridLayout.itemAtPosition(ind + 1, i).widget().setFont(font)
        
        

class statisticsDialog(QDialog):
    
    def __init__(self, easyRankList = [], easy_totalGame = 0, easy_winGame = 0, mediumRankList = [], medium_totalGame = 0, medium_winGame = 0, difficultRankList = [], difficult_totalGame = 0, difficult_winGame = 0):
        super().__init__()
        self.setWindowTitle("Statistics")
        self.setWindowIcon(QIcon("sources/mine.png"))
        self.setMinimumWidth(350)
        
        self.chooseItem = QComboBox()
        self.chooseItem.addItems(["Easy mode", "Medium mode", "Difficult mode"])
        
        self.stackedWidget = QStackedWidget()
        self.easyPage = basePage("easy mode", easyRankList, easy_totalGame, easy_winGame)
        self.mediumPage = basePage("medium mode", mediumRankList, medium_totalGame, medium_winGame)
        self.difficultPage = basePage("difficult mode", difficultRankList, difficult_totalGame, difficult_winGame)
        self.stackedWidget.addWidget(self.easyPage)
        self.stackedWidget.addWidget(self.mediumPage)
        self.stackedWidget.addWidget(self.difficultPage)
        
        self.buttonBox = QDialogButtonBox(self)
        self.resetButton = QPushButton("Reset")
        self.okButton = QPushButton("OK")
        self.buttonBox.addButton(self.resetButton, QDialogButtonBox.ResetRole)
        self.buttonBox.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.chooseItem)
        mainLayout.addWidget(self.stackedWidget)
        mainLayout.addWidget(self.buttonBox)
        
        self.setLayout(mainLayout)
        
        self.chooseItem.activated.connect(self.changePage)
        self.buttonBox.accepted.connect(self.accept)
        self.resetButton.clicked.connect(self.reset)
    
    def reset(self):
        pass
    
    def changePage(self, index):
        self.stackedWidget.setCurrentIndex(index)


class basePage(QWidget):
    
    def __init__(self, mode, rankList, totalGame, winGame):
        super().__init__()
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(baseBestBox(mode, rankList))
        mainLayout.addWidget(baseOverallBox(mode, totalGame, winGame))
        self.setLayout(mainLayout)
        
    
    
class baseBestBox(QGroupBox):
    
    def __init__(self, mode, rankList):
        super().__init__()
        self.setTitle("Best of {}".format(mode))
        self.setAlignment(Qt.AlignHCenter)
        self.gridLayout = QGridLayout(None)
        self.gridLayout.addWidget(QLabel("Rank", self), 0, 0)
        self.gridLayout.addWidget(QLabel("Time", self), 0, 1)
        self.gridLayout.addWidget(QLabel("User", self), 0, 2)
        self.gridLayout.addWidget(QLabel("Date", self), 0, 3)
        
        for i in range(1, 11):
            for j in range(4):
                if j == 0:
                    w = QLabel(str(i), self)
                else:
                    w = QLabel(self)
                self.gridLayout.addWidget(w, i, j)
        self.setLayout(self.gridLayout)
        
        rank = 0
        for item in rankList:
            rank += 1
            self.gridLayout.itemAtPosition(rank, 1).widget().setText(str(item[0]))
            self.gridLayout.itemAtPosition(rank, 2).widget().setText(item[1])
            self.gridLayout.itemAtPosition(rank, 3).widget().setText(item[2])
        


class baseOverallBox(QGroupBox):
    
    def __init__(self, mode, totalGame, winGame):
        super().__init__()
        self.setTitle("Overall of {}".format(mode))
        self.setAlignment(Qt.AlignHCenter)
        self.gridLayout = QGridLayout(None)
        self.gridLayout.addWidget(QLabel("Games:", self), 0, 0)
        self.gridLayout.addWidget(QLabel("Wins:", self), 1, 0)
        self.gridLayout.addWidget(QLabel("Percentage:", self), 2, 0)
        self.gridLayout.addWidget(QLabel(str(totalGame), self), 0, 1)
        self.gridLayout.addWidget(QLabel(str(winGame), self), 1, 1)
        if totalGame == 0:
            self.gridLayout.addWidget(QLabel("Null", self), 2, 1)
        else:
            self.gridLayout.addWidget(QLabel("{}%".format(round(winGame / totalGame * 100, 2)), self), 2, 1)
        self.setLayout(self.gridLayout)



def main():
    app = QApplication(sys.argv)
    w = statisticsDialog()
    w.show()
    sys.exit(app.exec_()) 


if __name__ == "__main__":
    main()
