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
        return numpy.cross(self.v,other.v)


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
    def __add__(self,other):
        if isinstance(other,Normal):
            return Normal(self.v + other.v)
        else:
            return Vector3D(self.v + other.v)
    def __neg__(self):
        return Normal(self.v *-1)
    def __mul__(self,c):
        return Normal(self.v*c)
    def dot(self,other):
        return numpy.dot(self.v,other.v)



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

    #Random Cube
    fll = Point3D(1,1,1)
    bur = Point3D(5,5,5)
    n = 3
    allPoints = randomCube(fll,bur,n)
