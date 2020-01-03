import os,re,math,sys
import pyglet
class Player:

    #kills a player and stops them from making in further actions
    def die(self):
        pyglet.clock.unschedule(self.movement)
        self.doing = "Dead"
        self.actions["alt"] = False
        self.actions["ctrl"] = False
        self.update()
        if(self.alive):
            self.death_sound.play()
        self.alive = False
        if self.whatami =="hero":
            pyglet.clock.unschedule(self.gravity)
            pyglet.clock.unschedule(self.win)
            pyglet.clock.unschedule(self.jump)

    #makes a player go back to their previous action after attacking
    def back_to_idle(self,dt):
        if(self.actions["right"] or self.actions["left"]):
            self.doing = "Run"
        else:
            self.doing = "Idle"
            self.actions["idle"] = True
        self.actions["alt"] = False
        self.actions["ctrl"] = False

    #Checks for a winning condition
    def win(self,dt):
        row = round(self.y/50)
        col = round(self.x/50)
        if(int(row) in self.objective):
            if(int(col) in self.objective[int(row)]):
                print("Winner!")
                sys.exit()

    #Makes a player fall
    def gravity(self,dt):
        row = round(self.y/50)
        col = round(self.x/50)
        if(not self.actions["space"]):
            if(int(row-1) in self.ground):
                if(int(col) in self.ground[int(row-1)]):
                    self.y = int(row)*50
                    self.falling_speed = 1.0
                else:
                    self.y -= self.falling_speed
                    if(self.falling_speed < 45):
                        self.falling_speed *= 1.1
            else:
                self.y -= self.falling_speed
                if(self.falling_speed < 45):
                    self.falling_speed *= 1.1
            self.update()
        if(row == 0):
            self.die()

    #Allows a player to jump
    def jump(self,dt):
        # if you press the space bar sets jumps to 30
        if(self.actions["space"] and self.jumps == 0):
            self.jumps = 30
        # if jumps is between 30 and 16
        if(self.jumps >15):
            delta = math.sin(math.radians((31-self.jumps)*(90.0/15.0)))*160 -math.sin(math.radians((31-self.jumps-1)*(90.0/15.0)))*160
            self.y += delta
            self.jumps -=1
        elif(self.jumps <= 15 and self.jumps >0):
            self.y -= self.falling_speed
            self.jumps -= 1
            if(self.falling_speed<=45):
                self.falling_speed *= 1.1
        if(self.jumps == 0):
            self.actions["space"] = False
            if(self.doing == "Attack" or self.doing == "Throw"):
                self.useless_var = 1
            elif(self.actions["right"] or self.actions["left"]):
                self.doing = "Run"
            else:
                self.doing = "Idle"

        self.update()

    #Allows a player to move left and right, and blocks them from walls
    def movement(self,dt):
        left_wall = True
        right_wall = True

        row = round(self.y/50)
        col = round(self.x/50)
        left_col = round((self.x-3)/50)
        right_col = round((self.x+3)/50)

        if(int(row) in self.ground):
            # Have I hit a wall to the left
            if(int(left_col-1) in self.ground[int(row)]):
                left_wall = False
                if(self.whatami == "enemy-1" or self.whatami == "enemy-2" and self.alive):
                    self.going_right = True
                    self.actions["right"] = True
                    self.actions["left"] = False
            else:
                left_wall = True

            # Have I hit a wall to the right
            if(int(right_col) in self.ground[int(row)]):
                right_wall = False
                if((self.whatami == "enemy-1" or self.whatami == "enemy-2") and self.alive):
                    self.going_right = False
                    self.actions["right"] = False
                    self.actions["left"] = True
            else:
                right_wall = True

        # Has a zombie hit an edge so they should turn around
        if(int(row-1) in self.ground and (self.whatami == "enemy-1" or self.whatami == "enemy-2") and self.alive):
            if(int(left_col-1) not in self.ground[int(row-1)]):
                self.going_right = True
                self.actions["right"] = True
                self.actions["left"] = False
            if(int(col+1) not in self.ground[int(row-1)]):
                self.going_right = False
                self.actions["right"] = False
                self.actions["left"] = True

        #Move Left
        if(self.actions["left"]):
            self.steps = 10
            if(self.actions["shift"] and left_wall):
                self.x -= self.run_speed*3
            elif left_wall:
                self.x -= self.run_speed
        elif self.steps > 0 and not self.going_right and left_wall:
            self.x -= self.run_speed
            self.steps -= 1
        elif self.steps > 0 and not self.going_right and not left_wall:
            self.steps -= 1

        elif self.steps < 1 and not self.going_right and not self.actions["idle"]:
            self.doing = "Idle"
            self.actions["idle"] = True

        #Move Right
        if(self.actions["right"]):
            self.steps = 10
            if(self.actions["shift"] and right_wall):
                self.x+= self.run_speed*3
            elif right_wall:
                self.x += self.run_speed
        elif self.steps > 0 and self.going_right and right_wall:
            self.x+= self.run_speed
            self.steps -= 1
        elif self.steps > 0 and self.going_right and not right_wall:
            self.steps -= 1
        elif self.steps <1 and self.going_right and not self.actions["idle"]:
            self.doing = "Idle"
            self.actions["idle"] = True

        self.update()

    #Updates the x and y coordinates of a player
    def update(self):
        self.Player_Right_Animations[self.doing].x = self.x
        self.Player_Left_Animations[self.doing].x = self.x
        self.Player_Right_Animations[self.doing].y = self.y
        self.Player_Left_Animations[self.doing].y = self.y

    #Movement function for kunai
    def throw(self,dt):
        if self.steps == 0:
            self.actions["ctrl"] = False
        left_wall = True
        right_wall = True

        row = round(self.y/50)
        col = round(self.x/50)
        left_col = round((self.x-3)/50)
        right_col = round((self.x+3)/50)
        if(int(row) in self.ground):
            # Have I hit a wall to the left
            if(int(left_col-1) in self.ground[int(row)]):
                left_wall = False
                self.actions["ctrl"] = False
            else:
                left_wall = True
            # Have I hit a wall to the right
            if(int(col-1) in self.ground[int(row)]):
                right_wall = False
                self.actions["ctrl"] = False

            else:
                right_wall = True

        if self.going_right and right_wall:
            self.x += 3
        elif not self.going_right and left_wall:
            self.x -= 3
        self.update()
        self.steps -= 1

    #Sets up player variables, Very ugly
    def __init__(self,startx,starty,ground,whatami,objective = 0):
        self.useless_var = 0
        self.alive = True
        self.run_speed = 3
        self.jumps = 0
        self.ground = ground
        self.objective = objective
        self.falling_speed = 1.0
        self.going_right= True
        self.actions = {"left":False,"right":False,"shift":False,"space":False,"ctrl":False,"alt":False,"idle":False}
        self.steps = 0
        self.x = startx
        self.y = starty
        animationSpeed = 0.05
        actions = []
        self.whatami = whatami

        # Hero Sounds


        #How the player will start
        if(whatami == "hero"):
            self.attack_sound = pyglet.media.StaticSource(pyglet.media.load('music/attack.wav'))
            self.throw_sound = pyglet.media.StaticSource(pyglet.media.load('music/throw.wav'))
            self.jump_sound = pyglet.media.StaticSource(pyglet.media.load('music/jump.wav'))
            self.death_sound = pyglet.media.StaticSource(pyglet.media.load('music/hero_death.wav'))
            self.doing = "Idle"
            self.actions["idle"] = True
            pyglet.clock.schedule_interval(self.win,.01)
            pyglet.clock.schedule_interval(self.gravity,.02)
            pyglet.clock.schedule_interval(self.movement,.01)
            pyglet.clock.schedule_interval(self.jump,.02)

        elif(whatami == "enemy-1"):
            self.death_sound = pyglet.media.StaticSource(pyglet.media.load('music/enemy_death.wav'))
            self.doing = "Run"
            self.run_speed = 4
            self.actions["right"] = True
            self.actions["alt"] = True
            self.actions["ctrl"] = True
            pyglet.clock.schedule_interval(self.movement,.01)


        elif(whatami == "enemy-2"):
            self.death_sound = pyglet.media.StaticSource(pyglet.media.load('music/enemy_death.wav'))
            self.doing = "Run"
            self.run_speed = 2
            self.actions["right"] = True
            self.actions["alt"] = True
            self.actions["ctrl"] = True
            pyglet.clock.schedule_interval(self.movement,.01)

        elif(whatami == "weapon"):
            self.doing = "Kunai"
            self.actions["alt"] = True
            self.actions["ctrl"] = True
            pyglet.clock.schedule_interval(self.throw,.01)


        #the sprites for the hero
        direct = os.listdir("sprites/"+whatami)
        for item in direct:
            newit = os.path.splitext("sprites/"+whatami+"/"+item)
            newit = (re.sub('[()0-9]','',newit[0]))
            if newit.strip().split("/")[2] not in actions:
                actions.append(newit.strip().split("/")[2])
        self.Player_Right_images = {}
        self.Player_Left_images = {}
        self.Player_Right_Animations = {}
        self.Player_Left_Animations = {}

        for i in actions:
            self.Player_Right_images[i] = []
            self.Player_Left_images[i] = []
            for j in range(10):
                if(whatami == "hero" or whatami == "weapon"):
                    self.Player_Right_images[i].append(pyglet.resource.image('sprites/'+whatami+'/'+i+' ('+str(j+1)+').png',flip_x=False))
                    self.Player_Left_images[i].append(pyglet.resource.image('sprites/'+whatami+'/'+i+' ('+str(j+1)+').png',flip_x=True))
                    self.Player_Right_images[i][j].anchor_x = self.Player_Right_images[i][j].width/2
                    self.Player_Right_images[i][j].anchor_y = 0
                    self.Player_Left_images[i][j].anchor_x = self.Player_Left_images[i][j].width/2
                    self.Player_Left_images[i][j].anchor_y = 0
                if(whatami == "enemy-1" or whatami == "enemy-2"):
                    if(j <=7 ):
                        self.Player_Right_images[i].append(pyglet.resource.image('sprites/'+whatami+'/'+i+' ('+str(j+1)+').png',flip_x=False))
                        self.Player_Left_images[i].append(pyglet.resource.image('sprites/'+whatami+'/'+i+' ('+str(j+1)+').png',flip_x=True))
                        self.Player_Right_images[i][j].anchor_x = self.Player_Right_images[i][j].width/2
                        self.Player_Right_images[i][j].anchor_y = 0
                        self.Player_Left_images[i][j].anchor_x = self.Player_Left_images[i][j].width/2
                        self.Player_Left_images[i][j].anchor_y = 0

        for item in actions:
            if whatami == "weapon" or item == "Dead":
                self.Player_Right_Animations[item] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(self.Player_Right_images[item],animationSpeed,False),self.x,self.y)
                self.Player_Right_Animations[item].scale = .15
                self.Player_Left_Animations[item] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(self.Player_Left_images[item],animationSpeed,False),self.x,self.y)
                self.Player_Left_Animations[item].scale = .15
            else:
                self.Player_Right_Animations[item] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(self.Player_Right_images[item],animationSpeed,True),self.x,self.y)
                self.Player_Right_Animations[item].scale = .15
                self.Player_Left_Animations[item] = pyglet.sprite.Sprite(pyglet.image.Animation.from_image_sequence(self.Player_Left_images[item],animationSpeed,True),self.x,self.y)
                self.Player_Left_Animations[item].scale = .15
