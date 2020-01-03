#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos
from math import sin


# The function that we will use to draw the environment
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glBegin(GL_TRIANGLE_FAN)

    radius = 25
    y1 = 50
    vertices = 50
    for i in range(vertices):
        radian = i * (3.14159/180)*(360/vertices)
        x = 50+cos(radian)*radius
        y = 50+sin(radian)*radius

        glVertex3f(x,y,0.0)
        glColor3f(1.0, 1.0, 1.0)   # White

    glEnd()

    glFlush()

# Initialize the environment
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

# Set the initial window position and size (if we want to)
glutInitWindowPosition(100,50)
glutInitWindowSize(400, 400)

# Create the window and name it
glutCreateWindow("Hall, Micky S. 172412")

# Build the scene
glutDisplayFunc(display)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

# Build the Bounding box - much more on this later!
glOrtho(0.0, 100.0, 0.0, 100.0, -2.0, 1.0)

# Go into a loop
glutMainLoop()
