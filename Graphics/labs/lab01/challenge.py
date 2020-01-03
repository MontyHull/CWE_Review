#!/usr/bin/python3
import sys

class census:
    """Self Documenting! Woohoo!"""
    byNumber = {}
    byDistrict = {}
    def __init__(self,filename):
        """filename should be the name of the census file """
        self.filename = filename
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

    def saveKML(self,whereToSave):
        with open(self.filename,'r') as fileobj:
            newfile = open(whereToSave,'w')

            newfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n")
            newfile.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
            newfile.write("<Document>\n")
            for line in fileobj:
                placeword= line[212:316]
                place = placeword[14:].rstrip()
                number = placeword[:14].strip()
                word= line[336:361]
                lat = word[1:11]
                lon = word[-14:].rstrip()
                newfile.write(" <Placemark>\n")
                newfile.write("     <name>"+place+"</name>\n")
                newfile.write("     <description>"+number+"</description>\n")
                newfile.write("     <Point>\n")
                newfile.write("         <coordinates>"+lon+","+lat+"</coordinates>\n")
                newfile.write("     </Point>\n")
                newfile.write(" </Placemark>\n")
            newfile.write("</Document>\n")
            newfile.write("</kml>\n")
