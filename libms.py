#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: sanfanling
#program name: libms.py
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
            self.base = []
            for i in range(self.height):
                self.base.append([0 for j in range(self.width)])
        else:
            self.base = zeros((self.height, self.width), dtype = "int")
        
        self.minesMap = []
        
        
    def generate(self):
        self.__getMines()
        self.__detectMines()

    def __getMines(self):
        while len(self.minesMap) < self.mines:
            heightPos = random.choice(range(self.height))
            widthPos = random.choice(range(self.width))
            if (heightPos, widthPos) not in self.minesMap:
                self.minesMap.append((heightPos, widthPos))
        for i, j in self.minesMap:
            self.base[i][j] = -1        

    def __detectMines(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.base[i][j] == -1:
                    continue
                else:
                    mn = self.__mineNum(i, j)
                    self.base[i][j] = mn

    def __mineNum(self, hp, wp):
        direction = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        mn = 0
        for h, w in direction:
            newH = hp + h
            newW = wp + w
            if newH not in range(0, self.height) or newW not in range(0, self.width):
                continue
            else:
                if self.base[newH][newW] == -1:
                    mn += 1
        return mn




def main():
    a = mineSweeper(15, 20, 80)
    print(a.generate())

if __name__ == "__main__":
    main()
