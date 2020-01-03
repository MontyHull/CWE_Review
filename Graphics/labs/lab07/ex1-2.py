#!/usr/bin/python3

# Load in Required libraries
import math, numpy

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Our new Scene Class
class Scene:
    # Construct the Scene Class
    def __init__(self):
        self.width = 400
        self.height = 400
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("example2.py")
        glutDisplayFunc(self.display)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glutMainLoop()
    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -15.0)
        glRotatef(45.0, 0.0, 0.0, 1.0)
        glTranslatef(10.0, 0.0, 0.0)
        glutWireCube(5.0)
        glDisable(GL_DEPTH_TEST)
        glFlush()

myProgram = Scene()
