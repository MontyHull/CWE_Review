from Scene import Point

fp = open('savestate1.txt','r')
lists = []
for line in fp:
    lists.append([])
    p = line.strip().split(",")
    for elements in p:
        twonumbs = elements.split(":")
        if(len(twonumbs) == 2):
            lists[len(lists)-1].append(Point(twonumbs[0],twonumbs[1]))
        print twonumbs

print(len(lists[1]))
