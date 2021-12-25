#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: statistics.py
#Author: sanfanling
#licence: GPL-V3 

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys



class statistics(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistics")
        self.setWindowIcon(QIcon("sources/mine.png"))
        
        self.chooseItem = QComboBox()
        self.chooseItem.addItems(["Easy mode", "Medium mode", "Difficult mode"])
        
        self.stackedWidget = QStackedWidget()
        self.easyPage = basePage("easy mode")
        self.mediumPage = basePage("medium mode")
        self.difficultPage = basePage("difficult mode")
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
    
    def __init__(self, mode):
        super().__init__()
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(baseBestBox(mode))
        mainLayout.addWidget(baseOverallBox(mode))
        self.setLayout(mainLayout)
        
    
    
class baseBestBox(QGroupBox):
    
    def __init__(self, mode):
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
                w = QLabel(self)
                self.gridLayout.addWidget(w, i, j)
        self.setLayout(self.gridLayout)
        


class baseOverallBox(QGroupBox):
    
    def __init__(self, mode):
        super().__init__()
        self.setTitle("Overall of {}".format(mode))
        self.setAlignment(Qt.AlignHCenter)
        self.gridLayout = QGridLayout(None)
        self.gridLayout.addWidget(QLabel("Games:", self), 0, 0)
        self.gridLayout.addWidget(QLabel("Wins:", self), 1, 0)
        self.gridLayout.addWidget(QLabel("Percentage:", self), 2, 0)
        self.gridLayout.addWidget(QLabel(""), 0, 1)
        self.gridLayout.addWidget(QLabel(""), 1, 1)
        self.gridLayout.addWidget(QLabel(""), 2, 1)
        self.setLayout(self.gridLayout)



def main():
    app = QApplication(sys.argv)
    w = statistics()
    w.show()
    sys.exit(app.exec_()) 


if __name__ == "__main__":
    main()
