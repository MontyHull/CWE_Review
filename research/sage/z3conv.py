#/usr/bin/env python3

import sys
import re

def read_model(s):
    mm = re.fullmatch(r'\s*\(\s*model\s*(\(.*\))\s*\)\s*', s, re.DOTALL)
    if mm:
        res = {}
        for dm in re.finditer(r'\s*\(\s*define-fun\s*(\S+)\s*\(\)\s*Int\s*(\(-\s*\w+\)|\w+)\s*\)',
                              mm.group(1), re.DOTALL):
            vname = dm.group(1)
            vval = dm.group(2)
            cm = re.fullmatch(r'\(-\s*(\w+)\)', vval)
            if cm:
                vval = -int(cm.group(1))
            else:
                vval = int(vval)
            res[vname] = vval
        return res

def splitvar(vn):
    vm = re.fullmatch(r'([a-z]+)(\d+)o(\d+)', vn)
    assert vm
    return (vm.group(1), int(vm.group(2)), int(vm.group(3)))

def parse_vars(V):
    sv = sorted((splitvar(vn), val) for vn,val in V.items())
    res = {}
    lastn = None
    lasti = None
    lastj = None
    maxj = None
    for (n, i, j), val in sv:
        if n != lastn:
            assert n not in res
            res[n] = []
            lastn = n
            lasti = lastj = maxj = None
        if i != lasti:
            if maxj is not None:
                assert lastj == maxj
            else:
                maxj = lastj
            res[n].append([])
            lasti = i
            lastj = None
        if lastj is None:
            assert j == 1
        else:
            assert j == lastj + 1
        res[n][-1].append(val)
        lastj = j
    return res

class SLP:
    def __init__(self, nvars):
        self.nvars = nvars
        self.ops = []

    def print(self, f=sys.stdout):
        print(self.nvars, len(self.ops), file=f)
        for (a1,oc,a2,ot) in self.ops:
            print(a1, oc, a2, ot, file=f)

    def next(self, a1, oc, a2, ot):
        assert -self.nvars <= a1 < len(self.ops)
        assert oc in 'asx'
        if ot == 'r':
            assert -self.nvars <= a2 < len(self.ops)
        else:
            assert ot == 's'
        self.ops.append((a1,oc,a2,ot))
        return len(self.ops) - 1

def addmul(slp, cur, coeff, arg):
    if coeff == 0:
        return cur
    elif coeff == 1:
        if cur is not None:
            return slp.next(cur, 'a', arg, 'r')
        else:
            return arg
    elif cur is not None and coeff == -1:
        return slp.next(cur, 's', arg, 'r')
    else:
        prod = slp.next(arg, 'x', coeff, 's')
        if cur is not None:
            return slp.next(cur, 'a', prod, 'r')
        else:
            return prod

def comb(slp, inputs, mmat):
    outputs = []
    if mmat:
        assert len(inputs) == len(mmat[0])
        for lc in mmat:
            cur = None
            for coeff, arg in zip(lc, inputs):
                cur = addmul(slp, cur, coeff, arg)
            if cur is None:
                cur = slp.next(-1, 's', -1, 'r')
            outputs.append(cur)
    return outputs

def pairs(lst):
    it = iter(lst)
    while True:
        try:
            yield (next(it), next(it))
        except StopIteration:
            return

if __name__ == '__main__':
    # read from stdin write to stdout
    wholething = sys.stdin.read().strip()
    if wholething.startswith('sat'):
        wholething = wholething[3:]
    V = read_model(wholething)
    F = parse_vars(V)

    nvars = len(F['a'][0])

    slp = SLP(nvars)
    S0 = list(reversed(range(-nvars, 0)))
    S1 = comb(slp, S0, F['a'])
    S2 = [slp.next(a1, 'x', a2, 'r') for a1,a2 in pairs(S1)]
    S3 = comb(slp, S2, F['b'])
    assert len(S3) == 1
    slp.print()
