# Prevent the creation of pyc files
import sys
sys.dont_write_bytecode = True

# Allow for importing a library by provideing the library name as a string
import imp,pyglet,player2
from pyglet.window import mouse, key
from pyglet.gl import glEnable, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_BLEND
from pyglet.gl import glLoadIdentity, glTranslatef
# load the level (Provide as an argument on the command line)
# example: python load-level.py level1
levelname = sys.argv[-1]
level = imp.load_source('happy',levelname+'.py')

# Provide some debugging, just to see:
print(str(['rows=',level.rows,'cols=',level.cols]))

class Scene:

    #Checks if a player has come in contact with another player
    def contact(self):
        row = round(self.hero.y/50)
        w_row = round((self.weapon.y-30)/50)
        for enemy in self.enemies:
            if self.weapon.x >= enemy.x-5 and self.weapon.x <= enemy.x+5 and w_row == round(enemy.y/50):
                enemy.die()
            if self.hero.x >= enemy.x-5 and self.hero.x <= enemy.x+5 and row == round(enemy.y/50):
                if self.hero.actions["alt"]:
                    enemy.die()
                elif enemy.alive:
                    self.hero.die()

    #Restarts the background music
    def background_music(self,dt):
        self.music.seek(0)

    #Makes the kunai follow the hero around
    def follow_hero(self):
        self.weapon.x = self.hero.x
        self.weapon.y = self.hero.y+30
        self.weapon.going_right = self.hero.going_right
        self.weapon.update()


    def __init__(self,width=800,height=600,caption="Would you like to play a game?"):
        self.window = pyglet.window.Window(width=width, height=height,caption=caption)

        # Fix transparent issue...  *needed depending on how you load transparent images*
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Create the Background
        self.background = pyglet.image.load(level.background)

        # Create and play the music
        self.music = pyglet.media.load(level.music)
        pyglet.clock.schedule_interval(self.background_music,self.music.duration)
        self.music.play()


        #hero/weapon init
        self.hero = player2.Player(level.playerStartCol*50,level.playerStartRow*50,level.level,"hero",level.goals)
        self.weapon = player2.Player(level.playerStartCol*50,level.playerStartRow*50,level.level,"weapon",level.enemies)

        #enemy init
        self.enemies = []
        for i in level.enemies:
            if i[2] == "e2":
                self.enemies.append(player2.Player(i[0]*50,i[1]*50,level.level,"enemy-2"))
            elif i[2] == "e1":
                self.enemies.append(player2.Player(i[0]*50,i[1]*50,level.level,"enemy-1"))

        # Event for pressing a key
        @self.window.event
        def on_key_press(symbol, modifiers):
            if self.hero.alive:
                if symbol == key.RIGHT:
                    self.hero.actions["right"] = True
                    self.hero.actions["left"] = False
                    self.hero.going_right = True
                    self.hero.actions["idle"] = False
                    self.hero.doing = "Run"

                if symbol == key.LEFT:
                    self.hero.actions["right"] = False
                    self.hero.actions["left"] = True
                    self.hero.going_right = False
                    self.hero.actions["idle"] = False
                    self.hero.doing = "Run"

                if symbol == key.SPACE:
                    self.hero.actions["space"] = True
                    self.hero.jump_sound.play()
                    self.hero.doing = "Jump"

                if symbol == key.LCTRL or symbol == key.RCTRL:
                    self.hero.doing = "Throw"
                    self.follow_hero()
                    self.hero.throw_sound.play()
                    self.weapon.actions["ctrl"] = True
                    self.weapon.steps = 200

                if symbol == key.RSHIFT or symbol == key.LSHIFT:
                    self.hero.actions["shift"] = True

                if symbol == key.RALT or symbol == key.LALT:
                    self.hero.actions["alt"] = True
                    self.hero.doing = "Attack"
                    self.hero.attack_sound.play()

        #Returning actions to false when key is released
        @self.window.event
        def on_key_release(symbol,modifiers):
            if symbol == key.RIGHT:
                self.hero.actions["right"] = False

            if symbol == key.LEFT:
                self.hero.actions["left"] = False

            if symbol == key.RSHIFT or symbol == key.LSHIFT:
                self.hero.actions["shift"] = False

        # Great for debugging
        #self.window.push_handlers(pyglet.window.event.WindowEventLogger())


        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()
            self.background.blit(0,0,height=height)
            level.drawBoard(level.level)
            level.drawBoard(level.goals)
            if self.hero.doing == "Attack" or self.hero.doing == "Throw":
                pyglet.clock.schedule_once(self.hero.back_to_idle,.5)
            if self.hero.going_right:
                self.hero.Player_Right_Animations[self.hero.doing].draw()
            else:
                self.hero.Player_Left_Animations[self.hero.doing].draw()
            for es in self.enemies:
                if es.going_right:
                    es.Player_Right_Animations[es.doing].draw()
                else:
                    es.Player_Left_Animations[es.doing].draw()
            if self.weapon.actions["ctrl"]:
                if self.weapon.going_right:
                    self.weapon.Player_Right_Animations[self.weapon.doing].draw()
                else:
                    self.weapon.Player_Left_Animations[self.weapon.doing].draw()
            self.contact()

            #print(self.hero.actions)

if __name__ == '__main__':
    myGame = Scene()
    pyglet.app.run()
