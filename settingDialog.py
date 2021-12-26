#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: settingDialog.py
#Author: sanfanling
#licence: GPL-V3  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys 


class settingDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setting")
        self.setWindowIcon(QIcon("sources/mine.png"))
        
        buttonBox = QDialogButtonBox(self)
        cancelButton = QPushButton("Cancel")
        okButton = QPushButton("OK")
        buttonBox.addButton(cancelButton, QDialogButtonBox.RejectRole)
        buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        
        self.generalBox = generalBox()
        self.interfaceBox = interfaceBox()
        self.customBox = customBox()
        
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.generalBox)
        mainLayout.addWidget(self.interfaceBox)
        mainLayout.addWidget(self.customBox)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
                
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class generalBox(QGroupBox):
    
    def __init__(self):
        super().__init__()
        self.setTitle("General")
        self.setAlignment(Qt.AlignHCenter)
        
        self.questionMark = QCheckBox("Enable \"?\" mark in the game", self)
        self.autoStart = QCheckBox("Auto start at first", self)
        self.autoStart.setEnabled(False)
        self.sound = QCheckBox("Enable sound effect", self)
        #self.sound.setEnabled(False)
        
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.questionMark)
        mainLayout.addWidget(self.autoStart)
        mainLayout.addWidget(self.sound)
        self.setLayout(mainLayout)


class interfaceBox(QGroupBox):
    
    def __init__(self):
        super().__init__()
        self.setTitle("Interface")
        self.setAlignment(Qt.AlignHCenter)
        
        mainLayout = QGridLayout(None)
        self.gridSizeLabel = QLabel("Set the grid size:", self)
        mainLayout.addWidget(self.gridSizeLabel, 0, 0)
        self.gridSize = QSpinBox(self)
        self.gridSize.setMinimum(24) # very interesting, to MAMBA
        mainLayout.addWidget(self.gridSize, 0, 1)
        self.numberSizeLabel = QLabel("Set the number size:", self)
        mainLayout.addWidget(self.numberSizeLabel, 1, 0)
        self.numberSize = QSpinBox(self)
        self.numberSize.setMinimum(8) # very interesting, to MAMBA
        mainLayout.addWidget(self.numberSize, 1, 1)
        self.setLayout(mainLayout)
        

class customBox(QGroupBox):
    
    def __init__(self):
        super().__init__()
        self.setTitle("Custom mode")
        self.setAlignment(Qt.AlignHCenter)
        
        mainLayout = QGridLayout(None)
        self.customHeightLabel = QLabel("Set custom height:", self)
        mainLayout.addWidget(self.customHeightLabel, 0, 0)
        self.customHeight = QSpinBox(self)
        self.customHeight.setMinimum(2)
        mainLayout.addWidget(self.customHeight, 0, 1)
        self.customWidthLabel = QLabel("Set custom width:", self)
        mainLayout.addWidget(self.customWidthLabel, 1, 0)
        self.customWidth = QSpinBox(self)
        self.customWidth.setMinimum(2)
        mainLayout.addWidget(self.customWidth, 1, 1)
        self.customMinesLabel = QLabel("Set custom mines:", self)
        mainLayout.addWidget(self.customMinesLabel, 2, 0)
        self.customMines = QSpinBox(self)
        self.customMines.setMinimum(1)
        mainLayout.addWidget(self.customMines, 2, 1)
        self.setLayout(mainLayout)
        



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = settingDialog()
	w.show()
	sys.exit(app.exec_())
