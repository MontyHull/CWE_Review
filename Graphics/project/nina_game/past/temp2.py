# Prevent the creation of pyc files
import sys
sys.dont_write_bytecode = True

# pyglet event handler demo
import pyglet
from pyglet.window import mouse, key
from pyglet.gl import glEnable, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_BLEND
from pyglet.gl import glLoadIdentity, glTranslatef

# Our World
class Scene:
    # Move objects between keyboard input
    def movement(self, dt):
        print('%f seconds since last callback' %dt)

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?"):

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, caption=caption)

        # Fix transparent issue...  *needed depending on how you load transparent images*
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Create the Background
        self.background = pyglet.image.load("background.png")
        self.background_x = 0
        self.background_y = 0

        # Example Text
        self.x = pyglet.text.Label('Look - Text!',
                   font_name='Times New Roman',
                   font_size=36,
                   x=width/2, y=height/2,
                   anchor_x='center', anchor_y='center')

        # Great for debugging
        self.window.push_handlers(pyglet.window.event.WindowEventLogger())

        # Schedule player movements
        pyglet.clock.schedule_interval(self.movement, 2.5)

        # Example event for pressing a key
        @self.window.event
        def on_key_press(symbol, modifiers):
            print(str(['on_key_press', 'symbol=', symbol, 'modifiers=', modifiers]))

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()
            self.background.blit(self.background_x,self.background_y,height=height)
            self.x.draw()

if __name__ == '__main__':
    myGame = Scene()
    pyglet.app.run()
