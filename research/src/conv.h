/* conversion between SLPs and polynomials */

#ifndef CONV_H
#define CONV_H

#include "circuit.h"
#include "poly.h"

typedef struct {
  const SLP* slp;
  Poly* inputs;
  Poly* outputs;
} PolyEval;
typedef PolyEval PolyEvalT[1];

static __inline__ void poly_eval_init(PolyEvalT eval, const SLPT p) {
  long i;
  eval->slp = p;

  eval->inputs = malloc(p->inputs * sizeof *eval->inputs);
  for (i = 0; i < p->inputs; ++i) {
    poly_init2(eval->inputs + i, p->inputs, 1);
    poly_set_var(eval->inputs + i, i);
  }

  eval->outputs = malloc(p->length * sizeof *eval->outputs);
  for (i = 0; i < p->length; ++i)
    poly_init(eval->outputs + i, p->inputs);
}

static __inline__ void poly_eval_clear(PolyEvalT eval) {
  long i;
  for (i = 0; i < eval->slp->inputs; ++i)
    poly_clear(eval->inputs + i);
  for (i = 0; i < eval->slp->length; ++i)
    poly_clear(eval->outputs + i);
  free(eval->inputs);
  free(eval->outputs);
}

void slp_poly_eval(PolyEvalT eval,int mainline, int rank);

/* init == 1 iff the polynomial is already initialized. */
void slp2poly(PolyT out, const SLPT in, int init,int linenumber,int rank);

/* init == 1 iff the SLP is already initialized. */
void poly2slp(SLPT out, const PolyT in, int init);

#endif /* CONV_H */
