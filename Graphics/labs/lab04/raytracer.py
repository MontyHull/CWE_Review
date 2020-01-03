from graphics import Sphere, Plane, Point3D, Normal, ColorRGB, ViewPlane
from ppm import PPM

# Build the Spheres that will be in our world
S1 = Sphere(Point3D(300,200,200), 100, ColorRGB(1.0,0.2,0.4))
S2 = Sphere(Point3D(-200,-100,50), 35, ColorRGB(0.3,0.8,0.2))
S3 = Sphere(Point3D(50,20,100), 25, ColorRGB(0.4,0.1,0.4))
S4 = Sphere(Point3D(300,-200,600), 250, ColorRGB(0.6,0.6,0.4))
S5 = Sphere(Point3D(400,400,900), 400, ColorRGB(0.0,0.2,1.0))

world_objects = [S1,S2,S3,S4,S5]

# Build the Planes that will be in our world
world_objects.append(Plane(Point3D(50,50,999), Normal(0,0,1), ColorRGB(0.8,0.8,0.8)))
world_objects.append(Plane(Point3D(50,50,900), Normal(1,1,1), ColorRGB(1.0,1.0,1.0)))

#Our orthographic viewing plane
#world = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 200, 100, 1.0)
#world = ViewPlane(Point3D(50,50,-50), Normal(0,0,1), 200, 100, 1.0)
#world = ViewPlane(Point3D(50,50,-50), Normal(1,1,1), 200, 100, 1.0)
#world = ViewPlane(Point3D(0,0,0), Normal(0,0,1), 640, 480, 1.0)
world = ViewPlane(Point3D(50,50,-50), Normal(-0.2,0,1), 200, 100, 1.0)
mins = []
cols,rows = world.get_resolution()

for row in range(rows):
    mins.append([])
    for col in range(cols):

        #j and i may be backwards
        #(row,col)
        ray = world.orthographic_ray(row,col)
        mins[row].append(0)

        #goes throught all objects that we have created and checks there t values for the smallest
        for k in range(len(world_objects)):
            if_hit,t,where,color = world_objects[k].hit(ray,1.0)
            if(if_hit is True):
                if mins[row][col] == 0 and t > 0:
                    mins[row][col] = t
                    world.set_color(row,col,color)
                elif t < mins[row][col]:
                    mins[row][col] = t
                    world.set_color(row,col,color)
PPM(world, 'ex5.ppm')
