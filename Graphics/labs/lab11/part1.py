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

        self.M = makeTopoMap.get_matrix(rows=10, cols=10, seed=331)

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

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        eye_x = 60 * math.cos(math.radians(self.angleX))
        eye_y = 0
        eye_z = 60 * math.sin(math.radians(self.angleX))
        gluLookAt(eye_x , eye_y , eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glScalef(5.0,5.0,2.0)
        for i in range(9):
            for j in range(9):

                glBegin(GL_LINE_LOOP)
                ULx = self.ULX+j
                ULy = self.ULY-i
                ULz = self.M[i][j]
                glVertex3f(ULx,ULy,ULz)

                URx = self.ULX+j+1
                URy = self.ULY-i
                URz = self.M[i][j+1]
                glVertex3f(URx,URy,URz)

                LRx = self.ULX+j+1
                LRy = self.ULY-(i+1)
                LRz = self.M[i+1][j+1]
                glVertex3f(LRx,LRy,LRz)

                LLx = self.ULX+j
                LLy = self.ULY-(i+1)
                LLz = self.M[i+1][j]
                glVertex3f(LLx,LLy,LLz)
                glEnd()



        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
