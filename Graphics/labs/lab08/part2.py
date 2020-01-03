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
            self.angle += .01
            glutPostRedisplay()

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        #2 - Aim the "camera", has the same effect, with the same output.
        #    Not yet animating
        #gluLookAt(eyex,eyey,eyez,centerx,centery,centerz,upx,upy,upz)
        gluLookAt(10*math.cos(self.angle) ,0.0,10* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #3 - Rotate the Camera, around the center point.
        #    Remember that the radius of the helix was 20, and we pushed it back 60
        #    originally, so we want to keep the camera 60 away from the center as we
        #    Rotate it around the scene...
        # Goal: Comment out Step 2, and make the camera circle the slinky

        #1
        glColor3f(.15,.15 ,.15 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, 2.5,-2.5)
        glVertex3f(-2.5, -2.5,-2.5)
        glVertex3f(2.5, -2.5,-2.5)
        glEnd()

        #1
        glColor3f(.2,.2 ,.2 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, 2.5,-2.5)
        glVertex3f(2.5, 2.5,-2.5)
        glVertex3f(2.5, -2.5,-2.5)
        glEnd()

        #2
        glColor3f(.25,.25 ,.25 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, 2.5,-2.5)
        glVertex3f(-2.5, 2.5,2.5)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #2
        glColor3f(.3,.3 ,.3 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, 2.5,-2.5)
        glVertex3f(2.5, 2.5,-2.5)
        glVertex3f(-2.5, 2.5,2.5)
        glEnd()

        #3
        glColor3f(.35,.35 ,.35 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, -2.5,-2.5)
        glVertex3f(-2.5, -2.5,-2.5)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        #3 done
        glColor3f(.4,.4 ,.4 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, -2.5,-2.5)
        glVertex3f(-2.5, -2.5,2.5)
        glVertex3f(2.5, -2.5,2.5)
        glEnd()

        #4
        glColor3f(.45,.45 ,.45 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, -2.5,2.5)
        glVertex3f(-2.5, 2.5,2.5)
        glVertex3f(2.5, -2.5,2.5)
        glEnd()

        #4 done
        glColor3f(.5,.5 ,.5 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, -2.5,2.5)
        glVertex3f(2.5, 2.5,2.5)
        glVertex3f(-2.5, 2.5,2.5)
        glEnd()

        #5
        glColor3f(.55,.55 ,.55 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, -2.5,-2.5)
        glVertex3f(2.5, 2.5,-2.5)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #5 done
        glColor3f(.6,.6 ,.6 )
        glBegin(GL_TRIANGLES)
        glVertex3f(2.5, -2.5,-2.5)
        glVertex3f(2.5, -2.5,2.5)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #6
        glColor3f(.65,.65 ,.65 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, -2.5,-2.5)
        glVertex3f(-2.5, 2.5,-2.5)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        #6
        glColor3f(.7,.7 ,.7 )
        glBegin(GL_TRIANGLES)
        glVertex3f(-2.5, 2.5,-2.5)
        glVertex3f(-2.5, 2.5,2.5)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        glColor3f(1.0, 0.0, 0.0)
        glutWireCube(5.0)

        glPopMatrix()
        glutSwapBuffers()

if __name__ == '__main__':
    myProgram = Scene()
