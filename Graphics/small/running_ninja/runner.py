import pyglet as pyg



runner = []
for i in range(1,11):
    image =pyg.resource.image("sprites/hero/run"+str(i)+".png")
    runner.append(image)
    #sprite = pyg.sprite.Sprite(image)


sequence = pyg.image.Animation.from_image_sequence(runner,.05,True)

sprite = pyg.sprite.Sprite(sequence)
window = pyg.window.Window()

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyg.app.run()
