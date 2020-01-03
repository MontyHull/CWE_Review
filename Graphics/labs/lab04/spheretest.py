# Prevents the creation of .pyc files
import sys, traceback, inspect
sys.dont_write_bytecode = True

try:
    from graphics import Ray
except:
    print("FAIL - NO Ray Class")

try:
    from graphics import ColorRGB
except:
    print("FAIL - NO ColorRGB Class")

try:
    from graphics import Sphere
except:
    print("FAIL - NO Sphere Class")

try:
    from graphics import Plane
except:
    print("FAIL - NO Plane Class")

try:
    from graphics import Point3D
except:
    print("FAIL - NO Point3D Class")

try:
    from graphics import Vector3D
except:
    print("FAIL - NO Vector3D Class")

try:
    from graphics import Normal
except:
    print("FAIL - NO Normal Class")

epsilon = 0.000001

try:
    TEST = "Creating Ray"
    R = Ray(Point3D(0,0,0), Vector3D(0,0,1))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Creating ColorRGB"
    C = ColorRGB(0.2, 0.4, 0.6)
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

POK = False
try:
    TEST = "Creating Plane"
    P = Plane(Point3D(1,2,3), Normal(0.3, 0.5, 0.7), ColorRGB(0.6,0.7,0.8))
    POK = True
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

if POK == False:
    try:
        TEST = "Creating Plane - Without Color"
        P = Plane(Point3D(1,2,3), Normal(0.3, 0.5, 0.7))
        POK = True
        print ("PASS "+TEST)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print ("FAIL "+TEST+" ("+str(e)+")")
        myerror = traceback.format_tb(exc_traceback)
        for line in myerror:
            line = str(line).split('\n')
            for item in line:
                print("ERROR: "+item)


SOK = False
try:
    TEST = "Creating Sphere"
    S = Sphere(Point3D(4,5,6), 45.0, ColorRGB(0.9,0.7,0.5))
    SOK = True
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

if SOK == False:
    try:
        TEST = "Creating Sphere"
        S = Sphere(Point3D(4,5,6), 45.0, ColorRGB(0.9,0.7,0.5))
        SOK = True
        print ("PASS "+TEST)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print ("FAIL "+TEST+" ("+str(e)+")")
        myerror = traceback.format_tb(exc_traceback)
        for line in myerror:
            line = str(line).split('\n')
            for item in line:
                print("ERROR: "+item)

try:
    TEST = "ColorRGB Print"
    print("CHECK "+str(C))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "ColorRGB Get"
    r,g,b = C.get()
    print("CHECK "+str([r,g,b]))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Plane Print"
    print("CHECK "+str(P))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Plane Hit"
    if len(inspect.getargspec(P.hit)[0]) == 4:
        print("CHECK "+str(P.hit(R, epsilon, False)))
    else:
        print("CHECK "+str(P.hit(R, epsilon)))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Plane Copy"
    PP = P
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Sphere Print"
    print("CHECK "+str(S))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Sphere Copy"
    SS = S
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

try:
    TEST = "Sphere Hit"
    if len(inspect.getargspec(S.hit)[0]) == 4:
        print("CHECK "+str(S.hit(R, epsilon, False)))
    else:
        print("CHECK "+str(S.hit(R, epsilon)))
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)
