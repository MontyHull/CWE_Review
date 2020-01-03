import numpy
# Vector3D Class
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
        if isinstance(other, Point3D):
            return Point3D(self.v + other.v)
        elif isinstance(other, Normal):
            return Vector3D(self.v + other.v)
        else:
            return Vector3D(self.v + other.v)
    def __sub__(self, other):
        return Vector3D(self.v - other.v)
    def __div__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.v / other.v)
        else:
            return Vector3D(self.v / other)
    def __truediv__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.v / other.v)
        else:
            return Vector3D(self.v / other)
    def magnitude(self):
        return numpy.linalg.norm(self.v)
    def square(self):
        return numpy.square(self.magnitude())
    def __mul__(self, other):
        if isinstance(other, Vector3D) or isinstance(other, Normal):
            return numpy.dot(self.v, other.v)
        else:
            return Vector3D(self.v * other)
    def dot(self, other):
        if isinstance(other, Vector3D) or isinstance(other, Normal):
            return numpy.dot(self.v, other.v)
        else:
            raise Exception("You can only calc the dot product between a Normal and a Vector3D")
    def dotangle(self, other, angle):
        return self.magnitude() * other.magnitude() * numpy.cos(numpy.radians(angle))
    def cross(self, other):
        return Vector3D(numpy.cross(self.v, other.v))
    def copy(self):
        return Vector3D(self.v.copy())

# Point3D Class
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
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.v + other.v)
        else:
            raise Exception("You can only add a Vector3D to a Point3D")
    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Point3D(self.v - other.v)
        elif isinstance(other, Point3D):
            return Vector3D(self.v - other.v)
        else:
            raise Exception("You can only subtract either a Vector3D or a Point3D from a Point3D")
    def __mul__(self, other):
        return Point3D(self.v * other)
    def distance(self, other):
        tmpVector = self.__sub__(other)
        return tmpVector.magnitude()
    def distancesquared(self, other):
        return numpy.square(self.distance(other))
    def copy(self):
        return Point3D(self.v.copy())

# Graphics Normal Class
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
    def __neg__(self):
        return Normal(self.v * -1)
    def __add__(self, other):
        if isinstance(other, Normal):
            return Normal(self.v + other.v)
        elif isinstance(other, Vector3D):
            return Vector3D(self.v + other.v)
        else:
            raise Exception("You can only add a Vector3D or a Normal to a Normal")
    def __mul__(self, other):
        if isinstance(other, Vector3D) or isinstance(other, Normal):
            return numpy.dot(self.v, other.v)
        else:
            return Normal(self.v * other)
    def dot(self, other):
        if isinstance(other, Vector3D):
            return numpy.dot(self.v, other.v)
        else:
            raise Exception("You can only calc the dot product between a Normal and a Vector3D")

# Ray Class
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = Vector3D(direction.v)
    def copy(self):
        return Ray(self.origin.copy(), self.direction.copy())
    def __repr__(self):
        return str([self.origin, self.direction])

# ColorRGB Class
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
    def copy(self):
        return ColorRGB(self.v.copy())
    def get(self):
        return self.v[0], self.v[1], self.v[2]
    def __add__(self, other):
        return ColorRGB(self.v + other.v)
    def __mul__(self, other):
        if isinstance(other, ColorRGB):
            return ColorRGB(self.v * other.v)
        else:
            return ColorRGB(self.v * other)
    def __div__(self, other):
        return ColorRGB(self.v / other)
    def __truediv__(self, other):
        return ColorRGB(self.v / other)
    def __pow__(self, other):
        return ColorRGB(self.v ** other)

# Plane Class with Hit Point Detection
class Plane:
    def __init__(self, point, normal, color=ColorRGB(1,1,1)):
        self.point = point
        self.normal = normal
        self.color = color
    def copy(self):
        return Plane(self.point.copy(), self.normal.copy())
    def __repr__(self):
        return str([self.point, self.normal])
    def hit(self, ray, epsilon, shadeRec=False):
        t = ((self.point - ray.origin) * self.normal) / (ray.direction * self.normal)
        hit = ray.origin + ray.direction * t
        return True, t, hit, self.color

# Sphere Class with Hit Point Detection
class Sphere:
    def __init__(self, center, radius, color=ColorRGB(1,1,1)):
        self.center = center
        self.radius = radius
        self.color = color
    def copy(self):
        return Sphere(self.center.copy(), self.radius)
    def __repr__(self):
        return str([self.center, self.radius])
    def hit(self, ray, epsilon, shadeRec=False):
        a = ray.direction * ray.direction
        b = 2.0 * ((ray.origin - self.center) * ray.direction)
        c = (ray.origin - self.center) * (ray.origin - self.center) - self.radius**2
        d = b**2 - 4*a*c
        if d < 0:
            return False, False, False, False
        t1 = (-b + numpy.sqrt(d)) / (a*2)
        t2 = (-b - numpy.sqrt(d)) / (a*2)
        p1 = ray.origin + ray.direction*t1
        p2 = ray.origin + ray.direction*t2
        if max(t1,t2) < epsilon:
            return False, False, False, False
        if t1 > epsilon and t2 < epsilon:
            return True, t1, p1, self.color
        elif t2 > epsilon and t1 < epsilon:
            return True, t2, p2, self.color
        elif t1 < t2:
            return True, t1, p1, self.color
        else:
            return True, t2, p2, self.color

# ViewPlane Class with all of the fun number things
class ViewPlane:
    def __init__(self,icenter,inormal,ihres,ivres,ipixelsize):
        #Point in center of plane
        self.center = icenter
        #Normal which is just a ray really
        self.norm = inormal
        #horizontal resolution/int/float
        self.hres = ihres
        #vertical resolution/int/float
        self.vres = ivres
        #vertical resolution X horizontal resolution
        self.hvres = []
        for i in range(ivres):
            self.hvres.append([])
            for j in range(ihres):
                self.hvres[i].append(ColorRGB(0.0,0.0,0.0))
        #pixel modifier
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
