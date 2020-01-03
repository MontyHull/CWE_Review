# M.S. Hall (m172412)
#!/usr/bin/python3
import numpy



# The beginnings of a Vector3D - For you to edit
class Vector3D:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Vector3D")
    def __repr__(self):
        return str(self.v)
    def __add__(self, other):
        return Vector3D(self.v + other.v)
    def __sub__(self,other):
        return Vector3D(self.v - other.v)
    def __mul__(self,a):
        #Ask if we need to check for anything else
        if isinstance(a,Vector3D) or isinstance(a,Normal):
            return numpy.dot(self.v,a.v)
        else:
            return Vector3D(self.v*a)
    def __truediv__(self,a):
        return Vector3D(self.v/a)
    def copy(self):
        return Vector3D(self.v.copy())
    def magnitude(self):
        return((self.v[0]**2 +self.v[1]**2 +self.v[2]**2)**.5)
    def square(self):
        return numpy.sum(numpy.square(self.v))
    def dot(self,other):
        return numpy.dot(self.v,other.v)
    def dotangle(self,other,angle):
        return self.magnitude() * other.magnitude() * numpy.cos(numpy.radians(angle))
    def cross(self,other):
        return Vector3D(numpy.cross(self.v,other.v))


class Point3D:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Point3D")
    def __repr__(self):
        return str(self.v)
    def __add__(self,other):
        return Point3D(self.v + other.v)
    def __sub__(self,other):
        if isinstance(other, Vector3D) is False:
            return Vector3D(self.v - other.v)
        else:
            return Point3D(self.v - other.v)
    def distancesquared(self,other):
        return numpy.sum(numpy.square(self.v-other.v))
    def distance(self,other):
        return numpy.sqrt(numpy.sum(numpy.square(self.v-other.v)))
    def copy(self):
        return Point3D(self.v.copy())
    def __mul__(self,c):
        return Point3D(self.v*c)


class Normal:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to Normal")
    def __repr__(self):
        return str(self.v)
    def copy(self):
        return Normal(self.v.copy())
    def __add__(self,other):
        if isinstance(other,Normal):
            return Normal(self.v + other.v)
        else:
            return Vector3D(self.v + other.v)
    def __neg__(self):
        return Normal(self.v *-1)
    def __mul__(self,c):
        if isinstance(c,Vector3D) or isinstance(c,Normal):
            return numpy.dot(self.v,c.v)
        else:
            return Normal(self.v*c)
    def dot(self,other):
        return numpy.dot(self.v,other.v)

class Ray:
    def __init__(self,origin,direction):
        if isinstance(origin, Point3D) and isinstance(direction,Vector3D):
            self.origin = origin.copy()
            self.direction = direction.copy()
        else:
            raise Exception("Invalid Arguments to Ray")
    def __repr__(self):
        return "[" + str(self.origin) + ", " + str(self.direction) + "]"
    def copy(self):
        return Ray(self.origin.copy(),self.direction.copy())
    def get(self):
        return self.origin, self.direction

class ColorRGB:
    def __init__(self, val, *args):
        if type(val) is numpy.ndarray:
            self.v = val
        elif args and len(args) == 2:
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("Invalid Arguments to ColorRGB")
    def __repr__(self):
        return str(self.v)
    def get(self):
        return self.v[0],self.v[1],self.v[2]
    def __add__(self,other):
        return ColorRGB(self.v+other.v)
    def __mul__(self,other):
        if type(other) is ColorRGB:
            return ColorRGB(self.v*other.v)
        else:
            return ColorRGB(self.v*other)
    def __truediv__(self,other):
        return ColorRGB(self.v/other)
    def __pow__(self,other):
        return ColorRGB(self.v**other)
    def copy(self):
        return ColorRGB(self.v.copy())

class Plane:
    def __init__(self,point,normal,color):
        if type(point) is Point3D and type(normal) is Normal and type(color) is ColorRGB:
            self.p = point.copy()
            self.n = normal.copy()
            self.c = color.copy()
        else:
            raise Exception("Invalid Arguments to Plane")
    def __repr__(self):
        return "[" + str(self.p) +", " +str(self.n)+"]"
    def copy(self):
        return Plane(self.p,self.n,self.c)
    def hit(self,aRay,epsilon,shadeRec):
        t = (self.p - aRay.origin)*self.n(aRay.direction*self.n)
        hit_point = aRay.origin+aRay.direction*t
        if(t > epsilon):
            return True,t,hit_point,self.c
        else:
            return False,t,hit_point,self.c

class Sphere:
    def __init__(self,aPoint,radius,aColor):
        if type(aPoint) is Point3D and type(aColor) is ColorRGB:
            self.p = aPoint
            self.r = radius
            self.c = aColor
        else:
            raise Exception("Invalid Arguments to Sphere")
    def copy(self):
        return Sphere(self.p,self.r,self.c)
    def __repr__(self):
        x = "["+str(self.p)+", "+str(self.r)+"]"
        return str(x)
    def hit(self,aRay,epsilon,shadeRec):
        a = aRay.direction * aRay.direction
        b = ((aRay.origin-self.p)*2)*aRay.direction
        c = (aRay.origin-self.p) * (aRay.origin - self.p) - (self.r**2)
        #return a,b,c
        t1 = (-b + numpy.sqrt(numpy.square(b)-4*a*c))/2*a
        t2 = (-b - numpy.sqrt(numpy.square(b)-4*a*c))/2*a
        #min if both greater than epsilon
        discrim = numpy.square(b) - (4 * a *c )
        x1 = a*numpy.square(t1)+b*t1+c
        x2 = a*numpy.square(t2)+b*t2+c
        p = aRay.origin + aRay.direction * t
        if(discrim >= 0):
            return True,t1,p,self.c
        else:
            return False,t1,p,self.c

class ViewPlane:
    def __init__(self,icenter,inormal,ihres,ivres,ipixelsize):
        self.center = icenter
        self.norm = inormal
        self.hres = ihres
        self.vres = ivres
        self.hvres = []
        for i in range(ivres):
            self.hvres.append([])
            for j in range(ihres):
                self.hvres[i].append(ColorRGB(0.0,0.0,0.0))
        self.pixsize = ipixelsize
        Vup = Vector3D(0,-1,0)
        top = Vup.cross(-inormal)
        bot = Vup.cross(-inormal)
        self.u = top/(bot.magnitude())

        self.v = self.u.cross(-inormal)
        self.LL = icenter - self.u*(ihres/2.0)-self.v*(ivres/2.0)*ipixelsize
    def get_color(self,row,col):
        return self.hvres[row][col]
    def set_color(self,row,col,newColor):
        self.hvres[row][col] = newColor
    def get_point(self,row,col):
        return self.LL + self.u * (col+.5) * self.pixsize + self.v * (row+.5) * self.pixsize
    def get_resolution(self):
        return self.hres,self.vres
    def orthographic_ray(self,row,col):
        return Ray(self.get_point(row,col),Vector3D(self.norm.v))

def randomCube(fll,bur,n):
    if(fll.v[0] > bur.v[0]):
        side = fll.v[0] - bur.v[0]
    else:
        side = bur.v[0] - fll.v[0]
    allPoints = []
    for i in range(n):
        x = side * numpy.random.rand() + fll.v[0]
        y = side * numpy.random.rand() + fll.v[1]
        z = side * numpy.random.rand() + fll.v[2]
        newPoint = Point3D(x,y,z)
        allPoints.append(newPoint)
    return allPoints
# We should always have debugging in our libraries
# that run if the file is called from the command line
# vice from an import statement!
if __name__ == '__main__':
    u = Vector3D(1,2,3)
    v = Vector3D(4,5,6)
    w = Vector3D(2,4,6)

    #Printing
    print("Testing Printing...")
    if str(u) != '[ 1.  2.  3.]':
        raise Exception("Printing Error!")

    #Addition
    print("Testing Addition...")
    c = u + v
    if str(c) != '[ 5.  7.  9.]':
        raise Exception("Addition Error!")

    #Subtraction
    print("Testing Subtraction...")
    d = v - u
    if str(d) != '[ 3.  3.  3.]':
        raise Exception("Subtraction Error!")

    #Multiplication
    print("Testing Multiplication...")
    e = u * 2.0
    if str(e) != '[ 2.  4.  6.]':
        raise Exception("Multiplication Error!")

    #Division
    print("Testing Division...")
    f = w / 2.0
    if str(f) != '[ 1.  2.  3.]':
        raise Exception("Division Error!")

    #Copy
    print("Testing Copy...")
    g = u.copy()
    if str(g) != '[ 1.  2.  3.]':
        raise Exception("Equality Error!")

    #Magnitude
    print("Testing Magnitude...")
    h = u.magnitude()
    if isinstance(h,numpy.float64) is False:
        raise Exception("Magnitude Error!")

    #Square
    print("Testing Square...")
    i = u.square()
    if isinstance(i,numpy.float64) is False:
        raise Exception("Magnitude Error!")

    #Dot
    print("Testing Dot...")
    j = u.dot(v)
    if  str(j) != '32.0' or isinstance(j,numpy.float64) is False:
        raise Exception("Dot Error!")

    #Dotangle
    print("Testing Dotangle...")
    k = u.dotangle(v,60)
    if isinstance(k,numpy.float64) is False:
        raise Exception("Dotangle Error!")

    #Cross
    print("Testing Cross...")
    l = u.cross(v)
    if isinstance(k,numpy.float64) is False:
        raise Exception("Cross Error!")

    print("\nHUZZAH! The Vector3D class was successful!\n\n")



    u = Point3D(1,2,3)
    v = Point3D(4,5,6)
    w = Vector3D(4,5,6)

    #Printing
    print("Testing Printing...")
    if str(u) != '[ 1.  2.  3.]':
        raise Exception("Printing Error!")

    #Adding
    print("Testing Adding...")
    c = u+v
    if str(c) != '[ 5.  7.  9.]':
        raise Exception("Addition Error!")

    #Subtraction of Point and Vector
    print("Testing Subtraction of Point and Vector...")
    c = u-w
    if str(c) != '[-3. -3. -3.]' or not isinstance(c,Point3D):
        raise Exception("Subtraction Error!")

    #Subtraction of Point and Point
    print("Testing Subtraction of Point and Point...")
    c = u-v
    if str(c) != '[-3. -3. -3.]' or not isinstance(c,Vector3D):
        raise Exception("Subtraction Error!")

    #Distancesquared
    print("Testing Distancesquared...")
    c = u.distancesquared(v)
    if str(c) != "27.0":
        raise Exception("Distancesquared Error!")

    #Distance
    print("Testing Distance...")
    c = u.distance(v)
    if str(c) != "5.19615242271":
        raise Exception("Distance Error!")

    #Copy
    print("Testing Copy...")
    c = v.copy()
    if str(c) != str(v):
        raise Exception("Distance Error!")

    #Multiplication
    print("Testing Multiplication...")
    c = u * 2
    if str(c) != '[ 2.  4.  6.]':
        raise Exception("Multiplication Error!")

    print("\nHUZZAH! The Point3D class was successful!\n\n")


    u = Normal(1,2,3)
    v = Normal(4,5,6)
    w = Vector3D(4,5,6)

    #Printing
    print("Testing Printing...")
    if str(u) != '[ 1.  2.  3.]':
        raise Exception("Printing Error!")

    #Adding Normal and Normal
    print("Testing Adding Normal and Normal...")
    c = u+v
    if str(c) != '[ 5.  7.  9.]' or isinstance(c, Normal) is False:
        raise Exception("Addition of Normal and Normal Error!")

    #Adding Normal and Vector
    print("Testing Adding Normal and Vector...")
    c = u + w
    if str(c) != '[ 5.  7.  9.]' or isinstance(c, Vector3D) is False:
        raise Exception("Addition of Normal and Vector Error!")

    #Adding Vector and Normal
    print("Testing Adding Vector and Normal...")
    c = w + u
    if str(c) != '[ 5.  7.  9.]' or isinstance(c, Vector3D) is False:
        raise Exception("Addition of Vector and Normal Error!")

    #Multiplication
    print("Testing Multiplication...")
    c = u * 2
    if str(c) != '[ 2.  4.  6.]' or isinstance(c,Normal) is False:
        raise Exception("Multiplication Error!")

    #Dot
    print("Testing Dot...")
    c = u.dot(v)
    if str(c) != '32.0':
        raise Exception("Dot Error!")

    print("\nHUZZAH! The Normal class was successful!\n\n")
    '''
    poi = Point3D(1,2,4)
    Norm = Normal(3,4,5)
    col2 = ColorRGB(1,2,3)
    col3 = col2**2
    pla = Plane(poi,Norm,col1)
    print(pla)
    sph = Sphere(poi,10.0,col1)
    print(sph)
    v = Vector3D(1,2,3)
    R = Ray(poi,v)
    a = sph.hit(R,1,1)
    print(type(a))
    #print(type(b))
    #print(type(c))
    '''
    Vector = Vector3D(1,2,3)
    Point = Point3D(0,0,0)
    n = Normal(0,0,1)
    col1 = ColorRGB(.5,.6,.7)
    vp = ViewPlane(Point,n,640,480,1)
    vp.set_color(0,0,col1)
    print(vp.get_color(0,0))
    np = vp.get_point(100,250)
    print(np)
    oray = vp.orthographic_ray(100,250)
