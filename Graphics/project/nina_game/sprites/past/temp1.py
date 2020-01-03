# pyglet event handler demo

import pyglet
from pyglet.window import mouse, key

# Our World
class Scene:
    # Move objects between keyboard input
    def movement(self, dt):
        print('%f seconds since last callback' %dt)
        self.background_x -= 1

    # Initialize and run our environment
    def __init__(self, width=800, height=600, caption="Would you like to play a game?"):

        # Build the OpenGL / Pyglet Window
        self.window = pyglet.window.Window(width=width, height=height, caption=caption)

        # Create the Background
        self.background = pyglet.resource.image("background.png")
        self.background_x = 0

        # Example Text
        self.label1 = pyglet.text.Label('Look at the debugging data!',
                          font_name='Times New Roman',
                          font_size=36,
                          x=width//2, y=height//3*2,
                          anchor_x='center', anchor_y='center')

        self.label2 = pyglet.text.Label('Press ESC to exit',
                          font_name='Times New Roman',
                          font_size=24,
                          x=width//2, y=height//3,
                          anchor_x='center', anchor_y='center')

        # Great for debugging
        self.window.push_handlers(pyglet.window.event.WindowEventLogger())

        # Schedule player movements
        pyglet.clock.schedule_interval(self.movement, 2.5)

        # Event Handler for drawing the screen
        @self.window.event
        def on_draw():
            self.window.clear()
            self.background.blit(self.background_x,0,height=height)
            self.label1.draw()
            self.label2.draw()

if __name__ == '__main__':
    myGame = Scene()
    pyglet.app.run()
