#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos
from math import sin
import sys
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


class Scene:
    def __init__(self,save_or_load="neither",filename="none"):
        self.sol = save_or_load
        self.filename = filename
        if(save_or_load == "load"):
            fp = open(self.filename,'r')
            self.lines = []
            for line in fp:
                self.lines.append([])
                p = line.strip().split(",")
                for elements in p:
                    twonumbs = elements.split(":")
                    if(len(twonumbs)==2):
                        self.lines[len(self.lines)-1].append(Point(int(twonumbs[0]),int(twonumbs[1])))
        else:
            self.lines = []
        self.prev = Point(0,0)
        # Initialize the environment
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

        # Set the initial window position and size (if we want to)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(600, 500)
        self.width = 600
        self.height = 500
        # Create the window and name it
        glutCreateWindow("Lab 4 - Etch-a-Sketch")

        # Build the scene
        glutDisplayFunc(self.display)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # Build the Bounding box - much more on this later!
        glOrtho(0.0, 600.0, 0.0, 500.0, -2.0, 1.0)
        # Go into a loop
        glutMainLoop()
    def draw_circle(self,x,y,z,radius):
        glColor3f(1.0, 1.0, 1.0)   # White
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
            radian = i * (3.14159/180)
            x1 = x+cos(radian)*radius
            y1 = y+sin(radian)*radius
            glVertex3f(x1,y1,0.0)
        glEnd()
    def draw_box(self,x1,y1,z1,x2,y2,z2):
        glBegin(GL_LINE_LOOP)
        glVertex3f(x1,y1,z1)
        glVertex3f(x1,y2,z1)
        glVertex3f(x2,y2,z2)
        glVertex3f(x2,y1,z2)
        glEnd()

    def draw_text(self,x,y,z,message):
        # Position our cursor within the scene
        glRasterPos3f(x,y,z)
        for char in message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))


    def draw_all_lines(self):
        for i in range(len(self.lines)):
            if(len(self.lines[i]) == 1):
                glBegin(GL_POINTS)
                glVertex(self.lines[i][0].x,self.lines[i][0].y)
                glEnd()
            else:
                glBegin(GL_LINE_STRIP)
                for j in range(len(self.lines[i])):
                    glVertex(self.lines[i][j].x,self.lines[i][j].y)
                glEnd()
    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            if(self.sol == "save"):
                print("we should save")
                fp = open(self.filename,'w')
                for item in(self.lines):
                    for point in item:
                        fp.write(str(point.x)+":"+str(point.y)+",")
                    fp.write("\n")
            sys.exit(0)
        if key == 'c':
            self.lines = []
        glutPostRedisplay()
    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"
        glutPostRedisplay()


    def mouse(self,buttonNumber,state,x,y):
        print"['mouse', "+str(buttonNumber)+", "+str(state)+", "+str(x)+", "+str(y)+"]"
        #when you start append a new [] then start adding points to it in motion
        #when you end add the final point
        if(state == 0):
            self.lines.append([])
            if(x > 100 and x < 500 and y > 50 and y < 400):
                self.lines[len(self.lines)-1].append(Point(x,self.height-y))
        glutPostRedisplay()

    def motion(self,x,y):
        print"['motion', "+str(x)+", "+str(y)+"]"
        if(x > 100 and x < 500 and (self.prev.x <= 100 or self.prev.x >=500)):
            self.lines.append([])
        if(y > 50 and y < 400 and (self.prev.y <= 50 or self.prev.y >=400)):
            self.lines.append([])
        if(x > 100 and x < 500 and y > 50 and y < 400):
            self.lines[len(self.lines)-1].append(Point(x,self.height-y))
        self.prev.x = x
        glutPostRedisplay()
    # The function that we will use to draw the environment
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.draw_circle(50,50,0,40)
        self.draw_circle(550,50,0,40)
        self.draw_box(100,100,0,500,450,0)
        self.draw_text(220,470,0,"Etch-a-Sketch")
        self.draw_all_lines()
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboardSpecial)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        glFlush()







if __name__ == '__main__':
    if(len(sys.argv) == 1):
        new_Scence = Scene()
    elif(len(sys.argv) == 2):
        print("You need to choose to save/load and give a file name")
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == "-s"):
            new_Scence = Scene("save",sys.argv[2])
        elif(sys.argv[1] == "-l"):
            new_Scene = Scene("load",sys.argv[2])
        else:
            print("You must use -s or -l as the second argument")
    else:
        print("USAGE: python Scene.py [-l,-s] filename")














        #glutMotionFunc(self.motion)
