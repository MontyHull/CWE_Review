#!/usr/bin/python3

# Load in Required libraries
import math, numpy, time
import PIL.Image as Image
# Our required libraries!
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Our new Scene Class
class Scene:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.timeStep = 0
        self.timeStepSize = 0.02
        self.angle = 0.0

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
        #glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
        glutInitWindowPosition(100,50)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow("ex6.py")
        glutDisplayFunc(self.display)
        glutIdleFunc(self.idle)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-5.0, 5.0, -5.0, 5.0, 5.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        # New lines for images/textures
        glShadeModel( GL_SMOOTH )
        glEnable( GL_TEXTURE_2D )

        #Load Image 1
        im = Image.open(sys.argv[-1])
        self.xSize = im.size[0]
        self.ySize = im.size[1]
        self.rawReference = im.tobytes("raw", "RGB", 0, -1)

        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
        glTexImage2D( GL_TEXTURE_2D, 0, 3, self.xSize, self.ySize, 0,GL_RGB, GL_UNSIGNED_BYTE, self.rawReference )
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,0)
        glutMainLoop()

    # Run the idle loop
    def idle(self):
        if (time.time() - self.timeStep) > self.timeStepSize:
            self.timeStep = time.time()
            self.angle += .01
            glutPostRedisplay()

    # Build the scene
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()

        #2 - Aim the "camera", has the same effect, with the same output.
        #    Not yet animating
        #gluLookAt(eyex,eyey,eyez,centerx,centery,centerz,upx,upy,upz)
        gluLookAt(10*math.cos(self.angle) ,0.0,10* math.sin(self.angle), 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        #3 - Rotate the Camera, around the center point.
        #    Remember that the radius of the helix was 20, and we pushed it back 60
        #    originally, so we want to keep the camera 60 away from the center as we
        #    Rotate it around the scene...
        # Goal: Comment out Step 2, and make the camera circle the slinky

        #1
        glBegin(GL_TRIANGLES)
        #Magenta
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(0.0,1.0)
        glVertex3f(-2.5, 2.5,-2.5)
        #Red
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(0.0,0.0)
        glVertex3f(-2.5, -2.5,-2.5)
        #Yellow
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        glEnd()

        #1
        glBegin(GL_TRIANGLES)
        #Magenta
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(0.0,1.0)
        glVertex3f(-2.5, 2.5,-2.5)
        #White
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(1.0,1.0)
        glVertex3f(2.5, 2.5,-2.5)
        #Yellow
        glColor3f(1.0,1.0,1.0)
        glTexCoord2f(1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        glEnd()

        #2
        glBegin(GL_TRIANGLES)
        #White
        glColor3f(1.0,1.0,1.0)
        glVertex3f(2.5, 2.5,-2.5)
        #Blue
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,2.5)
        #Cyan
        glColor3f(0.0,1.0,1.0)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #2
        glBegin(GL_TRIANGLES)
        #Magenta
        glColor3f(1.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,-2.5)
        #White
        glColor3f(1.0,1.0,1.0)
        glVertex3f(2.5, 2.5,-2.5)
        #Blue
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,2.5)
        glEnd()

        #3
        glBegin(GL_TRIANGLES)
        #Yellow
        glColor3f(1.0,1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        #Red
        glColor3f(1.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,-2.5)
        #Black
        glColor3f(0.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        #3 done
        glBegin(GL_TRIANGLES)
        #Yellow
        glColor3f(1.0,1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        #Black
        glColor3f(0.0,0.0,0.0)
        #Black
        glColor3f(0.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,2.5)
        #Green
        glColor3f(0.0,1.0,0.0)
        glVertex3f(2.5, -2.5,2.5)
        glEnd()

        #4
        glBegin(GL_TRIANGLES)
        #Black
        glColor3f(0.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,2.5)
        #Blue
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,2.5)
        #Green
        glColor3f(0.0,1.0,0.0)
        glVertex3f(2.5, -2.5,2.5)
        glEnd()

        #4 done
        glBegin(GL_TRIANGLES)
        #Green
        glColor3f(0.0,1.0,0.0)
        glVertex3f(2.5, -2.5,2.5)
        #Cyan
        glColor3f(0.0,1.0,1.0)
        glVertex3f(2.5, 2.5,2.5)
        #Blue
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,2.5)
        glEnd()

        #5
        glBegin(GL_TRIANGLES)
        #Yellow
        glColor3f(1.0,1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        #White
        glColor3f(1.0,1.0,1.0)
        glVertex3f(2.5, 2.5,-2.5)
        #Cyan
        glColor3f(0.0,1.0,1.0)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #5 done
        glBegin(GL_TRIANGLES)
        #Yellow
        glColor3f(1.0,1.0,0.0)
        glVertex3f(2.5, -2.5,-2.5)
        #Green
        glColor3f(0.0,1.0,0.0)
        glVertex3f(2.5, -2.5,2.5)
        #Cyan
        glColor3f(0.0,1.0,1.0)
        glVertex3f(2.5, 2.5,2.5)
        glEnd()

        #6
        glBegin(GL_TRIANGLES)
        #Red
        glColor3f(1.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,-2.5)
        #Magenta
        glColor3f(1.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,-2.5)
        #Black
        glColor3f(0.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        #6
        glBegin(GL_TRIANGLES)
        #Magenta
        glColor3f(1.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,-2.5)
        #Blue
        glColor3f(0.0,0.0,1.0)
        glVertex3f(-2.5, 2.5,2.5)
        #Black
        glColor3f(0.0,0.0,0.0)
        glVertex3f(-2.5, -2.5,2.5)
        glEnd()

        glColor3f(1.0, 0.0, 0.0)
        glutWireCube(5.0)

        glPopMatrix()
        glutSwapBuffers()

if __name__ == '__main__':
    myProgram = Scene()
