#!/usr/bin/python3
import sys

class census:
    """Self Documenting! Woohoo!"""
    byNumber = {}
    byDistrict = {}
    def __init__(self,filename):
        """filename should be the name of the census file """
        with open(filename,'r') as fileobj:
            for line in fileobj:
                word= line[212:316]
                number = word[:14]
                place = word[14:].rstrip()
                fullset = place + number
                prettyprint = fullset[-14:].strip().ljust(21) + fullset[:-14].rstrip()
                self.byNumber[number.strip()] = prettyprint
                self.byDistrict[place] = prettyprint

    def display(self):
        """will display in alphabetical order each district and their number """
        b = sorted(self.byDistrict)
        for key in b:
            print(self.byDistrict[key])


    def searchByNum(self,number):
        """Number variable should be the number asociated with the district that is to be printed"""
        if(str(number) in self.byNumber):
            print(self.byNumber[str(number)])


    def searchByDistrict(self,district):
        """District should be the district that you are looking for"""
        if(district in self.byDistrict):
            print(self.byDistrict[district])
