import pyglet as pig

window = pig.window.Window()

label = pig.text.Label('Hello World!',
                        font_name = 'Times New Roman',
                        font_size = 36,
                        x = window.width//2, y=window.height//2,
                        anchor_x = 'center', anchor_y = 'center')

@window.event
def on_draw():
    window.clear()
    label.draw()

pig.app.run()
