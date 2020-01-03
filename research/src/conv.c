#include "conv.h"
#include "limits.h"

/*uses add/mull */
void slp_poly_eval(PolyEvalT e,int linenumber,int rank) {
  const SLP* p = e->slp;

  /* iterate through array of ops (aka length of SLP) */
  int i;
  PolyT literal;
  Index arg1;
  const Poly* src1;
  const Poly* src2;

  poly_init2(literal, p->inputs, 1);

  for(i = 0; i < p[0].length; i++){
    /* src1:
     * arg1 is always an index */
    arg1 = p->ops[i].arg1;

    /* check if arg1 is from the input or output */
    /* src1 is index from outputs */
    if(arg1 >= 0){
      src1 = e->outputs + arg1;
    }
    /* src1 is index from inputs */
    else{
      src1 = e->inputs + input_index(arg1);
    }

    /* src2: */

    /* src2 is value */
    if(p->ops[i].type == SCALAR){
      poly_set_const(literal, p->ops[i].arg2.literal);
      src2 = literal;
    }
    /* src2 is index from outputs */
    else if(p->ops[i].arg2.ind >= 0){
      assert(p->ops[i].type == REGULAR);
      src2 = e->outputs + p->ops[i].arg2.ind;
    }
    /* src2 is index from inputs */
    else{
      assert(p->ops[i].type == REGULAR && p->ops[i].arg2.ind < 0);
      src2 = e->inputs + input_index(p->ops[i].arg2.ind);
    }


    /* addition */
    if(p->ops[i].func == ADD){
      poly_add(e->outputs + i, src1, src2,linenumber,rank);
    }
    /* subtraction */
    else if(p->ops[i].func == SUB){
      poly_sub(e->outputs + i, src1, src2,linenumber,rank);
    }
    /* multiplication */
    else{
      assert(p->ops[i].func == MUL);
      poly_mul(e->outputs + i, src1, src2);
    }
  }

  poly_clear(literal);
}

void slp2poly(PolyT out, const SLPT in, int init,int linenumber,int rank) {
  PolyEvalT eval;

  /* good */
  poly_eval_init(eval, in);

  /* bad */
  slp_poly_eval(eval,linenumber,rank);

  if (!init) poly_init(out, in->inputs);

  /* good */
  poly_set(out, eval->outputs + (in->length - 1));

#if 0 /* debug */
  {
    int i;
    Op* x;
    char op;
    printf("DEBUG slp2poly\n");
    for (i=0; i < in->length; ++i) {
      printf("%2d SLP stmt: ", i);
      x = get_op(in, i);
      if(x->func == MUL){
        op = 'x';
      }
      else if(x->func == ADD){
        op = 'a';
      }
      else{
        assert(x->func == SUB);
        op = 's';
      }

      if(x->type == REGULAR){
        printf("%ld %c %ld r\n",x->arg1,op,x->arg2.ind);
      }
      else{
        assert(x->type == SCALAR);
        printf("%ld %c %ld s\n",x->arg1,op,x->arg2.literal);
      }

      printf("   Poly: ");
      poly_print(eval->outputs + i);
    }
    printf("END DEBUG\n");
  }
#endif

  /* good */
  poly_eval_clear(eval);
}

/* returns the number of 1's in the binary representation of e */
static __inline__ int popcount(ExponT e) {
  int res = 0;
  while (e) {
    if (e & (ExponT)1) ++res;
    e >>= 1;
  }
  return res;
}

/* number of bits in binary representation of e.
 * By convention, bitlen(0) == bitlen(1) == 1.
 */
static __inline__ int bitlen(ExponT e) {
  ExponT comp = 1;
  int res = 1;
  while (e > comp) {
    comp = comp * 2 + 1;
    res++;
  }
  return res;
}

static __inline__ void _slp_resize(SLPT p, int nvars, long len, int init) {
  if (init) {
    if (p->inputs != nvars || p->length != len) {
      slp_clear(p);
      slp_init(p, nvars, len);
    }
  }
  else slp_init(p, nvars, len);
}

#define ACCUM_SENTINEL (LONG_MIN)

/* adds on one more multiplication for the current term.
 * Either saves the operand if it's first, or multiplies with the
 * saved result if it's later.
 */
static __inline__ void term_update(Op* ops, long* numops,
                                   Index* accum, Index ind)
{
  if (*accum == ACCUM_SENTINEL)
    *accum = ind;
  else {
    regular_op(ops + *numops, MUL, *accum, ind);
    *accum = (*numops)++;
  }
}

void poly2slp(SLPT out, const PolyT in, int init) {
  int var, nvars = in->nvars;
  long term, nterms = in->len;
  long* varpows;
  ExponT* maxpows;
  long numops = 0;
  Index accum, taccum, curpow;
  CoeffT c;
  ExponT e;

  assert(nvars >= 1);

  if (nterms == 0) {
    /* special case: zero polynomial */
    _slp_resize(out, nvars, 1, init);
    regular_op(out->ops + 0, SUB, -1, -1);
    return;
  }

  if (nterms == 1 && zero_expon(in->terms[0].expons, nvars)) {
    /* special case: constant polynomial */
    _slp_resize(out, nvars, 2, init);
    regular_op(out->ops + 0, SUB, -1, -1);
    scalar_op(out->ops + 1, ADD, 0, in->terms[0].coeff);
    return;
  }

  varpows = malloc(nvars * sizeof *varpows);
  maxpows = malloc(nvars * sizeof *maxpows);

  /* find the highest power of each variable */
  memcpy(maxpows, in->terms[0].expons, nvars * sizeof(ExponT));
  for (term = 1; term < in->len; ++term) {
    for (var = 0; var < in->nvars; ++var) {
      if (in->terms[term].expons[var] > maxpows[var])
        maxpows[var] = in->terms[term].expons[var];
    }
  }

  /* calculate how many ops needed for each variable powering */
  for (var = 0; var < nvars; ++var) {
    numops += bitlen(maxpows[var]) - 1;
  }

  /* calculate how many ops needed for each term */
  for (term = 0; term < nterms; ++term) {
    int novars = 1;
    for (var = 0; var < nvars; ++var) {
      if (in->terms[term].expons[var]) {
        novars = 0;
        numops += popcount(in->terms[term].expons[var]);
      }
    }
    /* special cases */
    if (term == 0) {
      assert(!novars);
      if (in->terms[term].coeff == 1) --numops;
    }
    else if (novars) {
      assert(term == nterms - 1);
      ++numops;
    }
    else {
      if (in->terms[term].coeff != 1 && in->terms[term].coeff != -1) ++numops;
    }
  }

  if (numops == 0) numops = 1;

  /* (re)initialize the SLP */
  _slp_resize(out, nvars, numops, init);

  numops = 0;
  /* compute x^2, x^4, x^8, ... for each var up to highest power */
  for (var = 0; var < nvars; ++var) {
    /* The 1st power of variable i is the input in position (-1 - i).
     * The 2nd power (if it exists) is in the location indicated by varpows[var].
     * The 3rd and higher powers are sequentially after the 2nd power.
     */
    int powcomp = bitlen(maxpows[var]) - 1;
    assert(powcomp >= 0);
    if (powcomp == 0) {
      varpows[var] = -1;
      continue;
    }

    varpows[var] = numops;
    regular_op(out->ops + numops, MUL, -1 - var, -1 - var);
    ++numops;

    while (--powcomp) {
      regular_op(out->ops + numops, MUL, numops-1, numops-1);
      ++numops;
    }
  }

  /* compute first term */
  accum = ACCUM_SENTINEL;
  assert(nterms >= 1);
  c = in->terms[0].coeff;
  assert(c != 0);
  for (var = 0; var < nvars; ++var) {
    e = in->terms[0].expons[var];
    if (e & (ExponT)1) {
      term_update(out->ops, &numops, &accum, -1 - var);
    }
    curpow = varpows[var];
    for (e /= 2; e; e /= 2) {
      if (e & (ExponT)1)
        term_update(out->ops, &numops, &accum, curpow);
      ++curpow;
    }
  }
  assert(accum != ACCUM_SENTINEL);
  if (c != 1) {
    scalar_op(out->ops + numops, MUL, accum, c);
    accum = numops++;
  }

  /* compute remaining terms */
  for (term = 1; term < nterms; ++term) {
    taccum = ACCUM_SENTINEL;
    c = in->terms[term].coeff;
    assert(c != 0);
    for (var = 0; var < nvars; ++var) {
      e = in->terms[term].expons[var];
      if (e & (ExponT)1) {
        term_update(out->ops, &numops, &taccum, -1 - var);
      }
      curpow = varpows[var];
      for (e /= 2; e; e /= 2) {
        if (e & (ExponT)1)
          term_update(out->ops, &numops, &taccum, curpow);
        ++curpow;
      }
    }
    if (taccum == ACCUM_SENTINEL) {
      /* special case of constant term */
      assert(term == nterms - 1);
      scalar_op(out->ops + numops, ADD, accum, c);
      accum = numops++;
    } else {
      OpCode op = ADD;
      if (c < 0) {
        op = SUB;
        c *= -1;
      }
      if (c != 1) {
        scalar_op(out->ops + numops, MUL, taccum, c);
        taccum = numops++;
      }
      regular_op(out->ops + numops, op, accum, taccum);
      accum = numops++;
    }
  }

  if (numops == 0) {
    assert(accum != ACCUM_SENTINEL);
    scalar_op(out->ops + numops, ADD, accum, 0);
    accum = numops++;
  }

  assert(numops == out->length);
  free(varpows);
  free(maxpows);
}
