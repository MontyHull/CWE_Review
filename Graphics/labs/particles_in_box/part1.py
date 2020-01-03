#!/usr/bin/python3

# Load in Required libraries
import math, numpy, time, random

# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Our new Particle class
class Particle:
    def __init__(self,init_pos,init_v, acceleration,timelag):
        self.init_pos = init_pos
        self.v = init_v
        self.accel = acceleration
        self.lag = timelag
    def p_t(self,newtime):
        newtime = newtime - self.lag
        p2 = self.v * newtime
        p3 = (self.accel) * (newtime ** 2)
        p3 = p3/2
        return_value = self.init_pos + p2 + p3
        return return_value

    def draw(self,newtime):
        if (newtime - self.lag) >=0:
            pos = self.p_t(newtime)
            glBegin(GL_POINTS)
            glVertex3f(pos[0],pos[1],pos[2])
            glEnd()

# Our new Scene Class
class Scene:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.camera = 60

        self.P1 = numpy.array([0,0,0])
        self.P2 = numpy.array([0,0,0])
        self.theta = 0.0
        self.u = numpy.array([0,0,0])
        self.wr = []

        self.track = time.time()
        self.trackstep = .02
        self.timestep = .01
        self.newtime = 0.0

        self.particles = []
        acceleration = numpy.array([0.0,-9.8,0.0],dtype='float64')
        init_pos = numpy.array([0.0,0.0,0.0],dtype='float64')

        for i in range(0,10000):
            theta = random.random()*20.0
            phi = random.random()*360.0
            alpha = theta/20
            Vx = math.sin(math.radians(theta)) * math.sin(math.radians(phi))
            Vy = math.cos(math.radians(theta))
            Vz = math.sin(math.radians(theta)) * math.cos(math.radians(phi))
            V = numpy.array([Vx,Vy,Vz],dtype='float64')
            init_v = 90*(1-(alpha**2))
            inv = init_v*V
            newParticle = Particle(init_pos,inv,acceleration,.05*i)
            self.particles.append(newParticle)

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        #glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("ex6.py")
        glutDisplayFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        glutIdleFunc(self.idle)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.keyboardSpecial)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutMainLoop()

    def idle(self):
        if(time.time()-self.track > self.trackstep):
            self.track = time.time()
            self.newtime += self.timestep
            glutPostRedisplay()

    def zxy(self,x,y,w,h):
        if ((x - (w/2.0))**2 + (y - (h/2.0))**2) < ((h/2.0)**2):
            return numpy.sqrt((h/2.0)**2 - (x - (w/2.0))**2 - (y - (h/2.0))**2)
        return 0.01

    def vector_angle(self, p1, p2):
        # Calculate the angle between the two vectors
        theta = numpy.arccos((p1.dot(p2))/(numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
        # Calculate the axis of rotation (u)
        u = (numpy.cross(p1, p2) / (numpy.linalg.norm(p2) * numpy.linalg.norm(p1)))
        return theta, u

    def mouse(self, button, state, x, y):
        z = self.zxy(x,y,self.width, self.height)
        x = -1.0 * (self.width/2.0 - x)
        y = self.height/2.0 - y
        if button == 0 and state == 0:
            self.wr.append([0.0, numpy.array([0,0,0])])
            self.P1 = numpy.array([x,y,z])

    def motion(self, x, y):
        z = self.zxy(x,y,self.width, self.height)
        x = -1.0 * (self.width/2.0 - x)
        y = self.height/2.0 - y
        self.P2 = numpy.array([x,y,z])
        theta, u = self.vector_angle(self.P1, self.P2)
        self.wr[-1] = [theta, u]
        glutPostRedisplay()

    def keyboard(self,key,x,y):
        print"['keyboard', "+str(key)+", "+str(x)+", "+str(y)+"]"
        if key == 'q':
            sys.exit()

    def keyboardSpecial(self,key,x,y):
        print"['special', "+str(key)+", "+str(x)+", "+str(y)+"]"

    def difference(self,a,b):
        if(a > b):
            return((self.t-b)/(a-b))
        return((self.t-a)/(b-a))

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        glTranslatef(0.0,0.0,-self.camera)
        for i in range(len(self.wr)-1,-1,-1):
            r = self.wr[i]
            glRotatef(numpy.degrees(r[0]), r[1][0], r[1][1], r[1][2])


        glutWireCube(20.0)
        for part in self.particles:
            part.draw(self.newtime)




        glPopMatrix()
        glutSwapBuffers()


if __name__ == '__main__':
    myProgram = Scene()
