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
        self.angle = 0.0
        self.stepSizeX = 5
        self.stepSizeY = 5
        self.pressed = False

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
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutMainLoop()

    def mouse(self,buttonNumber,state,x,y):
        print"['mouse', "+str(buttonNumber)+", "+str(state)+", "+str(x)+", "+str(y)+"]"
        if state == 0:
            self.pressed = True
            self.dragX = x
        if state == 1:
            self.pressed = False
        glutPostRedisplay()

    def motion(self,x,y):
        print"['motion', "+str(x)+", "+str(y)+"]"

        if(x > self.dragX):
            self.angle += .02
        if(x < self.dragX):
            self.angle -= .02
        self.dragX = x
        glutPostRedisplay()

    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit()

    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if(key ==100):
            self.angle -= .01
        if(key == 102):
            self.angle += .01
        if(key == 101 and self.stepSizeX <= 180):
            self.stepSizeX += 1
            self.stepSizeY += 1

        if(key == 103 and self.stepSizeX >= 2):
            self.stepSizeX -= 1
            self.stepSizeY -= 1
        glutPostRedisplay()

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        gluLookAt(60*math.cos(self.angle) ,0.0,60* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glBegin(GL_POINTS)
        for angleX in range(0,360,self.stepSizeX):
            for angleY in range(0, 360, self.stepSizeY):
                # Solve for x, y, z
                radX = math.pi/180*angleX
                radY = math.pi/180*angleY
                x = 30.0 * math.cos(radX) * math.sin(radY)
                y = 30.0 * math.sin(radX) * math.sin(radY)
                z = 30.0 * math.cos(radY)
                glVertex3f(x,y,z)
        glEnd()
        glutWireSphere( 5.0,10,10)
        glutWireCube(20.0)
        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
