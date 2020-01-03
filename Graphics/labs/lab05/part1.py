#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos
from math import sin

def draw_circle(x,y,z,radius):
    glColor3f(1.0, 1.0, 1.0)   # White
    glBegin(GL_TRIANGLE_FAN)
    for i in range(360):
        radian = i * (3.14159/180)
        x1 = x+cos(radian)*radius
        y1 = y+sin(radian)*radius
        glVertex3f(x1,y1,0.0)
    glEnd()
def draw_box(x1,y1,z1,x2,y2,z2):
    glBegin(GL_LINE_LOOP)
    glVertex3f(x1,y1,z1)
    glVertex3f(x1,y2,z1)
    glVertex3f(x2,y2,z2)
    glVertex3f(x2,y1,z2)
    glEnd()

def draw_text(x,y,z,message):
    # Position our cursor within the scene
    glRasterPos3f(x,y,z)
    for char in message:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def keyboardHandler(key, x, y):
  print(key)
# The function that we will use to draw the environment
def display():

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    draw_circle(50,50,0,40)
    draw_circle(550,50,0,40)
    draw_box(100,100,0,500,450,0)
    draw_text(220,470,0,"Etch-a-Sketch")
    glutKeyboardFunc(keyboardHandler)

    glFlush()
'''
class Scene:
    __init__(self):
'''

# Initialize the environment
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)

# Set the initial window position and size (if we want to)
glutInitWindowPosition(100,50)
glutInitWindowSize(600, 500)

# Create the window and name it
glutCreateWindow("Lab 4 - Etch-a-Sketch")

# Build the scene
glutDisplayFunc(display)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
# Build the Bounding box - much more on this later!
glOrtho(0.0, 600.0, 0.0, 500.0, -2.0, 1.0)

# Go into a loop
glutMainLoop()
