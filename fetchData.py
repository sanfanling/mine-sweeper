#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: fetchData.py
#Author: sanfanling
#licence: GPL-V3 


from configparser import ConfigParser
import os.path



class fetchData:
    
    def __init__(self):
        self.fileName = expanduser("~/.minesweeper.conf")
        if not os.path.exists(self.fileName):
            self.initConfigfile()
    
    def getAllData(self):
        self.cf = ConfigParser()
        self.cf.read(self.fileName)
        self.questionMark = self.cf.getboolean("general", "questionMark")
        self.autoStart = self.cf.getboolean("general", "autoStart")
        self.sound = self.cf.getboolean("general", "sound")
        self.lastMode = self.cf.get("general", "lastMode")
        self.gridSize = self.cf.getint("general", "gridSize")
        self.numberSize = self.cf.getint("general", "numberSize")
        self.straightWin = self.cf.getint("general", "straightWin")
        self.straightLose = self.cf. getint("general", "straightLose")
        self.currentStraight = self.cf. getint("general", "currentStraight")
        self.customSize = self.cf.get("custom", "size")
        for x in ("easy", "medium", "difficult"):
            exec("self.{}_totalGame = self.cf.getint('{}Mode', 'totalGame')".format(x, x))
            exec("self.{}_totalGame = self.cf.getint('{}Mode', 'winGame')".format(x, x))
            for y in range(1, 11):
                exec("self.{}_{} = self.cf.get('{}Mode', '{}')".format(x, y, x, y))
        self.__toPythonType()
    
    def setAllData(self):
        self.__toStrTpye()
        self.cf.set("general", "questionMark", str(self.questionMark))
        self.cf.set("general", "autoStart", str(self.autoStart))
        self.cf.set("general", "sound", str(self.sound))
        self.cf.set("general", "gridSize", str(self.gridSize))
        self.cf.set("general", "numberSize", str(self.numberSize))
        self.cf.set("general", "lastMode", self.lastMode)
        self.cf.set("general", "straightWin", str(self.straightWin))
        self.cf.set("general", "straightLose", str(self.straightLose))
        self.cf.set("general", "currentStraight", str(self.currentStraight))
        for x in ("easy", "medium", "difficult"):
            eval("self.cf.set('{}Mode', 'totalGame', self.{}_totalGame".format(x, x))
            eval("self.cf.set('{}Mode', 'winGame', self.{}_totalGame".format(x, x))
            for y in range(1, 11):
                eval("self.cf.set('{}Mode', '{}', self.{}_{}".format(x, y, x, y))
    
    def __toPythonType(self):
        self.customSize = tuple(int(x) for x in self.customSize.split(","))
    
    def __toStrTpye(self):
        self.customSize = ",".join(map(str, self.customSize))
    
    def writeToFile(self):
        with open(self.fileName, "w") as f:
            self.cf.write(f)
    
    def initConfigfile(self):
        conf = """
        ### this file is generated by application, recording all settings and statistics
        
        [general]
        questionMark = True
        autoStart = False
        sound = False
        gridSize = 25
        numberSize = 10
        lastMode = Easy
        straightWin = 0
        straightLose = 0
        currentStraight = 0
        
        
        [easyMode]
        1 = 
        2 = 
        3 = 
        4 =
        5 = 
        6 =
        7 =
        8 =
        9 =
        10 =
        totalGame = 0
        winGame = 0
        
        [mediumMode]
        1 = 
        2 = 
        3 = 
        4 =
        5 = 
        6 =
        7 =
        8 =
        9 =
        10 =
        totalGame = 0
        winGame = 0
        
        [difficultMode]
        1 = 
        2 = 
        3 = 
        4 =
        5 = 
        6 =
        7 =
        8 =
        9 =
        10 =
        totalGame = 0
        winGame = 0
        
        [custom]
        size = 10, 10, 10
        """
        with open(self.fileName, "w") as f:
            f.write(conf)
