#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos
from math import sin
from math import pi
import sys

class Scene:
    def __init__(self,save_or_load="neither",filename="none"):

        # Initialize the environment
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

        # Set the initial window position and size (if we want to)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(600, 500)
        self.width = 600
        self.height = 500
        # Create the window and name it
        glutCreateWindow("Lab 5 - Dodge Ball")

        # Build the scene
        glutDisplayFunc(self.display)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # Build the Bounding box - much more on this later!
        glOrtho(0.0, 600.0, 0.0, 500.0, -2.0, 1.0)
        # Go into a loop
        glutMainLoop()
    def circle(self,deltaX,deltaY,X,Y,Z,R,numberOfVertices,fill=False):
        if fill:
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(X, Y, 0.0)
        else:
            glBegin(GL_LINE_LOOP)
        theta=0
        for i in range(numberOfVertices):
            glVertex3f(X + R * cos(theta), Y + R * sin(theta), 0.0)
            theta = theta + 2 * pi / numberOfVertices
        glEnd()

    def box(self,deltaX,deltaY,LLX,LLY,URX,URY,Z,fill=False):
        glBegin(GL_LINE_LOOP)
        glVertex3f(LLX,LLY,Z)
        glVertex3f(LLX,URY,Z)
        glVertex3f(URX,URY,Z)
        glVertex3f(URX,LLY,Z)
        glEnd()

    def text(self,deltaX,deltaY,scale,X,Y,Z,font,myText):
        # Position our cursor within the scene
        glRasterPos3f(X,Y,Z)
        for char in myText:
            glutBitmapCharacter(font, ord(char))

    def line(self,deltaX,deltaY,scale,x1,y1,x2,y2,Z):
        glBegin(GL_LINES)
        glVertex3f(x1,y1,Z)
        glVertex3f(x2,y2,Z)
        glEnd()

    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit(0)
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
        #if(y > 50 and y < 400 and (self.prev.y <= 50 or self.prev.y >=400)):
        #    self.lines.append([])
        if(x > 100 and x < 500 and y > 50 and y < 400):
            self.lines[len(self.lines)-1].append(Point(x,self.height-y))
        self.prev.x = x
        glutPostRedisplay()


    # The function that we will use to draw the environment
    def display(self):
        F1 = [[self.circle, [50, 80, 0, 15, 35], "head"],
      [self.circle, [43, 85, 0, 5, 35], "right eye"],
      [self.circle, [57, 85, 0, 5, 35], "left eye"],
      [self.line, [46, 70, 54, 70, 0], "mouth"],
      [self.line, [50, 20, 50, 65, 0], "body"],
      [self.line, [50, 50, 10, 60, 0], "right arm"],
      [self.line, [50, 50, 90, 60, 0], "left arm"],
      [self.line, [50, 20, 10, 0, 0], "right leg"],
      [self.line, [50, 20, 90, 0, 0], "left leg"]]
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for component in F1:
            print("Drawing: "+component[-1])
            component[0](deltaX,deltaY,scaleFactor,*component[1])
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboardSpecial)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        glFlush()

if __name__ == '__main__':
    scene = Scene()
