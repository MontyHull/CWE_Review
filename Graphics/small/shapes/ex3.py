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
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(50.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(50.0, 100.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(50.0, 100.0, 0.0)
    glVertex3f(100.0, 100.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(50.0, 0.0, 0.0)
    glVertex3f(100.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(-50.0, 50.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(-50.0, 50.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(150.0, 50.0, 0.0)
    glVertex3f(100.0, 0.0, 0.0)
    glEnd()

    glBegin(GL_POLYGON)
    glVertex3f(50.0, 50.0, 0.0)
    glVertex3f(150.0, 50.0, 0.0)
    glVertex3f(100.0, 100.0, 0.0)
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
glOrtho(-100.0, 200.0, -50.0, 150.0, -2.0, 1.0)

# Go into a loop
glutMainLoop()
