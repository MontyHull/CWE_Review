from __future__ import print_function
import makeTopoMap
M = makeTopoMap.get_matrix(seed=331, rows=10, cols=10, delta=3, maxval=20)
t = 1.5
M = [[1,3,1],
     [0,1,0],
     [1,3,1]]

#for x add j to ULX and the difference
#for y add i to ULY and the difference
#formula for between 2 points = (threshold - Low)/ (high-low)

def difference(a,b,t):
    if(a > b):
        return ((t-b)/(a-b))
    return ((t-a)/(b-a))

ULX = -1
ULY = 1
for i in range(2):
    for j in range(2):

        print("checking (",M[i][j],",",M[i][j+1],"),",end="")
        print("(",M[i][j+1],",",M[i+1][j+1],"),",end="")
        print("(",M[i+1][j+1],",",M[i+1][j],"),",end="")
        print("(",M[i+1][j],",",M[i][j],")")

        # UL to UR
        a = M[i][j]
        b = M[i][j+1]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            if(a > b):
                dif = 1-dif
            x=j+ULX+dif
            y=ULY-i
            print("ul to ur between ",a,b)
            print("Point at",x,",",y,"        dif = ",dif)
            print()

        # UR to LR I think good
        a = M[i][j+1]
        b = M[i+1][j+1]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            if(a > b):
                dif = 1-dif
            x=ULX+(j+1)
            y=ULY-i-dif
            print("ur to lr between",a,b)
            print("Point at",x,",",y,"        dif = ",dif)
            print()

        # LR to LL
        a = M[i+1][j+1]
        b = M[i+1][j]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            if(b > a):
                dif = 1-dif
            x=j+ULX+dif
            y=ULY-(i+1)
            print("lr to ll between", a, b)
            print("Point at",x,",",y,"        dif = ",dif)
            print()

        # LL to UL I think good
        a = M[i+1][j]
        b = M[i][j]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            if(b > a):
                dif = 1-dif
            x=j+ULX
            y=ULY-i-dif
            print("ll to uL between",a,b)
            print("Point at",x,",",y,"        dif = ",dif)
            print()


        #print()




print(M)
