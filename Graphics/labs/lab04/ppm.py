import graphics as g

def PPM(VPO,fn):
    col,row = VPO.get_resolution()
    fp = open(fn,"w")
    fp.write("P3\n")
    fp.write(str(col)+" "+str(row)+"\n255\n")
    for i in range(row-1,-1,-1):
        for j in range(col):
            r,g,b = VPO.get_color(i,j).get()
            r = int(r*255)
            g = int(g*255)
            b = int(b*255)

            fp.write(str(r)+" "+str(g)+" "+str(b)+" ")
        fp.write("\n")
