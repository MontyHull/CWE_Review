# code for 2x2 determinant algebraic stuff

import sys

def printl(S):
    print len(S), "polynomials:"
    for s in S:
        print s
        print

def comb(R, S, k, v, zeros=0):
    """Given a ring R and list of polys S, returns a tuple (R',S')
    where R' is a new ring with the same base field but a bunch more
    variables, and S' is a list of k linear combinations of elements
    in S according to those new variables.
    v is a string that will form the base name of the new variables."""
    newvarn = [[v + str(i) + 'o' + str(j) for j in range(1,len(S)+1)] for i in range(1, k+1)]
    for i,j in sample([(i,j) for i in range(len(newvarn)) for j in range(len(newvarn[i]))], zeros):
        newvarn[i][j] = 0
    gens = R.gens() + sum((tuple(v for v in namerow if v != 0) for namerow in newvarn), ())
    
    R1 = PolynomialRing(R.base_ring(), gens)
    gd = R1.gens_dict()
    newvar = tuple(tuple(gd[vn] if vn != 0 else R1.zero() for vn in namerow) for namerow in newvarn)
    
    S1 = [sum(sx * y for (sx,y) in zip(S, nvrow)) for nvrow in newvar]

    return R1, S1

def kdict(f, v=None, degs=None):
    """Performs a Kronecker substitution on the given polynomial.
    v is a list of variables to substitute (default: all of 'em)
    and degs is a corresponding list of degrees (default: their
    actual degrees in f).
    Returns a dictionary of Xdegree:coefficient terms
    """
    R = f.parent()
    curvars = R.gens()
    newvars = list(curvars)
    if v is None:
        v = list(curvars)
    inds = [curvars.index(x) for x in v]
    remind = list(range(len(curvars)))
    for ind in reversed(sorted(inds)):
        del newvars[ind]
        del remind[ind]
    assert set(inds).union(remind) == set(range(len(curvars)))
    assert not set(inds).intersection(remind)
    if degs is None:
        curdeg = f.degrees()
        degs = [curdeg[i] for i in inds]
    pows = [1]
    assert len(degs) == len(v)
    for i in range(len(degs)-1):
        pows.append(pows[-1] * (degs[i]+1))
    assert len(pows) == len(degs)
    assert len(newvars) == len(remind)
    if newvars:
        R1 = PolynomialRing(R.base_ring(), tuple(newvars), sparse=True)
        res = {}
        for exp, coeff in f.dict().iteritems():
            kvexp = [exp[i] for i in inds]
            remexp = tuple(exp[i] for i in remind)
            newexp = sum(kve * p for (kve,p) in zip(kvexp, pows))
            if newexp in res:
                res[newexp] += R1({remexp:coeff})
            else:
                res[newexp] = R1({remexp:coeff})
        return res, v, degs
    else:
        res = {}
        for exp, coeff in f.dict().iteritems():
            kvexp = [exp[i] for i in inds]
            newexp = sum(kve * p for (kve,p) in zip(kvexp, pows))
            if newexp in res:
                res[newexp] += coeff
            else:
                res[newexp] = coeff
        return res, v, degs
        
def lispify(f):
    """Converts a poly into lisp-like notation."""
    terms = []
    vnames = map(str, f.parent().gens())
    for elist, coeff in f.dict().iteritems():
        parts = []
        if coeff != 1:
            parts.append(str(coeff))
        for i,e in enumerate(elist):
            for _ in range(e):
                parts.append(vnames[i])
        if len(parts) == 1:
            terms.append(parts[0])
        elif len(parts) > 1:
            terms.append('(* ' + ' '.join(parts) + ')')
    if len(terms) == 1:
        return terms[0]
    else:
        return '(+ ' + ' '.join(terms) + ')'

args = sys.argv[1:]

part1 = 5 # how many degree-1 products
part2 = 3 # how many degree-1 times degree-2 products
zeros = 50 # how many of the 'a' variables to try setting to 0
z3file = 'det33z3.txt' if len(args) < 1 else args[0]
    
R0.<r,s,t,u,v,w,x,y,z> = PolynomialRing(ZZ, 9, 'rstuvwxyz')
target = r*v*z - r*w*y - s*u*z + s*w*x + t*u*y - t*v*x

# S0 = inputs
S0 = list(R0.gens())

R1, S1 = comb(R0, S0, 2*part1 + part2, 'a', zeros)

S2 = [S1[i] * S1[i+1] for i in range(0,2*part1,2)]

R3, S3 = comb(R1, S2, part2, 'b')

S4 = [S1[2*part1+i] * S3[i] for i in range(part2)]

R5, S5 = comb(R3, S4, 1, 'c')

f = S5[0]

print len(f.degrees())
print len(f.degrees()) - len(S0)
print
print f.degrees()
print
print len(f.coefficients())
print
print "--------------------------------------------------------------------"

fk, _, degs = kdict(f, v=S0)

print len(fk)
print
print max(ff.total_degree() for ff in fk.itervalues())
print
print max(len(ff.coefficients()) for ff in fk.itervalues())
print
print all(ff.is_homogeneous() for ff in fk.itervalues())
print "--------------------------------------------------------------------"

tkterms, _, _ = kdict(target, degs=degs)

print sorted(fk.keys())
print
print sorted(tkterms.keys())
print
if not all(k in fk for k in tkterms):
    print "FAIL"
    exit(1)
print "--------------------------------------------------------------------"

system = []
s2 = []
allvars = set()
for expon, coeff in fk.iteritems():
    try:
        rhs = tkterms[expon]
    except KeyError:
        rhs = 0
    sc = symbolic_expression(coeff)
    allvars.update(sc.variables())
    system.append(sc - rhs)
    s2.append((coeff, rhs))

print len(allvars)
print len(system)

"""
bertfile = 'bertini_3x3.txt'
fout = open(bertfile, 'w')
print >> fout, "CONFIG"
print >> fout, 'TRACKTYPE: 1;'
print >> fout, 'END;'
print >> fout, 'INPUT'
print >> fout, 'variable_group', ', '.join(str(v) for v in allvars), ';'
print >> fout, 'function', ', '.join('f' + str(i) for i in range(1, len(system)+1)), ';'
for i, p in enumerate(system):
    print >> fout, 'f{} ='.format(i+1), p, ';'
print >> fout, 'END;'
fout.close()
print "saved bertini to", bertfile
"""

fout = open(z3file, 'w')
for v in allvars:
    print >> fout, '(declare-const', str(v), 'Int)'
for lhs,rhs in s2:
    print >> fout, '(assert (=', rhs, lispify(lhs), '))'
print >> fout, '(check-sat-using smt)'
print >> fout, '(get-model)'
fout.close()
print "saved z3 to", z3file

