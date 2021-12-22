#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: ms.py
#Author: sanfanling
#licence: GPL-V3


from PyQt5.QtWidgets import QApplication
from mainWindow import mainWindow
import sys


def main():
    app = QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_()) 


if __name__ == "__main__":
    main()
