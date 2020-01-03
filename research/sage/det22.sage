# code for 2x2 determinant algebraic stuff

def printl(S):
    print len(S), "polynomials:"
    for s in S:
        print s
        print

def comb(R, S, k, v):
    """Given a ring R and list of polys S, returns a tuple (R',S')
    where R' is a new ring with the same base field but a bunch more
    variables, and S' is a list of k linear combinations of elements
    in S according to those new variables.
    v is a string that will form the base name of the new variables."""
    newvarn = tuple(tuple(v + str(i) + 'o' + str(j) for j in range(1,len(S)+1)) for i in range(1, k+1))
    gens = R.gens() + sum(newvarn, ())
    
    R1 = PolynomialRing(R.base_ring(), gens)
    gd = R1.gens_dict()
    newvar = tuple(tuple(gd[vn] for vn in namerow) for namerow in newvarn)
    
    S1 = [sum(sx * y for (sx,y) in zip(S, nvrow)) for nvrow in newvar]

    return R1, S1

def kron(f, kv, v=None, degs=None):
    """Performs a Kronecker substitution on the given polynomial
    using the new variable kv.
    v is a list of variables to substitute (default: all of 'em)
    and degs is a corresponding list of degrees (default: their
    actual degrees in f).
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
    R1 = PolynomialRing(R.base_ring(), (kv,) + tuple(newvars), sparse=True)
    kvv = R1.gens()[0]
    pows = [1]
    assert len(degs) == len(v)
    for i in range(len(degs)-1):
        pows.append(pows[-1] * (degs[i]+1))
    assert len(pows) == len(degs)
    res = R1(0)
    for exp, coeff in f.dict().iteritems():
        kvexp = [exp[i] for i in inds]
        remexp = tuple(exp[i] for i in remind)
        newexp = (sum(kve * p for (kve,p) in zip(kvexp, pows)),) + remexp
        if len(newexp) > 1:
            res += R1({newexp:coeff})
        else:
            res += coeff * kvv^newexp[0]
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
    
R0.<w,x,y,z> = PolynomialRing(ZZ, 4, 'wxyz')
target = w*z - x*y

# S0 = inputs
S0 = list(R0.gens())

R1, S1 = comb(R0, S0, 4, 'a')

S2 = [S1[i] * S1[i+1] for i in range(0,4,2)]

R3, S3 = comb(R1, S2, 1, 'b')

f = S3[0]

fk, _, degs = kron(f, 'X', v=S0)
RX = fk.parent()
X = RX.gens()[0]

tk, _, _ = kron(target, 'X', degs=degs)
tkterms = tk.dict()

system = []
s2 = []
g = fk.polynomial(X)
allvars = set()
for expon, coeff in g.dict().iteritems():
    try:
        rhs = tkterms[expon]
    except KeyError:
        rhs = 0
    sc = symbolic_expression(coeff)
    allvars.update(sc.variables())
    system.append(sc - rhs)
    s2.append((coeff, rhs))
    

if True: # z3
    for v in allvars:
        print '(declare-const', str(v), 'Int)'
    for lhs,rhs in s2:
        print '(assert (=', rhs, lispify(lhs), '))'
    print '(check-sat)'
    print '(get-model)'

if False: # bertini
    print 'variable_group', ', '.join(str(v) for v in allvars), ';'
    print 'function', ', '.join('f' + str(i) for i in range(1, len(system)+1)), ';'
    print
    for i, p in enumerate(system):
        print 'f{} ='.format(i+1), p, ';'
