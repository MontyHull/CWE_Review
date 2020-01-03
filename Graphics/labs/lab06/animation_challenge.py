#!/usr/bin/python3

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos
from math import sin
from math import pi
import sys
import objects as o
import time
from random import randint

def circle(deltaX,deltaY,scale,X,Y,Z,R,numberOfVertices,fill=False):
    X = (X + deltaX)*scale
    Y = (Y + deltaY)*scale
    if fill:
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(X, Y, 0.0)
    else:
        glBegin(GL_LINE_LOOP)
    theta=0
    for i in range(numberOfVertices):
        glVertex3f(X + R*scale * cos(theta), Y + R*scale * sin(theta), 0.0)
        theta = theta + 2 * pi / numberOfVertices
    glEnd()

def box(deltaX,deltaY,scale,LLX,LLY,URX,URY,Z,fill=False):
    LLX = (LLX+deltaX)*scale
    LLY = (LLY+deltaY)*scale
    URX = (URX+deltaX)*scale
    URY = (URY+deltaY)*scale

    glBegin(GL_LINE_LOOP)
    glVertex3f(LLX,LLY,Z)
    glVertex3f(LLX,URY,Z)
    glVertex3f(URX,URY,Z)
    glVertex3f(URX,LLY,Z)
    glEnd()

def text(deltaX,deltaY,scale,X,Y,Z,font,myText):
    # Position our cursor within the scene
    glRasterPos3f(X,Y,Z)
    for char in myText:
        glutBitmapCharacter(font, ord(char))

def line(deltaX,deltaY,scale,x1,y1,x2,y2,Z):
    x1 = (deltaX +x1)*scale
    x2 = (deltaX +x2)*scale
    y1 = (deltaY +y1)*scale
    y2 = (deltaY +y2)*scale

    glBegin(GL_LINES)
    glVertex3f(x1,y1,Z)
    glVertex3f(x2,y2,Z)
    glEnd()

def color(deltaX,deltaY,scale,r,g,b):
    glColor3f(r,g,b)

class Scene:
    def __init__(self,save_or_load="neither",filename="none"):

        # Initialize the environment
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
        # Starting delats for my stickFigure
        self.deltaX = 100
        self.deltaY = 100
        # The direcdtions that he could be facing
        self.which_way = ['front','left','right']
        self.facing = 0
        self.which_animation= [0,0,0]
        self.step_size = 4
        self.scale = 1.0
        self.idle_time = time.time()
        #Ball variables
        self.idle_timeBall = time.time()
        self.radius = 15
        self.BallX = 300
        self.BallY = 300
        self.direction = 180
        #Score
        self.score = 0
        #Color
        self.ball_color_values = {'red':[1.0,0,0],'green':[0,1.0,0],'blue':[0,0,1.0]}
        self.ball_color = 'red'
        self.telport = [[20,30],[20,350],[475,350],[475,30]]
        self.next_tele = randint(0,3);
        # Set the initial window position and size (if we want to)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(600, 500)
        self.width = 600
        self.height = 500
        # Create the window and name it
        glutCreateWindow("Lab 5 - Animation")

        # Build the scene
        glutDisplayFunc(self.display)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # Build the Bounding box - much more on this later!
        glOrtho(0.0, 600.0, 0.0, 500.0, -2.0, 1.0)
        # Go into a loop
        glutMainLoop()

    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit(0)
        glutPostRedisplay()
        if key == 'r':
            self.ball_color = 'red'
        if key == 'g':
            self.ball_color = 'green'
        if key == 'b':
            self.ball_color = 'blue'
        if key == 't':
            self.deltaX = self.telport[self.next_tele%4][0]
            self.deltaY = self.telport[self.next_tele%4][1]
            self.next_tele = self.next_tele + 1

    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"
        glutPostRedisplay()
        if key == 101:
            self.facing = 0
            self.which_animation[0] = self.which_animation[0] + 1
            self.deltaY = self.deltaY + self.step_size
        if key == 103:
            self.facing = 0
            self.which_animation[0] = self.which_animation[0] + 1
            self.deltaY = self.deltaY - self.step_size

        if key == 100:
            self.facing = 1
            self.which_animation[1] = self.which_animation[1] + 1
            self.deltaX = self.deltaX - self.step_size

        if key == 102:
            self.facing = 2
            self.which_animation[2] = self.which_animation[2] + 1
            self.deltaX = self.deltaX + self.step_size
        if key == 104:
            if self.scale <= 1.5:
                self.scale = self.scale + 0.1
        if key == 105:
            if self.scale >= 0.5:
                self.scale = self.scale - 0.1

    def mouse(self,buttonNumber,state,x,y):
        print"['mouse', "+str(buttonNumber)+", "+str(state)+", "+str(x)+", "+str(y)+"]"
        glutPostRedisplay()

    def motion(self,x,y):
        print"['motion', "+str(x)+", "+str(y)+"]"
        glutPostRedisplay()

    def idle(self):
        if time.time() > self.idle_time+.2:
            print("['time',"+str(time.time())+"]")
            self.idle_time = time.time()
            self.which_animation[0] = self.which_animation[0] + 1
            glutPostRedisplay()
        if time.time() > self.idle_timeBall+.005:
            self.idle_timeBall = time.time()
            turn = randint(0,50)
            if turn == 1:
                new_dir = randint(0,1)
                if new_dir == 1:
                    self.direction = self.direction + 20
                else:
                    self.direction = self.direction - 20
            self.BallX=self.BallX+cos(self.direction)
            self.BallY=self.BallY+sin(self.direction)
            #checking for hitting a wall
            if self.BallX > 575-self.radius or self.BallX < 25+self.radius or self.BallY > 450-self.radius or self.BallY < 25+self.radius:
                self.direction = self.direction+180
            rad_square1 = (15 - self.radius)
            rad_square2 = (15 + self.radius)**2
            middle = (((50+self.deltaX)-(self.BallX))**2) + (((80+self.deltaY)-(self.BallY))**2)
            #checking to see if you hit stickman
            if rad_square1 <= middle and middle <= rad_square2:
                self.score = self.score + 1
                self.direction = self.direction + 180
            glutPostRedisplay()


    # The function that we will use to draw the environment
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        box(0,0,1,25,25,575,450,0)
        text(0,0,1,190,470,0,GLUT_BITMAP_TIMES_ROMAN_24,"Our Game Experience - Score: "+str(self.score))
        for component in o.stickFigure[self.which_way[self.facing]][self.which_animation[self.facing]%3]:
            #print("Drawing: "+component[-1])
            component[0](self.deltaX,self.deltaY,self.scale,*component[1])
        color(0,0,0,self.ball_color_values[self.ball_color][0],self.ball_color_values[self.ball_color][1],self.ball_color_values[self.ball_color][2])
        circle(0,0,self.scale,self.BallX,self.BallY,0,self.radius,360,True)
        color(0,0,0,1,1,1)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboardSpecial)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutIdleFunc(self.idle)
        glFlush()

if __name__ == '__main__':
    scene = Scene()
    #print("hello")
