import sys

if(len(sys.argv) == 1):
    print("usage: isprime.py ###")
elif(int(sys.argv[1]) > 512):
    print("Choose a number less than 512")
else:
    for i in range(2,int(sys.argv[1])):
        if(int(sys.argv[1])%i == 0):
            print("Not Prime!")
            sys.exit()
    print("Prime!");
