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
        glutIdleFunc(self.idle)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        glutMainLoop()

    # Run the idle loop
    def idle(self):
        if (time.time() - self.timeStep) > self.timeStepSize:
            self.timeStep = time.time()
            self.angle += 5
            glutPostRedisplay()

    # Build the scene
    def display(self):

        r = 20.0                # Radius of helix
        t = -10.0 * math.pi     # Angle along helix
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()
        glPushMatrix()

        # The Trick: to align the axis of the helix along the y-axis prior to rotation
        # and then return it to its original location.
        glTranslatef(0.0, 0.0, -15.0)
        #glRotatef(self.angle, 0.0, 1.0, 0.0)
        #glTranslatef(0.0, 0.0, 60.0)
        glPushMatrix()
        glRotatef(-self.angle/7, 0.0, 1.0, 0.0)
        glutWireSphere(4.0, 10, 8)
        glPopMatrix()

        glRotatef(self.angle, 0.0, 1.0, 0.0)
        glTranslatef(5.0, 0.0, -6.0)
        glutWireSphere(2.0, 10, 8)

        glPopMatrix()

        glutSwapBuffers()
        #glFlush()

if __name__ == '__main__':
    myProgram = Scene()
