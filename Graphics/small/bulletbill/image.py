import pyglet as pig
from pyglet.window import key
window = pig.window.Window()

image = pig.resource.image('logo.png')

x = 0
y = 0

@window.event
def on_draw():
    global x,y
    window.clear()
    image.blit(x,y)

@window.event
def on_key_press(symbol,modifier):
    global x,y
    if symbol == key.RIGHT:
        x = x+1
        print("moved right")
window.push_handlers(pig.window.event.WindowEventLogger())   
pig.app.run()
