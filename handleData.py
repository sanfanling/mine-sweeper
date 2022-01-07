#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: fetchData.py
#Author: sanfanling
#licence: GPL-V3 


from configparser import ConfigParser
import os.path



class handleData:
    
    def __init__(self):
        self.fileName = os.path.expanduser("~/.minesweeper.conf")
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
        self.easy_totalGame = self.cf.getint("easyMode", "totalGame")
        self.easy_winGame = self.cf.getint("easyMode", "winGame")
        self.medium_totalGame = self.cf.getint("mediumMode", "totalGame")
        self.medium_winGame = self.cf.getint("mediumMode", "winGame")
        self.difficult_totalGame = self.cf.getint("difficultMode", "totalGame")
        self.difficult_winGame = self.cf.getint("difficultMode", "winGame")
        self.__toAppType()
        #print(self.easyRankList, self.mediumRankList, self.difficultRankList)
    
    def __toAppType(self):
        self.customSize = tuple(int(x) for x in self.cf.get("custom", "size").split(","))
        easyList = []
        mediumList = []
        difficultList = []
        
        for i in range(1, 11):
            item1 = self.cf.get("easyMode", str(i)).strip()
            if item1 != "":
                easyList.append(item1)
                
            item2 = self.cf.get("mediumMode", str(i)).strip()
            if item2 != "":
                mediumList.append(item2)
                
            item3 = self.cf.get("difficultMode", str(i)).strip()
            if item3 != "":
                difficultList.append(item3)
        
        self.easyRankList = []
        self.mediumRankList = []
        self.difficultRankList = []
        for alpha in easyList:
            t= alpha.split(",")
            m1 = int(t[0])
            m2 = t[1].strip()
            m3 = t[2].strip()
            self.easyRankList.append((m1, m2, m3))
        for beta in mediumList:
            t = beta.split(",")
            m1 = int(t[0])
            m2 = t[1].strip()
            m3 = t[2].strip()
            self.mediumRankList.append((m1, m2, m3))
        for gama in difficultList:
            t = gama.split(",")
            m1 = int(t[0])
            m2 = t[1].strip()
            m3 = t[2].strip()
            self.difficultRankList.append((m1, m2, m3))
    
    
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
        self.cf.set("easyMode", "totalGame", str(self.easy_totalGame))
        self.cf.set("easyMode", "winGame", str(self.easy_winGame))
        self.cf.set("mediumMode", "totalGame", str(self.medium_totalGame))
        self.cf.set("mediumMode", "winGame", str(self.medium_winGame))
        self.cf.set("difficultMode", "totalGame", str(self.difficult_totalGame))
        self.cf.set("difficultMode", "winGame", str(self.difficult_winGame))
        self.cf.set("custom", "size", self.customSize)
        for p in range(1, 11):
            self.cf.set("easyMode", str(p), self.easyRankList[p - 1])
            self.cf.set("mediumMode", str(p), self.mediumRankList[p -1])
            self.cf.set("difficultMode", str(p), self.difficultRankList[p - 1])
    
    def __toStrTpye(self):
        self.customSize = ", ".join(map(str, self.customSize))
        
        
        tmpEasyList = []
        for i in self.easyRankList:
            item = (", ").join([str(x) for x in i])
            tmpEasyList.append(item)
        self.easyRankList = tmpEasyList + [""] * (10 - len(tmpEasyList))
        
        tmpMediumList = []
        for i in self.mediumRankList:
            item = (", ").join([str(x) for x in i])
            tmpMediumList.append(item)
        self.mediumRankList = tmpMediumList + [""] * (10 - len(tmpMediumList))
        
        tmpDifficultList = []
        for i in self.difficultRankList:
            item = (", ").join([str(x) for x in i])
            tmpDifficultList.append(item)
        self.difficultRankList = tmpDifficultList + [""] * (10 - len(tmpDifficultList))
    
    def compareToBest(self, timeUsage, mode):
        if mode == "Easy":
            compareList = self.easyRankList
        elif mode == "Medium":
            compareList = self.mediumRankList
        else:
            compareList = self.difficultRankList
        index = 0
        add = False
        for i in compareList:
            if timeUsage < i[0]:
                #compareList.insert(index, timeUsage)
                add = True
                return add, index
            else:
                index += 1
        if not add and len(compareList) < 10:
            return True, index
        else:
            return False, -1
    
    def updateBest(self, record, index, mode):
        if mode == "Easy":
            self.easyRankList.insert(index, record)
            if len(self.easyRankList) > 10:
                self.easyRankList = self.easyRankList[:10]
        elif mode == "Medium":
            self.mediumRankList.insert(index, record)
            if len(self.mediumRankList) > 10:
                self.mediumRankList = self.mediumRankList[:10]
        else:
            self.difficultRankList.insert(index, record)
            if len(self.difficultRankList) > 10:
                self.difficultRankList = self.difficultRankList[:10]
    
    def resetRecords(self, mode):
        if mode == "Easy":
            self.easyRankList = []
            self.easy_totalGame = 0
            self.easy_winGame = 0
        elif mode == "Medium":
            self.mediumRankList = []
            self.medium_totalGame = 0
            self.medium_winGame = 0
        elif mode == "Difficult":
            self.difficultRankList = []            
            self.difficult_totalGame = 0
            self.difficult_winGame = 0
    
    def updateTotalGame(self, mode):
        if mode == "Easy":
            self.easy_totalGame += 1
        elif mode == "Medium":
            self.medium_totalGame += 1
        else:
            self.difficult_totalGame += 1
        
    
    def updateWinGame(self, mode):
        if mode == "Easy":
            self.easy_winGame += 1
        elif mode == "Medium":
            self.medium_winGame += 1
        else:
            self.difficult_winGame += 1
    
    def updateLastMode(self, mode):
        self.lastMode = mode
            
    
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
