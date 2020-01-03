import os
import pyglet
class Player:
    def __init__(self,startx,starty):
        self.x = startx
        self.y=starty
        heroRun = "sprites/hero/Run"
        self.run_Right = []
        self.run_Left = []
        self.attack = []
        self.throw = []
        self.jump = []
        self.idle = []
        for i in range(10):
            self.run_Right.append(pyglet.resource.image('sprites/hero/Run ('+str(i+1)+').png', flip_x=False))
            self.run_Left.append(pyglet.resource.image('sprites/hero/Run ('+str(i+1)+').png', flip_x=True))
            self.idle.append(pyglet.resource.image('sprites/hero/Idle ('+str(i+1)+').png', flip_x=False))
            self.attack.append(pyglet.resource.image('sprites/hero/Attack ('+str(i+1)+').png', flip_x=False))
            self.throw.append(pyglet.resource.image('sprites/hero/Throw ('+str(i+1)+').png', flip_x=False))
            self.jump.append(pyglet.resource.image('sprites/hero/Jump ('+str(i+1)+').png', flip_x=False))
            self.idle[i].anchor_x = self.idle[i].width/2
            self.idle[i].anchor_y = 0
            self.run_Left[i].anchor_x = self.run_Left[i].width/2
            self.run_Left[i].anchor_y = 0
            print(self.idle[i].width)
        animationSpeed = 0.05
        animationScale = 0.15
        animationLoop = True
        animationX = 400
        animationY = 300
        self.Run_Right_Sprite = pyglet.image.Animation.from_image_sequence(self.run_Right,animationSpeed,animationLoop)
        self.Run_Left_Sprite = pyglet.image.Animation.from_image_sequence(self.run_Left,animationSpeed,animationLoop)
        self.Attack_Sprite = pyglet.image.Animation.from_image_sequence(self.attack,animationSpeed,animationLoop)
        self.Idle_Sprite = pyglet.image.Animation.from_image_sequence(self.idle,animationSpeed,animationLoop)
        self.Throw_Sprite = pyglet.image.Animation.from_image_sequence(self.throw,animationSpeed,animationLoop)
        self.Jump_Sprite = pyglet.image.Animation.from_image_sequence(self.jump,animationSpeed,animationLoop)
