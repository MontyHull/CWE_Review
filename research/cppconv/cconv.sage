# program to convert a bilinear map circuit to C code

# helper function to write out a linear combination
def lincomb(colist, varlist, out, indent=''):
    first = True
    for c,v in zip(colist, varlist):
        if c.is_zero():
            continue
        out.write(indent)

        cneg = 'sign' in dir(c) and c.sign() == -1

        if first:
            if cneg:
                out.write('-')
                c *= c.sign()
            first = False
        elif cneg:
            out.write('- ')
            c *= c.sign()
        else:
            out.write('+ ')

        if not c.is_one():
            out.write('{} * '.format(c))

        out.write('{}\n'.format(v))
    assert not first

# X, Y, Z should be coefficient matrices that define the map
# fname is the name of the C function to generate.
# T is the C type to use in the computation (default int)
# outfile is the source code file to generate (default <fname>.c)
def cconv(X, Y, Z, fname, T="int", outfile=None): 
    if outfile is None:
        outfile = "{}.c".format(fname)

    numin = X.nrows()
    nummul = X.ncols()
    numout = Z.ncols()

    assert X.nrows() == Y.nrows() == numin
    assert X.ncols() == Y.ncols() == Z.nrows() == nummul
    assert Z.ncols() == numout

    with open(outfile, "w") as out:
        out.write('/* change this to make the function work for a different type */\n')
        out.write('typedef {} T;\n'.format(T))
        out.write('\n')

        out.write('/* generated function below.\n')
        out.write(' * note: aliasing between outputs and inputs IS allowed. */\n')
        out.write('void {} (T* outputs /* size {} */, const T* inputs /* size {} */)\n'
                  .format(fname, numout, numin))
        out.write('{\n')

        zeros = set()
        inputs = ['inputs[{}]'.format(i) for i in range(numin)]
        muls = ['p{}'.format(i) for i in range(nummul)]
        for i in range(nummul):
            if all(X[j][i].is_zero() for j in range(numin)):
                zeros.add(i)
                continue
            if all(Y[j][i].is_zero() for j in range(numin)):
                zeros.add(i)
                continue
            out.write('  T {} =\n    (\n'.format(muls[i]))
            lincomb(X.column(i), inputs, out, '      ')
            out.write('    ) * (\n')
            lincomb(Y.column(i), inputs, out, '      ')
            out.write('    );\n')

        for i in range(numout):
            out.write('  outputs[{}] ='.format(i))
            col = list(Z.column(i))
            for j in zeros:
                col[j] = 0

            if all(x.is_zero() for x in col):
                out.write(' 0;\n')
            else:
                out.write('\n')
                lincomb(col, muls, out, '    ')
                out.write('    ;\n')

        out.write('}\n')

    print("Function {} saved to {}.".format(fname, outfile))
