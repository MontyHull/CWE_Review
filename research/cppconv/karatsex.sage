# matrices defining bilinear map for Karatsuba's algorithm

load('cconv.sage')

X = Matrix(ZZ,
    [[1, 0, 1],
     [0, 1, 1],
     [0, 0, 0],
     [0, 0, 0]])

Y = Matrix(ZZ,
    [[0, 0, 0],
     [0, 0, 0],
     [1, 0, 1],
     [0, 1, 1]])

Z = Matrix(ZZ,
    [[1, -1, 0],
     [0, -1, 1],
     [0, 1, 0]])

cconv(X, Y, Z, 'karatsuba', T="double")
