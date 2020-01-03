#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# The function that we will use to draw the environment
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)   # White
    y = 90.0
    for i in range(9,0,-1):
        glRasterPos3f(20.0, y, 0.0)
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('P'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('o'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('i'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('n'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('t'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(' '))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('S'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('i'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('z'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord('e'))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(' '))
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(str(i)))

        glPointSize(i)
        glBegin(GL_POINTS)
        glVertex(10.0, y, 0.0)
        glEnd()
        glFlush()
        y = y-10.0


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
