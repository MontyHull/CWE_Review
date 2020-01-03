from __future__ import print_function
import makeTopoMap
M = makeTopoMap.get_matrix(seed=331, rows=10, cols=10, delta=3, maxval=20)
t = 1.5
M = [[1,3,1],
     [0,0,0],
     [1,3,1]]
#for x add j to ULX and the difference
#for y add i to ULY and the difference
#formula for between 2 points = (threshold - Low)/ (high-low)

def difference(a,b,t):
    if(a > b):
        return((t-b)/(a-b))
    return((t-a)/(b-a))

ULX = -2
ULY = 2
for i in range(2):
    for j in range(2):

        # UL to UR
        a = M[i][j]
        b = M[i][j+1]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            x=j+ULX+dif
            y=i
            print("Point at",x,",",y,"dif = ",dif)

        # UR to LR
        a = M[i][j+1]
        b = M[i+1][j+1]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            x=j
            y=i+ULY-dif
            print("Point at",x,",",y,"dif = ",dif)

        # LR to LL
        a = M[i+1][j+1]
        b = M[i+1][j]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            x=j+ULX+dif
            y=i
            print("Point at",x,",",y,"dif = ",dif)

        # LL to UR
        a = M[i+1][j]
        b = M[i][j]
        if((a >= t) ^ (b >= t)):
            dif = difference(a,b,t)
            x=j
            y=i+ULY-dif
            print("Point at",x,",",y,"dif = ",dif)


        #print()




print(M)
