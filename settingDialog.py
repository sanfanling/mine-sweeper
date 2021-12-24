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
        
        mainLayout = QVBoxLayout(None)
        mainLayout.addWidget(self.generalBox)
        mainLayout.addWidget(self.interfaceBox)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
        
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)







class generalBox(QGroupBox):
    
    def __init__(self):
        super().__init__()
        self.setTitle("General")
        self.setAlignment(Qt.AlignHCenter)
        
        self.questionMark = QCheckBox("Use \"?\" mark", self)
        self.autoStart = QCheckBox("Auto start at first", self)
        self.sound = QCheckBox("Enable sound effect", self)
        
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
        self.gridSizeLabel = QLabel("Set the grid size: ", self)
        mainLayout.addWidget(self.gridSizeLabel, 0, 0)
        self.gridSizeSpin = QSpinBox(self)
        mainLayout.addWidget(self.gridSizeSpin, 0, 1)
        self.numberSizeLabel = QLabel("Set the number size:", self)
        mainLayout.addWidget(self.numberSizeLabel, 1, 0)
        self.numberSizeSpin = QSpinBox(self)
        mainLayout.addWidget(self.numberSizeSpin, 1, 1)
        self.setLayout(mainLayout)
        
        
        



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = settingDialog()
	w.show()
	sys.exit(app.exec_())
