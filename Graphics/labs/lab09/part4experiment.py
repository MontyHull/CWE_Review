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
        self.sphereX = 0.0
        self.sphereY = 0.0
        self.sphereZ = 30.0
        self.sphereAngleX = 0.0
        self.sphereAngleY = 0.0
        self.sphereAngleZ = 0.0




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
            self.dragY = y
        if state == 1:
            self.pressed = False
        glutPostRedisplay()

    def motion(self,x,y):
        print"['motion', "+str(x)+", "+str(y)+"]"


        
        if(x > self.dragX):
            self.sphereAngleX += 1
            self.sphereAngleZ += 1

            self.sphereX = 30*math.sin(math.radians(self.sphereAngleX))
            self.sphereZ = 30*math.cos(math.radians(self.sphereAngleX))
            #self.sphereZ = 30*math.cos(math.radians(self.sphereAngleZ))

        if(x < self.dragX):
            self.sphereAngleX -= 1
            self.sphereAngleZ -= 1

            self.sphereX = 30*math.sin(math.radians(self.sphereAngleX))
            self.sphereZ = 30*math.cos(math.radians(self.sphereAngleX))
            #self.sphereZ = 30*math.cos(math.radians(self.sphereAngleZ))


        if(y > self.dragY):
            self.sphereAngleY += 1
            self.sphereAngleZ += 1

            self.sphereY = 30*math.sin(math.radians(self.sphereAngleY))
            self.sphereZ = 30*math.cos(math.radians(self.sphereAngleY))
            #self.sphereZ = 30*math.cos(math.radians(self.sphereAngleZ))

        if(y < self.dragY):
            self.sphereAngleY -= 1
            self.sphereAngleZ -= 1

            self.sphereY = 30*math.sin(math.radians(self.sphereAngleY))
            self.sphereZ = 30*math.cos(math.radians(self.sphereAngleY))
            #self.sphereZ = 30*math.cos(math.radians(self.sphereAngleZ))


        self.dragX = x
        self.dragY = y
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

        #gluLookAt(60*math.sin(self.angle) ,0.0,60* math.cos(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        gluLookAt(60*math.cos(self.angle) ,0.0,60* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glBegin(GL_POINTS)
        for angleX in range(0,360,self.stepSizeX):
            for angleY in range(0, 360, self.stepSizeY):
                # Solve for x, y, z
                radY = math.pi/180*angleY
                radX = math.pi/180*angleX
                x = 30.0 * math.cos(radX) * math.sin(radY)
                y = 30.0 * math.sin(radX) * math.sin(radY)
                z = 30.0 * math.cos(radY)
                glVertex3f(x,y,z)
        glEnd()

        '''
        self.sphereX = 30*math.cos(math.radians(self.sphereAngle))*math.sin(math.radians(self.sphereAngle))
        self.sphereZ = 30*math.cos(math.radians(self.sphereAngle))
        '''

        glColor3f(1.0, 0, 0)
        glBegin(GL_POINTS)
        for angX in range(0,360,5):
            for angY in range(0,360,5):
                # Solve for x, y, z
                radY = math.pi/180*angY
                radX = math.pi/180*angX
                x = 5.0 * math.cos(radX) * math.sin(radY) + self.sphereX
                y = 5.0 * math.sin(radX) * math.sin(radY) +self.sphereY
                z = 5.0 * math.cos(radY)+self.sphereZ
                glVertex3f(x,y,z)
        glEnd()

        glutWireCube(20.0)
        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
