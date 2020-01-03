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
            self.angle += .08
            glutPostRedisplay()

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        #1 - The original Way, rotate along the center,
        #    and then translate into the frustum
        #glTranslatef(0.0, 0.0, -60.0)
        #glRotatef(self.angle, 0.0, 1.0, 0.0)

        #2 - Aim the "camera", has the same effect, with the same output.
        #    Not yet animating
        #gluLookAt(eyex,eyey,eyez,centerx,centery,centerz,upx,upy,upz)
        r = 20.0                # Radius of helix
        gluLookAt(60*math.cos(self.angle) ,0.0,60* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #3 - Rotate the Camera, around the center point.
        #    Remember that the radius of the helix was 20, and we pushed it back 60
        #    originally, so we want to keep the camera 60 away from the center as we
        #    Rotate it around the scene...
        # Goal: Comment out Step 2, and make the camera circle the slinky

        t = -10.0 * math.pi     # Angle along helix

        glBegin(GL_LINE_STRIP)
        while(t <= 10.0 * math.pi):
            glVertex3f(r * math.cos(t), t, r * math.sin(t))
            t += math.pi / 20.0
        glEnd()

        glPopMatrix()
        glutSwapBuffers()
        #glFlush()

if __name__ == '__main__':
    myProgram = Scene()
