#!/usr/bin/python3

# Load in Required libraries
import math, numpy, time

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Our new Scene Class
class Scene:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.timeStep = 0
        self.timeStepSize = 0.02
        self.angle = 0.0

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        #glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("ex6.py")
        glutDisplayFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboardSpecial)
        glutMainLoop()


    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit()

    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if(key ==100):
            self.angle -= .01
            glutPostRedisplay()

        if(key == 102):
            self.angle += .01
            glutPostRedisplay()

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        gluLookAt(60*math.cos(self.angle) ,0.0,60* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glutWireSphere(30.0,20,20)
        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
