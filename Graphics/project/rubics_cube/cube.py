#!/usr/bin/python3

# Load in Required libraries
import math, numpy, time, random

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Cube:
    def __init__(self):
        # XYZ
        # X) L = LEFT, M = MIDDLE, R = RIGHT
        # Y) T = TOP, M = MIDDLE, B = BOTTOM
        # Z) F = FRONT, M = MIDDLE, R = REAR
        self.pieces = {}

        self.pieces["LTF"] = Piece(["BLUE","BLACK","YELLOW","BLACK","RED","BLACK"])
        self.pieces["LTM"] = Piece(["BLUE","BLACK","BLACK","BLACK","RED","BLACK"])
        self.pieces["LTR"] = Piece(["BLUE","BLACK","BLACK","WHITE","RED","BLACK"])
        self.pieces["LMF"] = Piece(["BLACK","BLACK","YELLOW","BLACK","RED","BLACK"])
        self.pieces["LMM"] = Piece(["BLACK","BLACK","BLACK","BLACK","RED","BLACK"])
        self.pieces["LMR"] = Piece(["BLACK","BLACK","BLACK","WHITE","RED","BLACK"])
        self.pieces["LBF"] = Piece(["BLACK","GREEN","YELLOW","BLACK","RED","BLACK"])
        self.pieces["LBM"] = Piece(["BLACK","GREEN","BLACK","BLACK","RED","BLACK"])
        self.pieces["LBR"] = Piece(["BLACK","GREEN","BLACK","WHITE","RED","BLACK"])

        self.pieces["MTF"] = Piece(["BLUE","BLACK","YELLOW","BLACK","BLACK","BLACK"])
        self.pieces["MTM"] = Piece(["BLUE","BLACK","BLACK","BLACK","BLACK","BLACK"])
        self.pieces["MTR"] = Piece(["BLUE","BLACK","BLACK","WHITE","BLACK","BLACK"])
        self.pieces["MMF"] = Piece(["BLACK","BLACK","YELLOW","BLACK","BLACK","BLACK"])
        self.pieces["MMM"] = Piece(["BLACK","BLACK","BLACK","BLACK","BLACK","BLACK"])
        self.pieces["MMR"] = Piece(["BLACK","BLACK","BLACK","WHITE","BLACK","BLACK"])
        self.pieces["MBF"] = Piece(["BLACK","GREEN","YELLOW","BLACK","BLACK","BLACK"])
        self.pieces["MBM"] = Piece(["BLACK","GREEN","BLACK","BLACK","BLACK","BLACK"])
        self.pieces["MBR"] = Piece(["BLACK","GREEN","BLACK","WHITE","BLACK","BLACK"])

        self.pieces["RTF"] = Piece(["BLUE","BLACK","YELLOW","BLACK","BLACK","ORANGE"])
        self.pieces["RTM"] = Piece(["BLUE","BLACK","BLACK","BLACK","BLACK","ORANGE"])
        self.pieces["RTR"] = Piece(["BLUE","BLACK","BLACK","WHITE","BLACK","ORANGE"])
        self.pieces["RMF"] = Piece(["BLACK","BLACK","YELLOW","BLACK","BLACK","ORANGE"])
        self.pieces["RMM"] = Piece(["BLACK","BLACK","BLACK","BLACK","BLACK","ORANGE"])
        self.pieces["RMR"] = Piece(["BLACK","BLACK","BLACK","WHITE","BLACK","ORANGE"])
        self.pieces["RBF"] = Piece(["BLACK","GREEN","YELLOW","BLACK","BLACK","ORANGE"])
        self.pieces["RBM"] = Piece(["BLACK","GREEN","BLACK","BLACK","BLACK","ORANGE"])
        self.pieces["RBR"] = Piece(["BLACK","GREEN","BLACK","WHITE","BLACK","ORANGE"])


    def rotateTop(self):
        glPushMatrix()
        glRotatef(45.0, 0.0, 1.0, 0.0)

        for key in self.pieces:
            if key[1] == "T":
                print("yes")
                self.pieces[key].draw()
        glPopMatrix()
        print("I should have rotated")

    def draw(self):

        # X) L = LEFT, M = MIDDLE, R = RIGHT
        # Y) T = TOP, M = MIDDLE, B = BOTTOM
        # Z) F = FRONT, M = MIDDLE, R = REAR
        for key in self.pieces:
            glPushMatrix()
            if key[0] == "L":
                x = -10.0
            elif key[0] == "R":
                x = 10.0
            else:
                x = 0.0
            if key[1] == "T":
                y = 10.0
            elif key[1] == "B":
                y = -10.0
            else:
                y = 0.0
            if key[2] == "F":
                z = 10.0
            elif key[2] =="R":
                z = -10.0
            else:
                z = 0.0
            glTranslatef(x,y,z)
            self.pieces[key].draw()
            glPopMatrix()


class Piece:
    def __init__(self,which_piece=["BLUE","BLACK","BLACK","WHITE","RED","BLACK"]):
        self.c = {"RED":[1.0,0.0,0.0],"WHITE":[1.0,1.0,1.0],"ORANGE":[1.0,.64,0.0],"YELLOW":[1.0,1.0,0.0],"GREEN":[0.0,1.0,0.0],"BLUE":[0.0,0.0,1.0],"BLACK":[0.0,0.0,0.0]}

        '''
        top = [0] , bottom = [1]
        front = [2] , back = [3]
        left = [4] , right = [5]
        '''
        self.pos = which_piece

        #corners
        self.FLT = [-5,5,5]
        self.FLB = [-5,-5,5]
        self.FRT = [5,5,5]
        self.FRB = [5,-5,5]

        self.BLT = [-5,5,-5]
        self.BLB = [-5,-5,-5]
        self.BRT = [5,5,-5]
        self.BRB = [5,-5,-5]
    def draw(self):

        # FRONT
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[2]][0],self.c[self.pos[2]][1],self.c[self.pos[2]][2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.FLT[0],self.FLT[1],self.FLT[2])
        glVertex3f(self.FRT[0],self.FRT[1],self.FRT[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[2]][0],self.c[self.pos[2]][1],self.c[self.pos[2]][2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.FRB[0],self.FRB[1],self.FRB[2])
        glVertex3f(self.FRT[0],self.FRT[1],self.FRT[2])
        glEnd()

        # LEFT
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[4]][0],self.c[self.pos[4]][1],self.c[self.pos[4]][2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.FLT[0],self.FLT[1],self.FLT[2])
        glVertex3f(self.BLT[0],self.BLT[1],self.BLT[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[4]][0],self.c[self.pos[4]][1],self.c[self.pos[4]][2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.BLB[0],self.BLB[1],self.BLB[2])
        glVertex3f(self.BLT[0],self.BLT[1],self.BLT[2])
        glEnd()
        # BACK
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[3]][0],self.c[self.pos[3]][1],self.c[self.pos[3]][2])
        glVertex3f(self.BLB[0],self.BLB[1],self.BLB[2])
        glVertex3f(self.BLT[0],self.BLT[1],self.BLT[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[3]][0],self.c[self.pos[3]][1],self.c[self.pos[3]][2])
        glVertex3f(self.BLB[0],self.BLB[1],self.BLB[2])
        glVertex3f(self.BRB[0],self.BRB[1],self.BRB[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glEnd()
        # RIGHT
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[5]][0],self.c[self.pos[5]][1],self.c[self.pos[5]][2])
        glVertex3f(self.FRB[0],self.FRB[1],self.FRB[2])
        glVertex3f(self.FRT[0],self.FRT[1],self.FRT[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[5]][0],self.c[self.pos[5]][1],self.c[self.pos[5]][2])
        glVertex3f(self.FRB[0],self.FRB[1],self.FRB[2])
        glVertex3f(self.BRB[0],self.BRB[1],self.BRB[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glEnd()
        # TOP
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[0]][0],self.c[self.pos[0]][1],self.c[self.pos[0]][2])
        glVertex3f(self.FRT[0],self.FRT[1],self.FRT[2])
        glVertex3f(self.FLT[0],self.FLT[1],self.FLT[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[0]][0],self.c[self.pos[0]][1],self.c[self.pos[0]][2])
        glVertex3f(self.FLT[0],self.FLT[1],self.FLT[2])
        glVertex3f(self.BRT[0],self.BRT[1],self.BRT[2])
        glVertex3f(self.BLT[0],self.BLT[1],self.BLT[2])
        glEnd()
        # BOTTOM
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[1]][0],self.c[self.pos[1]][1],self.c[self.pos[1]][2])
        glVertex3f(self.FRB[0],self.FRB[1],self.FRB[2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.BRB[0],self.BRB[1],self.BRB[2])
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor3f(self.c[self.pos[1]][0],self.c[self.pos[1]][1],self.c[self.pos[1]][2])
        glVertex3f(self.FLB[0],self.FLB[1],self.FLB[2])
        glVertex3f(self.BRB[0],self.BRB[1],self.BRB[2])
        glVertex3f(self.BLB[0],self.BLB[1],self.BLB[2])
        glEnd()
        glColor3f(0.0,0.0,0.0)
        glutWireCube(10.0)
