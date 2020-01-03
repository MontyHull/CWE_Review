from graphics import Sphere, Plane, Point3D, Normal, ColorRGB, ViewPlane

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
center = Point3D(0,0,0)
normal = Normal(0,0,1)
width = 640
height = 480
scalingFactor = 1.0
world = ViewPlane(center,normal,width,height,scalingFactor)

#Create a ray that originates from the center point of a row/column on the viewing-plane (.orthographic_ray)
origin_rays= [world.orthographic_ray(0,0),world.orthographic_ray(479,639)]
mins = []
colors = []

for i in range(len(origin_rays)):
    mins.append(0)
    colors.append(0)
    for j in range(len(world_objects)):
        if_hit,t,where,color = world_objects[j].hit(origin_rays[i],1.0)
        if(if_hit is True):
            if mins[i] == 0 and t > 0:
                mins[i] = t
                colors[i] = color
            elif t < mins[i]:
                mins[i] = t
                colors[i] = color

for i in range(len(mins)):
    print(mins[i]," ",colors[i])
