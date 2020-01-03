# Prevents the creation of .pyc files
import sys, traceback
sys.dont_write_bytecode = True

vp_center, vp_normal, vp_normal2, vp_normal3, vp, vp2, vp3, vp_c1, vp_c2 = None, None, None, None, None, None, None, None, None

# Load in classes
try:
    from graphics import Point3D
except:
    print("FAIL - NO Point3D Class")

# Load in classes
try:
    from graphics import ColorRGB
except:
    print("FAIL - NO ColorRGB Class")

try:
    from graphics import Normal
except:
    print("FAIL - NO Normal Class")

try:
    from graphics import ViewPlane
except:
    print("FAIL - NO ViewPlane Class")

try:
    TEST = "Creating ViewPlane CenterPoint"
    vp_center = Point3D(10,10,10)
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
    TEST = "Creating ViewPlane Colors"
    vp_c1 = ColorRGB(0.2,0.9,0.8)
    vp_c2 = ColorRGB(0.6,0.6,0.6)
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
    TEST = "Creating ViewPlane Normal"
    vp_normal = Normal(1,1,1)
    vp_normal2 = Normal(0,0,1)
    vp_normal3 = Normal(0.3, 0.7, 0.9)
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)

# Create Variables
try:
    TEST = "Creating ViewPlane"
    vp = ViewPlane(vp_center, vp_normal, 640, 480, 1.0)
    vp2 = ViewPlane(vp_center, vp_normal2, 640, 480, 1.0)
    vp3 = ViewPlane(vp_center, vp_normal3, 640, 480, 1.0)
    print ("PASS "+TEST)
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print ("FAIL "+TEST+" ("+str(e)+")")
    myerror = traceback.format_tb(exc_traceback)
    for line in myerror:
        line = str(line).split('\n')
        for item in line:
            print("ERROR: "+item)


# Return the string value (protected by try)
def show(t):
    try:
        return str(t)
    except:
        return 'INVALID STRING'

# Evaluate for errors
def test(TEST, vp, vp_c1, vp_c2):
    try:
        t = eval(TEST)
        print ("PASS "+TEST.ljust(20)+' => '+show(t))
        return t
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print ("FAIL "+TEST+" ("+str(e)+")")
        myerror = traceback.format_tb(exc_traceback)
        for line in myerror:
            line = str(line).split('\n')
            for item in line:
                print("ERROR: "+item)
        return None

# Lab3 Part1 Tests
t = test('vp.get_color(420,630)', vp, vp_c1, vp_c2)
t = test('vp.set_color(420,630, vp_c1)', vp, vp_c1, vp_c2)
t = test('vp.get_color(420,630)', vp, vp_c1, vp_c2)
t = test('vp.get_resolution()', vp, vp_c1, vp_c2)

print("Viewplane w/ Normal (1,1,1)")
t = test('vp.get_point(420,630)', vp, vp_c1, vp_c2)
t = test('vp.orthographic_ray(420,630)', vp, vp_c1, vp_c2)

print("Viewplane w/ Normal (0,0,1)")
t = test('vp.get_point(420,630)', vp2, vp_c1, vp_c2)
t = test('vp.orthographic_ray(420,630)', vp2, vp_c1, vp_c2)

print("Viewplane w/ Normal (0.3, 0.7, 0.9)")
t = test('vp.get_point(420,630)', vp3, vp_c1, vp_c2)
t = test('vp.orthographic_ray(420,630)', vp3, vp_c1, vp_c2)
