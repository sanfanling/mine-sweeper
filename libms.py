#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: libms.py
#Author: sanfanling
#license: GPL-V3

import random

class mineSweeper:
    def __init__(self, height = 10, width = 10, mines = 5):
        self.height = height
        self.width = width
        self.mines = mines
        if self.mines > self.height * self.width / 2:
            raise ValueError("too many mines in defined area.")
        
        try:
            from numpy import zeros
        except ModuleNotFoundError:
            self.base = [[0 for i in range(self.width)] for j in range(self.height)]
        else:
            self.base = zeros((self.height, self.width), dtype = "int")
        self.minesMap = []
        
        
    def generate(self):
        self.__getMines()
        self.__detectMines()
        self.__getZeroPoint()
        #print(self.base)

    def __getMines(self):
        while len(self.minesMap) < self.mines:
            heightPos = random.choice(range(self.height))
            widthPos = random.choice(range(self.width))
            if (heightPos, widthPos) not in self.minesMap:
                self.minesMap.append((heightPos, widthPos))
        for i, j in self.minesMap:
            self.base[i][j] = -1

    def __detectMines(self):
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for row, col in self.minesMap:
            for offsetRow, offsetCol in direction:
                nowRow = row + offsetRow
                nowCol = col + offsetCol
                if nowRow in range(self.height) and nowCol in range(self.width) and self.base[nowRow][nowCol] != -1:
                    self.base[nowRow][nowCol] += 1
    
    def __getZeroPoint(self):
        zeroMap = []
        for i in range(self.height):
            for j in range(self.width):
                if self.base[i][j] == 0:
                    zeroMap.append((i, j))
        direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for point in zeroMap:
            tmpList = list(map(lambda x: (x[0] + point[0], x[1] + point[1]), zeroMap))
            if set(tmpList).issubset(set(zeroMap)):
                self.zeroPoint = point
                return
        self.zeroPoint = random.choice(zeroMap)
            

def main():
    a = mineSweeper(3, 9, 10)
    a.generate()

if __name__ == "__main__":
    main()
