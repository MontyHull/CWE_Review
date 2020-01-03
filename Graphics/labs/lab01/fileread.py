import sys

if(len(sys.argv) == 1):
    print("usage: fileread.py filename")
    sys.exit()
array = []
try:
    with open(sys.argv[1],'r') as fileobj:
        for line in fileobj:
            word= line[212:316]
            number = word[:14]
            place = word[14:].rstrip()
            fullset = place + number
            array.append(fullset)
        array.sort()
        for i in range(len(array)):
            print(array[i][-14:].strip().ljust(21) + array[i][:-14].rstrip())
except IOError as e:
    print("File does not exist")
    print(str(e))
except:
    print("Exception not related to IO")
