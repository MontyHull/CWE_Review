#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# The function that we will use to draw the environment
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)   # White

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(25.0, 50.0, 0.0)
    glVertex3f(35.0, 75.0, 0.0)
    glVertex3f(65.0, 75.0, 0.0)
    glVertex3f(75.0, 50.0, 0.0)
    glVertex3f(65.0, 25.0, 0.0)
    glVertex3f(35.0, 25.0, 0.0)
    glVertex3f(25.0, 50.0, 0.0)

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
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# Build the Bounding box - much more on this later!
glOrtho(0.0, 100.0, 0.0, 100.0, -2.0, 1.0)

# Go into a loop
glutMainLoop()
