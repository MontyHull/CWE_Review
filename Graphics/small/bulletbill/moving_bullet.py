import pyglet as pig

window = pig.window.Window()
image = pig.resource.image('bullet_bill.png')
sprite = pig.sprite.Sprite(image)
sprite.x = -150
sprite.y = -50

@window.event
def on_draw():
    window.clear()
    sprite.draw()

def update(dt):
    sprite.x += dt * 100

pig.clock.schedule_interval(update, 1/360.)

pig.app.run()
