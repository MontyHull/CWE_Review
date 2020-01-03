#!/usr/bin/python3

import math

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# The function that we will use to draw the environment
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)   # White

    glBegin(GL_LINES)
    glVertex3f(-40,0,-40)
    glVertex3f(40,0,-40)
    glVertex3f(0,-40,-40)
    glVertex3f(0,40,-40)
    glEnd()

    glColor3f(0.6, 0.6, 0.6)   # Gray
    glBegin(GL_TRIANGLE_STRIP)
    glVertex3f(-30,25,-40)
    glVertex3f(-2,25,-35)
    glVertex3f(-2,28,-30)
    glEnd()

    glColor3f(0.79, 0.19, 0.99)   # Purple
    glBegin(GL_LINE_STRIP)
    x = -30.0
    step = 0.005
    while x < 30.0:
        x = x + step
        y = 30.0 * math.sin(x/3.0) + 8.0
        glVertex3f(x,y,-37.0)
        glVertex3f(x,y,-33.0)
        print(str([x,y]))
    glEnd()

    glDisable(GL_DEPTH_TEST)
    glFlush()

# Initialize the environment
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

# Set the initial window position and size (if we want to)
glutInitWindowPosition(100,50)
glutInitWindowSize(400, 400)

# Create the window and name it
glutCreateWindow("ex3.py")

# Build the scene
glutDisplayFunc(display)

# Build the Viewing Plane!
#glOrtho(-50.0, 50.0, -50.0, 50.0, -50.0, 50.0)
#glFrustum(-50.0,50.0,-50.0,50.0,5.0,100.0)
#glFrustum(-50.0,50.0,-50.0,50.0,15.0,100.0)
glFrustum(-50.0,50.0,-50.0,50.0,30.0,50000.0)

# Go into a loop
glutMainLoop()
