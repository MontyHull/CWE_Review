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

        self.angleX = 90.0
        self.angleY = 0.0

        self.cameraInitX = 0
        self.cameraInitY = 0

        self.angle = 90.0
        self.stepSizeX = 5
        self.stepSizeY = 5
        self.buttonDown = False

        self.M = makeTopoMap.get_matrix(rows=10, cols=10, seed=1117, maxval=8)
        self.maxval = 8.0
        #self.M = [[1,3,1],
        #     [0,0,0],
        #     [1,3,1]]
        self.t = 6.5
        self.ULX = -5
        self.ULY = 5
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

    def mouse(self, button, state, x, y):
        print(str(['button-action', button, state, x, y]))
        if button == 0 and state == 0:
            self.buttonDown = True
            self.cameraInitX = self.angleX
            self.cameraInitY = self.angleY

            self.dragX = x
            self.dragY = y

        elif button == 0 and state == 1:
            self.buttonDown = False

    def motion(self, x, y):
        print(str(['motion',x,y]))
        if x > self.dragX:
            self.angleX += .5
        if x < self.dragX:
            self.angleX -= .5
        self.dragX = x
        glutPostRedisplay()

    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit()


    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if(key ==100):
            self.angleX -= 1
        if(key == 102):
            self.angleX += 1
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

        glPushMatrix()

        eye_x = 60 * math.cos(math.radians(self.angleX))
        eye_y = 0
        eye_z = 60 * math.sin(math.radians(self.angleX))
        gluLookAt(eye_x , eye_y , eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glScalef(5.0,5.0,2.0)
        for i in range(9):
            for j in range(9):

                ULx = self.ULX+j
                ULy = self.ULY-i
                ULz = self.M[i][j]
                ULshade = .3+(ULz/self.maxval)*.7

                URx = self.ULX+j+1
                URy = self.ULY-i
                URz = self.M[i][j+1]
                URshade = .3+(URz/self.maxval)*.7

                LRx = self.ULX+j+1
                LRy = self.ULY-(i+1)
                LRz = self.M[i+1][j+1]
                LRshade = .3+(LRz/self.maxval)*.7

                LLx = self.ULX+j
                LLy = self.ULY-(i+1)
                LLz = self.M[i+1][j]
                LLshade = .3+(LLz/self.maxval)*.7
                print("ULshade =",ULshade)
                print("URshade =",URshade)
                print("LLshade =",LLshade)
                print("LRshade =",LRshade)
                print(self.M)
                glBegin(GL_TRIANGLES)
                glColor3f(URshade, URshade, URshade)
                glVertex3f(URx,URy,URz)
                glColor3f(ULshade, ULshade, ULshade)
                glVertex3f(ULx,ULy,ULz)
                glColor3f(LLshade, LLshade, LLshade)
                glVertex3f(LLx,LLy,LLz)
                glEnd()
                glBegin(GL_TRIANGLES)
                glColor3f(LLshade, LLshade, LLshade)
                glVertex3f(LLx,LLy,LLz)
                glColor3f(LRshade, LRshade, LRshade)
                glVertex3f(LRx,LRy,LRz)
                glColor3f(URshade, URshade, URshade)
                glVertex3f(URx,URy,URz)
                glEnd()



        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
