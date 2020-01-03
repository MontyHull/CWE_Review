#!/usr/bin/python3

# Load in Required libraries
import math, numpy, time, makeTopoMap

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Our new Scene Class
class Scene:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.angle = 90.0
        self.stepSizeX = 5
        self.stepSizeY = 5
        self.pressed = False

        self.rows = 100
        self.cols = 100

        self.M = makeTopoMap.get_matrix(seed=331, rows=self.rows, cols=self.cols, delta=3, maxval=20)
        #self.M = [[1,3,1],
        #     [0,0,0],
        #     [1,3,1]]
        self.t = 0.5
        self.ULX = -(self.cols//2)
        self.ULY = self.rows//2
        print(self.ULX,self.ULY)
        print(self.M)
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

    def difference(self,a,b):
        if(a > b):
            return((self.t-b)/(a-b))
        return((self.t-a)/(b-a))

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        #gluLookAt(-60.0,0.0,70.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        eye_x = 100 * math.cos(math.radians(self.angle))
        eye_y = 0
        eye_z = 100 * math.sin(math.radians(self.angle))
        gluLookAt(eye_x , eye_y , eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #gluLookAt(100*math.cos(self.angle) ,0.0,100* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        for k in range(20):
            for i in range(9):
                for j in range(9):
                    glBegin(GL_LINES)
                    # UL to UR
                    a = self.M[i][j]
                    b = self.M[i][j+1]
                    if((a >= self.t) ^ (b >= self.t)):
                        dif = self.difference(a,b)
                        if(a > b):
                            dif = 1-dif
                        x=j+self.ULX+dif
                        y=self.ULY-i
                        glVertex3f(x,y,0)

                    # UR to LR
                    a = self.M[i][j+1]
                    b = self.M[i+1][j+1]
                    if((a >= self.t) ^ (b >= self.t)):
                        dif = self.difference(a,b)
                        if(a > b):
                            dif = 1-dif
                        x=self.ULX +(j+1)
                        y=self.ULY-i-dif
                        glVertex3f(x,y,0)

                    # LR to LL
                    a = self.M[i+1][j+1]
                    b = self.M[i+1][j]
                    if((a >= self.t) ^ (b >= self.t)):
                        dif = self.difference(a,b)
                        if(b > a):
                            dif = 1-dif
                        x=j+self.ULX+dif
                        y=self.ULY-(i+1)
                        glVertex3f(x,y,0)

                    # LL to UL
                    a = self.M[i+1][j]
                    b = self.M[i][j]
                    if((a >= self.t) ^ (b >= self.t)):
                        dif = self.difference(a,b)
                        if(b > a):
                            dif = 1-dif
                        x=j+self.ULX
                        y=self.ULY-i-dif
                        glVertex3f(x,y,0)

                    glEnd()
            self.t = self.t + 1.0
        self.t = 0.5
        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
