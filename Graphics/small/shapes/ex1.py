#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# The function that we will use to draw the environment
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)   # White

    glBegin(GL_POLYGON)
    glVertex3f(10.0, 10.0, 0.0)
    glVertex3f(60.0, 10.0, 0.0)
    glVertex3f(60.0, 60.0, 0.0)
    glEnd()

    glColor3f(0.79, 0.19, 0.99)   # Purple
    glBegin(GL_POLYGON)
    glVertex3f(45.0, 10.0, 0.0)
    glVertex3f(85.0, 10.0, 0.0)
    glVertex3f(85.0, 85.0, 0.0)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)   # Red
    glVertex3f(8.0, 8.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)    # Green
    glVertex3f(62.0, 8.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)    # Blue
    glVertex3f(62.0, 62.0, 0.0)
    glColor3f(1.0, 1.0, 0.0)    # Yellow
    glVertex3f(8.0, 62.0, 0.0)
    glEnd()

    glFlush()

# Initialize the environment
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

# Set the initial window position and size (if we want to)
glutInitWindowPosition(100,50)
glutInitWindowSize(400, 400)

# Create the window and name it
glutCreateWindow("ex1.py")

# Build the scene
glutDisplayFunc(display)

# Build the Bounding box - much more on this later!
glOrtho(0.0, 100.0, 0.0, 100.0, -2.0, 1.0)

# Go into a loop
glutMainLoop()
